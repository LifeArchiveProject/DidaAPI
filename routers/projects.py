"""清单管理相关API路由"""
from fastapi import APIRouter
from services import project_service, dida_service
from utils import app_logger

router = APIRouter(prefix="/projects", tags=["清单管理"])


@router.get("/all",
           summary="获取所有项目/清单",
           description="获取当前用户的所有项目/清单列表")
async def get_all_projects():
    """
    获取所有项目/清单
    
    返回当前用户的所有项目/清单列表，包括：
    - 项目ID、名称、颜色
    - 项目权限、类型、用户数量
    - 创建时间、修改时间等信息
    
    **注意**: 需要先完成微信登录获取认证会话
    """
    try:
        app_logger.info("请求获取所有项目")
        
        # 检查认证状态
        session_status = dida_service.get_session_status()
        if not session_status["has_session"]:
            return {"error": "no_auth_session", "message": "未设置认证会话，请先完成微信登录"}

        # 获取认证信息
        current_session = dida_service.current_session
        auth_token = current_session['auth_token']
        csrf_token = current_session['csrf_token']

        # 调用项目服务
        result = await project_service.get_projects(auth_token, csrf_token)

        if not result:
            return {"error": "service_error", "message": "获取项目列表失败，请稍后重试"}

        # 记录日志
        if 'error' in result:
            app_logger.info(f"项目获取失败: {result.get('error')}")
        else:
            project_count = len(result) if isinstance(result, list) else 0
            app_logger.info(f"项目获取完成，项目数: {project_count}")

        # 直接返回原始响应
        return result

    except Exception as e:
        app_logger.error(f"获取项目时发生未知错误: {e}")
        return {"error": "server_error", "message": f"服务器内部错误: {str(e)}"}
