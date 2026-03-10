# 依赖函数文件
# 处理API端点的依赖，特别是用户认证相关

from fastapi import Depends, status, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Optional
from datetime import timedelta

from database import get_db
from models import User
from auth import decode_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from schemas import TokenData
from errors import AuthenticationError

# OAuth2密码Bearer模式
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """
    获取当前认证用户
    
    Args:
        token: OAuth2访问令牌
        db: 数据库会话
    
    Returns:
        User: 当前认证的用户对象
    
    Raises:
        AuthenticationError: 如果令牌无效或用户不存在
    """
    payload = decode_access_token(token)
    if payload is None:
        raise AuthenticationError(message="无法验证凭据", details="无效的访问令牌")
    
    user_id: Optional[int] = payload.get("sub")
    if user_id is None:
        raise AuthenticationError(message="无法验证凭据", details="令牌缺少用户信息")
    
    token_data = TokenData(user_id=user_id)
    user = db.query(User).filter(User.id == token_data.user_id).first()
    
    if user is None:
        raise AuthenticationError(message="无法验证凭据", details="用户不存在")
    
    if not user.is_active:
        raise AuthenticationError(message="用户已被禁用")
    
    return user


def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """
    获取当前活跃用户
    
    Args:
        current_user: 当前认证的用户对象
    
    Returns:
        User: 当前活跃用户对象
    
    Raises:
        AuthenticationError: 如果用户不活跃
    """
    if not current_user.is_active:
        raise AuthenticationError(message="用户已被禁用")
    
    return current_user


def get_current_admin_user(current_user: User = Depends(get_current_active_user)) -> User:
    """
    获取当前管理员用户
    
    Args:
        current_user: 当前活跃的用户对象
    
    Returns:
        User: 当前管理员用户对象
    
    Raises:
        AuthorizationError: 如果用户不是管理员
    """
    from errors import AuthorizationError
    if not current_user.is_admin:
        raise AuthorizationError(message="无权访问", details="需要管理员权限才能访问此资源")
    
    return current_user


def get_current_user_optional(request: Request, db: Session = Depends(get_db)) -> Optional[User]:
    """
    获取可选的当前用户（未登录时返回None）
    
    Args:
        request: FastAPI请求对象
        db: 数据库会话
    
    Returns:
        Optional[User]: 当前认证的用户对象，未登录时返回None
    """
    try:
        from fastapi.security.utils import get_authorization_scheme_param
        
        auth_header = request.headers.get("authorization")
        if not auth_header:
            return None
        
        scheme, token = get_authorization_scheme_param(auth_header)
        if scheme.lower() != "bearer":
            return None
        
        payload = decode_access_token(token)
        if payload is None:
            return None
        
        user_id: Optional[int] = payload.get("sub")
        if user_id is None:
            return None
        
        token_data = TokenData(user_id=user_id)
        user = db.query(User).filter(User.id == token_data.user_id).first()
        
        if user is None or not user.is_active:
            return None
        
        return user
    except:
        return None
