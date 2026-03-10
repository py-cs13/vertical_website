# 数据库模型定义文件
# 包含用户认证和内容管理所需的数据模型

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Date, func, ForeignKey, DECIMAL, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base  # 从database模块导入Base，确保使用同一个实例


class User(Base):
    """
    用户模型
    用于存储用户认证信息和基本资料
    """
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True, comment="用户ID")
    username = Column(String(50), unique=True, index=True, nullable=False, comment="用户名")
    email = Column(String(100), unique=True, index=True, nullable=False, comment="邮箱")
    hashed_password = Column(String(255), nullable=False, comment="哈希后的密码")
    is_active = Column(Boolean, default=True, comment="用户是否激活")
    is_admin = Column(Boolean, default=False, comment="是否为管理员")
    avatar = Column(String(255), nullable=True, comment="用户头像URL")
    gender = Column(String(10), nullable=True, comment="性别")
    birthday = Column(Date, nullable=True, comment="生日")
    bio = Column(Text, nullable=True, comment="个人简介")
    # 母婴特色字段
    baby_name = Column(String(50), nullable=True, comment="宝宝姓名")
    baby_birthday = Column(Date, nullable=True, comment="宝宝生日")
    baby_gender = Column(String(10), nullable=True, comment="宝宝性别")
    baby_milestones = Column(Text, nullable=True, comment="宝宝成长里程碑")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")


class Content(Base):
    """
    内容模型
    用于存储文章等内容信息
    """
    __tablename__ = "contents"
    
    id = Column(Integer, primary_key=True, index=True, comment="内容ID")
    title = Column(String(200), nullable=False, comment="标题")
    category = Column(String(50), index=True, nullable=False, comment="分类")
    summary = Column(Text, nullable=False, comment="摘要")
    content = Column(Text, nullable=False, comment="内容详情")
    author_id = Column(Integer, ForeignKey("users.id"), index=True, comment="作者ID")
    is_published = Column(Boolean, default=False, index=True, comment="是否发布")
    view_count = Column(Integer, default=0, comment="浏览量")
    likes = Column(Integer, default=0, comment="点赞数")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True, comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")
    published_at = Column(DateTime(timezone=True), nullable=True, index=True, comment="发布时间")
    price = Column(DECIMAL(10, 2), nullable=True, default=9.9, comment="价格")


class PasswordResetToken(Base):
    """
    密码重置令牌模型
    用于处理用户密码重置功能
    """
    __tablename__ = "password_reset_tokens"
    
    id = Column(Integer, primary_key=True, index=True, comment="令牌ID")
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False, comment="用户ID")
    token = Column(String(255), unique=True, nullable=False, comment="重置令牌")
    expires_at = Column(DateTime(timezone=True), index=True, nullable=False, comment="过期时间")
    is_used = Column(Boolean, default=False, index=True, comment="是否已使用")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")


class Order(Base):
    """
    订单模型
    用于记录用户的购买订单信息
    """
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True, comment="订单ID")
    order_number = Column(String(100), unique=True, index=True, nullable=False, comment="订单编号")
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False, comment="用户ID")
    amount = Column(DECIMAL(10, 2), nullable=False, comment="订单金额")
    status = Column(String(20), index=True, nullable=False, default="pending", comment="订单状态：pending(待支付), paid(已支付), cancelled(已取消), refunded(已退款)")
    payment_method = Column(String(20), nullable=True, comment="支付方式：wechat(微信支付), alipay(支付宝)")
    payment_transaction_id = Column(String(100), nullable=True, comment="支付平台交易ID")
    product_type = Column(String(50), nullable=False, comment="产品类型：toolkit(工具包), membership(会员)")
    product_id = Column(Integer, nullable=False, comment="产品ID")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True, comment="创建时间")
    paid_at = Column(DateTime(timezone=True), nullable=True, comment="支付时间")
    cancelled_at = Column(DateTime(timezone=True), nullable=True, comment="取消时间")
    
    # 与OrderItem的关系
    items = relationship("OrderItem", backref="order", lazy="selectin")


class OrderItem(Base):
    """
    订单项模型
    用于记录订单中的具体产品信息
    """
    __tablename__ = "order_items"
    
    id = Column(Integer, primary_key=True, index=True, comment="订单项ID")
    order_id = Column(Integer, ForeignKey("orders.id"), index=True, nullable=False, comment="订单ID")
    product_name = Column(String(255), nullable=False, comment="产品名称")
    product_price = Column(DECIMAL(10, 2), nullable=False, comment="产品单价")
    quantity = Column(Integer, nullable=False, default=1, comment="产品数量")
    total_amount = Column(DECIMAL(10, 2), nullable=False, comment="项总价")


class AffiliateLink(Base):
    """
    推广链接模型
    用于存储用户的推广链接信息
    """
    __tablename__ = "affiliate_links"
    
    id = Column(Integer, primary_key=True, index=True, comment="推广链接ID")
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False, comment="用户ID")
    unique_code = Column(String(100), unique=True, index=True, nullable=False, comment="唯一推广码")
    is_active = Column(Boolean, default=True, comment="推广链接是否激活")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")


class AffiliateClick(Base):
    """
    推广点击模型
    用于记录推广链接的点击情况
    """
    __tablename__ = "affiliate_clicks"
    
    id = Column(Integer, primary_key=True, index=True, comment="点击记录ID")
    affiliate_link_id = Column(Integer, ForeignKey("affiliate_links.id"), index=True, nullable=False, comment="推广链接ID")
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=True, comment="用户ID")
    ip_address = Column(String(50), nullable=True, comment="点击者IP地址")
    user_agent = Column(String(500), nullable=True, comment="点击者用户代理")
    referrer = Column(String(500), nullable=True, comment="来源页面")
    clicked_at = Column(DateTime(timezone=True), server_default=func.now(), index=True, comment="点击时间")


class AffiliateCommission(Base):
    """
    推广佣金模型
    用于记录用户通过推广获得的佣金
    """
    __tablename__ = "affiliate_commissions"
    
    id = Column(Integer, primary_key=True, index=True, comment="佣金记录ID")
    order_id = Column(Integer, ForeignKey("orders.id"), index=True, nullable=False, comment="订单ID")
    affiliate_link_id = Column(Integer, ForeignKey("affiliate_links.id"), index=True, nullable=False, comment="推广链接ID")
    amount = Column(DECIMAL(10, 2), nullable=False, comment="佣金金额")
    status = Column(String(20), index=True, nullable=False, default="pending", comment="佣金状态：pending(待结算), paid(已结算), cancelled(已取消)")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    paid_at = Column(DateTime(timezone=True), nullable=True, comment="结算时间")
    cancelled_at = Column(DateTime(timezone=True), nullable=True, comment="取消时间")


class Favorite(Base):
    """
    收藏模型
    用于记录用户收藏的文章
    """
    __tablename__ = "favorites"
    
    id = Column(Integer, primary_key=True, index=True, comment="收藏记录ID")
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False, comment="用户ID")
    content_id = Column(Integer, ForeignKey("contents.id"), index=True, nullable=False, comment="内容ID")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True, comment="收藏时间")
    
    # 联合唯一索引，防止重复收藏
    __table_args__ = (
        UniqueConstraint("user_id", "content_id", name="uq_user_content_favorite"),
        {"comment": "用户收藏表，记录用户收藏的文章"},
    )


class Like(Base):
    """
    点赞模型
    用于记录用户点赞的文章，实现用户独立的点赞状态
    """
    __tablename__ = "likes"
    
    id = Column(Integer, primary_key=True, index=True, comment="点赞记录ID")
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False, comment="用户ID")
    content_id = Column(Integer, ForeignKey("contents.id"), index=True, nullable=False, comment="内容ID")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True, comment="点赞时间")
    
    # 联合唯一索引，防止重复点赞
    __table_args__ = (
        UniqueConstraint("user_id", "content_id", name="uq_user_content_like"),
        {"comment": "用户点赞表，记录用户点赞的文章，实现用户独立的点赞状态"},
    )


class Product(Base):
    """
    商品模型
    用于存储淘宝联盟商品信息
    """
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True, comment="商品ID")
    name = Column(String(200), nullable=False, comment="商品名称")
    description = Column(Text, nullable=True, comment="商品描述")
    image_url = Column(String(500), nullable=False, comment="商品图片URL")
    link_url = Column(String(500), nullable=False, comment="淘宝联盟链接")
    price = Column(DECIMAL(10, 2), nullable=False, comment="商品价格")
    category = Column(String(50), index=True, nullable=False, comment="商品分类（对应8大分类）")
    is_active = Column(Boolean, default=True, index=True, comment="是否上架")
    click_count = Column(Integer, default=0, comment="点击次数")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    __table_args__ = (
        {"comment": "商品表，存储淘宝联盟商品信息，用于文章详情页广告推荐"},
    )


class ViewHistory(Base):
    """
    浏览历史模型
    用于记录用户的文章浏览历史，用于个性化推荐
    """
    __tablename__ = "view_history"
    
    id = Column(Integer, primary_key=True, index=True, comment="浏览记录ID")
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=True, comment="用户ID（未登录用户为NULL）")
    article_id = Column(Integer, ForeignKey("contents.id"), index=True, nullable=False, comment="文章ID")
    session_id = Column(String(100), index=True, nullable=True, comment="会话ID（用于未登录用户）")
    viewed_at = Column(DateTime(timezone=True), server_default=func.now(), index=True, comment="浏览时间")
    
    __table_args__ = (
        UniqueConstraint('user_id', 'article_id', name='unique_user_article_view'),
        {"comment": "浏览历史表，记录用户浏览的文章，用于个性化商品推荐"},
    )
