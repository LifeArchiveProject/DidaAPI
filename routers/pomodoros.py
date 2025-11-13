"""番茄专注相关API路由"""
from dataclasses import asdict
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Query

from services import pomodoro_service, dida_service
from models import (
    FocusStartOptions,
    FocusControlOptions,
    FocusStopOptions,
)
from utils import app_logger

pomodoro_router = APIRouter(prefix="/pomodoros", tags=["番茄专注"])
stopwatch_router = APIRouter(prefix="/pomodoros", tags=["正计时专注"])


router = pomodoro_router

timer_router = stopwatch_router


def _get_auth_tokens():
    session_status = dida_service.get_session_status()
    if not session_status["has_session"]:
        return None, {"error": "no_auth_session", "message": "未设置认证会话，请先完成微信登录"}

    current_session = dida_service.current_session
    return (current_session["auth_token"], current_session["csrf_token"]), None


@pomodoro_router.get("/general",
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


@stopwatch_router.get("/distribution",
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


@stopwatch_router.get("/timeline",
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


@stopwatch_router.get("/heatmap",
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


@stopwatch_router.get("/time-distribution",
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


@stopwatch_router.get("/hour-distribution",
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


@pomodoro_router.get(
    "/focus/start",
    summary="开始番茄钟（自动填充参数）",
    description="根据传入的番茄配置自动生成滴答 focusOp 所需字段，避免手动拼装请求体。",
)
async def start_focus(options: FocusStartOptions = Depends()):
    app_logger.info(
        "请求开始番茄钟，duration={}, autoPomoLeft={}, pomoCount={}",
        options.duration,
        options.auto_pomo_left,
        options.pomo_count,
    )
    app_logger.debug("[api_focus_start] options={}", options.model_dump())
    tokens, error = _get_auth_tokens()
    if error:
        return error

    auth_token, csrf_token = tokens
    result = await pomodoro_service.start_focus(
        auth_token,
        csrf_token,
        duration=options.duration,
        auto_pomo_left=options.auto_pomo_left,
        pomo_count=options.pomo_count,
        manual=options.manual,
        note=options.note,
        focus_on_id=options.focus_on_id,
        focus_on_type=options.focus_on_type,
        focus_on_title=options.focus_on_title,
        last_point=options.last_point,
    )
    return result


@pomodoro_router.get(
    "/focus/pause",
    summary="暂停番茄钟（自动填充参数）",
    description="调用滴答 pause 操作并自动补全必要字段。",
)
async def pause_focus(options: FocusControlOptions = Depends()):
    app_logger.info("请求暂停番茄钟")
    app_logger.debug("[api_focus_pause] options={}", options.model_dump())
    tokens, error = _get_auth_tokens()
    if error:
        return error

    auth_token, csrf_token = tokens
    result = await pomodoro_service.pause_focus(
        auth_token,
        csrf_token,
        manual=options.manual,
        note=options.note,
        focus_on_type=options.focus_on_type,
        focus_on_title=options.focus_on_title,
        last_point=options.last_point,
    )
    return result


@pomodoro_router.get(
    "/focus/continue",
    summary="继续番茄钟（自动填充参数）",
    description="调用滴答 continue 操作并自动补全必要字段。",
)
async def continue_focus(options: FocusControlOptions = Depends()):
    app_logger.info("请求继续番茄钟")
    app_logger.debug("[api_focus_continue] options={}", options.model_dump())
    tokens, error = _get_auth_tokens()
    if error:
        return error

    auth_token, csrf_token = tokens
    result = await pomodoro_service.continue_focus(
        auth_token,
        csrf_token,
        manual=options.manual,
        note=options.note,
        focus_on_type=options.focus_on_type,
        focus_on_title=options.focus_on_title,
        last_point=options.last_point,
    )
    return result


@pomodoro_router.get(
    "/focus/finish",
    summary="结束番茄钟（正常完成）",
    description="调用滴答 finish 操作，用于正常结束番茄。",
)
async def finish_focus(options: FocusControlOptions = Depends()):
    app_logger.info("请求结束番茄钟（正常完成）")
    app_logger.debug("[api_focus_finish] options={}", options.model_dump())
    tokens, error = _get_auth_tokens()
    if error:
        return error

    auth_token, csrf_token = tokens
    result = await pomodoro_service.finish_focus(
        auth_token,
        csrf_token,
        manual=options.manual,
        note=options.note,
        focus_on_type=options.focus_on_type,
        focus_on_title=options.focus_on_title,
        last_point=options.last_point,
    )
    return result


@pomodoro_router.get(
    "/focus/stop",
    summary="不足 5 分钟强制结束番茄钟",
    description="当番茄时长未满 5 分钟需要终止时，自动发送 drop + exit 操作。",
)
async def stop_focus(options: FocusStopOptions = Depends()):
    app_logger.info("请求结束番茄钟，include_exit={}", options.include_exit)
    app_logger.debug("[api_focus_stop] options={}", options.model_dump())
    tokens, error = _get_auth_tokens()
    if error:
        return error

    auth_token, csrf_token = tokens
    result = await pomodoro_service.stop_focus(
        auth_token,
        csrf_token,
        manual=options.manual,
        note=options.note,
        focus_on_type=options.focus_on_type,
        focus_on_title=options.focus_on_title,
        last_point=options.last_point,
        include_exit=options.include_exit,
    )
    return result


@pomodoro_router.post(
    "/focus/point/{point}",
    summary="设置番茄操作指针",
    description="手动覆盖 focusOp 请求的 lastPoint 缓存值。",
)
async def set_focus_point(point: int):
    if point < 0:
        return {"error": "invalid_point", "message": "指针值必须为非负整数"}

    pomodoro_service.set_last_point(point)
    app_logger.info("已更新番茄操作指针: %s", point)
    return {"lastPoint": point}


@pomodoro_router.post(
    "/focus/reset",
    summary="重置番茄钟本地状态",
    description="清空服务端缓存的番茄会话信息，仅保留 lastPoint。",
)
async def reset_focus_state():
    pomodoro_service.reset_focus_session()
    app_logger.info("已重置本地番茄钟状态缓存")
    return {"message": "focus_state_reset"}


@pomodoro_router.get(
    "/focus/state",
    summary="获取番茄钟本地状态",
    description="返回当前缓存的番茄会话信息，便于排查 lastPoint 与 firstFocusId 等字段。",
)
async def get_focus_state():
    state = pomodoro_service.get_focus_state_snapshot()
    state_dict = asdict(state)
    return {
        "lastPoint": state_dict["last_point"],
        "focusId": state_dict["focus_id"],
        "firstFocusId": state_dict["first_focus_id"],
        "duration": state_dict["duration"],
        "autoPomoLeft": state_dict["auto_pomo_left"],
        "pomoCount": state_dict["pomo_count"],
        "manual": state_dict["manual"],
        "note": state_dict["note"],
        "focusOnId": state_dict["focus_on_id"],
        "status": state_dict["status"],
        "rawCurrent": state_dict["raw_current"],
    }


@pomodoro_router.get(
    "/focus/current",
    summary="查看当前番茄钟状态",
    description="同步滴答清单服务器返回的当前番茄状态，不提交任何操作。",
)
async def get_focus_current(last_point: Optional[int] = Query(None, description="覆盖使用的 lastPoint")):
    app_logger.debug("[api_focus_current] last_point={}", last_point)
    tokens, error = _get_auth_tokens()
    if error:
        return error

    auth_token, csrf_token = tokens
    result = await pomodoro_service.query_focus_state(
        auth_token,
        csrf_token,
        last_point=last_point,
    )
    return result
