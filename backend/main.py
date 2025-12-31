# 首先设置日志
from logging_config import setup_logging, get_logger
setup_logging()
logger = get_logger(__name__)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.encoders import jsonable_encoder
from pydantic.json import custom_pydantic_encoder
import json
from contextlib import asynccontextmanager
import logging
from fastapi_csrf_protect import CsrfProtect
from fastapi_csrf_protect.exceptions import CsrfProtectError
import redis.asyncio as redis
import os

# 导入配置
from config import settings

# 定义全局变量，标记Redis是否可用
redis_available = False

# 根据Redis可用性选择RateLimiter
import os
import asyncio
is_test = os.environ.get("TESTING", "false").lower() == "true"

# 默认使用模拟的RateLimiter
from fastapi import Request

class RateLimiter:
    def __init__(self, times: int = None, seconds: int = None):
        pass
    
    async def __call__(self, request: Request = None):
        pass

if not is_test:
    try:
        from fastapi_limiter import FastAPILimiter
        from fastapi_limiter.depends import RateLimiter as RealRateLimiter
        import redis.asyncio as redis
        
        # 测试Redis连接
        async def test_redis_connection():
            try:
                redis_url = settings.REDIS_URL
                redis_connection = redis.from_url(redis_url)
                await redis_connection.ping()
                await redis_connection.close()
                return True
            except Exception:
                return False
        
        # 同步测试Redis连接
        loop = asyncio.get_event_loop()
        redis_available = loop.run_until_complete(test_redis_connection())
        
        if redis_available:
            RateLimiter = RealRateLimiter
            logger.info("Redis连接测试成功，将使用真实的RateLimiter")
        else:
            logger.warning("Redis连接测试失败，将使用模拟的RateLimiter")
            redis_available = False
    except (ImportError, Exception) as e:
        # 如果导入失败，则使用模拟的RateLimiter
        logger.warning(f"无法导入Redis或FastAPILimiter，请求限流功能将不可用: {str(e)}")
        redis_available = False

from database import Base, engine
import models  # 导入模型，确保表能被创建
from routes import router
from agent_routes import router as agent_router

# 创建数据库表
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    应用生命周期管理
    - 启动时创建数据库表、初始化Redis连接和FastAPILimiter
    - 关闭时关闭Redis连接
    """
    # 创建所有数据库表
    Base.metadata.create_all(bind=engine)
    
    # 初始化Redis连接和FastAPILimiter
    import os
    is_test = os.environ.get("TESTING", "false").lower() == "true"
    if not is_test and redis_available:
        try:
            from fastapi_limiter import FastAPILimiter
            redis_url = settings.REDIS_URL
            redis_connection = redis.from_url(redis_url)
            await FastAPILimiter.init(redis_connection)
            logger.info("Redis连接和FastAPILimiter初始化完成")
        except Exception as e:
            logger.warning(f"Redis连接失败，请求限流功能将不可用: {str(e)}")
    else:
        logger.info("测试环境下或Redis不可用，跳过Redis和FastAPILimiter初始化")
    
    yield
    
    # 关闭Redis连接
    if redis_available:
        try:
            from fastapi_limiter import FastAPILimiter
            await FastAPILimiter.close()
            logger.info("Redis连接关闭完成")
        except Exception as e:
            logger.warning(f"关闭Redis连接失败: {str(e)}")

# 创建FastAPI应用实例
app = FastAPI(
    title=settings.APP_NAME,
    description="提供内容管理、用户认证和商业化功能的API",
    version=settings.APP_VERSION,
    lifespan=lifespan,  # 添加生命周期管理
    json_encoder=jsonable_encoder
)

# 创建静态文件目录
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
avatar_dir = os.path.join(static_dir, "avatars")

# 确保目录存在
os.makedirs(avatar_dir, exist_ok=True)

# 挂载静态文件服务
app.mount("/static", StaticFiles(directory=static_dir), name="static")

logger.info("FastAPI应用初始化完成")

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOW_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)

# 注册全局异常处理程序
from errors import register_exception_handlers
register_exception_handlers(app)

# 配置CSRF保护
# 直接设置秘密密钥
CsrfProtect._secret_key = settings.CSRF_SECRET_KEY
CsrfProtect._cookie_samesite = settings.CSRF_COOKIE_SAMESITE
CsrfProtect._cookie_secure = settings.CSRF_COOKIE_SECURE

# 健康检查端点
@app.get("/health")
async def health_check():
    logger.info("健康检查请求")
    return {"status": "healthy", "service": "fastapi-backend"}

# 根路径
@app.get("/")
async def root():
    return {
        "message": "垂直领域内容变现平台API服务正在运行",
        "version": "1.0.0",
        "endpoints": {
            "auth": {
                "register": "/api/auth/register",
                "login": "/api/auth/login",
                "me": "/api/auth/me"
            },
            "content": {
                "list": "/api/content",
                "create": "/api/content",
                "detail": "/api/content/{id}"
            }
        }
    }

# 包含路由
app.include_router(router)
app.include_router(agent_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)