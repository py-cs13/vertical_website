from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict
import os
from typing import Optional


class Settings(BaseSettings):
    """
    应用配置类，使用pydantic_settings的BaseSettings来管理所有配置
    支持从环境变量或.env文件加载配置
    """
    # 基本配置
    APP_NAME: str = "垂直领域内容变现平台API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False  # 生产环境默认关闭DEBUG
    TESTING: bool = False  # 测试环境标识，默认关闭
    
    # 安全配置
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # 数据库配置
    DATABASE_URL: str = "postgresql://vertical_user:pg123456@101.43.177.216:5432/vertical_website"  # 生产数据库
    TEST_DATABASE_URL: str = "sqlite:///./test.db"  # 测试数据库（SQLite）
    
    # Redis配置
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # CSRF配置
    CSRF_SECRET_KEY: str = SECRET_KEY  # 默认使用SECRET_KEY
    CSRF_COOKIE_SAMESITE: str = "lax"
    CSRF_COOKIE_SECURE: bool = not DEBUG
    
    # CORS配置
    CORS_ALLOW_ORIGINS: list = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: list = ["*"]
    CORS_ALLOW_HEADERS: list = ["*"]
    
    # 邮件配置（预留）
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: Optional[int] = None
    SMTP_USERNAME: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    FROM_EMAIL: Optional[str] = None
    
    # DeepSeek API配置（百度千帆）
    DEEPSEEK_API_KEY: Optional[str] = None
    DEEPSEEK_API_BASE_URL: str = "https://qianfan.baidubce.com/v2/chat/completions"
    
    # 支付宝支付配置
    ALIPAY_APP_ID: Optional[str] = None
    ALIPAY_APP_PRIVATE_KEY: Optional[str] = None
    ALIPAY_PUBLIC_KEY: Optional[str] = None
    ALIPAY_GATEWAY: str = "https://openapi.alipay.com/gateway.do"  # 生产环境
    # ALIPAY_GATEWAY: str = "https://openapi.alipaydev.com/gateway.do"  # 沙箱环境
    ALIPAY_DEBUG: bool = False  # 是否为调试模式
    ALIPAY_NOTIFY_URL: Optional[str] = None  # 回调URL
    ALIPAY_RETURN_URL: Optional[str] = None  # 返回URL
    
    # 支付测试模式配置
    PAYMENT_TEST_MODE: bool = True  # 是否启用支付测试模式，生产环境关闭测试模式
    
    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file_encoding="utf-8"
    )
    
    def __init__(self, **kwargs):
        """
        自定义初始化方法，根据APP_ENV加载对应的.env文件
        """
        import logging
        logger = logging.getLogger(__name__)
        
        # 获取当前环境
        app_env = os.getenv("APP_ENV", "development")
        logger.info(f"Initializing configuration for APP_ENV: {app_env}")
        
        # 构建环境文件路径
        env_files = []
        if app_env != "development":
            env_file_path = f".env.{app_env}"
            if os.path.exists(env_file_path):
                env_files.append(env_file_path)
                logger.info(f"Will load environment file: {env_file_path}")
        
        # 添加默认.env文件
        if os.path.exists(".env"):
            env_files.append(".env")
            logger.info("Will load default environment file: .env")
        
        # 设置环境文件
        if env_files:
            # 注意：列表中后添加的文件优先级更高
            self.__class__.model_config["env_file"] = env_files
            logger.info(f"Environment files to load: {env_files}")
        else:
            logger.warning("No .env files found, using default values or environment variables")
        
        super().__init__(**kwargs)


# 创建全局配置实例
settings = Settings()
