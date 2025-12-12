# 数据库连接配置文件
# 管理数据库会话和连接

import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from logging_config import get_logger

# 导入配置
from config import settings

# 获取日志器
logger = get_logger(__name__)

# 创建基础类
# 所有的数据库模型都将继承自这个类
Base = declarative_base()
logger.info("数据库模型基类创建成功")

# 数据库连接字符串
# 使用配置文件中的设置
DATABASE_URL = settings.DATABASE_URL
logger.info(f"数据库连接URL: {DATABASE_URL}")

# 创建SQLAlchemy引擎
# 引擎是与数据库通信的核心接口
# 使用PostgreSQL特定配置
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # 连接池预检查，确保连接有效
    pool_size=10,        # 连接池大小
    max_overflow=20      # 连接池最大溢出
)
logger.info("数据库引擎创建成功")

# 创建会话工厂
# 会话用于与数据库进行交互
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
logger.info("数据库会话工厂创建成功")

# 获取数据库会话的依赖函数
# 在FastAPI路径操作中使用，用于自动管理数据库会话

def get_db():
    """
    获取数据库会话的依赖函数
    用于FastAPI路径操作，自动管理数据库连接的创建和关闭
    
    Yields:
        Session: SQLAlchemy数据库会话对象
    """
    db = SessionLocal()
    logger.debug(f"创建数据库会话: {id(db)}")
    try:
        yield db  # 提供数据库会话给路径操作函数
    except Exception as e:
        logger.error(f"数据库会话错误: {str(e)}")
        raise
    finally:
        logger.debug(f"关闭数据库会话: {id(db)}")
        db.close()  # 确保会话总是会被关闭
