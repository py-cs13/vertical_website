# 认证工具函数文件
# 处理密码哈希、JWT令牌生成和验证

from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from typing import Optional
from logging_config import get_logger
from errors import AuthenticationError, AuthorizationError

# 导入配置
from config import settings

# 获取日志器
logger = get_logger(__name__)

# JWT配置
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

logger.info("JWT配置加载完成")

# 密码哈希上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    验证密码是否匹配
    
    Args:
        plain_password: 明文密码
        hashed_password: 哈希后的密码
    
    Returns:
        bool: 密码是否匹配
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    生成密码的哈希值
    
    Args:
        password: 明文密码
    
    Returns:
        str: 哈希后的密码
    """
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    创建访问令牌
    
    Args:
        data: 要编码到令牌中的数据
        expires_delta: 令牌过期时间增量
    
    Returns:
        str: JWT访问令牌
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    logger.debug(f"生成JWT令牌，用户ID: {data.get('sub')}, 过期时间: {expire}")
    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict]:
    """
    解码访问令牌
    
    Args:
        token: JWT访问令牌
    
    Returns:
        Optional[dict]: 解码后的令牌数据，如果令牌无效则返回None
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        logger.debug(f"JWT令牌解码成功，用户ID: {payload.get('sub')}")
        return payload
    except JWTError as e:
        logger.error(f"JWT令牌解码失败: {str(e)}")
        return None


def get_current_user_optional(token: Optional[str] = None) -> Optional[dict]:
    """
    获取可选的当前用户信息
    
    Args:
        token: JWT访问令牌（可选）
    
    Returns:
        Optional[dict]: 解码后的令牌数据，如果令牌无效或未提供则返回None
    """
    if not token:
        return None
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        logger.debug(f"JWT令牌解码成功（可选），用户ID: {payload.get('sub')}")
        return payload
    except JWTError as e:
        logger.debug(f"JWT令牌解码失败（可选）: {str(e)}")
        return None


