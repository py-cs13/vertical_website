# 数据验证模型文件
# 定义API请求和响应的数据结构

from pydantic import BaseModel, EmailStr, Field, validator, constr
from datetime import datetime, date
from typing import Optional, List
import re


# 用户相关模型

class UserBase(BaseModel):
    """用户基础模型，包含公共字段"""
    username: str = Field(..., min_length=3, max_length=50, description="用户名")
    email: EmailStr = Field(..., description="邮箱地址")
    
    @validator('username')
    def username_alphanumeric(cls, v):
        """验证用户名只能包含字母、数字和下划线"""
        if not re.match(r'^[a-zA-Z0-9_]+$', v):
            raise ValueError('用户名只能包含字母、数字和下划线')
        return v


class UserCreate(UserBase):
    """用户创建请求模型"""
    password: str = Field(..., min_length=8, max_length=128, description="密码，至少8位，包含大小写字母、数字和特殊字符")
    referral_code: Optional[str] = Field(None, description="推广码")
    
    @validator('password')
    def password_complexity(cls, v):
        """验证密码复杂度：至少8位，包含大小写字母、数字和特殊字符"""
        if len(v) < 8:
            raise ValueError('密码长度至少为8位')
        if not re.search(r'[A-Z]', v):
            raise ValueError('密码必须包含至少一个大写字母')
        if not re.search(r'[a-z]', v):
            raise ValueError('密码必须包含至少一个小写字母')
        if not re.search(r'[0-9]', v):
            raise ValueError('密码必须包含至少一个数字')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError('密码必须包含至少一个特殊字符')
        return v


class UserLogin(BaseModel):
    """用户登录请求模型"""
    email: EmailStr = Field(..., description="邮箱地址")
    password: str = Field(..., min_length=1, description="密码")


class UserUpdate(BaseModel):
    """用户信息更新请求模型"""
    username: Optional[str] = Field(None, min_length=3, max_length=50, description="用户名")
    email: Optional[EmailStr] = Field(None, description="邮箱地址")
    avatar: Optional[str] = Field(None)
    gender: Optional[str] = Field(None, max_length=10, description="性别")
    birthday: Optional[date] = Field(None, description="生日")
    bio: Optional[str] = Field(None, description="个人简介")
    # 母婴特色字段
    baby_name: Optional[str] = Field(None, max_length=50, description="宝宝姓名")
    baby_birthday: Optional[date] = Field(None, description="宝宝生日")
    baby_gender: Optional[str] = Field(None, max_length=10, description="宝宝性别")
    baby_milestones: Optional[str] = Field(None, description="宝宝成长里程碑")
    
    @validator('username')
    def username_alphanumeric(cls, v):
        """验证用户名只能包含字母、数字和下划线"""
        if v is not None and not re.match(r'^[a-zA-Z0-9_]+$', v):
            raise ValueError('用户名只能包含字母、数字和下划线')
        return v


class UserResponse(UserBase):
    """用户响应模型"""
    id: int
    is_active: bool
    is_admin: Optional[bool] = None
    avatar: Optional[str] = None
    gender: Optional[str] = None
    birthday: Optional[date] = None
    bio: Optional[str] = None
    # 母婴特色字段
    baby_name: Optional[str] = None
    baby_birthday: Optional[date] = None
    baby_gender: Optional[str] = None
    baby_milestones: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True  # 支持从ORM模型直接转换


# 内容相关模型

class ContentBase(BaseModel):
    """内容基础模型，包含公共字段"""
    title: str = Field(..., min_length=5, max_length=200, description="内容标题")
    category: str = Field(..., min_length=1, max_length=50, description="内容分类")
    summary: str = Field(..., min_length=10, max_length=500, description="内容摘要")
    content: str = Field(..., min_length=50, max_length=100000, description="内容详情，最多10万字")
    
    @validator('category')
    def category_alphanumeric(cls, v):
        """验证分类只能包含字母、数字、空格和中文"""
        if not re.match(r'^[a-zA-Z0-9\u4e00-\u9fa5\s]+$', v):
            raise ValueError('分类只能包含字母、数字、空格和中文')
        return v


class ContentCreate(ContentBase):
    """内容创建请求模型"""
    pass


class ContentUpdate(BaseModel):
    """内容更新请求模型"""
    title: Optional[str] = Field(None, min_length=5, max_length=200, description="内容标题")
    category: Optional[str] = Field(None, min_length=1, max_length=50, description="内容分类")
    summary: Optional[str] = Field(None, min_length=10, max_length=500, description="内容摘要")
    content: Optional[str] = Field(None, min_length=50, max_length=100000, description="内容详情，最多10万字")
    is_published: Optional[bool] = Field(None, description="是否发布")
    
    @validator('category')
    def category_alphanumeric(cls, v):
        """验证分类只能包含字母、数字、空格和中文"""
        if v is None:
            return v
        if not re.match(r'^[a-zA-Z0-9\u4e00-\u9fa5\s]+$', v):
            raise ValueError('分类只能包含字母、数字、空格和中文')
        return v


class ContentResponse(BaseModel):
    """内容响应模型"""
    id: int
    title: str = Field(..., min_length=5, max_length=200, description="内容标题")
    category: str = Field(..., min_length=1, max_length=50, description="内容分类")
    summary: str = Field(..., min_length=10, max_length=500, description="内容摘要")
    content: str = Field(..., min_length=1, max_length=100000, description="内容详情，最多10万字")
    author_id: int
    is_published: bool
    view_count: int
    created_at: datetime
    updated_at: datetime
    published_at: Optional[datetime]
    price: Optional[float] = Field(None, description="价格")
    
    class Config:
        from_attributes = True  # 支持从ORM模型直接转换


class ContentListResponse(BaseModel):
    """内容列表响应模型"""
    status: str
    data: List[ContentResponse]
    total: int


# 认证相关模型

class Token(BaseModel):
    """令牌响应模型"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """令牌数据模型"""
    user_id: Optional[int] = None


class PasswordResetRequest(BaseModel):
    """密码重置请求模型"""
    email: EmailStr = Field(..., description="邮箱地址")


class PasswordReset(BaseModel):
    """密码重置确认模型"""
    token: str = Field(..., min_length=10, description="重置令牌")
    new_password: str = Field(..., min_length=8, max_length=128, description="新密码，至少8位，包含大小写字母、数字和特殊字符")
    
    @validator('new_password')
    def password_complexity(cls, v):
        """验证密码复杂度：至少8位，包含大小写字母、数字和特殊字符"""
        if len(v) < 8:
            raise ValueError('密码长度至少为8位')
        if not re.search(r'[A-Z]', v):
            raise ValueError('密码必须包含至少一个大写字母')
        if not re.search(r'[a-z]', v):
            raise ValueError('密码必须包含至少一个小写字母')
        if not re.search(r'[0-9]', v):
            raise ValueError('密码必须包含至少一个数字')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError('密码必须包含至少一个特殊字符')
        return v


# 通用响应模型

class MessageResponse(BaseModel):
    """通用消息响应模型"""
    status: str
    message: str


# 支付相关模型

class OrderItemCreate(BaseModel):
    """订单项创建请求模型"""
    product_name: str = Field(..., min_length=1, max_length=255, description="产品名称")
    product_price: float = Field(..., gt=0, description="产品单价，必须大于0")
    quantity: int = Field(..., ge=1, description="产品数量，必须大于等于1")
    total_amount: float = Field(..., gt=0, description="项总价，必须大于0")


class OrderCreate(BaseModel):
    """订单创建请求模型"""
    product_type: str = Field(..., min_length=1, max_length=50, description="产品类型：toolkit(工具包), membership(会员)")
    product_id: int = Field(..., ge=1, description="产品ID，必须大于等于1")
    amount: float = Field(..., gt=0, description="订单金额，必须大于0")
    items: List[OrderItemCreate] = Field(..., min_items=1, description="订单项列表，至少包含一个订单项")


class OrderItemResponse(BaseModel):
    """订单项响应模型"""
    id: int
    order_id: int
    product_name: str
    product_price: float
    quantity: int
    total_amount: float
    
    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    """订单响应模型"""
    id: int
    order_number: str
    user_id: int
    amount: float
    status: str
    payment_method: Optional[str]
    payment_transaction_id: Optional[str]
    product_type: str
    product_id: int
    items: List[OrderItemResponse]
    created_at: datetime
    paid_at: Optional[datetime]
    cancelled_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class PaymentRequest(BaseModel):
    """支付请求模型"""
    order_id: int = Field(..., ge=1, description="订单ID，必须大于等于1")
    payment_method: str = Field(..., min_length=1, max_length=20, description="支付方式：wechat(微信支付), alipay(支付宝)")
    return_url: Optional[str] = Field(None, description="支付完成后跳转URL")


class PaymentResponse(BaseModel):
    """支付响应模型"""
    status: str
    order_id: int
    order_number: str
    payment_method: str
    payment_url: Optional[str] = Field(None, description="支付页面URL")
    transaction_id: Optional[str] = Field(None, description="支付平台交易ID")
    message: str


class PaymentCallback(BaseModel):
    """支付回调请求模型"""
    order_number: str = Field(..., min_length=1, max_length=100, description="订单编号")
    transaction_id: str = Field(..., min_length=1, max_length=100, description="支付平台交易ID")
    status: str = Field(..., min_length=1, max_length=20, description="支付状态：success(成功), failed(失败)")
    amount: float = Field(..., gt=0, description="支付金额，必须大于0")
    payment_method: str = Field(..., min_length=1, max_length=20, description="支付方式：wechat(微信支付), alipay(支付宝)")


class OrderListResponse(BaseModel):
    """订单列表响应模型"""
    status: str
    data: List[OrderResponse]
    total: int
