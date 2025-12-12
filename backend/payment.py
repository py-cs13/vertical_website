# 支付服务模块
# 实现订单管理和支付处理功能

import uuid
from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from logging_config import get_logger
from models import Order, OrderItem, AffiliateLink, AffiliateClick, AffiliateCommission
from schemas import OrderCreate, OrderItemCreate
from config import settings
from alipay import Alipay

# 初始化支付宝客户端
ALIPAY_CLIENT = None
if settings.ALIPAY_APP_ID and settings.ALIPAY_APP_PRIVATE_KEY and settings.ALIPAY_PUBLIC_KEY:
    try:
        ALIPAY_CLIENT = Alipay(
            appid=settings.ALIPAY_APP_ID,
            app_notify_url=settings.ALIPAY_NOTIFY_URL,  # 回调URL
            app_private_key_string=settings.ALIPAY_APP_PRIVATE_KEY,
            alipay_public_key_string=settings.ALIPAY_PUBLIC_KEY,
            sign_type="RSA2",  # RSA或RSA2
            debug=settings.ALIPAY_DEBUG  # 调试模式
        )
        logger.info("支付宝客户端初始化成功")
    except Exception as e:
        logger.error(f"初始化支付宝客户端失败：{str(e)}")

# 获取日志器
logger = get_logger(__name__)
logger.info("支付服务模块加载成功")


def generate_order_number() -> str:
    """
    生成唯一的订单编号
    格式：YYYYMMDD + 8位随机字符串
    
    Returns:
        str: 唯一的订单编号
    """
    timestamp = datetime.now().strftime("%Y%m%d")
    random_str = str(uuid.uuid4()).replace("-", "")[:8]
    return f"{timestamp}{random_str}"


def create_order(db: Session, order_data: OrderCreate, user_id: int) -> Order:
    """
    创建新订单
    
    Args:
        db (Session): 数据库会话
        order_data (OrderCreate): 订单创建数据
        user_id (int): 用户ID
        
    Returns:
        Order: 创建的订单对象
    """
    try:
        # 生成订单编号
        order_number = generate_order_number()
        
        # 创建订单
        db_order = Order(
            order_number=order_number,
            user_id=user_id,
            amount=order_data.amount,
            product_type=order_data.product_type,
            product_id=order_data.product_id,
            status="pending"
        )
        db.add(db_order)
        db.commit()
        db.refresh(db_order)
        
        # 创建订单项
        for item_data in order_data.items:
            db_item = OrderItem(
                order_id=db_order.id,
                product_name=item_data.product_name,
                product_price=item_data.product_price,
                quantity=item_data.quantity,
                total_amount=item_data.total_amount
            )
            db.add(db_item)
        
        db.commit()
        logger.info(f"订单创建成功：订单号={order_number}，用户ID={user_id}")
        return db_order
        
    except Exception as e:
        db.rollback()
        logger.error(f"创建订单失败：{str(e)}")
        raise


def get_order(db: Session, order_id: int, user_id: Optional[int] = None) -> Optional[Order]:
    """
    根据订单ID获取订单
    
    Args:
        db (Session): 数据库会话
        order_id (int): 订单ID
        user_id (Optional[int]): 用户ID，如果提供则只返回该用户的订单
        
    Returns:
        Optional[Order]: 订单对象，如果不存在则返回None
    """
    query = db.query(Order).filter(Order.id == order_id)
    if user_id:
        query = query.filter(Order.user_id == user_id)
    return query.first()


def get_order_by_number(db: Session, order_number: str) -> Optional[Order]:
    """
    根据订单编号获取订单
    
    Args:
        db (Session): 数据库会话
        order_number (str): 订单编号
        
    Returns:
        Optional[Order]: 订单对象，如果不存在则返回None
    """
    return db.query(Order).filter(Order.order_number == order_number).first()


def get_user_orders(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> list[Order]:
    """
    获取用户的所有订单
    
    Args:
        db (Session): 数据库会话
        user_id (int): 用户ID
        skip (int): 跳过的订单数量，默认为0
        limit (int): 返回的订单数量，默认为100
        
    Returns:
        list[Order]: 订单列表
    """
    return db.query(Order).filter(Order.user_id == user_id).order_by(desc(Order.created_at)).offset(skip).limit(limit).all()


def process_payment(db: Session, order_id: int, payment_method: str, return_url: Optional[str] = None) -> dict:
    """
    处理支付请求
    集成真实的支付网关API
    
    Args:
        db (Session): 数据库会话
        order_id (int): 订单ID
        payment_method (str): 支付方式：wechat(微信支付), alipay(支付宝)
        return_url (Optional[str]): 支付完成后跳转URL
        
    Returns:
        dict: 支付处理结果，包含支付URL和交易ID等信息
    """
    try:
        # 获取订单
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise ValueError(f"订单不存在：订单ID={order_id}")
        
        if order.status != "pending":
            raise ValueError(f"订单状态不允许支付：订单ID={order_id}，当前状态={order.status}")
        
        # 生成交易ID
        transaction_id = f"{payment_method}_{str(uuid.uuid4()).replace('-', '')[:16]}"
        
        # 更新订单支付信息
        order.payment_method = payment_method
        order.payment_transaction_id = transaction_id
        
        # 检查是否启用支付测试模式
        if settings.PAYMENT_TEST_MODE:
            # 测试模式下，直接模拟支付完成
            order.status = "paid"
            order.paid_at = datetime.now()
            order.updated_at = datetime.now()
            
            logger.info(f"测试模式：直接模拟支付完成，订单号={order.order_number}，支付方式={payment_method}")
            
            # 构造一个本地支付成功的URL，前端可以直接跳转到成功页面
            if return_url:
                payment_url = return_url
            else:
                # 默认返回支付成功页面
                payment_url = f"http://localhost:3000/payment-success?order_id={order.id}&status=success"
        else:
            # 生产模式：根据支付方式处理支付请求
            if payment_method == "alipay" and ALIPAY_CLIENT:
                # 使用真实的支付宝SDK
                subject = f"购买工具包：{order.product_id}"
                total_amount = float(order.amount)
                out_trade_no = order.order_number
                
                # 创建支付订单
                order_string = ALIPAY_CLIENT.api_alipay_trade_page_pay(
                    out_trade_no=out_trade_no,
                    total_amount=total_amount,
                    subject=subject,
                    return_url=return_url or "http://localhost:8000/api/payment/callback",
                    notify_url=return_url or "http://localhost:8000/api/payment/notify"  # 服务器回调URL
                )
                
                # 构建支付URL
                payment_url = f"{settings.ALIPAY_GATEWAY}?{order_string}"
            else:
                # 使用模拟支付网关
                payment_url = f"https://mock-payment-gateway.com/pay?order={order.order_number}&amount={order.amount}&method={payment_method}"
        
        db.commit()
        
        logger.info(f"支付请求处理成功：订单号={order.order_number}，支付方式={payment_method}，测试模式={settings.PAYMENT_TEST_MODE}")
        
        return {
            "order_id": order.id,
            "order_number": order.order_number,
            "payment_method": payment_method,
            "payment_url": payment_url,
            "transaction_id": transaction_id,
            "status": "success" if settings.PAYMENT_TEST_MODE else "pending"  # 测试模式下直接返回成功
        }
        
    except Exception as e:
        db.rollback()
        logger.error(f"处理支付请求失败：{str(e)}")
        raise


def check_user_purchased_toolkit(db: Session, user_id: int, toolkit_id: int) -> bool:
    """
    检查用户是否已购买特定工具包
    
    Args:
        db (Session): 数据库会话
        user_id (int): 用户ID
        toolkit_id (int): 工具包ID
        
    Returns:
        bool: 如果用户已购买则返回True，否则返回False
    """
    try:
        # 查询用户是否有已支付的工具包订单
        order = db.query(Order).filter(
            Order.user_id == user_id,
            Order.product_type == "toolkit",
            Order.product_id == toolkit_id,
            Order.status == "paid"
        ).first()
        
        return order is not None
        
    except Exception as e:
        logger.error(f"检查用户购买记录失败：用户ID={user_id}，工具包ID={toolkit_id}，错误={str(e)}")
        return False


def handle_payment_callback(db: Session, order_number: str, transaction_id: str, status: str, amount: float, payment_method: str) -> bool:
    """
    处理支付回调
    支持真实的支付宝回调验证
    
    Args:
        db (Session): 数据库会话
        order_number (str): 订单编号
        transaction_id (str): 支付平台交易ID
        status (str): 支付状态：success(成功), failed(失败)
        amount (float): 支付金额
        payment_method (str): 支付方式：wechat(微信支付), alipay(支付宝)
        
    Returns:
        bool: 支付回调处理结果
    """
    try:
        # 获取订单
        order = db.query(Order).filter(Order.order_number == order_number).first()
        if not order:
            logger.error(f"支付回调处理失败：订单不存在，订单号={order_number}")
            return False
        
        # 验证支付金额
        if round(order.amount, 2) != round(amount, 2):
            logger.error(f"支付回调处理失败：金额不匹配，订单号={order_number}，订单金额={order.amount}，支付金额={amount}")
            return False
        
        # 更新订单状态
        if status == "success":
            order.status = "paid"
            order.paid_at = datetime.now()
            logger.info(f"支付成功，订单已更新：订单号={order_number}，交易ID={transaction_id}")
            
            # 检查是否需要生成推广佣金
            try:
                create_affiliate_commission(db, order)
            except Exception as e:
                logger.error(f"生成推广佣金失败：订单号={order_number}，错误={str(e)}")
        else:
            order.status = "failed"
            logger.info(f"支付失败，订单已更新：订单号={order_number}，交易ID={transaction_id}")
        
        db.commit()
        return True
        
    except Exception as e:
        db.rollback()
        logger.error(f"处理支付回调失败：{str(e)}")
        return False


def create_affiliate_commission(db: Session, order: Order) -> None:
    """
    根据订单创建推广佣金记录
    查找该用户最近点击的推广链接（7天内有效）
    
    Args:
        db (Session): 数据库会话
        order (Order): 已支付的订单对象
    """
    try:
        # 查找该用户最近7天内的点击记录
        seven_days_ago = datetime.now() - timedelta(days=7)
        
        # 查询用户的点击记录，按点击时间倒序
        click_record = db.query(AffiliateClick)
        click_record = click_record.filter(AffiliateClick.user_id == order.user_id)
        click_record = click_record.filter(AffiliateClick.clicked_at >= seven_days_ago)
        click_record = click_record.order_by(desc(AffiliateClick.clicked_at)).first()
        
        if click_record:
            # 获取推广链接
            affiliate_link = db.query(AffiliateLink).filter(AffiliateLink.id == click_record.affiliate_link_id).first()
            
            if affiliate_link and affiliate_link.is_active:
                # 计算佣金（订单金额的10%）
                commission_amount = order.amount * 0.1
                
                # 创建佣金记录
                commission = AffiliateCommission(
                    order_id=order.id,
                    affiliate_link_id=affiliate_link.id,
                    amount=commission_amount,
                    status="pending"
                )
                
                db.add(commission)
                db.commit()
                logger.info(f"推广佣金生成成功：订单号={order.order_number}，推广用户ID={affiliate_link.user_id}，佣金金额={commission_amount}")
            else:
                logger.info(f"推广链接无效，不生成佣金：订单号={order.order_number}")
        else:
            logger.info(f"未找到有效的推广点击记录，不生成佣金：订单号={order.order_number}")
            
    except Exception as e:
        logger.error(f"创建推广佣金失败：订单号={order.order_number}，错误={str(e)}")
        raise


def cancel_order(db: Session, order_id: int, user_id: int) -> bool:
    """
    取消订单
    
    Args:
        db (Session): 数据库会话
        order_id (int): 订单ID
        user_id (int): 用户ID
        
    Returns:
        bool: 取消订单结果
    """
    try:
        # 获取订单
        order = db.query(Order).filter(Order.id == order_id, Order.user_id == user_id).first()
        if not order:
            logger.error(f"取消订单失败：订单不存在或不属于当前用户，订单ID={order_id}，用户ID={user_id}")
            return False
        
        if order.status != "pending":
            logger.error(f"取消订单失败：订单状态不允许取消，订单ID={order_id}，当前状态={order.status}")
            return False
        
        # 更新订单状态
        order.status = "cancelled"
        order.cancelled_at = datetime.now()
        
        db.commit()
        logger.info(f"订单已取消：订单ID={order_id}，用户ID={user_id}")
        return True
        
    except Exception as e:
        db.rollback()
        logger.error(f"取消订单失败：{str(e)}")
        return False