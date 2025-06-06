"""用户相关API路由"""
from fastapi import APIRouter
from services import user_service, dida_service
from utils import app_logger

router = APIRouter(prefix="/users", tags=["用户信息"])


@router.get("/profile",
           summary="获取用户信息",
           description="获取当前登录用户的详细信息")
async def get_user_profile():
    """
    获取用户信息
    
    返回当前登录用户的详细信息，包括：
    - 用户名、邮箱、手机号
    - 用户头像、显示名称
    - 账户域名、外部ID
    - 邮箱验证状态、性别、语言设置
    - 用户代码等基本信息
    
    **注意**: 需要先完成微信登录获取认证会话
    """
    try:
        app_logger.info("请求获取用户信息")
        
        # 检查认证状态
        session_status = dida_service.get_session_status()
        if not session_status["has_session"]:
            return {"error": "no_auth_session", "message": "未设置认证会话，请先完成微信登录"}
        
        # 获取认证信息
        current_session = dida_service.current_session
        auth_token = current_session['auth_token']
        csrf_token = current_session['csrf_token']
        
        # 调用用户服务
        result = await user_service.get_user_profile(auth_token, csrf_token)
        
        if not result:
            return {"error": "service_error", "message": "获取用户信息失败，请稍后重试"}

        # 记录日志
        if 'error' in result:
            app_logger.info(f"用户信息获取失败: {result.get('error')}")
        else:
            username = result.get('username', 'N/A')
            app_logger.info(f"用户信息获取完成，用户名: {username}")

        # 直接返回原始响应
        return result

    except Exception as e:
        app_logger.error(f"获取用户信息时发生未知错误: {e}")
        return {"error": "server_error", "message": f"服务器内部错误: {str(e)}"}
