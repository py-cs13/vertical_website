# 错误处理模块
# 定义统一的错误响应格式和全局异常处理

from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Any, Optional
from logging_config import get_logger

logger = get_logger(__name__)


# 标准错误响应模型
class ErrorResponse(BaseModel):
    """统一的错误响应格式"""
    code: str  # 错误代码
    message: str  # 错误消息
    details: Optional[Any] = None  # 详细错误信息
    request_id: Optional[str] = None  # 请求ID，用于跟踪错误


# 自定义异常类
class AppException(HTTPException):
    """应用程序自定义异常基类"""
    def __init__(
        self,
        status_code: int,
        code: str,
        message: str,
        details: Any = None,
        request_id: str = None
    ):
        super().__init__(status_code=status_code, detail=message)
        self.code = code
        self.message = message
        self.details = details
        self.request_id = request_id


class AuthenticationError(AppException):
    """认证相关错误"""
    def __init__(self, message: str = "认证失败", details: Any = None, request_id: str = None):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            code="AUTHENTICATION_ERROR",
            message=message,
            details=details,
            request_id=request_id
        )


class AuthorizationError(AppException):
    """授权相关错误"""
    def __init__(self, message: str = "权限不足", details: Any = None, request_id: str = None):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            code="AUTHORIZATION_ERROR",
            message=message,
            details=details,
            request_id=request_id
        )


class ValidationError(AppException):
    """数据验证错误"""
    def __init__(self, message: str = "数据验证失败", details: Any = None, request_id: str = None):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            code="VALIDATION_ERROR",
            message=message,
            details=details,
            request_id=request_id
        )


class ResourceNotFoundError(AppException):
    """资源不存在错误"""
    def __init__(self, message: str = "资源不存在", details: Any = None, request_id: str = None):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            code="RESOURCE_NOT_FOUND",
            message=message,
            details=details,
            request_id=request_id
        )


class ConflictError(AppException):
    """资源冲突错误"""
    def __init__(self, message: str = "资源冲突", details: Any = None, request_id: str = None):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            code="CONFLICT_ERROR",
            message=message,
            details=details,
            request_id=request_id
        )


class BadRequestError(AppException):
    """请求参数错误"""
    def __init__(self, message: str = "请求参数错误", details: Any = None, request_id: str = None):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            code="BAD_REQUEST",
            message=message,
            details=details,
            request_id=request_id
        )


class InternalServerError(AppException):
    """服务器内部错误"""
    def __init__(self, message: str = "服务器内部错误", details: Any = None, request_id: str = None):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            code="INTERNAL_SERVER_ERROR",
            message=message,
            details=details,
            request_id=request_id
        )


# 全局异常处理函数
def register_exception_handlers(app):
    """注册全局异常处理程序"""
    
    @app.exception_handler(AppException)
    async def app_exception_handler(request, exc):
        """自定义应用异常处理"""
        logger.error(f"应用异常: {exc.code} - {exc.message}", exc_info=True)
        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorResponse(
                code=exc.code,
                message=exc.message,
                details=exc.details,
                request_id=exc.request_id
            ).dict()
        )
    
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request, exc):
        """HTTP异常处理"""
        logger.error(f"HTTP异常: {exc.status_code} - {exc.detail}", exc_info=True)
        # 将FastAPI的HTTPException转换为统一的错误格式
        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorResponse(
                code=f"HTTP_{exc.status_code}",
                message=exc.detail
            ).dict()
        )
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request, exc):
        """通用异常处理"""
        logger.error(f"未捕获的异常: {str(exc)}", exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ErrorResponse(
                code="UNEXPECTED_ERROR",
                message="服务器遇到了意外错误",
                details=str(exc) if app.debug else None  # 调试模式下显示详细错误
            ).dict()
        )
