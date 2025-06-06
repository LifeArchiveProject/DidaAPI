"""自定义导出功能API路由"""
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
import io
import urllib.parse
from services.export_service import export_service
from services.dida_service import dida_service
from utils import app_logger

router = APIRouter(prefix="/custom", tags=["自定义接口"])


@router.get("/export/tasks/excel",
           summary="导出任务到Excel",
           description="导出所有任务到Excel文件，包含全部任务、已完成任务、放弃任务、垃圾桶任务四个工作表")
async def export_tasks_to_excel():
    """
    导出任务到Excel

    将用户的所有任务导出为Excel文件，包含以下工作表：
    - **全部任务**: 当前所有任务（未完成和已完成）
    - **已完成任务**: 历史已完成的任务
    - **放弃任务**: 历史放弃的任务
    - **垃圾桶任务**: 已删除的任务
    
    每个工作表包含任务的完整字段信息，包括：
    - 基本信息：任务ID、标题、内容、描述、项目信息
    - 状态信息：任务状态、优先级、完成进度
    - 时间信息：创建时间、修改时间、开始日期、截止日期
    - 重复设置：重复标志、重复来源、首次重复日期
    - 提醒设置：提醒配置、排除日期
    - 层级关系：父任务、子任务关系
    - 其他属性：标签、附件、评论数量等
    
    **注意**: 需要先调用认证接口设置会话
    """
    try:
        app_logger.info("请求导出任务到Excel")
        
        # 检查认证状态
        session_status = dida_service.get_session_status()
        if not session_status["has_session"]:
            raise HTTPException(
                status_code=401,
                detail="未设置认证会话，请先完成登录"
            )
        
        # 调用导出服务
        result = await export_service.export_tasks_to_excel()
        
        if 'error' in result:
            app_logger.error(f"导出任务失败: {result['error']}")
            raise HTTPException(
                status_code=500,
                detail=f"导出失败: {result['error']}"
            )
        
        app_logger.info(f"任务导出成功，文件大小: {result['size']} 字节")

        # 对文件名进行URL编码以支持中文
        encoded_filename = urllib.parse.quote(result['filename'], safe='')

        # 返回文件下载响应
        return StreamingResponse(
            io.BytesIO(result['content']),
            media_type=result['content_type'],
            headers={
                "Content-Disposition": f"attachment; filename*=UTF-8''{encoded_filename}"
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        app_logger.error(f"导出任务时发生未知错误: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"服务器内部错误: {str(e)}"
        )


@router.get("/export/tasks/excel/info",
           summary="获取任务导出信息",
           description="获取当前用户任务的统计信息，用于导出前预览")
async def get_export_info():
    """
    获取任务导出信息
    
    返回当前用户任务的统计信息，包括：
    - 全部任务数量
    - 已完成任务数量
    - 垃圾桶任务数量
    - 认证状态
    
    **注意**: 需要先调用认证接口设置会话
    """
    try:
        app_logger.info("请求获取任务导出信息")
        
        # 检查认证状态
        session_status = dida_service.get_session_status()
        if not session_status["has_session"]:
            return {
                "error": "no_auth_session",
                "message": "未设置认证会话，请先完成登录",
                "auth_status": False
            }
        
        # 获取各类任务统计
        stats = {
            "auth_status": True,
            "all_tasks_count": 0,
            "completed_tasks_count": 0,
            "abandoned_tasks_count": 0,
            "trash_tasks_count": 0,
            "session_info": session_status
        }
        
        # 获取全部任务统计
        try:
            all_tasks_result = await dida_service.get_all_tasks()
            if all_tasks_result and 'error' not in all_tasks_result:
                tasks = all_tasks_result.get('syncTaskBean', {}).get('update', [])
                stats["all_tasks_count"] = len(tasks)
        except Exception as e:
            app_logger.warning(f"获取全部任务统计失败: {e}")
        
        # 获取已完成任务统计（只获取第一页用于统计）
        try:
            completed_result = await dida_service.get_completed_tasks(None, "Completed")
            if completed_result and 'error' not in completed_result:
                if isinstance(completed_result, list):
                    stats["completed_tasks_count"] = len(completed_result)
        except Exception as e:
            app_logger.warning(f"获取已完成任务统计失败: {e}")

        # 获取放弃任务统计
        try:
            abandoned_tasks_result = await dida_service.get_completed_tasks(None, "Abandoned")
            if abandoned_tasks_result and 'error' not in abandoned_tasks_result:
                if isinstance(abandoned_tasks_result, list):
                    stats["abandoned_tasks_count"] = len(abandoned_tasks_result)
        except Exception as e:
            app_logger.warning(f"获取放弃任务统计失败: {e}")

        # 获取垃圾桶任务统计
        try:
            trash_result = await dida_service.get_trash_tasks()
            if trash_result and 'error' not in trash_result:
                tasks = trash_result.get('tasks', [])
                stats["trash_tasks_count"] = len(tasks)
        except Exception as e:
            app_logger.warning(f"获取垃圾桶任务统计失败: {e}")
        
        app_logger.info(f"任务统计获取完成: {stats}")
        return stats
        
    except Exception as e:
        app_logger.error(f"获取任务导出信息时发生错误: {e}")
        return {
            "error": "server_error",
            "message": f"服务器内部错误: {str(e)}",
            "auth_status": False
        }


@router.get("/export/focus/excel",
           summary="导出专注记录到Excel",
           description="导出所有专注记录到Excel文件，包含完整的专注时间线数据")
async def export_focus_records_to_excel():
    """
    导出专注记录到Excel

    将用户的所有专注记录导出为Excel文件，包含：
    - **专注记录时间线**: 所有专注记录的详细信息

    每个工作表包含专注记录的完整字段信息，包括：
    - 基本信息：专注记录ID、开始时间、结束时间、创建时间
    - 专注状态：专注状态、专注时长、暂停时长、实际专注时长
    - 任务信息：任务ID、任务标题、项目ID、项目名称
    - 标签信息：标签列表、标签ID列表
    - 设备信息：设备类型、平台、应用版本
    - 专注模式：专注模式、番茄钟时长、休息时长
    - 其他属性：用户ID、时区、删除状态等

    **注意**:
    - 需要先调用认证接口设置会话
    - 会自动分页获取所有历史专注记录
    """
    try:
        app_logger.info("请求导出专注记录到Excel")

        # 检查认证状态
        session_status = dida_service.get_session_status()
        if not session_status["has_session"]:
            raise HTTPException(
                status_code=401,
                detail="未设置认证会话，请先完成登录"
            )

        # 调用导出服务
        result = await export_service.export_focus_records_to_excel()

        if 'error' in result:
            app_logger.error(f"导出专注记录失败: {result['error']}")
            raise HTTPException(
                status_code=500,
                detail=f"导出失败: {result['error']}"
            )

        app_logger.info(f"专注记录导出成功，文件大小: {result['size']} 字节")

        # 对文件名进行URL编码以支持中文
        encoded_filename = urllib.parse.quote(result['filename'], safe='')

        # 返回文件下载响应
        return StreamingResponse(
            io.BytesIO(result['content']),
            media_type=result['content_type'],
            headers={
                "Content-Disposition": f"attachment; filename*=UTF-8''{encoded_filename}"
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        app_logger.error(f"导出专注记录时发生未知错误: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"服务器内部错误: {str(e)}"
        )


@router.get("/export/focus/excel/info",
           summary="获取专注记录导出信息",
           description="获取当前用户专注记录的统计信息，用于导出前预览")
async def get_focus_export_info():
    """
    获取专注记录导出信息

    返回当前用户专注记录的统计信息，包括：
    - 专注记录总数量（预估）
    - 认证状态

    **注意**: 需要先调用认证接口设置会话
    """
    try:
        app_logger.info("请求获取专注记录导出信息")

        # 检查认证状态
        session_status = dida_service.get_session_status()
        if not session_status["has_session"]:
            return {
                "error": "no_auth_session",
                "message": "未设置认证会话，请先完成登录",
                "auth_status": False
            }

        # 获取专注记录统计（只获取第一页用于预估）
        stats = {
            "auth_status": True,
            "focus_records_count_estimate": 0,
            "session_info": session_status,
            "note": "专注记录数量为预估值，实际导出时会获取所有历史数据"
        }

        try:
            # 获取认证信息
            current_session = dida_service.current_session
            auth_token = current_session['auth_token']
            csrf_token = current_session['csrf_token']

            # 获取第一页专注记录用于预估
            from services.pomodoro_service import pomodoro_service
            result = await pomodoro_service.get_focus_timeline(auth_token, csrf_token, None)
            if result and 'error' not in result:
                if isinstance(result, list):
                    # 如果第一页有31条记录，预估可能有更多数据
                    first_page_count = len(result)
                    if first_page_count >= 31:
                        stats["focus_records_count_estimate"] = f"{first_page_count}+ (需要分页获取完整数据)"
                    else:
                        stats["focus_records_count_estimate"] = first_page_count
                else:
                    stats["focus_records_count_estimate"] = "无法预估"
        except Exception as e:
            app_logger.warning(f"获取专注记录统计失败: {e}")
            stats["focus_records_count_estimate"] = "获取失败"

        app_logger.info(f"专注记录统计获取完成: {stats}")
        return stats

    except Exception as e:
        app_logger.error(f"获取专注记录导出信息时发生错误: {e}")
        return {
            "error": "server_error",
            "message": f"服务器内部错误: {str(e)}",
            "auth_status": False
        }
