"""习惯管理相关API路由"""
from fastapi import APIRouter
from fastapi.responses import Response
# 不再需要响应模型导入
from services import habit_service, dida_service
from utils import app_logger

router = APIRouter(prefix="/habits", tags=["习惯管理"])


@router.get("/all",
           summary="获取所有习惯",
           description="获取当前用户的所有习惯列表")
async def get_all_habits():
    """
    获取所有习惯
    
    返回当前用户的所有习惯列表，包括：
    - 习惯ID、名称、图标、颜色
    - 习惯状态、激励语句、总打卡次数
    - 创建时间、修改时间、类型、目标值等信息
    
    **注意**: 需要先完成微信登录获取认证会话
    """
    try:
        app_logger.info("请求获取所有习惯")
        
        # 检查认证状态
        session_status = dida_service.get_session_status()
        if not session_status["has_session"]:
            return {"error": "no_auth_session", "message": "未设置认证会话，请先完成微信登录"}
        
        # 获取认证信息
        current_session = dida_service.current_session
        auth_token = current_session['auth_token']
        csrf_token = current_session['csrf_token']
        
        # 调用习惯服务
        result = await habit_service.get_habits(auth_token, csrf_token)
        
        if not result:
            return {"error": "service_error", "message": "获取习惯列表失败，请稍后重试"}

        # 记录日志
        if 'error' in result:
            app_logger.info(f"习惯获取失败: {result.get('error')}")
        else:
            habit_count = len(result) if isinstance(result, list) else 0
            app_logger.info(f"习惯获取完成，习惯数: {habit_count}")

        # 直接返回原始响应
        return result

    except Exception as e:
        app_logger.error(f"获取习惯时发生未知错误: {e}")
        return {"error": "server_error", "message": f"服务器内部错误: {str(e)}"}


@router.get("/statistics/week/current",
           summary="获取本周习惯打卡统计",
           description="获取本周的习惯打卡统计信息")
async def get_week_current_statistics():
    """
    获取本周习惯打卡统计
    
    返回本周的习惯打卡统计，包括：
    - 每日打卡情况
    - 习惯完成率
    - 连续打卡天数等信息
    
    **注意**: 需要先完成微信登录获取认证会话
    """
    try:
        app_logger.info("请求获取本周习惯打卡统计")
        
        # 检查认证状态
        session_status = dida_service.get_session_status()
        if not session_status["has_session"]:
            return {"error": "no_auth_session", "message": "未设置认证会话，请先完成微信登录"}
        
        # 获取认证信息
        current_session = dida_service.current_session
        auth_token = current_session['auth_token']
        csrf_token = current_session['csrf_token']
        
        # 调用习惯服务
        result = await habit_service.get_week_current_statistics(auth_token, csrf_token)
        
        if not result:
            return {"error": "service_error", "message": "获取本周习惯打卡统计失败，请稍后重试"}

        # 记录日志
        if 'error' in result:
            app_logger.info(f"本周习惯打卡统计获取失败: {result.get('error')}")
        else:
            app_logger.info(f"本周习惯打卡统计获取完成")

        # 直接返回原始响应
        return result

    except Exception as e:
        app_logger.error(f"获取本周习惯打卡统计时发生未知错误: {e}")
        return {"error": "server_error", "message": f"服务器内部错误: {str(e)}"}


@router.get("/export",
           summary="导出习惯数据",
           description="导出习惯数据为Excel文件")
async def export_habits():
    """
    导出习惯数据（Excel格式）

    导出当前用户的所有习惯数据为Excel文件，包括：
    - 习惯基本信息
    - 打卡记录
    - 统计数据等

    **注意**: 需要先完成微信登录获取认证会话
    """
    try:
        app_logger.info("请求导出习惯数据")

        # 检查认证状态
        session_status = dida_service.get_session_status()
        if not session_status["has_session"]:
            return {"error": "no_auth_session", "message": "未设置认证会话，请先完成微信登录"}

        # 获取认证信息
        current_session = dida_service.current_session
        auth_token = current_session['auth_token']
        csrf_token = current_session['csrf_token']

        # 调用习惯服务
        result = await habit_service.export_habits(auth_token, csrf_token)

        if not result:
            return {"error": "service_error", "message": "导出习惯数据失败，请稍后重试"}

        # 检查是否有错误
        if 'error' in result:
            app_logger.info(f"习惯数据导出失败: {result.get('error')}")
            return result

        # 成功获取文件内容
        app_logger.info(f"习惯数据导出完成，文件名: {result.get('filename')}")

        # 返回文件响应
        return Response(
            content=result['content'],
            media_type=result['content_type'],
            headers={
                "Content-Disposition": f"attachment; filename={result['filename']}"
            }
        )

    except Exception as e:
        app_logger.error(f"导出习惯数据时发生未知错误: {e}")
        return {"error": "server_error", "message": f"服务器内部错误: {str(e)}"}
