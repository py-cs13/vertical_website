# 日志配置文件
# 提供工业级的日志记录功能

import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime

# 默认日志级别
DEFAULT_LOG_LEVEL = logging.INFO

# 日志目录
LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")

# 确保日志目录存在
os.makedirs(LOG_DIR, exist_ok=True)

# 日志文件路径
LOG_FILE = os.path.join(LOG_DIR, f"app_{datetime.now().strftime('%Y-%m-%d')}.log")


def setup_logging(log_level: int = DEFAULT_LOG_LEVEL) -> None:
    """
    设置日志系统配置
    
    Args:
        log_level: 日志级别，默认为INFO
    """
    # 创建日志格式化器
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"
    )
    
    # 创建控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    
    # 创建文件处理器 (循环日志，最大10MB，保留10个备份)
    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=10,
        encoding="utf-8"
    )
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    
    # 获取根日志器
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.handlers.clear()  # 清除默认处理器
    
    # 添加处理器到根日志器
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
    
    # 设置第三方库的日志级别
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("fastapi").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """
    获取日志器实例
    
    Args:
        name: 日志器名称
    
    Returns:
        logging.Logger: 日志器实例
    """
    return logging.getLogger(name)
