# 智能体对话相关路由
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import User
from schemas import (
    AgentConversationRequest, AgentConversationResponse
)
from dependencies import get_current_active_user
from logging_config import get_logger
from errors import BadRequestError
from content_generator import agent_service

# 获取日志器
logger = get_logger(__name__)

# 创建路由实例
router = APIRouter()

# 智能体对话接口
@router.post("/api/agent/conversation", response_model=AgentConversationResponse)
def agent_conversation(request: AgentConversationRequest, current_user: User = Depends(get_current_active_user)):
    """
    智能体对话接口
    
    Args:
        request: 对话请求，包含当前消息和对话历史
        current_user: 当前活跃用户
    
    Returns:
        AgentConversationResponse: 智能体的响应
    """
    logger.info(f"智能体对话请求: 用户ID={current_user.id}, 消息内容={request.message[:50]}...")
    
    try:
        # 调用智能体服务进行对话
        response = agent_service.converse(
            agent_topic="母婴智能体",
            current_request=request.message,
            conversation_history=request.conversation_history
        )
        
        logger.info(f"智能体对话响应成功: 用户ID={current_user.id}, 响应类型={'智能体' if response.get('is_agent') else '普通消息'}")
        
        # 构建响应
        return AgentConversationResponse(
            status="success",
            content=response.get("content", ""),
            generated_agent=response.get("generated_agent"),
            agent_title=response.get("agent_title"),
            is_agent=response.get("is_agent", False)
        )
    except Exception as e:
        logger.error(f"智能体对话出错: 用户ID={current_user.id}, 错误={str(e)}")
        raise BadRequestError(message="智能体对话失败", details=str(e))
