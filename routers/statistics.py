"""统计相关API路由"""
from fastapi import APIRouter, Query
from datetime import datetime
from services import statistics_service, dida_service
from utils import app_logger

router = APIRouter(prefix="/statistics", tags=["统计分析"])


@router.get("/ranking",
           summary="获取用户排名统计",
           description="获取用户在滴答清单中的排名和基本统计信息")
async def get_user_ranking():
    """
    获取用户排名统计
    
    返回用户的排名信息，包括：
    - 排名百分比（你比X%的用户更勤奋）
    - 任务数量、项目数量、使用天数
    - 已完成任务数、成就值、账号等级
    
    **注意**: 需要先完成微信登录获取认证会话
    """
    try:
        app_logger.info("请求获取用户排名统计")
        
        # 检查认证状态
        session_status = dida_service.get_session_status()
        if not session_status["has_session"]:
            return {"error": "no_auth_session", "message": "未设置认证会话，请先完成微信登录"}

        # 获取认证信息
        current_session = dida_service.current_session
        auth_token = current_session['auth_token']
        csrf_token = current_session['csrf_token']

        # 调用统计服务
        result = await statistics_service.get_user_ranking(auth_token, csrf_token)

        if not result:
            return {"error": "service_error", "message": "获取用户排名统计失败，请稍后重试"}

        # 记录日志
        if 'error' in result:
            app_logger.info(f"用户排名统计获取失败: {result.get('error')}")
        else:
            app_logger.info("用户排名统计获取完成")

        # 直接返回原始响应
        return result

    except Exception as e:
        app_logger.error(f"获取用户排名统计时发生未知错误: {e}")
        return {"error": "server_error", "message": f"服务器内部错误: {str(e)}"}


@router.get("/general",
           summary="获取通用统计信息",
           description="获取概览、成就值、趋势等通用统计信息")
async def get_general_statistics():
    """
    获取通用统计信息
    
    返回通用统计信息，包括：
    - 成就值、账号等级
    - 昨日/今日/总完成任务数
    - 昨日/今日/总番茄数和专注时长
    - 目标番茄数和目标专注时长
    
    **注意**: 需要先完成微信登录获取认证会话
    """
    try:
        app_logger.info("请求获取通用统计信息")
        
        # 检查认证状态
        session_status = dida_service.get_session_status()
        if not session_status["has_session"]:
            return {"error": "no_auth_session", "message": "未设置认证会话，请先完成微信登录"}

        # 获取认证信息
        current_session = dida_service.current_session
        auth_token = current_session['auth_token']
        csrf_token = current_session['csrf_token']

        # 调用统计服务
        result = await statistics_service.get_general_statistics(auth_token, csrf_token)

        if not result:
            return {"error": "service_error", "message": "获取通用统计信息失败，请稍后重试"}

        # 记录日志
        if 'error' in result:
            app_logger.info(f"通用统计信息获取失败: {result.get('error')}")
        else:
            app_logger.info("通用统计信息获取完成")

        # 直接返回原始响应
        return result

    except Exception as e:
        app_logger.error(f"获取通用统计信息时发生未知错误: {e}")
        return {"error": "server_error", "message": f"服务器内部错误: {str(e)}"}


@router.get("/tasks",
           summary="获取任务统计信息",
           description="获取指定日期范围内的任务统计信息")
async def get_task_statistics(
    start_date: str = Query(..., description="开始日期，格式: YYYYMMDD", example="20231201"),
    end_date: str = Query(..., description="结束日期，格式: YYYYMMDD", example="20231207")
):
    """
    获取任务统计信息
    
    返回指定日期范围内的任务统计，包括：
    - 逾期完成数、按时完成数、无日期任务数
    - 未完成任务数
    - 按项目和标签的完成数量统计
    
    **注意**: 需要先完成微信登录获取认证会话
    """
    try:
        app_logger.info(f"请求获取任务统计信息，日期范围: {start_date} - {end_date}")
        
        # 验证日期格式
        try:
            datetime.strptime(start_date, "%Y%m%d")
            datetime.strptime(end_date, "%Y%m%d")
        except ValueError:
            return {"error": "invalid_date_format", "message": "日期格式错误，请使用 YYYYMMDD 格式"}

        # 检查认证状态
        session_status = dida_service.get_session_status()
        if not session_status["has_session"]:
            return {"error": "no_auth_session", "message": "未设置认证会话，请先完成微信登录"}

        # 获取认证信息
        current_session = dida_service.current_session
        auth_token = current_session['auth_token']
        csrf_token = current_session['csrf_token']

        # 调用统计服务
        result = await statistics_service.get_task_statistics(auth_token, csrf_token, start_date, end_date)

        if not result:
            return {"error": "service_error", "message": "获取任务统计信息失败，请稍后重试"}

        # 记录日志
        if 'error' in result:
            app_logger.info(f"任务统计信息获取失败: {result.get('error')}")
        else:
            app_logger.info("任务统计信息获取完成")

        # 直接返回原始响应
        return result

    except Exception as e:
        app_logger.error(f"获取任务统计信息时发生未知错误: {e}")
        return {"error": "server_error", "message": f"服务器内部错误: {str(e)}"}
