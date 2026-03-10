# API路由文件
# 实现用户认证和内容管理的所有API端点

from fastapi import APIRouter, Depends, status, Request, UploadFile, File, Body, Query
from fastapi.responses import JSONResponse, StreamingResponse, Response
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import timedelta, date
from typing import List, Optional
import os
import shutil
from io import BytesIO
from uuid import uuid4
from fastapi_csrf_protect import CsrfProtect
from fastapi_csrf_protect.exceptions import CsrfProtectError

# 从main模块导入自适应RateLimiter
from main import RateLimiter

from database import get_db
from models import User, Content, OrderItem, Like
from schemas import (
    UserCreate, UserLogin, UserResponse, UserUpdate, Token,
    ContentCreate, ContentUpdate, ContentResponse, ContentListResponse,
    PasswordResetRequest, PasswordReset, MessageResponse,
    OrderCreate, OrderResponse, OrderListResponse, PaymentRequest, PaymentResponse, PaymentCallback, OrderItemCreate,
    FavoriteCreate, FavoriteResponse, FavoriteContentResponse, FavoriteListResponse, ContentWithLikedResponse,
    LikeCreate, LikeResponse, LikeStatusResponse, ContentWithLikeStatusResponse,
    ProductCreate, ProductUpdate, ProductResponse, ProductListResponse
)
from auth import verify_password, get_password_hash, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from dependencies import get_current_active_user, get_current_admin_user, get_current_user_optional
from logging_config import get_logger
from errors import ConflictError, BadRequestError, ResourceNotFoundError, AuthorizationError
from payment import create_order, get_order, get_user_orders, process_payment, handle_payment_callback, cancel_order, get_order_by_number, check_user_purchased_agent
from pdf_generator import PDFGenerator

# 获取日志器
logger = get_logger(__name__)

# 检查是否为测试环境
import os
is_test = os.environ.get("TESTING", "false").lower() == "true"

# 创建路由实例
router = APIRouter()

# CSRF令牌获取端点
@router.get("/api/csrf-token")
async def get_csrf_token(csrf_protect: CsrfProtect = Depends()):
    """
    获取CSRF令牌的端点
    
    Args:
        csrf_protect: CSRF保护依赖
    
    Returns:
        JSONResponse: 包含CSRF令牌的响应
    """
    logger.info("获取CSRF令牌请求")
    token, signed = csrf_protect.generate_csrf_tokens()
    return JSONResponse({"csrf_token": token})


# 用户认证相关路由

@router.post("/api/auth/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(RateLimiter(times=5, seconds=60))])
def register_user(user: UserCreate, request: Request, db: Session = Depends(get_db)):
    """
    用户注册接口
    
    Args:
        user: 用户注册请求数据
        request: HTTP请求对象
        db: 数据库会话
    
    Returns:
        UserResponse: 注册成功的用户信息
    
    Raises:
        HTTPException: 400错误，如果用户名或邮箱已存在
    """
    logger.info(f"用户注册请求: 用户名={user.username}, 邮箱={user.email}")
    
    # 检查用户名是否已存在
    existing_user = db.query(User).filter(
        (User.username == user.username) | (User.email == user.email)
    ).first()
    
    if existing_user:
        if existing_user.username == user.username:
            logger.warning(f"用户名已存在: {user.username}")
            raise ConflictError(message="用户名已存在", details="该用户名已被注册，请使用其他用户名")
        else:
            logger.warning(f"邮箱已存在: {user.email}")
            raise ConflictError(message="邮箱已存在", details="该邮箱已被注册，请使用其他邮箱")
    
    # 创建新用户
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # 处理推广码
    if user.referral_code:
        logger.info(f"处理推广码: {user.referral_code} 为用户: {db_user.id}")
        # 查找推广链接
        affiliate_link = db.query(AffiliateLink).filter(
            AffiliateLink.unique_code == user.referral_code,
            AffiliateLink.is_active == True
        ).first()
        
        if affiliate_link:
            # 查找最近7天内的点击记录
            click_record = db.query(AffiliateClick).filter(
                AffiliateClick.affiliate_link_id == affiliate_link.id,
                AffiliateClick.created_at >= datetime.utcnow() - timedelta(days=7),
                AffiliateClick.user_id == None
            ).order_by(AffiliateClick.created_at.desc()).first()
            
            if click_record:
                # 将点击记录与用户关联
                click_record.user_id = db_user.id
                db.commit()
                logger.info(f"推广点击记录已与用户关联: 点击ID={click_record.id}, 用户ID={db_user.id}")
    
    logger.info(f"用户注册成功: 用户ID={db_user.id}, 用户名={db_user.username}")
    return db_user


@router.post("/api/auth/login", response_model=Token, dependencies=[Depends(RateLimiter(times=5, seconds=60))])
def login_user(request: Request, user: UserLogin, csrf_protect: CsrfProtect = Depends(), db: Session = Depends(get_db)):
    """
    用户登录接口
    
    Args:
        request: HTTP请求对象
        user: 用户登录请求数据
        csrf_protect: CSRF保护依赖
        db: 数据库会话
    
    Returns:
        Token: 包含访问令牌的响应
    
    Raises:
        BadRequestError: 400错误，如果邮箱或密码不正确，或者用户已被禁用
        CsrfProtectError: 403错误，如果CSRF令牌无效
    """
    # 在测试环境中跳过CSRF令牌验证
    if not is_test:
        csrf_protect.validate_csrf(request)
    logger.info(f"用户登录请求: 邮箱={user.email}")
    
    # 查找用户
    db_user = db.query(User).filter(User.email == user.email).first()
    
    # 验证用户和密码
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        logger.warning(f"登录失败: 邮箱={user.email}, 原因: 邮箱或密码不正确")
        raise BadRequestError(message="邮箱或密码不正确")
    
    # 检查用户是否激活
    if not db_user.is_active:
        logger.warning(f"登录失败: 邮箱={user.email}, 原因: 用户已被禁用")
        raise BadRequestError(message="用户已被禁用")
    
    # 创建访问令牌
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(db_user.id)},
        expires_delta=access_token_expires
    )
    
    logger.info(f"登录成功: 用户ID={db_user.id}, 用户名={db_user.username}")
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/api/auth/reset-password-request", response_model=MessageResponse, dependencies=[Depends(RateLimiter(times=5, seconds=60))])
def reset_password_request(request: Request, reset_request: PasswordResetRequest, csrf_protect: CsrfProtect = Depends(), db: Session = Depends(get_db)):
    """密码重置请求接口 - 添加CSRF保护"""
    csrf_protect.validate_csrf(request)
    """
    请求密码重置接口
    
    Args:
        reset_request: 密码重置请求数据
        db: 数据库会话
    
    Returns:
        MessageResponse: 密码重置请求处理结果
    """
    logger.info(f"密码重置请求: 邮箱={reset_request.email}")
    
    # 查找用户
    user = db.query(User).filter(User.email == reset_request.email).first()
    
    # 这里应该发送密码重置邮件，但目前只返回成功消息
    # 实际实现中需要生成重置令牌并发送到用户邮箱
    
    logger.info(f"密码重置邮件已发送（模拟）: 邮箱={reset_request.email}")
    return {
        "status": "success",
        "message": "密码重置邮件已发送（模拟）"
    }


@router.post("/api/auth/reset-password", response_model=MessageResponse, dependencies=[Depends(RateLimiter(times=5, seconds=60))])
def reset_password(request: Request, reset_data: PasswordReset, csrf_protect: CsrfProtect = Depends(), db: Session = Depends(get_db)):
    """密码重置确认接口 - 添加CSRF保护"""
    csrf_protect.validate_csrf(request)
    """
    密码重置确认接口
    
    Args:
        reset_data: 密码重置确认数据
        db: 数据库会话
    
    Returns:
        MessageResponse: 密码重置结果
    """
    logger.info(f"密码重置确认请求: 邮箱={reset_data.email}")
    
    # 实际实现中需要验证重置令牌
    # 这里简化处理，直接返回成功消息
    logger.info(f"密码重置成功（模拟）: 邮箱={reset_data.email}")
    return {
        "status": "success",
        "message": "密码已重置（模拟）"
    }


@router.get("/api/users/me", response_model=UserResponse)
def get_current_user(current_user: User = Depends(get_current_active_user)):
    """
    获取当前登录用户的信息
    
    Args:
        current_user: 当前活跃用户
    
    Returns:
        UserResponse: 当前用户信息
    """
    logger.info(f"获取当前用户信息: 用户ID={current_user.id}")
    return current_user


@router.get("/api/users/me/download")
def download_user_info(current_user: User = Depends(get_current_active_user)):
    """
    下载当前用户的个人信息
    
    Args:
        current_user: 当前活跃用户
    
    Returns:
        Response: CSV格式的用户信息文件
    """
    import csv
    from io import StringIO
    from fastapi.responses import Response
    
    logger.info(f"下载用户信息请求: 用户ID={current_user.id}")
    
    # 创建CSV内容
    csv_output = StringIO()
    writer = csv.writer(csv_output)
    
    # 写入表头
    writer.writerow(["字段名称", "字段值"])
    
    # 写入用户基本信息
    writer.writerow(["用户名", current_user.username])
    writer.writerow(["邮箱", current_user.email])
    writer.writerow(["性别", current_user.gender if current_user.gender else ""])
    writer.writerow(["生日", current_user.birthday.strftime("%Y-%m-%d") if current_user.birthday else ""])
    writer.writerow(["个人简介", current_user.bio if current_user.bio else ""])
    
    # 写入母婴特色字段
    writer.writerow(["宝宝姓名", current_user.baby_name if current_user.baby_name else ""])
    writer.writerow(["宝宝生日", current_user.baby_birthday.strftime("%Y-%m-%d") if current_user.baby_birthday else ""])
    writer.writerow(["宝宝性别", current_user.baby_gender if current_user.baby_gender else ""])
    writer.writerow(["宝宝成长里程碑", current_user.baby_milestones if current_user.baby_milestones else ""])
    
    # 设置响应头
    response = Response(
        content=csv_output.getvalue(),
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename=user_info_{current_user.id}.csv"
        }
    )
    
    return response


@router.get("/api/auth/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_active_user)):
    """
    获取当前用户信息接口
    
    Args:
        current_user: 当前认证的活跃用户
    
    Returns:
        UserResponse: 当前用户信息
    """
    logger.info(f"获取当前用户信息: 用户ID={current_user.id}, 用户名={current_user.username}")
    return current_user


@router.put("/api/users/me", response_model=UserResponse)
def update_user_info(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    更新当前用户信息接口
    
    Args:
        user_update: 用户信息更新请求数据
        db: 数据库会话
        current_user: 当前认证的活跃用户
    
    Returns:
        UserResponse: 更新后的用户信息
    """
    logger.info(f"更新用户信息请求: 用户ID={current_user.id}")
    logger.info(f"接收到的完整数据: {user_update.model_dump()}")
    logger.info(f"用户名值: {user_update.username}")
    logger.info(f"用户名类型: {type(user_update.username)}")
    logger.info(f"用户名长度: {len(user_update.username) if user_update.username else 0}")
    logger.info(f"更新内容: {user_update.model_dump(exclude_unset=True)}")
    
    # 检查用户名是否已存在（如果要更新用户名）
    if user_update.username is not None:
        # 只有当用户名不为空时才检查唯一性
        if user_update.username:
            existing_user = db.query(User).filter(
                User.username == user_update.username, 
                User.id != current_user.id
            ).first()
            if existing_user:
                raise ConflictError(message="用户名已存在", details="该用户名已被其他用户使用")
        
        current_user.username = user_update.username
    
    # 检查邮箱是否已存在（如果要更新邮箱）
    if user_update.email is not None:
        # 只有当邮箱不为空时才检查唯一性
        if user_update.email:
            existing_user = db.query(User).filter(
                User.email == user_update.email, 
                User.id != current_user.id
            ).first()
            if existing_user:
                raise ConflictError(message="邮箱已存在", details="该邮箱已被其他用户使用")
        
        current_user.email = user_update.email
    
    # 更新头像
    if user_update.avatar is not None:
        current_user.avatar = user_update.avatar
    
    # 更新性别
    if user_update.gender is not None:
        current_user.gender = user_update.gender
    
    # 更新生日
    if user_update.birthday is not None:
        current_user.birthday = user_update.birthday
    
    # 更新个人简介
    if user_update.bio is not None:
        current_user.bio = user_update.bio
    
    # 更新母婴特色字段
    if user_update.baby_name is not None:
        current_user.baby_name = user_update.baby_name
    
    if user_update.baby_birthday is not None:
        current_user.baby_birthday = user_update.baby_birthday
    
    if user_update.baby_gender is not None:
        current_user.baby_gender = user_update.baby_gender
    
    if user_update.baby_milestones is not None:
        current_user.baby_milestones = user_update.baby_milestones
    
    # 提交更改到数据库
    db.commit()
    db.refresh(current_user)
    
    logger.info(f"用户信息更新成功: 用户ID={current_user.id}")
    return current_user

@router.post("/api/users/me/avatar", response_model=UserResponse)
def upload_avatar(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    上传用户头像接口
    
    Args:
        file: 上传的头像文件
        db: 数据库会话
        current_user: 当前认证的活跃用户
    
    Returns:
        UserResponse: 更新后的用户信息
    """
    logger.info(f"上传头像请求: 用户ID={current_user.id}, 文件名={file.filename}")
    
    # 检查文件类型
    allowed_types = ["image/jpeg", "image/png", "image/gif"]
    if file.content_type not in allowed_types:
        raise BadRequestError(message="只支持JPEG、PNG和GIF格式的图片")
    
    # 检查文件大小（限制为5MB）
    file.file.seek(0, os.SEEK_END)
    file_size = file.file.tell()
    file.file.seek(0)
    
    if file_size > 5 * 1024 * 1024:
        raise BadRequestError(message="头像大小不能超过5MB")
    
    # 创建静态文件目录（如果不存在）
    static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
    avatar_dir = os.path.join(static_dir, "avatars")
    os.makedirs(avatar_dir, exist_ok=True)
    
    # 生成唯一的文件名
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid4()}{file_extension}"
    file_path = os.path.join(avatar_dir, unique_filename)
    
    # 保存文件
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # 更新用户头像URL
    avatar_url = f"/static/avatars/{unique_filename}"
    current_user.avatar = avatar_url
    
    # 保存更改到数据库
    db.commit()
    db.refresh(current_user)
    
    logger.info(f"头像上传成功: 用户ID={current_user.id}, 头像URL={avatar_url}")
    return current_user


# 导入内容生成服务
from content_generator import generator_service, AutoContentPublisher

# 内容管理相关路由

@router.post("/api/content/generate", response_model=ContentResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(RateLimiter(times=5, seconds=60))])
def generate_content(
    request: Request,
    content_gen_request: ContentCreate,
    csrf_protect: CsrfProtect = Depends(),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """生成内容接口 - 自动生成内容草稿 - 添加CSRF保护"""
    csrf_protect.validate_csrf(request)
    """
    自动生成内容接口
    
    Args:
        content_gen_request: 内容生成请求数据
        db: 数据库会话
        current_user: 当前认证的活跃用户
    
    Returns:
        ContentResponse: 生成的内容信息
    """
    logger.info(f"自动生成内容请求: 标题={content_gen_request.title}, 分类={content_gen_request.category}, 用户ID={current_user.id}")
    
    # 使用内容生成服务生成内容
    generated = generator_service.generate_content(
        template_type="article",
        category=content_gen_request.category,
        title=content_gen_request.title,
        keywords=""
    )
    
    if not generated:
        logger.error(f"内容生成失败: 标题={content_gen_request.title}")
        raise BadRequestError(message="内容生成失败，请稍后重试")
    
    # 创建内容草稿
    db_content = Content(
        title=generated["title"],
        category=content_gen_request.category,
        summary=generated["summary"],
        content=generated["content"],
        author_id=current_user.id,
        is_published=False
    )
    
    db.add(db_content)
    db.commit()
    db.refresh(db_content)
    
    logger.info(f"内容生成成功: 内容ID={db_content.id}, 标题={db_content.title}")
    return db_content

@router.post("/api/content/auto-publish", response_model=ContentResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(RateLimiter(times=5, seconds=60))])
def auto_publish_content(
    request: Request,
    content_gen_request: ContentCreate,
    csrf_protect: CsrfProtect = Depends(),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """自动生成并发布内容接口 - 添加CSRF保护"""
    csrf_protect.validate_csrf(request)
    """
    自动生成并发布内容接口
    
    Args:
        content_gen_request: 内容生成请求数据
        db: 数据库会话
        current_user: 当前认证的活跃用户
    
    Returns:
        ContentResponse: 生成并发布的内容信息
    """
    logger.info(f"自动生成并发布内容请求: 标题={content_gen_request.title}, 分类={content_gen_request.category}, 用户ID={current_user.id}")
    
    try:
        # 使用自动发布服务
        publisher = AutoContentPublisher(db)
        result = publisher.generate_and_publish(
            category=content_gen_request.category,
            title=content_gen_request.title,
            keywords="",
            template_type="article",
            author_id=current_user.id
        )
        
        if not result:
            logger.error(f"自动发布失败: 标题={content_gen_request.title}")
            raise BadRequestError(message="内容生成或发布失败，请稍后重试")
        
        # 获取完整的内容信息
        content = db.query(Content).filter(Content.id == result["id"]).first()
        logger.info(f"内容自动发布成功: 内容ID={content.id}, 标题={content.title}")
        return content
        
    except Exception as e:
        logger.error(f"自动发布过程中发生错误: {str(e)}")
        raise BadRequestError(message="内容生成或发布失败，请稍后重试")

@router.post("/api/content", response_model=ContentResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(RateLimiter(times=10, seconds=60))])
def create_content(
    request: Request,
    content: ContentCreate,
    csrf_protect: CsrfProtect = Depends(),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """创建内容接口 - 添加CSRF保护"""
    csrf_protect.validate_csrf(request)
    """
    创建内容接口
    
    Args:
        content: 内容创建请求数据
        db: 数据库会话
        current_user: 当前认证的活跃用户
    
    Returns:
        ContentResponse: 创建成功的内容信息
    """
    logger.info(f"创建内容请求: 标题={content.title}, 分类={content.category}, 用户ID={current_user.id}")
    
    # 创建新内容
    db_content = Content(
        title=content.title,
        category=content.category,
        summary=content.summary,
        content=content.content,
        author_id=current_user.id
    )
    
    db.add(db_content)
    db.commit()
    db.refresh(db_content)
    
    logger.info(f"内容创建成功: 内容ID={db_content.id}, 标题={db_content.title}")
    return db_content


@router.get("/api/content", response_model=List[ContentResponse])
def get_content_list(
    category: Optional[str] = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    获取内容列表接口
    
    Args:
        category: 可选的内容分类筛选
        skip: 跳过的记录数（用于分页）
        limit: 返回的最大记录数（用于分页）
        db: 数据库会话
    
    Returns:
        List[ContentResponse]: 内容列表
    """
    logger.info(f"获取内容列表请求: 分类={category}, skip={skip}, limit={limit}")
    
    # 构建查询：只获取已发布且不是智能体的内容
    query = db.query(Content).filter(
        Content.is_published == True,
        Content.category != "agent"
    )
    
    # 如果提供了分类，添加分类筛选
    if category:
        query = query.filter(Content.category == category)
    
    # 获取内容列表
    contents = query.order_by(Content.created_at.desc()).offset(skip).limit(limit).all()
    
    # 为每个内容获取实时点赞数（从Like表查询，而不是使用缓存的Content.likes）
    for content in contents:
        real_time_likes = db.query(Like).filter(Like.content_id == content.id).count()
        content.likes = real_time_likes
    
    logger.info(f"获取内容列表成功: 返回数量={len(contents)}, 分类={category}")
    return contents


@router.get("/api/content/{content_id}", response_model=ContentResponse)
def get_content_detail(
    content_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_optional)
):
    """
    获取内容详情接口
    
    Args:
        content_id: 内容ID
        db: 数据库会话
        current_user: 当前用户（可选）
    
    Returns:
        ContentResponse: 内容详情
    
    Raises:
        HTTPException: 404错误，如果内容不存在或未发布
    """
    logger.info(f"获取内容详情请求: 内容ID={content_id}")
    
    # 查找内容
    content = db.query(Content).filter(
        Content.id == content_id, Content.is_published == True
    ).first()
    
    if not content:
        logger.warning(f"内容不存在或未发布: 内容ID={content_id}")
        raise ResourceNotFoundError(message="内容不存在或未发布", details={"content_id": content_id})
    
    # 更新浏览量
    content.view_count += 1
    
    # 记录浏览历史
    from models import ViewHistory
    import uuid
    
    if current_user:
        # 已登录用户，记录用户ID
        existing_history = db.query(ViewHistory).filter(
            ViewHistory.user_id == current_user.id,
            ViewHistory.article_id == content_id
        ).first()
        
        if not existing_history:
            view_history = ViewHistory(
                user_id=current_user.id,
                article_id=content_id,
                session_id=None
            )
            db.add(view_history)
            logger.info(f"记录用户浏览历史: 用户ID={current_user.id}, 文章ID={content_id}")
    
    # 移除内容中的字数统计信息
    import re
    if content.content:
        # 移除所有位置的字数统计信息 (全文约xxx字) 或 ((全文约xxx字))
        content.content = re.sub(r'^\s*\(?全文约\d+字\)?\s*\n*', '', content.content)
        content.content = re.sub(r'(?:\s*\n+)?\(?全文约\d+字\)?\s*$', '', content.content)
        content.content = re.sub(r'\n*\s*\(?全文约\d+字\)?\s*\n*', '\n', content.content)
        
        # 处理连续的p标签 - 在HTML标签中添加换行符，确保标签结构完整
        content.content = re.sub(r'</p>\s*<p>', '</p>\n<p>', content.content)
        
        # 处理空括号的方法：
        # 1. 移除所有空括号（包括括号内有空格的情况）
        content.content = re.sub(r'\s*\(\s*\)\s*', '', content.content)
        
        # 清理可能产生的多余换行符
        content.content = re.sub(r'\n+', '\n', content.content)
        content.content = content.content.strip()
    
    db.commit()
    
    logger.info(f"获取内容详情成功: 内容ID={content_id}, 标题={content.title}, 浏览量={content.view_count}")
    return content


@router.post("/api/content/{content_id}/like", response_model=LikeStatusResponse, dependencies=[Depends(RateLimiter(times=20, seconds=60))])
def toggle_like(
    content_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    点赞/取消点赞内容接口
    
    Args:
        content_id: 要点赞的内容ID
        db: 数据库会话
        current_user: 当前认证的活跃用户
    
    Returns:
        LikeStatusResponse: 包含是否已点赞和点赞总数的响应
    
    Raises:
        ResourceNotFoundError: 404错误，如果内容不存在或未发布
    """
    logger.info(f"点赞请求: 内容ID={content_id}, 用户ID={current_user.id}")
    
    # 查找内容
    content = db.query(Content).filter(
        Content.id == content_id, Content.is_published == True
    ).first()
    
    if not content:
        logger.warning(f"内容不存在或未发布: 内容ID={content_id}")
        raise ResourceNotFoundError(message="内容不存在或未发布", details={"content_id": content_id})
    
    # 检查用户是否已点赞
    existing_like = db.query(Like).filter(
        Like.user_id == current_user.id,
        Like.content_id == content_id
    ).first()
    
    if existing_like:
        # 已点赞，取消点赞
        db.delete(existing_like)
        content.likes = max(0, content.likes - 1)
        is_liked = False
        logger.info(f"取消点赞成功: 内容ID={content_id}, 用户ID={current_user.id}")
    else:
        # 未点赞，添加点赞
        new_like = Like(
            user_id=current_user.id,
            content_id=content_id
        )
        db.add(new_like)
        content.likes += 1
        is_liked = True
        logger.info(f"点赞成功: 内容ID={content_id}, 用户ID={current_user.id}")
    
    db.commit()
    
    # 获取最新的点赞总数
    like_count = db.query(Like).filter(Like.content_id == content_id).count()
    
    return {"is_liked": is_liked, "like_count": like_count}


@router.get("/api/content/{content_id}/like/status", response_model=LikeStatusResponse, dependencies=[Depends(RateLimiter(times=20, seconds=60))])
def get_like_status(
    content_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    获取内容点赞状态接口
    
    Args:
        content_id: 要获取点赞状态的内容ID
        db: 数据库会话
        current_user: 当前认证的活跃用户
    
    Returns:
        LikeStatusResponse: 包含是否已点赞和点赞总数的响应
    
    Raises:
        ResourceNotFoundError: 404错误，如果内容不存在
    """
    logger.info(f"获取点赞状态请求: 内容ID={content_id}, 用户ID={current_user.id}")
    
    # 查找内容
    content = db.query(Content).filter(Content.id == content_id).first()
    
    if not content:
        logger.warning(f"内容不存在: 内容ID={content_id}")
        raise ResourceNotFoundError(message="内容不存在", details={"content_id": content_id})
    
    # 检查用户是否已点赞
    existing_like = db.query(Like).filter(
        Like.user_id == current_user.id,
        Like.content_id == content_id
    ).first()
    
    # 获取点赞总数
    like_count = db.query(Like).filter(Like.content_id == content_id).count()
    
    is_liked = existing_like is not None
    
    logger.info(f"获取点赞状态成功: 内容ID={content_id}, 用户ID={current_user.id}, 是否已点赞={is_liked}, 点赞数={like_count}")
    return {"is_liked": is_liked, "like_count": like_count}


@router.get("/api/articles", response_model=List[ContentResponse])
def get_all_articles(db: Session = Depends(get_db)):
    """
    获取所有文章接口
    
    Args:
        db: 数据库会话
    
    Returns:
        List[ContentResponse]: 所有文章列表
    """
    logger.info("获取所有文章请求")
    
    # 获取所有已发布的非智能体文章
    articles = db.query(Content).filter(
        Content.is_published == True,
        Content.category != "agent"
    ).order_by(Content.created_at.desc()).all()
    
    # 为每个文章获取实时点赞数（从Like表查询，而不是使用缓存的Content.likes）
    for article in articles:
        real_time_likes = db.query(Like).filter(Like.content_id == article.id).count()
        article.likes = real_time_likes
    
    logger.info(f"获取所有文章成功: 返回数量={len(articles)}")
    return articles


@router.get("/api/articles/latest", response_model=List[ContentResponse])
def get_latest_articles(limit: int = 5, db: Session = Depends(get_db)):
    """
    获取最新文章接口
    
    Args:
        limit: 返回的最大文章数
        db: 数据库会话
    
    Returns:
        List[ContentResponse]: 最新文章列表
    """
    logger.info(f"获取最新文章请求: limit={limit}")
    
    # 获取最新发布的非智能体文章
    articles = db.query(Content).filter(
        Content.is_published == True,
        Content.category != "agent"
    ).order_by(Content.created_at.desc()).limit(limit).all()
    
    # 为每个文章获取实时点赞数（从Like表查询，而不是使用缓存的Content.likes）
    for article in articles:
        real_time_likes = db.query(Like).filter(Like.content_id == article.id).count()
        article.likes = real_time_likes
    
    logger.info(f"获取最新文章成功: 返回数量={len(articles)}")
    return articles


@router.get("/api/agents", response_model=List[ContentResponse])
def get_all_agents(db: Session = Depends(get_db)):
    """
    获取所有智能体接口
    
    Args:
        db: 数据库会话
    
    Returns:
        List[ContentResponse]: 所有智能体列表
    """
    logger.info("获取所有智能体请求")
    
    # 获取所有已发布的智能体（包含母婴相关智能体分类）
    agents = db.query(Content).filter(
        Content.is_published == True,
        Content.category == "agent"
    ).order_by(Content.created_at.desc()).all()
    
    # 为每个智能体获取实时点赞数（从Like表查询）
    for agent in agents:
        real_time_likes = db.query(Like).filter(Like.content_id == agent.id).count()
        agent.likes = real_time_likes
    
    logger.info(f"获取所有智能体成功: 返回数量={len(agents)}")
    return agents


@router.get("/api/agents/latest", response_model=List[ContentResponse])
def get_latest_agents(limit: int = 5, db: Session = Depends(get_db)):
    """
    获取最新智能体接口
    
    Args:
        limit: 返回的最大智能体数
        db: 数据库会话
    
    Returns:
        List[ContentResponse]: 最新智能体列表
    """
    logger.info(f"获取最新智能体请求: limit={limit}")
    
    # 获取最新发布的智能体（包含母婴相关智能体分类）
    agents = db.query(Content).filter(
        Content.is_published == True,
        Content.category == "agent"
    ).order_by(Content.created_at.desc()).limit(limit).all()
    
    # 为每个智能体获取实时点赞数（从Like表查询）
    for agent in agents:
        real_time_likes = db.query(Like).filter(Like.content_id == agent.id).count()
        agent.likes = real_time_likes
    
    logger.info(f"获取最新智能体成功: 返回数量={len(agents)}")
    return agents


@router.get("/api/agents/{agent_id}/download")
def download_agent(
    agent_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    下载智能体PDF接口
    
    Args:
        agent_id: 要下载的智能体ID
        db: 数据库会话
        current_user: 当前认证的活跃用户
    
    Returns:
        StreamingResponse: 智能体PDF文件流
    
    Raises:
        ResourceNotFoundError: 404错误，如果智能体不存在
        AuthorizationError: 403错误，如果用户没有购买该智能体
    """
    logger.info(f"下载智能体请求: 智能体ID={agent_id}, 用户ID={current_user.id}")
    
    # 查找智能体
    agent = db.query(Content).filter(
        Content.id == agent_id,
        Content.is_published == True,
        Content.category == "agent"
    ).first()
    
    if not agent:
        logger.warning(f"智能体不存在: 智能体ID={agent_id}")
        raise ResourceNotFoundError(message="智能体不存在", details={"agent_id": agent_id})
    
    # 检查用户是否已购买该智能体
    if not check_user_purchased_agent(db, current_user.id, agent_id):
        logger.warning(f"用户未购买该智能体: 用户ID={current_user.id}, 智能体ID={agent_id}")
        raise AuthorizationError(message="您尚未购买该智能体", details={"agent_id": agent_id})
    
    # 生成PDF
    pdf_generator = PDFGenerator()
    agent_content = {
        "title": agent.title,
        "content": agent.content
    }
    
    pdf_buffer = pdf_generator.generate_agent_pdf(agent_content, agent.title)
    
    # 创建响应
    pdf_buffer.seek(0)
    
    logger.info(f"智能体PDF生成成功: 智能体ID={agent_id}, 用户ID={current_user.id}")
    
    # 使用RFC 5987标准对中文文件名进行编码
    from urllib.parse import quote
    filename = f"{agent.title}.pdf"
    encoded_filename = quote(filename.encode('utf-8'))
    
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename*=UTF-8''{encoded_filename}"
        }
    )


@router.put("/api/content/{content_id}", response_model=ContentResponse, dependencies=[Depends(RateLimiter(times=10, seconds=60))])
def update_content(
    content_id: int,
    request: Request,
    content_update: ContentUpdate,
    csrf_protect: CsrfProtect = Depends(),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """更新内容接口 - 添加CSRF保护"""
    csrf_protect.validate_csrf(request)
    """
    更新内容接口
    
    Args:
        content_id: 要更新的内容ID
        content_update: 内容更新请求数据
        db: 数据库会话
        current_user: 当前认证的活跃用户
    
    Returns:
        ContentResponse: 更新后的内容信息
    
    Raises:
        HTTPException: 404错误，如果内容不存在
        HTTPException: 403错误，如果用户没有权限更新内容
    """
    logger.info(f"更新内容请求: 内容ID={content_id}, 用户ID={current_user.id}, 更新字段={content_update.model_dump(exclude_unset=True).keys()}")
    
    # 查找内容
    content = db.query(Content).filter(Content.id == content_id).first()
    
    if not content:
        logger.warning(f"内容不存在: 内容ID={content_id}")
        raise ResourceNotFoundError(message="内容不存在", details={"content_id": content_id})
    
    # 检查用户是否有权限更新内容
    if content.author_id != current_user.id:
        logger.warning(f"没有权限更新此内容: 内容ID={content_id}, 用户ID={current_user.id}")
        raise AuthorizationError(message="没有权限更新此内容", details={"content_id": content_id, "user_id": current_user.id})
    
    # 更新内容
    update_data = content_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(content, field, value)
    
    db.commit()
    db.refresh(content)
    
    logger.info(f"内容更新成功: 内容ID={content_id}, 标题={content.title}")
    return content


@router.delete("/api/content/{content_id}", response_model=MessageResponse, dependencies=[Depends(RateLimiter(times=5, seconds=60))])
def delete_content(
    content_id: int,
    request: Request,
    csrf_protect: CsrfProtect = Depends(),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """删除内容接口 - 添加CSRF保护"""
    csrf_protect.validate_csrf(request)
    """
    删除内容接口
    
    Args:
        content_id: 要删除的内容ID
        db: 数据库会话
        current_user: 当前认证的活跃用户
    
    Returns:
        MessageResponse: 删除结果
    
    Raises:
        HTTPException: 404错误，如果内容不存在
        HTTPException: 403错误，如果用户没有权限删除内容
    """
    logger.info(f"删除内容请求: 内容ID={content_id}, 用户ID={current_user.id}")
    
    # 查找内容
    content = db.query(Content).filter(Content.id == content_id).first()
    
    if not content:
        logger.warning(f"删除内容失败: 内容ID={content_id}, 原因: 内容不存在")
        raise ResourceNotFoundError(message="内容不存在", details={"content_id": content_id})
    
    # 检查用户是否有权限删除内容
    if content.author_id != current_user.id:
        logger.warning(f"删除内容失败: 内容ID={content_id}, 用户ID={current_user.id}, 原因: 权限不足")
        raise AuthorizationError(message="没有权限删除此内容", details={"content_id": content_id, "user_id": current_user.id})
    
    # 删除内容
    db.delete(content)
    db.commit()
    
    logger.info(f"内容删除成功: 内容ID={content_id}, 标题={content.title}")
    return {
        "status": "success",
        "message": "内容已删除"
    }


# 订单管理相关路由

@router.post("/api/orders", response_model=OrderResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(RateLimiter(times=5, seconds=60))])
def create_new_order(
    request: Request,
    order: OrderCreate,
    csrf_protect: CsrfProtect = Depends(),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """创建订单接口 - 添加CSRF保护
    
    Args:
        request: HTTP请求对象
        order: 订单创建请求数据
        csrf_protect: CSRF保护依赖
        db: 数据库会话
        current_user: 当前认证的活跃用户
    
    Returns:
        OrderResponse: 创建成功的订单信息
    """
    # 在测试环境中跳过CSRF令牌验证
    if not is_test:
        csrf_protect.validate_csrf(request)
    
    # 调试信息：打印请求数据
    logger.info(f"创建订单请求: 用户ID={current_user.id}")
    logger.info(f"订单数据: 产品类型={order.product_type}, 产品ID={order.product_id}, 金额={order.amount}")
    logger.info(f"订单项数量: {len(order.items)}")
    for i, item in enumerate(order.items):
        logger.info(f"订单项 {i+1}: 产品名称={item.product_name}, 价格={item.product_price}, 数量={item.quantity}, 总金额={item.total_amount}")
    
    try:
        # 创建订单
        db_order = create_order(db, order, current_user.id)
        
        # 加载订单项
        db.refresh(db_order)
        db_order.order_items = db.query(OrderItem).filter(OrderItem.order_id == db_order.id).all()
        
        logger.info(f"订单创建成功: 订单ID={db_order.id}, 订单号={db_order.order_number}")
        return db_order
        
    except Exception as e:
        logger.error(f"创建订单失败: 用户ID={current_user.id}, 错误={str(e)}")
        raise BadRequestError(message="创建订单失败", details=str(e))


@router.get("/api/orders", response_model=OrderListResponse, dependencies=[Depends(RateLimiter(times=10, seconds=60))])
def get_orders(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    获取用户订单列表接口
    
    Args:
        skip: 跳过的记录数（用于分页）
        limit: 返回的最大记录数（用于分页）
        db: 数据库会话
        current_user: 当前认证的活跃用户
    
    Returns:
        OrderListResponse: 订单列表
    """
    logger.info(f"获取订单列表请求: 用户ID={current_user.id}, skip={skip}, limit={limit}")
    
    try:
        # 获取用户订单
        orders = get_user_orders(db, current_user.id, skip, limit)
        
        # 加载每个订单的订单项
        for order in orders:
            order.order_items = db.query(OrderItem).filter(OrderItem.order_id == order.id).all()
        
        # 获取总订单数
        total = db.query(Order).filter(Order.user_id == current_user.id).count()
        
        logger.info(f"获取订单列表成功: 用户ID={current_user.id}, 订单数={len(orders)}, 总数={total}")
        return {
            "status": "success",
            "data": orders,
            "total": total
        }
        
    except Exception as e:
        logger.error(f"获取订单列表失败: 用户ID={current_user.id}, 错误={str(e)}")
        raise BadRequestError(message="获取订单列表失败", details=str(e))


@router.get("/api/orders/{order_id}", response_model=OrderResponse, dependencies=[Depends(RateLimiter(times=10, seconds=60))])
def get_order_detail(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    获取订单详情接口
    
    Args:
        order_id: 订单ID
        db: 数据库会话
        current_user: 当前认证的活跃用户
    
    Returns:
        OrderResponse: 订单详情
    
    Raises:
        HTTPException: 404错误，如果订单不存在
        HTTPException: 403错误，如果用户没有权限查看该订单
    """
    logger.info(f"获取订单详情请求: 订单ID={order_id}, 用户ID={current_user.id}")
    
    try:
        # 获取订单
        order = get_order(db, order_id, current_user.id)
        if not order:
            logger.warning(f"订单不存在或没有权限查看: 订单ID={order_id}, 用户ID={current_user.id}")
            raise ResourceNotFoundError(message="订单不存在或没有权限查看", details={"order_id": order_id})
        
        # 加载订单项
        order.order_items = db.query(OrderItem).filter(OrderItem.order_id == order.id).all()
        
        logger.info(f"获取订单详情成功: 订单ID={order_id}, 订单号={order.order_number}")
        return order
        
    except ResourceNotFoundError:
        raise
    except Exception as e:
        logger.error(f"获取订单详情失败: 订单ID={order_id}, 用户ID={current_user.id}, 错误={str(e)}")
        raise BadRequestError(message="获取订单详情失败", details=str(e))


@router.post("/api/orders/{order_id}/pay", response_model=PaymentResponse, dependencies=[Depends(RateLimiter(times=5, seconds=60))])
def pay_for_order(
    order_id: int,
    request: Request,
    payment: PaymentRequest,
    csrf_protect: CsrfProtect = Depends(),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """订单支付接口 - 添加CSRF保护
    
    Args:
        order_id: 订单ID
        request: HTTP请求对象
        payment: 支付请求数据
        csrf_protect: CSRF保护依赖
        db: 数据库会话
        current_user: 当前认证的活跃用户
    
    Returns:
        PaymentResponse: 支付处理结果
    """
    csrf_protect.validate_csrf(request)
    logger.info(f"订单支付请求: 订单ID={order_id}, 用户ID={current_user.id}, 支付方式={payment.payment_method}")
    
    try:
        # 验证用户是否有权限支付该订单
        order = get_order(db, order_id, current_user.id)
        if not order:
            logger.warning(f"订单不存在或没有权限支付: 订单ID={order_id}, 用户ID={current_user.id}")
            raise ResourceNotFoundError(message="订单不存在或没有权限支付", details={"order_id": order_id})
        
        # 处理支付请求
        payment_result = process_payment(db, order_id, payment.payment_method, payment.return_url)
        
        logger.info(f"订单支付请求处理成功: 订单ID={order_id}, 交易ID={payment_result['transaction_id']}")
        return {
            "status": "success",
            "order_id": payment_result["order_id"],
            "order_number": payment_result["order_number"],
            "payment_method": payment_result["payment_method"],
            "payment_url": payment_result["payment_url"],
            "transaction_id": payment_result["transaction_id"],
            "message": "支付请求处理成功，请跳转到支付页面完成支付"
        }
        
    except ResourceNotFoundError:
        raise
    except ValueError as e:
        logger.warning(f"支付请求失败: 订单ID={order_id}, 原因={str(e)}")
        raise BadRequestError(message="支付请求失败", details=str(e))
    except Exception as e:
        logger.error(f"处理支付请求失败: 订单ID={order_id}, 错误={str(e)}")
        raise BadRequestError(message="处理支付请求失败", details=str(e))


@router.post("/api/orders/{order_id}/cancel", response_model=MessageResponse, dependencies=[Depends(RateLimiter(times=5, seconds=60))])
def cancel_user_order(
    order_id: int,
    request: Request,
    csrf_protect: CsrfProtect = Depends(),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """取消订单接口 - 添加CSRF保护
    
    Args:
        order_id: 订单ID
        request: HTTP请求对象
        csrf_protect: CSRF保护依赖
        db: 数据库会话
        current_user: 当前认证的活跃用户
    
    Returns:
        MessageResponse: 取消订单结果
    """
    csrf_protect.validate_csrf(request)
    logger.info(f"取消订单请求: 订单ID={order_id}, 用户ID={current_user.id}")
    
    try:
        # 取消订单
        result = cancel_order(db, order_id, current_user.id)
        
        if not result:
            logger.warning(f"取消订单失败: 订单ID={order_id}, 用户ID={current_user.id}")
            raise BadRequestError(message="取消订单失败", details="订单不存在、已支付或没有权限取消")
        
        logger.info(f"订单取消成功: 订单ID={order_id}, 用户ID={current_user.id}")
        return {
            "status": "success",
            "message": "订单已成功取消"
        }
        
    except Exception as e:
        logger.error(f"取消订单失败: 订单ID={order_id}, 用户ID={current_user.id}, 错误={str(e)}")
        raise BadRequestError(message="取消订单失败", details=str(e))


@router.post("/api/payment/callback", dependencies=[Depends(RateLimiter(times=20, seconds=60))])
async def handle_payment_notification(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    支付回调接口
    支持自定义回调格式和支付宝真实回调格式
    
    Args:
        request: HTTP请求对象
        db: 数据库会话
    
    Returns:
        MessageResponse: 支付回调处理结果
    """
    callback_data = {}
    try:
        # 尝试获取请求数据
        try:
            # 尝试解析为JSON格式（自定义回调）
            callback_data = await request.json()
        except Exception:
            # 解析失败，尝试解析为表单格式（支付宝回调）
            callback_data = dict(await request.form())
            
            # 将字符串类型的金额转换为浮点数
            if 'total_amount' in callback_data:
                callback_data['total_amount'] = float(callback_data['total_amount'])
        
        logger.info(f"收到支付回调: {callback_data}")
        
        # 处理不同的回调格式
        if 'out_trade_no' in callback_data:  # 支付宝回调格式
            order_number = callback_data.get('out_trade_no')
            transaction_id = callback_data.get('trade_no')
            trade_status = callback_data.get('trade_status')
            amount = callback_data.get('total_amount')
            payment_method = 'alipay'
            
            # 转换支付宝状态为系统状态
            if trade_status == 'TRADE_SUCCESS':
                status = 'success'
            else:
                status = 'failed'
        else:  # 自定义回调格式
            order_number = callback_data.get('order_number')
            transaction_id = callback_data.get('transaction_id')
            status = callback_data.get('status')
            amount = callback_data.get('amount')
            payment_method = callback_data.get('payment_method')
        
        # 验证必填字段
        if not all([order_number, transaction_id, status, amount, payment_method]):
            logger.error("支付回调处理失败: 缺少必填字段")
            raise BadRequestError(message="支付回调处理失败", details="缺少必填字段")
        
        # 处理支付回调
        result = handle_payment_callback(
            db,
            order_number,
            transaction_id,
            status,
            amount,
            payment_method
        )
        
        if result:
            logger.info(f"支付回调处理成功: 订单号={order_number}")
            
            # 支付宝要求返回特定格式的响应
            if 'out_trade_no' in callback_data:
                return {"alipay_trade_notify_response": {"code": "10000", "msg": "Success"}}
            else:
                return {
                    "status": "success",
                    "message": "支付回调处理成功"
                }
        else:
            logger.warning(f"支付回调处理失败: 订单号={order_number}")
            
            # 支付宝要求返回特定格式的响应
            if 'out_trade_no' in callback_data:
                return {"alipay_trade_notify_response": {"code": "40004", "msg": "Failure"}}
            else:
                raise BadRequestError(message="支付回调处理失败", details="订单不存在或金额不匹配")
                
    except BadRequestError:
        raise
    except Exception as e:
        logger.error(f"处理支付回调失败: 错误={str(e)}")
        
        # 根据已保存的回调数据判断是否为支付宝回调
        if 'out_trade_no' in callback_data:
            return {"alipay_trade_notify_response": {"code": "40004", "msg": "Failure"}}
        else:
            raise BadRequestError(message="处理支付回调失败", details=str(e))


# 下载文件接口
@router.get("/api/download/{product_id}")
async def download_file(product_id: str):
    # 模拟文件下载功能
    # 在实际项目中，这里应该从数据库获取产品信息，然后返回实际的文件
    file_content = """This is a mock agent file content.

In a real project, this should return the actual agent content.

Product ID: %s
""" % product_id
    
    # 将字符串编码为字节
    file_bytes = file_content.encode('utf-8')
    
    headers = {
        "Content-Disposition": f"attachment; filename=agent_{product_id}.zip",
        "Content-Type": "application/zip"
    }
    
    return Response(content=file_bytes, headers=headers)


# 联盟推广系统API

# 生成推广链接
@router.post("/api/affiliate/links")
async def generate_affiliate_link(db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    """
    为当前用户生成推广链接
    """
    import uuid
    
    # 检查用户是否已有推广链接
    existing_link = db.query(AffiliateLink).filter(AffiliateLink.user_id == current_user.id).first()
    
    if existing_link:
        return JSONResponse(status_code=status.HTTP_200_OK, content={
            "message": "推广链接已存在",
            "data": {
                "id": existing_link.id,
                "unique_code": existing_link.unique_code,
                "link": f"http://localhost:5173?ref={existing_link.unique_code}",
                "is_active": existing_link.is_active,
                "created_at": existing_link.created_at,
                "updated_at": existing_link.updated_at
            }
        })
    
    # 生成唯一推广码
    unique_code = str(uuid.uuid4())[:8]
    
    # 创建推广链接
    new_link = AffiliateLink(
        user_id=current_user.id,
        unique_code=unique_code,
        is_active=True
    )
    
    db.add(new_link)
    db.commit()
    db.refresh(new_link)
    
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={
        "message": "推广链接生成成功",
        "data": {
            "id": new_link.id,
            "unique_code": new_link.unique_code,
            "link": f"http://localhost:5173?ref={new_link.unique_code}",
            "is_active": new_link.is_active,
            "created_at": new_link.created_at,
            "updated_at": new_link.updated_at
        }
    })


# 获取用户推广链接
@router.get("/api/affiliate/links")
async def get_affiliate_link(db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    """
    获取当前用户的推广链接
    """
    link = db.query(AffiliateLink).filter(AffiliateLink.user_id == current_user.id).first()
    
    if not link:
        raise ResourceNotFoundError(message="推广链接不存在，请先生成")
    
    return JSONResponse(status_code=status.HTTP_200_OK, content={
        "message": "获取推广链接成功",
        "data": {
            "id": link.id,
            "unique_code": link.unique_code,
            "link": f"http://localhost:5173?ref={link.unique_code}",
            "is_active": link.is_active,
            "created_at": link.created_at,
            "updated_at": link.updated_at
        }
    })


# 处理推广链接点击
@router.get("/api/affiliate/track/{unique_code}")
async def track_affiliate_click(unique_code: str, request: Request, db: Session = Depends(get_db)):
    """
    处理推广链接点击，记录点击信息
    """
    # 查找推广链接
    link = db.query(AffiliateLink).filter(AffiliateLink.unique_code == unique_code).first()
    
    if not link or not link.is_active:
        # 即使链接不存在或已失效，也重定向到首页
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url="http://localhost:5173")
    
    # 记录点击信息
    click = AffiliateClick(
        affiliate_link_id=link.id,
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("User-Agent"),
        referrer=request.headers.get("Referer")
    )
    
    db.add(click)
    db.commit()
    
    # 重定向到首页
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="http://localhost:5173")


# 处理前端发送的推广跟踪请求
@router.post("/api/affiliate/track")
async def track_referral(referral_code: str = Body(...), request: Request = None, db: Session = Depends(get_db)):
    """
    处理前端发送的推广跟踪请求，记录点击信息
    """
    # 查找推广链接
    link = db.query(AffiliateLink).filter(AffiliateLink.unique_code == referral_code).first()
    
    if link and link.is_active:
        # 记录点击信息
        click = AffiliateClick(
            affiliate_link_id=link.id,
            ip_address=request.client.host if request.client else None,
            user_agent=request.headers.get("User-Agent"),
            referrer=request.headers.get("Referer")
        )
        
        db.add(click)
        db.commit()
    
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Referral tracked successfully"})


# 获取推广统计数据
@router.get("/api/affiliate/stats")
async def get_affiliate_stats(db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    """
    获取当前用户的推广统计数据
    """
    # 获取用户的推广链接
    link = db.query(AffiliateLink).filter(AffiliateLink.user_id == current_user.id).first()
    
    if not link:
        raise ResourceNotFoundError(message="推广链接不存在，请先生成")
    
    # 计算点击次数
    click_count = db.query(func.count(AffiliateClick.id)).filter(AffiliateClick.affiliate_link_id == link.id).scalar()
    
    # 计算佣金总额
    commission_total = db.query(func.sum(AffiliateCommission.amount)).filter(
        AffiliateCommission.affiliate_link_id == link.id,
        AffiliateCommission.status == "paid"
    ).scalar() or 0
    
    # 计算待结算佣金
    pending_commission = db.query(func.sum(AffiliateCommission.amount)).filter(
        AffiliateCommission.affiliate_link_id == link.id,
        AffiliateCommission.status == "pending"
    ).scalar() or 0
    
    return JSONResponse(status_code=status.HTTP_200_OK, content={
        "message": "获取统计数据成功",
        "data": {
            "click_count": click_count,
            "commission_total": float(commission_total),
            "pending_commission": float(pending_commission),
            "link_id": link.id
        }
    })


# 获取佣金记录
@router.get("/api/affiliate/commissions")
async def get_affiliate_commissions(db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    """
    获取当前用户的佣金记录
    """
    # 获取用户的推广链接
    link = db.query(AffiliateLink).filter(AffiliateLink.user_id == current_user.id).first()
    
    if not link:
        raise ResourceNotFoundError(message="推广链接不存在，请先生成")
    
    # 获取佣金记录
    commissions = db.query(AffiliateCommission).filter(
        AffiliateCommission.affiliate_link_id == link.id
    ).order_by(AffiliateCommission.created_at.desc()).all()
    
    # 格式化佣金记录
    commission_list = []
    for commission in commissions:
        commission_list.append({
            "id": commission.id,
            "order_id": commission.order_id,
            "amount": float(commission.amount),
            "status": commission.status,
            "created_at": commission.created_at,
            "paid_at": commission.paid_at,
            "cancelled_at": commission.cancelled_at
        })
    
    return JSONResponse(status_code=status.HTTP_200_OK, content={
        "message": "获取佣金记录成功",
        "data": commission_list
    })


# ========== 管理后台API ==========

# 内容管理API

@router.get("/api/admin/contents", dependencies=[Depends(get_current_admin_user)])
def get_admin_contents(
    category: Optional[str] = None,
    is_published: Optional[bool] = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """
    获取所有内容列表（管理后台）
    
    Args:
        category: 可选的内容分类筛选
        is_published: 可选的发布状态筛选
        skip: 跳过的记录数
        limit: 返回的记录数
        db: 数据库会话
    
    Returns:
        JSONResponse: 内容列表
    """
    # 权限检查已在路由依赖中完成
    
    query = db.query(Content)
    
    if category:
        query = query.filter(Content.category == category)
    
    if is_published is not None:
        query = query.filter(Content.is_published == is_published)
    
    total = query.count()
    contents = query.offset(skip).limit(limit).all()
    
    return JSONResponse({
        "status": "success",
        "data": [{
            "id": content.id,
            "title": content.title,
            "category": content.category,
            "is_published": content.is_published,
            "view_count": content.view_count,
            "created_at": content.created_at.isoformat() if content.created_at else None,
            "updated_at": content.updated_at.isoformat() if content.updated_at else None,
            "published_at": content.published_at.isoformat() if content.published_at else None
        } for content in contents],
        "total": total
    })

@router.post("/api/admin/contents", dependencies=[Depends(get_current_admin_user)])
def create_admin_content(
    content_data: ContentCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    创建新内容（管理后台）
    
    Args:
        content_data: 内容数据
        current_user: 当前用户
        db: 数据库会话
    
    Returns:
        JSONResponse: 创建结果
    """
    new_content = Content(
        title=content_data.title,
        category=content_data.category,
        summary=content_data.summary,
        content=content_data.content,
        author_id=current_user.id,
        is_published=False
    )
    
    db.add(new_content)
    db.commit()
    db.refresh(new_content)
    
    return JSONResponse({
        "status": "success",
        "message": "内容创建成功",
        "data": {
            "id": new_content.id,
            "title": new_content.title
        }
    }, status_code=status.HTTP_201_CREATED)

@router.put("/api/admin/contents/{content_id}", dependencies=[Depends(get_current_admin_user)])
def update_admin_content(
    content_id: int,
    content_data: ContentUpdate,
    db: Session = Depends(get_db)
):
    """
    更新内容（管理后台）
    
    Args:
        content_id: 内容ID
        content_data: 更新的内容数据
        db: 数据库会话
    
    Returns:
        JSONResponse: 更新结果
    """
    content = db.query(Content).filter(Content.id == content_id).first()
    
    if not content:
        raise ResourceNotFoundError(message="内容不存在")
    
    # 更新内容字段
    update_data = content_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(content, field, value)
    
    # 如果设置为发布状态且之前未发布，则设置发布时间
    if content.is_published and not content.published_at:
        content.published_at = datetime.utcnow()
    
    db.commit()
    db.refresh(content)
    
    return JSONResponse({
        "status": "success",
        "message": "内容更新成功",
        "data": {
            "id": content.id,
            "title": content.title,
            "is_published": content.is_published
        }
    })

@router.delete("/api/admin/contents/{content_id}", dependencies=[Depends(get_current_admin_user)])
def delete_admin_content(
    content_id: int,
    db: Session = Depends(get_db)
):
    """
    删除内容（管理后台）
    
    Args:
        content_id: 内容ID
        db: 数据库会话
    
    Returns:
        JSONResponse: 删除结果
    """
    content = db.query(Content).filter(Content.id == content_id).first()
    
    if not content:
        raise ResourceNotFoundError(message="内容不存在")
    
    db.delete(content)
    db.commit()
    
    return JSONResponse({
        "status": "success",
        "message": "内容删除成功"
    })

# 用户管理API

@router.get("/api/admin/users", dependencies=[Depends(get_current_admin_user)])
def get_admin_users(
    is_active: Optional[bool] = None,
    is_admin: Optional[bool] = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """
    获取所有用户列表（管理后台）
    
    Args:
        is_active: 可选的用户状态筛选
        is_admin: 可选的管理员状态筛选
        skip: 跳过的记录数
        limit: 返回的记录数
        db: 数据库会话
    
    Returns:
        JSONResponse: 用户列表
    """
    query = db.query(User)
    
    if is_active is not None:
        query = query.filter(User.is_active == is_active)
    
    if is_admin is not None:
        query = query.filter(User.is_admin == is_admin)
    
    total = query.count()
    users = query.offset(skip).limit(limit).all()
    
    return JSONResponse({
        "status": "success",
        "data": [{
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "is_active": user.is_active,
            "is_admin": user.is_admin,
            "created_at": user.created_at.isoformat() if user.created_at else None
        } for user in users],
        "total": total
    })

@router.put("/api/admin/users/{user_id}", dependencies=[Depends(get_current_admin_user)])
def update_admin_user(
    user_id: int,
    is_active: Optional[bool] = None,
    is_admin: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """
    更新用户状态（管理后台）
    
    Args:
        user_id: 用户ID
        is_active: 可选的用户状态
        is_admin: 可选的管理员状态
        db: 数据库会话
    
    Returns:
        JSONResponse: 更新结果
    """
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise ResourceNotFoundError(message="用户不存在")
    
    # 更新用户字段
    if is_active is not None:
        user.is_active = is_active
    
    if is_admin is not None:
        user.is_admin = is_admin
    
    db.commit()
    db.refresh(user)
    
    return JSONResponse({
        "status": "success",
        "message": "用户信息更新成功",
        "data": {
            "id": user.id,
            "username": user.username,
            "is_active": user.is_active,
            "is_admin": user.is_admin
        }
    })

# 订单管理API

@router.get("/api/admin/orders", dependencies=[Depends(get_current_admin_user)])
def get_admin_orders(
    status: Optional[str] = None,
    product_type: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """
    获取所有订单列表（管理后台）
    
    Args:
        status: 可选的订单状态筛选
        product_type: 可选的产品类型筛选
        start_date: 可选的开始日期筛选
        end_date: 可选的结束日期筛选
        skip: 跳过的记录数
        limit: 返回的记录数
        db: 数据库会话
    
    Returns:
        JSONResponse: 订单列表
    """
    query = db.query(Order)
    
    if status:
        query = query.filter(Order.status == status)
    
    if product_type:
        query = query.filter(Order.product_type == product_type)
    
    if start_date:
        query = query.filter(Order.created_at >= datetime.combine(start_date, datetime.min.time()))
    
    if end_date:
        query = query.filter(Order.created_at <= datetime.combine(end_date, datetime.max.time()))
    
    total = query.count()
    orders = query.offset(skip).limit(limit).all()
    
    return JSONResponse({
        "status": "success",
        "data": [{
            "id": order.id,
            "order_number": order.order_number,
            "user_id": order.user_id,
            "amount": float(order.amount),
            "status": order.status,
            "payment_method": order.payment_method,
            "product_type": order.product_type,
            "product_id": order.product_id,
            "created_at": order.created_at.isoformat() if order.created_at else None,
            "paid_at": order.paid_at.isoformat() if order.paid_at else None
        } for order in orders],
        "total": total
    })

@router.get("/api/admin/orders/{order_id}", dependencies=[Depends(get_current_admin_user)])
def get_admin_order_detail(
    order_id: int,
    db: Session = Depends(get_db)
):
    """
    获取订单详情（管理后台）
    
    Args:
        order_id: 订单ID
        db: 数据库会话
    
    Returns:
        JSONResponse: 订单详情
    """
    order = db.query(Order).filter(Order.id == order_id).first()
    
    if not order:
        raise ResourceNotFoundError(message="订单不存在")
    
    return JSONResponse({
        "status": "success",
        "data": {
            "id": order.id,
            "order_number": order.order_number,
            "user_id": order.user_id,
            "amount": float(order.amount),
            "status": order.status,
            "payment_method": order.payment_method,
            "payment_transaction_id": order.payment_transaction_id,
            "product_type": order.product_type,
            "product_id": order.product_id,
            "created_at": order.created_at.isoformat() if order.created_at else None,
            "paid_at": order.paid_at.isoformat() if order.paid_at else None,
            "cancelled_at": order.cancelled_at.isoformat() if order.cancelled_at else None,
            "items": [{
                "id": item.id,
                "product_name": item.product_name,
                "product_price": float(item.product_price),
                "quantity": item.quantity,
                "total_amount": float(item.total_amount)
            } for item in order.items]
        }
    })

# 推广统计API

@router.get("/api/admin/affiliate/stats", dependencies=[Depends(get_current_admin_user)])
def get_admin_affiliate_stats(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db)
):
    """
    获取推广统计数据（管理后台）
    
    Args:
        start_date: 可选的开始日期筛选
        end_date: 可选的结束日期筛选
        db: 数据库会话
    
    Returns:
        JSONResponse: 推广统计数据
    """
    # 基础查询条件
    click_query = db.query(AffiliateClick)
    commission_query = db.query(AffiliateCommission)
    
    # 日期筛选
    if start_date:
        click_query = click_query.filter(AffiliateClick.clicked_at >= datetime.combine(start_date, datetime.min.time()))
        commission_query = commission_query.filter(AffiliateCommission.created_at >= datetime.combine(start_date, datetime.min.time()))
    
    if end_date:
        click_query = click_query.filter(AffiliateClick.clicked_at <= datetime.combine(end_date, datetime.max.time()))
        commission_query = commission_query.filter(AffiliateCommission.created_at <= datetime.combine(end_date, datetime.max.time()))
    
    # 计算各项统计指标
    total_clicks = click_query.count()
    total_commissions = commission_query.count()
    total_commission_amount = db.query(func.sum(AffiliateCommission.amount)).scalar() or 0
    
    # 统计不同状态的佣金
    commission_status_counts = db.query(
        AffiliateCommission.status,
        func.count(AffiliateCommission.id)
    ).group_by(AffiliateCommission.status).all()
    
    # 统计不同状态的佣金金额
    commission_status_amounts = db.query(
        AffiliateCommission.status,
        func.sum(AffiliateCommission.amount)
    ).group_by(AffiliateCommission.status).all()
    
    # 转换结果格式
    status_counts = {}
    status_amounts = {}
    
    for status, count in commission_status_counts:
        status_counts[status] = count
    
    for status, amount in commission_status_amounts:
        status_amounts[status] = float(amount or 0)
    
    return JSONResponse({
        "status": "success",
        "data": {
            "total_clicks": total_clicks,
            "total_commissions": total_commissions,
            "total_commission_amount": float(total_commission_amount),
            "commission_status_counts": status_counts,
            "commission_status_amounts": status_amounts
        }
    })

@router.get("/api/admin/affiliate/top-users", dependencies=[Depends(get_current_admin_user)])
def get_admin_top_affiliate_users(
    limit: int = 10,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db)
):
    """
    获取最活跃的推广用户排名（管理后台）
    
    Args:
        limit: 返回的用户数量
        start_date: 可选的开始日期筛选
        end_date: 可选的结束日期筛选
        db: 数据库会话
    
    Returns:
        JSONResponse: 推广用户排名
    """
    # 构建查询
    query = db.query(
        User.id,
        User.username,
        User.email,
        func.count(AffiliateClick.id).label('click_count'),
        func.count(AffiliateCommission.id).label('commission_count'),
        func.sum(AffiliateCommission.amount).label('total_commission_amount')
    ).join(
        AffiliateLink, User.id == AffiliateLink.user_id
    ).outerjoin(
        AffiliateClick, AffiliateLink.id == AffiliateClick.affiliate_link_id
    ).outerjoin(
        AffiliateCommission, AffiliateLink.id == AffiliateCommission.affiliate_link_id
    )
    
    # 日期筛选
    if start_date:
        query = query.filter(AffiliateClick.clicked_at >= datetime.combine(start_date, datetime.min.time()))
        query = query.filter(AffiliateCommission.created_at >= datetime.combine(start_date, datetime.min.time()))
    
    if end_date:
        query = query.filter(AffiliateClick.clicked_at <= datetime.combine(end_date, datetime.max.time()))
        query = query.filter(AffiliateCommission.created_at <= datetime.combine(end_date, datetime.max.time()))
    
    # 分组和排序
    top_users = query.group_by(User.id).order_by(func.sum(AffiliateCommission.amount).desc().nullslast()).limit(limit).all()
    
    return JSONResponse({
        "status": "success",
        "data": [{
            "user_id": user.id,
            "username": user.username,
            "email": user.email,
            "click_count": user.click_count,
            "commission_count": user.commission_count,
            "total_commission_amount": float(user.total_commission_amount or 0)
        } for user in top_users]
    })


# 内容统计API

@router.get("/api/admin/content/stats", dependencies=[Depends(get_current_admin_user)])
def get_admin_content_stats(
    db: Session = Depends(get_db)
):
    """
    获取内容统计数据（管理后台）
    
    Args:
        db: 数据库会话
    
    Returns:
        JSONResponse: 内容统计数据
    """
    # 统计总浏览量
    total_views = db.query(func.sum(Content.view_count)).scalar() or 0
    
    # 统计总点赞数
    total_likes = db.query(func.sum(Content.likes)).scalar() or 0
    
    # 统计各分类的内容数量
    category_counts = db.query(
        Content.category,
        func.count(Content.id)
    ).group_by(Content.category).all()
    
    # 转换结果格式
    category_stats = {}
    for category, count in category_counts:
        category_stats[category] = count
    
    return JSONResponse({
        "status": "success",
        "data": {
            "total_views": int(total_views),
            "total_likes": int(total_likes),
            "category_stats": category_stats
        }
    })


# 收藏API

@router.post("/api/content/{content_id}/collect", response_model=FavoriteResponse, dependencies=[Depends(RateLimiter(times=20, seconds=60))])
def toggle_collect(
    content_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    收藏/取消收藏内容接口
    
    Args:
        content_id: 要收藏的内容ID
        db: 数据库会话
        current_user: 当前认证的活跃用户
    
    Returns:
        FavoriteResponse: 收藏记录
    
    Raises:
        ResourceNotFoundError: 404错误，如果内容不存在或未发布
        ConflictError: 409错误，如果收藏记录已存在
    """
    from models import Favorite
    
    logger.info(f"收藏请求: 内容ID={content_id}, 用户ID={current_user.id}")
    
    # 查找内容
    content = db.query(Content).filter(
        Content.id == content_id, Content.is_published == True
    ).first()
    
    if not content:
        logger.warning(f"内容不存在或未发布: 内容ID={content_id}")
        raise ResourceNotFoundError(message="内容不存在或未发布", details={"content_id": content_id})
    
    # 检查是否已收藏
    existing_favorite = db.query(Favorite).filter(
        Favorite.user_id == current_user.id,
        Favorite.content_id == content_id
    ).first()
    
    if existing_favorite:
        # 取消收藏
        db.delete(existing_favorite)
        db.commit()
        logger.info(f"取消收藏成功: 内容ID={content_id}, 用户ID={current_user.id}")
        return JSONResponse({
            "status": "success",
            "message": "取消收藏成功",
            "data": {
                "id": existing_favorite.id,
                "user_id": current_user.id,
                "content_id": content_id,
                "created_at": existing_favorite.created_at.isoformat() if existing_favorite.created_at else None
            }
        })
    
    # 创建收藏记录
    favorite = Favorite(
        user_id=current_user.id,
        content_id=content_id
    )
    
    db.add(favorite)
    db.commit()
    db.refresh(favorite)
    
    logger.info(f"收藏成功: 内容ID={content_id}, 用户ID={current_user.id}, 收藏ID={favorite.id}")
    return favorite


@router.get("/api/users/me/favorites", response_model=FavoriteListResponse)
def get_my_favorites(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=50, description="每页数量"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    获取当前用户的收藏列表接口
    
    Args:
        page: 页码，从1开始
        page_size: 每页数量，最大50
        db: 数据库会话
        current_user: 当前认证的活跃用户
    
    Returns:
        FavoriteListResponse: 收藏列表
    """
    from models import Favorite
    
    logger.info(f"获取收藏列表请求: 用户ID={current_user.id}, 页码={page}, 每页={page_size}")
    
    # 查询收藏记录
    favorites_query = db.query(Favorite).filter(
        Favorite.user_id == current_user.id
    ).order_by(Favorite.created_at.desc())
    
    # 计算总数
    total = favorites_query.count()
    
    # 分页
    favorites = favorites_query.offset((page - 1) * page_size).limit(page_size).all()
    
    # 构建响应数据
    data = []
    for fav in favorites:
        # 获取内容详情
        content = db.query(Content).filter(Content.id == fav.content_id).first()
        if content:
            data.append({
                "id": fav.id,
                "content_id": fav.content_id,
                "content": content,
                "created_at": fav.created_at
            })
    
    logger.info(f"获取收藏列表成功: 用户ID={current_user.id}, 返回数量={len(data)}, 总数={total}")
    
    return {
        "status": "success",
        "data": data,
        "total": total
    }


@router.get("/api/content/{content_id}/collect/status")
def get_collect_status(
    content_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    获取内容的收藏状态接口
    
    Args:
        content_id: 内容ID
        db: 数据库会话
        current_user: 当前认证的活跃用户
    
    Returns:
        JSONResponse: 收藏状态
    """
    from models import Favorite
    
    logger.info(f"获取收藏状态请求: 内容ID={content_id}, 用户ID={current_user.id}")
    
    # 检查是否已收藏
    favorite = db.query(Favorite).filter(
        Favorite.user_id == current_user.id,
        Favorite.content_id == content_id
    ).first()
    
    is_collected = favorite is not None
    
    logger.info(f"获取收藏状态成功: 内容ID={content_id}, 用户ID={current_user.id}, is_collected={is_collected}")
    
    return JSONResponse({
        "status": "success",
        "data": {
            "content_id": content_id,
            "is_collected": is_collected
        }
    })


@router.get("/api/content/{content_id}/detail", response_model=ContentWithLikedResponse)
def get_content_with_status(
    content_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    获取内容详情（包含点赞和收藏状态）
    
    Args:
        content_id: 内容ID
        db: 数据库会话
        current_user: 当前认证的活跃用户
    
    Returns:
        ContentWithLikedResponse: 包含状态的内容详情
    """
    from models import Favorite
    
    logger.info(f"获取内容详情（带状态）: 内容ID={content_id}, 用户ID={current_user.id}")
    
    # 查找内容
    content = db.query(Content).filter(
        Content.id == content_id, Content.is_published == True
    ).first()
    
    if not content:
        logger.warning(f"内容不存在或未发布: 内容ID={content_id}")
        raise ResourceNotFoundError(message="内容不存在或未发布", details={"content_id": content_id})
    
    # 检查是否已收藏
    favorite = db.query(Favorite).filter(
        Favorite.user_id == current_user.id,
        Favorite.content_id == content_id
    ).first()
    
    is_collected = favorite is not None
    
    # 构建响应
    result = ContentWithLikedResponse(
        id=content.id,
        title=content.title,
        category=content.category,
        summary=content.summary,
        content=content.content,
        author_id=content.author_id,
        is_published=content.is_published,
        view_count=content.view_count,
        likes=content.likes,
        created_at=content.created_at,
        updated_at=content.updated_at,
        published_at=content.published_at,
        price=content.price,
        is_liked=False,  # 点赞状态可以后续添加点赞关联表来实现
        is_collected=is_collected
    )
    
    logger.info(f"获取内容详情（带状态）成功: 内容ID={content_id}, is_collected={is_collected}")
    return result


# 商品管理相关路由

@router.post("/api/products", response_model=ProductResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_current_admin_user)])
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """
    创建商品（管理员权限）
    
    Args:
        product: 商品创建请求数据
        db: 数据库会话
        current_user: 当前认证的管理员用户
    
    Returns:
        ProductResponse: 创建成功的商品信息
    """
    from models import Product
    
    logger.info(f"创建商品请求: 商品名称={product.name}, 分类={product.category}")
    
    db_product = Product(
        name=product.name,
        description=product.description,
        image_url=product.image_url,
        link_url=product.link_url,
        price=product.price,
        category=product.category,
        is_active=True
    )
    
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    
    logger.info(f"创建商品成功: 商品ID={db_product.id}, 商品名称={product.name}")
    return db_product


@router.get("/api/products", response_model=ProductListResponse)
def get_products(
    category: Optional[str] = Query(None, description="商品分类"),
    is_active: Optional[bool] = Query(True, description="是否只查询上架商品"),
    limit: Optional[int] = Query(10, description="返回数量限制"),
    page: Optional[int] = Query(1, description="页码，默认1"),
    page_size: Optional[int] = Query(12, description="每页数量，默认12"),
    sort_by: Optional[str] = Query("created_at", description="排序方式：created_at/price_asc/price_desc/click_count"),
    db: Session = Depends(get_db)
):
    """
    获取商品列表
    
    Args:
        category: 商品分类（可选）
        is_active: 是否只查询上架商品（默认True）
        limit: 返回数量限制（默认10，用于兼容旧版本）
        page: 页码（默认1）
        page_size: 每页数量（默认12）
        sort_by: 排序方式（默认created_at）
        db: 数据库会话
    
    Returns:
        ProductListResponse: 商品列表
    """
    from models import Product
    
    logger.info(f"获取商品列表请求: 分类={category}, is_active={is_active}, page={page}, page_size={page_size}, sort_by={sort_by}")
    
    query = db.query(Product)
    
    if category:
        query = query.filter(Product.category == category)
    
    if is_active is not None:
        query = query.filter(Product.is_active == is_active)
    
    if sort_by == "price_asc":
        query = query.order_by(Product.price.asc())
    elif sort_by == "price_desc":
        query = query.order_by(Product.price.desc())
    elif sort_by == "click_count":
        query = query.order_by(Product.click_count.desc())
    else:
        query = query.order_by(Product.created_at.desc())
    
    total = query.count()
    
    if limit:
        products = query.limit(limit).all()
    else:
        offset = (page - 1) * page_size
        products = query.offset(offset).limit(page_size).all()
    
    logger.info(f"获取商品列表成功: 总数={total}, 返回数={len(products)}")
    return ProductListResponse(products=products, total=total)


@router.get("/api/products/recommend", response_model=List[ProductResponse])
def get_recommend_products(
    category: str = Query(..., description="商品分类"),
    limit: int = Query(2, description="推荐数量，默认2"),
    db: Session = Depends(get_db)
):
    """
    根据分类随机推荐商品
    
    Args:
        category: 商品分类（必须）
        limit: 推荐数量（默认2）
        db: 数据库会话
    
    Returns:
        List[ProductResponse]: 随机推荐的商品列表
    """
    from models import Product
    import random
    
    logger.info(f"获取推荐商品请求: 分类={category}, 数量={limit}")
    
    products = db.query(Product).filter(
        Product.category == category,
        Product.is_active == True
    ).all()
    
    if not products:
        logger.warning(f"该分类下没有商品: 分类={category}")
        return []
    
    recommended = random.sample(products, min(limit, len(products)))
    
    logger.info(f"获取推荐商品成功: 分类={category}, 返回数={len(recommended)}")
    return recommended


@router.get("/api/products/recommend-by-content", response_model=List[ProductResponse])
def recommend_products_by_content(
    article_id: int = Query(..., description="文章ID"),
    limit: int = Query(2, description="推荐数量，默认2"),
    db: Session = Depends(get_db)
):
    """
    基于AI分析的文章内容推荐商品
    
    Args:
        article_id: 文章ID
        limit: 推荐数量（默认2）
        db: 数据库会话
    
    Returns:
        List[ProductResponse]: 推荐的商品列表
    """
    from models import Content
    from content_generator import DeepSeekGenerator
    from product_matcher import ProductMatcher
    
    logger.info(f"基于内容推荐商品请求: 文章ID={article_id}, 数量={limit}")
    
    article = db.query(Content).filter(Content.id == article_id).first()
    if not article:
        logger.warning(f"文章不存在: 文章ID={article_id}")
        return []
    
    try:
        generator = DeepSeekGenerator()
        analysis_result = generator.analyze_for_product_recommendation(
            article_title=article.title,
            article_content=article.content,
            article_category=article.category
        )
        
        if not analysis_result:
            logger.warning(f"AI分析失败，降级为基于分类推荐")
            products = db.query(Content.__table__.c if hasattr(Content.__table__.c, 'category') else None)
            if hasattr(Content.__table__.c, 'category'):
                from models import Product
                products = db.query(Product).filter(
                    Product.category == article.category,
                    Product.is_active == True
                ).limit(limit).all()
            else:
                from models import Product
                products = db.query(Product).filter(
                    Product.is_active == True
                ).limit(limit).all()
            return products
        
        logger.info(f"AI分析结果: {analysis_result}")
        
        matcher = ProductMatcher(db)
        products = matcher.match_products(analysis_result, limit)
        
        if not products:
            logger.warning(f"AI匹配无结果，降级为基于分类推荐")
            from models import Product
            products = db.query(Product).filter(
                Product.category == article.category,
                Product.is_active == True
            ).limit(limit).all()
        
        logger.info(f"基于内容推荐商品成功: 文章ID={article_id}, 返回数={len(products)}")
        return products
        
    except Exception as e:
        logger.error(f"基于内容推荐商品失败: {e}")
        from models import Product
        products = db.query(Product).filter(
            Product.category == article.category,
            Product.is_active == True
        ).limit(limit).all()
        return products


@router.get("/api/products/recommend-by-history", response_model=List[ProductResponse])
def recommend_products_by_history(
    limit: int = Query(4, description="推荐数量，默认4"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_optional)
):
    """
    基于用户浏览历史推荐商品
    
    Args:
        limit: 推荐数量（默认4）
        db: 数据库会话
        current_user: 当前用户（可选）
    
    Returns:
        List[ProductResponse]: 推荐的商品列表
    """
    from models import ViewHistory, Content
    from content_generator import DeepSeekGenerator
    from product_matcher import ProductMatcher
    
    logger.info(f"基于浏览历史推荐商品请求: 用户ID={current_user.id if current_user else None}, 数量={limit}")
    
    # 未登录用户，返回随机推荐
    if not current_user:
        logger.info("用户未登录，返回随机推荐")
        from models import Product
        products = db.query(Product).filter(
            Product.is_active == True
        ).order_by(func.random()).limit(limit).all()
        return products
    
    # 获取用户最近浏览的文章
    recent_articles = db.query(ViewHistory).filter(
        ViewHistory.user_id == current_user.id
    ).order_by(ViewHistory.viewed_at.desc()).limit(5).all()
    
    if not recent_articles:
        logger.info(f"用户无浏览历史，返回热门推荐: 用户ID={current_user.id}")
        from models import Product
        products = db.query(Product).filter(
            Product.is_active == True
        ).order_by(Product.click_count.desc()).limit(limit).all()
        return products
    
    # 获取最近浏览的文章内容
    article_ids = [h.article_id for h in recent_articles]
    articles = db.query(Content).filter(
        Content.id.in_(article_ids)
    ).all()
    
    if not articles:
        logger.warning(f"浏览历史中的文章不存在: 用户ID={current_user.id}")
        from models import Product
        products = db.query(Product).filter(
            Product.is_active == True
        ).order_by(Product.click_count.desc()).limit(limit).all()
        return products
    
    # 使用最近浏览的文章进行AI分析
    try:
        generator = DeepSeekGenerator()
        
        # 合并最近浏览的文章内容进行分析
        combined_title = articles[0].title
        combined_content = "\n\n".join([f"文章{i+1}: {a.title}\n{a.summary}" for i, a in enumerate(articles)])
        combined_category = articles[0].category
        
        analysis_result = generator.analyze_for_product_recommendation(
            article_title=combined_title,
            article_content=combined_content,
            article_category=combined_category
        )
        
        if not analysis_result:
            logger.warning(f"AI分析失败，降级为热门推荐: 用户ID={current_user.id}")
            from models import Product
            products = db.query(Product).filter(
                Product.is_active == True
            ).order_by(Product.click_count.desc()).limit(limit).all()
            return products
        
        logger.info(f"AI分析结果（基于浏览历史）: {analysis_result}")
        
        matcher = ProductMatcher(db)
        products = matcher.match_products(analysis_result, limit)
        
        if not products:
            logger.warning(f"AI匹配无结果，降级为热门推荐: 用户ID={current_user.id}")
            from models import Product
            products = db.query(Product).filter(
                Product.is_active == True
            ).order_by(Product.click_count.desc()).limit(limit).all()
        
        logger.info(f"基于浏览历史推荐商品成功: 用户ID={current_user.id}, 返回数={len(products)}")
        return products
        
    except Exception as e:
        logger.error(f"基于浏览历史推荐商品失败: {e}")
        from models import Product
        products = db.query(Product).filter(
            Product.is_active == True
        ).order_by(Product.click_count.desc()).limit(limit).all()
        return products


@router.get("/api/products/recommend-by-popular", response_model=List[ProductResponse])
def recommend_products_by_popular(
    limit: int = Query(4, description="推荐数量，默认4"),
    db: Session = Depends(get_db)
):
    """
    基于热门文章内容推荐商品
    
    Args:
        limit: 推荐数量（默认4）
        db: 数据库会话
    
    Returns:
        List[ProductResponse]: 推荐的商品列表
    """
    from models import Content
    from content_generator import DeepSeekGenerator
    from product_matcher import ProductMatcher
    
    logger.info(f"基于热门文章推荐商品请求: 数量={limit}")
    
    # 获取热门文章（按浏览量排序）
    popular_articles = db.query(Content).filter(
        Content.is_published == True
    ).order_by(Content.view_count.desc()).limit(5).all()
    
    if not popular_articles:
        logger.warning("没有找到热门文章，返回热门商品")
        from models import Product
        products = db.query(Product).filter(
            Product.is_active == True
        ).order_by(Product.click_count.desc()).limit(limit).all()
        return products
    
    # 使用热门文章进行AI分析
    try:
        generator = DeepSeekGenerator()
        
        # 合并热门文章内容进行分析
        combined_title = popular_articles[0].title
        combined_content = "\n\n".join([f"文章{i+1}: {a.title}\n{a.summary}" for i, a in enumerate(popular_articles)])
        combined_category = popular_articles[0].category
        
        analysis_result = generator.analyze_for_product_recommendation(
            article_title=combined_title,
            article_content=combined_content,
            article_category=combined_category
        )
        
        if not analysis_result:
            logger.warning("AI分析失败，降级为热门商品")
            from models import Product
            products = db.query(Product).filter(
                Product.is_active == True
            ).order_by(Product.click_count.desc()).limit(limit).all()
            return products
        
        logger.info(f"AI分析结果（基于热门文章）: {analysis_result}")
        
        matcher = ProductMatcher(db)
        products = matcher.match_products(analysis_result, limit)
        
        if not products:
            logger.warning("AI匹配无结果，降级为热门商品")
            from models import Product
            products = db.query(Product).filter(
                Product.is_active == True
            ).order_by(Product.click_count.desc()).limit(limit).all()
        
        logger.info(f"基于热门文章推荐商品成功: 返回数={len(products)}")
        return products
        
    except Exception as e:
        logger.error(f"基于热门文章推荐商品失败: {e}")
        from models import Product
        products = db.query(Product).filter(
            Product.is_active == True
        ).order_by(Product.click_count.desc()).limit(limit).all()
        return products


@router.get("/api/products/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    """
    获取商品详情
    
    Args:
        product_id: 商品ID
        db: 数据库会话
    
    Returns:
        ProductResponse: 商品详情
    """
    from models import Product
    
    logger.info(f"获取商品详情请求: 商品ID={product_id}")
    
    product = db.query(Product).filter(Product.id == product_id).first()
    
    if not product:
        logger.warning(f"商品不存在: 商品ID={product_id}")
        raise ResourceNotFoundError(message="商品不存在", details={"product_id": product_id})
    
    logger.info(f"获取商品详情成功: 商品ID={product_id}")
    return product


@router.put("/api/products/{product_id}", response_model=ProductResponse, dependencies=[Depends(get_current_admin_user)])
def update_product(
    product_id: int,
    product_update: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """
    更新商品（管理员权限）
    
    Args:
        product_id: 商品ID
        product_update: 商品更新请求数据
        db: 数据库会话
        current_user: 当前认证的管理员用户
    
    Returns:
        ProductResponse: 更新后的商品信息
    """
    from models import Product
    
    logger.info(f"更新商品请求: 商品ID={product_id}")
    
    product = db.query(Product).filter(Product.id == product_id).first()
    
    if not product:
        logger.warning(f"商品不存在: 商品ID={product_id}")
        raise ResourceNotFoundError(message="商品不存在", details={"product_id": product_id})
    
    update_data = product_update.dict(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(product, key, value)
    
    db.commit()
    db.refresh(product)
    
    logger.info(f"更新商品成功: 商品ID={product_id}")
    return product


@router.delete("/api/products/{product_id}", response_model=MessageResponse, dependencies=[Depends(get_current_admin_user)])
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """
    删除商品（管理员权限）
    
    Args:
        product_id: 商品ID
        db: 数据库会话
        current_user: 当前认证的管理员用户
    
    Returns:
        MessageResponse: 删除成功消息
    """
    from models import Product
    
    logger.info(f"删除商品请求: 商品ID={product_id}")
    
    product = db.query(Product).filter(Product.id == product_id).first()
    
    if not product:
        logger.warning(f"商品不存在: 商品ID={product_id}")
        raise ResourceNotFoundError(message="商品不存在", details={"product_id": product_id})
    
    db.delete(product)
    db.commit()
    
    logger.info(f"删除商品成功: 商品ID={product_id}")
    return MessageResponse(message="商品删除成功")


@router.post("/api/products/{product_id}/click", response_model=MessageResponse)
def record_product_click(
    product_id: int,
    db: Session = Depends(get_db)
):
    """
    记录商品点击次数
    
    Args:
        product_id: 商品ID
        db: 数据库会话
    
    Returns:
        MessageResponse: 记录成功消息
    """
    from models import Product
    
    logger.info(f"记录商品点击: 商品ID={product_id}")
    
    product = db.query(Product).filter(Product.id == product_id).first()
    
    if not product:
        logger.warning(f"商品不存在: 商品ID={product_id}")
        raise ResourceNotFoundError(message="商品不存在", details={"product_id": product_id})
    
    product.click_count += 1
    db.commit()
    
    logger.info(f"记录商品点击成功: 商品ID={product_id}, 点击次数={product.click_count}")
    return MessageResponse(message="点击记录成功")
