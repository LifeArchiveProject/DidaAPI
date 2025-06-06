"""任务相关API路由"""
from fastapi import APIRouter, HTTPException, Query, Body
from typing import Optional
from models import ApiResponse
from services import dida_service
from utils import app_logger

router = APIRouter(prefix="/tasks", tags=["任务管理"])


@router.post("/set-auth",
            response_model=ApiResponse,
            summary="设置认证会话",
            description="设置滴答清单API的认证令牌，用于后续API调用")
async def set_auth_session(
    auth_token: str = Body(..., description="认证令牌（t cookie值）"),
    csrf_token: str = Body(..., description="CSRF令牌")
) -> ApiResponse:
    """
    设置认证会话
    
    - **auth_token**: 认证令牌（从微信登录获得的 t cookie值）
    - **csrf_token**: CSRF令牌（从微信登录获得的 _csrf_token值）
    
    设置后可以调用其他需要认证的API接口
    """
    try:
        app_logger.info("设置认证会话")
        
        if not auth_token or not csrf_token:
            raise HTTPException(
                status_code=400,
                detail="认证令牌和CSRF令牌不能为空"
            )
        
        session_id = dida_service.set_auth_session(auth_token, csrf_token)
        
        return ApiResponse(
            code=200,
            message="认证会话设置成功",
            data={
                "session_id": session_id,
                "status": "已设置认证会话，可以调用其他API"
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        app_logger.error(f"设置认证会话时发生错误: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"设置认证会话失败: {str(e)}"
        )


@router.get("/all",
           summary="获取所有任务",
           description="获取当前用户的所有任务列表")
async def get_all_tasks():
    """
    获取所有任务
    
    返回当前用户的所有任务列表，包括：
    - 任务ID、标题、内容
    - 任务状态（0=未完成，2=已完成）
    - 优先级、创建时间、修改时间
    - 项目ID、标签等信息
    
    **注意**: 需要先调用 `/tasks/set-auth` 设置认证会话
    """
    try:
        app_logger.info("请求获取所有任务")
        
        result = await dida_service.get_all_tasks()

        if not result:
            return {"error": "获取任务失败，请稍后重试"}

        # 记录日志
        if 'error' in result:
            app_logger.info(f"获取任务失败: {result.get('error')}")
        else:
            app_logger.info(f"任务获取完成")

        # 直接返回原始响应
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        app_logger.error(f"获取任务时发生未知错误: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"服务器内部错误: {str(e)}"
        )


@router.get("/summary",
           response_model=ApiResponse,
           summary="获取任务统计",
           description="获取任务的统计信息")
async def get_tasks_summary() -> ApiResponse:
    """
    获取任务统计
    
    返回任务的统计信息：
    - 总任务数
    - 已完成任务数
    - 未完成任务数
    - 完成率等
    """
    try:
        app_logger.info("请求获取任务统计")
        
        result = await dida_service.get_all_tasks()

        if not result or "error" in result:
            return {"error": "获取任务统计失败", "details": result}

        # 统计任务信息 - 从原始响应中提取
        total_tasks = 0
        completed_tasks = 0
        pending_tasks = 0

        # 解析原始响应数据
        if isinstance(result, dict) and 'syncTaskBean' in result:
            task_data = result['syncTaskBean']
            if 'update' in task_data:
                raw_tasks = task_data['update']
                total_tasks = len(raw_tasks)

                for task in raw_tasks:
                    if task.get('status') == 2:  # 已完成
                        completed_tasks += 1
                    else:  # 未完成
                        pending_tasks += 1

        completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
        return ApiResponse(
            code=200,
            message="获取任务统计成功",
            data={
                "total_tasks": total_tasks,
                "completed_tasks": completed_tasks,
                "pending_tasks": pending_tasks,
                "completion_rate": round(completion_rate, 2)
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        app_logger.error(f"获取任务统计时发生错误: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"服务器内部错误: {str(e)}"
        )


@router.get("/completed",
           summary="获取已完成/已放弃任务",
           description="获取已完成或已放弃的任务列表，支持分页获取")
async def get_completed_tasks(
    to: Optional[str] = Query(None, description="分页参数，使用上次响应最后一个任务的completedTime字段，格式：2025-03-15T13:30:54.000+0000"),
    status: str = Query("Completed", description="任务状态：Completed(已完成) 或 Abandoned(已放弃)")
):
    """
    获取已完成/已放弃任务

    支持分页获取已完成或已放弃的任务列表：
    - **第一次请求**: 不传to参数，获取最新的任务
    - **后续请求**: 使用上次响应最后一个任务的completedTime字段作为to参数
    - **状态选择**: 通过status参数选择获取已完成(Completed)或已放弃(Abandoned)的任务

    **分页机制说明**:
    1. completedTime原始格式：2025-03-15T13:30:54.000+0000
    2. to参数传入：使用completedTime的原始格式
    3. API内部转换：2025-03-15T13:30:54.000+0000 → 2025-03-15 13:30:54
    4. URL示例：https://api.dida365.com/api/v2/project/all/closed?from=&to=2025-03-15%2013:30:54&status=Completed

    **状态参数说明**:
    - Completed: 获取已完成的任务
    - Abandoned: 获取已放弃的任务

    **注意**: 需要先完成微信登录获取认证会话
    """
    try:
        app_logger.info(f"请求获取任务，状态: {status}，分页参数: {to}")

        # 检查认证状态
        session_status = dida_service.get_session_status()
        if not session_status["has_session"]:
            return {"error": "no_auth_session", "message": "未设置认证会话，请先完成微信登录"}

        # 调用服务获取任务
        result = await dida_service.get_completed_tasks(to, status)

        if not result:
            return {"error": "service_error", "message": f"获取{status}任务失败，请稍后重试"}

        # 记录日志
        if 'error' in result:
            app_logger.info(f"{status}任务获取失败: {result.get('error')}")
        else:
            task_count = len(result) if isinstance(result, list) else 0
            app_logger.info(f"{status}任务获取完成，任务数: {task_count}")

            # 如果有任务，记录最后一个任务的completedTime，便于下次分页
            if isinstance(result, list) and len(result) > 0:
                last_task = result[-1]
                last_completed_time = last_task.get('completedTime')
                if last_completed_time:
                    app_logger.info(f"最后一个任务的completedTime: {last_completed_time}")

        # 直接返回原始响应
        return result

    except Exception as e:
        app_logger.error(f"获取{status}任务时发生未知错误: {e}")
        return {"error": "server_error", "message": f"服务器内部错误: {str(e)}"}


@router.get("/trash",
           summary="获取垃圾桶任务",
           description="获取垃圾桶中的任务列表")
async def get_trash_tasks(
    limit: int = Query(50, description="每页任务数量，默认50"),
    task_type: int = Query(1, description="任务类型，默认1")
):
    """
    获取垃圾桶任务

    获取垃圾桶中的任务列表：
    - **limit**: 每页返回的任务数量，默认50
    - **task_type**: 任务类型，默认1

    **响应格式**:
    ```json
    {
        "tasks": [...],  // 任务列表
        "next": 0        // 下一页标识
    }
    ```

    **注意**: 需要先完成微信登录获取认证会话
    """
    try:
        app_logger.info(f"请求获取垃圾桶任务，limit: {limit}, type: {task_type}")

        # 检查认证状态
        session_status = dida_service.get_session_status()
        if not session_status["has_session"]:
            return {"error": "no_auth_session", "message": "未设置认证会话，请先完成微信登录"}

        # 调用服务获取垃圾桶任务
        result = await dida_service.get_trash_tasks(limit, task_type)

        if not result:
            return {"error": "service_error", "message": "获取垃圾桶任务失败，请稍后重试"}

        # 记录日志
        if 'error' in result:
            app_logger.info(f"垃圾桶任务获取失败: {result.get('error')}")
        else:
            task_count = len(result.get('tasks', [])) if isinstance(result, dict) else 0
            next_page = result.get('next', 0) if isinstance(result, dict) else 0
            app_logger.info(f"垃圾桶任务获取完成，任务数: {task_count}, next: {next_page}")

        # 直接返回原始响应
        return result

    except Exception as e:
        app_logger.error(f"获取垃圾桶任务时发生未知错误: {e}")
        return {"error": "server_error", "message": f"服务器内部错误: {str(e)}"}
