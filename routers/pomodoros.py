"""番茄专注相关API路由"""
from fastapi import APIRouter, Query
from datetime import datetime
from services import pomodoro_service, dida_service
from utils import app_logger

router = APIRouter(prefix="/pomodoros", tags=["番茄专注"])


@router.get("/general",
           summary="获取番茄专注概览",
           description="获取番茄专注的概览统计信息（桌面版）")
async def get_pomodoro_general():
    """
    获取番茄专注概览
    
    返回番茄专注的概览信息，包括：
    - 今日番茄数量和专注时长
    - 总番茄数量和总专注时长
    
    **注意**: 需要先完成微信登录获取认证会话
    """
    try:
        app_logger.info("请求获取番茄专注概览")
        
        # 检查认证状态
        session_status = dida_service.get_session_status()
        if not session_status["has_session"]:
            return {"error": "no_auth_session", "message": "未设置认证会话，请先完成微信登录"}

        # 获取认证信息
        current_session = dida_service.current_session
        auth_token = current_session['auth_token']
        csrf_token = current_session['csrf_token']

        # 调用番茄专注服务
        result = await pomodoro_service.get_general_for_desktop(auth_token, csrf_token)

        if not result:
            return {"error": "service_error", "message": "获取番茄专注概览失败，请稍后重试"}

        # 记录日志
        if 'error' in result:
            app_logger.info(f"番茄专注概览获取失败: {result.get('error')}")
        else:
            app_logger.info("番茄专注概览获取完成")

        # 直接返回原始响应
        return result

    except Exception as e:
        app_logger.error(f"获取番茄专注概览时发生未知错误: {e}")
        return {"error": "server_error", "message": f"服务器内部错误: {str(e)}"}


@router.get("/distribution",
           summary="获取专注详情分布",
           description="获取指定日期范围内的专注时长分布统计")
async def get_focus_distribution(
    start_date: str = Query(..., description="开始日期，格式: YYYYMMDD", example="20231201"),
    end_date: str = Query(..., description="结束日期，格式: YYYYMMDD", example="20231207")
):
    """
    获取专注详情分布
    
    返回指定日期范围内的专注分布，包括：
    - 按项目分布的专注时长
    - 按标签分布的专注时长
    - 按任务分布的专注时长
    
    **注意**: 需要先完成微信登录获取认证会话
    """
    try:
        app_logger.info(f"请求获取专注详情分布，日期范围: {start_date} - {end_date}")
        
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

        # 调用番茄专注服务
        result = await pomodoro_service.get_focus_distribution(auth_token, csrf_token, start_date, end_date)

        if not result:
            return {"error": "service_error", "message": "获取专注详情分布失败，请稍后重试"}

        # 记录日志
        if 'error' in result:
            app_logger.info(f"专注详情分布获取失败: {result.get('error')}")
        else:
            app_logger.info("专注详情分布获取完成")

        # 直接返回原始响应
        return result

    except Exception as e:
        app_logger.error(f"获取专注详情分布时发生未知错误: {e}")
        return {"error": "server_error", "message": f"服务器内部错误: {str(e)}"}


@router.get("/timeline",
           summary="获取专注记录时间线",
           description="获取专注记录的时间线数据，支持分页")
async def get_focus_timeline(
    to: str = Query(None, description="分页参数：上一页最后一条记录的startTime，用于获取更早的数据", example="2025-04-22T08:43:31.000+0000")
):
    """
    获取专注记录时间线

    返回专注记录的时间线数据，包括：
    - 专注记录ID、开始时间、结束时间
    - 专注状态、暂停时长等信息

    **分页说明**:
    - 不传 `to` 参数：获取最新的专注记录（约31条）
    - 传入 `to` 参数：获取指定时间之前的专注记录
    - `to` 参数值为上一页最后一条记录的 `startTime` 字段值

    **注意**: 需要先完成微信登录获取认证会话
    """
    try:
        log_msg = "请求获取专注记录时间线"
        if to:
            log_msg += f"，分页参数: {to}"
        app_logger.info(log_msg)

        # 检查认证状态
        session_status = dida_service.get_session_status()
        if not session_status["has_session"]:
            return {"error": "no_auth_session", "message": "未设置认证会话，请先完成微信登录"}

        # 获取认证信息
        current_session = dida_service.current_session
        auth_token = current_session['auth_token']
        csrf_token = current_session['csrf_token']

        # 处理分页参数
        to_timestamp = None
        if to:
            try:
                to_timestamp = pomodoro_service._convert_time_to_timestamp(to)
                app_logger.info(f"时间转换成功: {to} -> {to_timestamp}")
            except ValueError as e:
                return {"error": "invalid_time_format", "message": f"时间格式错误: {str(e)}"}

        # 调用番茄专注服务
        result = await pomodoro_service.get_focus_timeline(auth_token, csrf_token, to_timestamp)

        if not result:
            return {"error": "service_error", "message": "获取专注记录时间线失败，请稍后重试"}

        # 记录日志
        if 'error' in result:
            app_logger.info(f"专注记录时间线获取失败: {result.get('error')}")
        else:
            app_logger.info("专注记录时间线获取完成")

        # 直接返回原始响应
        return result

    except Exception as e:
        app_logger.error(f"获取专注记录时间线时发生未知错误: {e}")
        return {"error": "server_error", "message": f"服务器内部错误: {str(e)}"}


@router.get("/heatmap",
           summary="获取专注趋势热力图",
           description="获取指定日期范围内的专注趋势热力图数据")
async def get_focus_heatmap(
    start_date: str = Query(..., description="开始日期，格式: YYYYMMDD", example="20231201"),
    end_date: str = Query(..., description="结束日期，格式: YYYYMMDD", example="20231207")
):
    """
    获取专注趋势热力图

    返回指定日期范围内的专注趋势数据，包括：
    - 每日专注时长
    - 日期和时区信息

    **注意**: 需要先完成微信登录获取认证会话
    """
    try:
        app_logger.info(f"请求获取专注趋势热力图，日期范围: {start_date} - {end_date}")

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

        # 调用番茄专注服务
        result = await pomodoro_service.get_focus_heatmap(auth_token, csrf_token, start_date, end_date)

        if not result:
            return {"error": "service_error", "message": "获取专注趋势热力图失败，请稍后重试"}

        # 记录日志
        if 'error' in result:
            app_logger.info(f"专注趋势热力图获取失败: {result.get('error')}")
        else:
            app_logger.info("专注趋势热力图获取完成")

        # 直接返回原始响应
        return result

    except Exception as e:
        app_logger.error(f"获取专注趋势热力图时发生未知错误: {e}")
        return {"error": "server_error", "message": f"服务器内部错误: {str(e)}"}


@router.get("/time-distribution",
           summary="获取专注时间分布",
           description="获取指定日期范围内按时间段分布的专注数据")
async def get_focus_time_distribution(
    start_date: str = Query(..., description="开始日期，格式: YYYYMMDD", example="20250526"),
    end_date: str = Query(..., description="结束日期，格式: YYYYMMDD", example="20250601")
):
    """
    获取专注时间分布

    返回指定日期范围内按时间段分布的专注数据，包括：
    - 每日的时间段专注分布
    - 每小时的专注时长统计

    **注意**: 需要先完成微信登录获取认证会话
    """
    try:
        app_logger.info(f"请求获取专注时间分布，日期范围: {start_date} - {end_date}")

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

        # 调用番茄专注服务
        result = await pomodoro_service.get_focus_time_distribution(auth_token, csrf_token, start_date, end_date)

        if not result:
            return {"error": "service_error", "message": "获取专注时间分布失败，请稍后重试"}

        # 记录日志
        if 'error' in result:
            app_logger.info(f"专注时间分布获取失败: {result.get('error')}")
        else:
            app_logger.info("专注时间分布获取完成")

        # 直接返回原始响应
        return result

    except Exception as e:
        app_logger.error(f"获取专注时间分布时发生未知错误: {e}")
        return {"error": "server_error", "message": f"服务器内部错误: {str(e)}"}


@router.get("/hour-distribution",
           summary="获取专注时间按小时分布",
           description="获取指定日期范围内按小时分布的专注时间统计")
async def get_focus_hour_distribution(
    start_date: str = Query(..., description="开始日期，格式: YYYYMMDD", example="20250601"),
    end_date: str = Query(..., description="结束日期，格式: YYYYMMDD", example="20250630")
):
    """
    获取专注时间按小时分布

    返回指定日期范围内按小时分布的专注时间统计，包括：
    - 每小时的总专注时长（分钟）
    - 24小时制的时间分布

    **注意**: 需要先完成微信登录获取认证会话
    """
    try:
        app_logger.info(f"请求获取专注时间按小时分布，日期范围: {start_date} - {end_date}")

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

        # 调用番茄专注服务
        result = await pomodoro_service.get_focus_hour_distribution(auth_token, csrf_token, start_date, end_date)

        if not result:
            return {"error": "service_error", "message": "获取专注时间按小时分布失败，请稍后重试"}

        # 记录日志
        if 'error' in result:
            app_logger.info(f"专注时间按小时分布获取失败: {result.get('error')}")
        else:
            app_logger.info("专注时间按小时分布获取完成")

        # 直接返回原始响应
        return result

    except Exception as e:
        app_logger.error(f"获取专注时间按小时分布时发生未知错误: {e}")
        return {"error": "server_error", "message": f"服务器内部错误: {str(e)}"}
