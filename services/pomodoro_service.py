"""番茄专注服务模块"""
import time
import uuid
from dataclasses import dataclass, field
from threading import Lock
from typing import Any, Dict, List, Optional

import httpx
from datetime import datetime, timezone, timedelta
from core import urls, config
from models import FocusOperation, FocusOperationRequest
from utils import app_logger, generate_object_id


@dataclass
class FocusSessionState:
    """本地缓存的番茄钟会话状态"""

    last_point: int = 0
    focus_id: Optional[str] = None
    first_focus_id: Optional[str] = None
    duration: int = 25
    auto_pomo_left: int = 0
    pomo_count: int = 0
    manual: bool = True
    note: str = ""
    focus_on_id: str = ""
    focus_on_type: Optional[int] = None
    focus_on_title: Optional[str] = None
    status: Optional[int] = None
    raw_current: Dict[str, Any] = field(default_factory=dict)

    def reset_session(self) -> None:
        """清理当前番茄会话，但保留指针与历史信息"""
        self.focus_id = None
        self.first_focus_id = None
        self.focus_on_id = ""
        self.focus_on_type = None
        self.focus_on_title = None
        self.status = None
        self.raw_current = {}


class PomodoroService:
    """番茄专注服务类"""
    
    def __init__(self):
        self.request_config = config.get('request_config', {})
        timeout = self.request_config.get('timeout', 30.0)
        self.client = httpx.AsyncClient(timeout=timeout)
        self.web_domain = urls.DIDA_API_BASE.get("web_domain", "https://dida365.com")
        self._focus_state = FocusSessionState()
        self._state_lock = Lock()

    def _generate_trace_id(self) -> str:
        """生成TraceID"""
        timestamp_hex = f"{int(time.time() * 1000):x}"
        random_suffix = uuid.uuid4().hex[:8]
        return f"{timestamp_hex}{random_suffix}"
    
    def _build_auth_headers(self, auth_token: str, csrf_token: str) -> dict:
        """构建认证请求头"""
        user_agent = self.request_config.get(
            'user_agent',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        timezone_name = self.request_config.get('timezone', 'Asia/Shanghai')
        return {
            'User-Agent': user_agent,
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'X-Tz': timezone_name,
        }
    
    def _build_auth_cookies(self, auth_token: str, csrf_token: str) -> dict:
        """构建认证cookies"""
        return {
            't': auth_token,
            '_csrf_token': csrf_token
        }

    def _convert_time_to_timestamp(self, time_str: str) -> int:
        """
        将时间字符串转换为时间戳（毫秒）

        Args:
            time_str: 时间字符串，格式如 "2025-04-22T08:43:31.000+0000"

        Returns:
            int: 毫秒时间戳
        """
        try:
            # 解析时间字符串
            dt = datetime.fromisoformat(time_str.replace('Z', '+00:00'))

            # 转换为中国时间（UTC+8）
            china_tz = timezone(timedelta(hours=8))
            china_time = dt.astimezone(china_tz)

            # 转换为时间戳（秒）然后转为毫秒
            timestamp_ms = int(china_time.timestamp() * 1000)

            return timestamp_ms
        except Exception as e:
            raise ValueError(f"时间转换失败: {e}")
    
    async def get_general_for_desktop(self, auth_token: str, csrf_token: str) -> dict:
        """获取番茄专注概览（桌面版），直接返回原始响应"""
        try:
            url = urls.build_dida_api_url(urls.DIDA_POMODORO_APIS["general_for_desktop"])
            headers = self._build_auth_headers(auth_token, csrf_token)
            cookies = self._build_auth_cookies(auth_token, csrf_token)

            response = await self.client.get(url, headers=headers, cookies=cookies)

            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"HTTP {response.status_code}", "text": response.text}
        except Exception as e:
            return {"error": str(e)}

    def _build_focus_operation_headers(self, auth_token: str, csrf_token: str) -> dict:
        """构建番茄钟操作请求头"""
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/json',
            'Origin': self.web_domain,
            'Pragma': 'no-cache',
            'Referer': f"{self.web_domain}/",
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'Traceid': self._generate_trace_id(),
            'User-Agent': self.request_config.get(
                'user_agent',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            ),
            'X-Csrftoken': csrf_token,
            'X-Device': self.request_config.get('device_info', '{}'),
            'X-Requested-With': 'XMLHttpRequest',
            'X-Tz': self.request_config.get('timezone', 'Asia/Shanghai'),
            'Hl': self.request_config.get('language', 'zh_CN'),
            'Sec-Ch-Ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
        }
        return headers

    async def perform_focus_operations(self, auth_token: str, csrf_token: str, payload: dict) -> dict:
        """
        执行番茄钟操作（开始、暂停、继续、结束等），直接返回原始响应

        Args:
            auth_token: 认证令牌
            csrf_token: CSRF令牌
            payload: 操作请求体（需符合滴答清单接口格式）

        Returns:
            dict: 滴答清单接口的原始响应
        """
        try:
            url = urls.build_dida_ms_url(urls.DIDA_FOCUS_APIS["focus_batch_operation"])
            headers = self._build_focus_operation_headers(auth_token, csrf_token)
            cookies = self._build_auth_cookies(auth_token, csrf_token)

            response = await self.client.post(url, headers=headers, cookies=cookies, json=payload)

            if response.status_code == 200:
                return response.json()
            else:
                app_logger.error(f"番茄钟操作请求失败，状态码: {response.status_code}, 响应: {response.text}")
                return {"error": f"HTTP {response.status_code}", "text": response.text}
        except Exception as e:
            app_logger.error(f"番茄钟操作请求异常: {e}")
            return {"error": str(e)}

    # ================================
    # 高阶操作辅助函数
    # ================================

    def _current_utc_time_string(self) -> str:
        """生成符合滴答接口要求的 UTC 时间字符串"""
        now = datetime.utcnow()
        return now.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "+0000"

    def _build_request_payload(
        self,
        operations: List[FocusOperation],
        last_point: Optional[int] = None,
    ) -> dict:
        """构造番茄操作请求体"""
        with self._state_lock:
            point = self._focus_state.last_point if last_point is None else last_point
        request = FocusOperationRequest(lastPoint=point, opList=operations)
        return request.model_dump(by_alias=True)

    def _update_local_state(
        self,
        *,
        manual: Optional[bool] = None,
        duration: Optional[int] = None,
        auto_pomo_left: Optional[int] = None,
        pomo_count: Optional[int] = None,
        note: Optional[str] = None,
        focus_on_id: Optional[str] = None,
        focus_on_type: Optional[int] = None,
        focus_on_title: Optional[str] = None,
    ) -> None:
        """更新本地缓存的会话属性"""
        with self._state_lock:
            if manual is not None:
                self._focus_state.manual = manual
            if duration is not None:
                self._focus_state.duration = duration
            if auto_pomo_left is not None:
                self._focus_state.auto_pomo_left = auto_pomo_left
            if pomo_count is not None:
                self._focus_state.pomo_count = pomo_count
            if note is not None:
                self._focus_state.note = note
            if focus_on_id is not None:
                self._focus_state.focus_on_id = focus_on_id
            if focus_on_type is not None:
                self._focus_state.focus_on_type = focus_on_type
            if focus_on_title is not None:
                self._focus_state.focus_on_title = focus_on_title

    def _compose_operation(
        self,
        op: str,
        *,
        manual: Optional[bool] = None,
        duration: Optional[int] = None,
        auto_pomo_left: Optional[int] = None,
        pomo_count: Optional[int] = None,
        note: Optional[str] = None,
        focus_on_id: Optional[str] = None,
        time_str: Optional[str] = None,
    ) -> FocusOperation:
        """根据当前会话状态构造番茄操作项"""
        with self._state_lock:
            focus_id = self._focus_state.focus_id
            if not focus_id:
                raise ValueError("no_active_focus")

            first_focus_id = self._focus_state.first_focus_id or focus_id
            base_manual = self._focus_state.manual
            base_duration = self._focus_state.duration
            base_auto = self._focus_state.auto_pomo_left
            base_pomo = self._focus_state.pomo_count
            base_note = self._focus_state.note
            base_focus_on_id = self._focus_state.focus_on_id

        return FocusOperation(
            id=generate_object_id(),
            oId=focus_id,
            oType=0,
            op=op,
            duration=duration if duration is not None else base_duration,
            firstFocusId=first_focus_id,
            focusOnId=(focus_on_id if focus_on_id is not None else base_focus_on_id),
            focusOnType=self._focus_state.focus_on_type,
            focusOnTitle=self._focus_state.focus_on_title,
            autoPomoLeft=auto_pomo_left if auto_pomo_left is not None else base_auto,
            pomoCount=pomo_count if pomo_count is not None else base_pomo,
            manual=manual if manual is not None else base_manual,
            note=note if note is not None else base_note,
            time=time_str or self._current_utc_time_string(),
            createdTime=int(datetime.utcnow().timestamp() * 1000),
        )

    def _update_focus_state_from_response(self, response: Dict[str, Any]) -> None:
        """根据接口响应刷新本地会话状态"""
        if not isinstance(response, dict):
            return

        with self._state_lock:
            point = response.get("point")
            if isinstance(point, int):
                self._focus_state.last_point = point

            current = response.get("current")
            if isinstance(current, dict) and current:
                self._focus_state.raw_current = current
                status = current.get("status")
                if status is not None:
                    self._focus_state.status = status

                focus_id = current.get("id")
                if focus_id:
                    self._focus_state.focus_id = focus_id

                first_focus_id = (
                    current.get("firstId")
                    or current.get("firstID")
                    or current.get("firstFocusId")
                )
                if first_focus_id:
                    self._focus_state.first_focus_id = first_focus_id

                duration = current.get("duration")
                if isinstance(duration, int):
                    self._focus_state.duration = duration

                auto_pomo_left = current.get("autoPomoLeft")
                if isinstance(auto_pomo_left, int):
                    self._focus_state.auto_pomo_left = auto_pomo_left

                pomo_count = current.get("pomoCount")
                if isinstance(pomo_count, int):
                    self._focus_state.pomo_count = pomo_count

                note = current.get("note")
                if isinstance(note, str):
                    self._focus_state.note = note

                focus_on_logs = current.get("focusOnLogs")
                if isinstance(focus_on_logs, list) and focus_on_logs:
                    focus_on_id = focus_on_logs[-1].get("id") or ""
                    if focus_on_id is not None:
                        self._focus_state.focus_on_id = focus_on_id

                focus_tasks = current.get("focusTasks")
                if isinstance(focus_tasks, list) and focus_tasks:
                    last_task = focus_tasks[-1]
                    task_type = last_task.get("type")
                    if task_type is not None:
                        try:
                            self._focus_state.focus_on_type = int(task_type)
                        except (TypeError, ValueError):
                            self._focus_state.focus_on_type = None
                    title = last_task.get("title")
                    if title is not None:
                        self._focus_state.focus_on_title = title

                if current.get("exited") or current.get("status") in (2, 3):
                    self._focus_state.reset_session()

    def get_focus_state_snapshot(self) -> FocusSessionState:
        """获取当前会话状态副本"""
        with self._state_lock:
            return FocusSessionState(
                last_point=self._focus_state.last_point,
                focus_id=self._focus_state.focus_id,
                first_focus_id=self._focus_state.first_focus_id,
                duration=self._focus_state.duration,
                auto_pomo_left=self._focus_state.auto_pomo_left,
                pomo_count=self._focus_state.pomo_count,
                manual=self._focus_state.manual,
                note=self._focus_state.note,
                focus_on_id=self._focus_state.focus_on_id,
                focus_on_type=self._focus_state.focus_on_type,
                focus_on_title=self._focus_state.focus_on_title,
                status=self._focus_state.status,
                raw_current=dict(self._focus_state.raw_current),
            )

    def set_last_point(self, point: int) -> None:
        """手动设置同步指针"""
        with self._state_lock:
            self._focus_state.last_point = max(0, int(point))

    def reset_focus_session(self) -> None:
        """手动重置番茄会话缓存"""
        with self._state_lock:
            current_point = self._focus_state.last_point
            self._focus_state = FocusSessionState(last_point=current_point)

    # ================================
    # 高阶番茄钟操作
    # ================================

    async def start_focus(
        self,
        auth_token: str,
        csrf_token: str,
        *,
        duration: int = 25,
        auto_pomo_left: int = 5,
        pomo_count: int = 1,
        manual: bool = True,
        note: str = "",
        focus_on_id: str = "",
        focus_on_type: Optional[int] = None,
        focus_on_title: Optional[str] = None,
        last_point: Optional[int] = None,
    ) -> Dict[str, Any]:
        """启动番茄钟"""
        focus_id = generate_object_id()
        operation_id = generate_object_id()
        time_str = self._current_utc_time_string()

        with self._state_lock:
            self._focus_state.focus_id = focus_id
            self._focus_state.first_focus_id = focus_id
            self._focus_state.duration = duration
            self._focus_state.auto_pomo_left = auto_pomo_left
            self._focus_state.pomo_count = pomo_count
            self._focus_state.manual = manual
            self._focus_state.note = note or ""
            self._focus_state.focus_on_id = focus_on_id or ""
            self._focus_state.focus_on_type = focus_on_type
            self._focus_state.focus_on_title = focus_on_title

        app_logger.debug(
            "[focus_start] focusId={} firstFocusId={} duration={} autoPomoLeft={} pomoCount={} focusOnId={} focusOnType={} focusOnTitle={}",
            focus_id,
            focus_id,
            duration,
            auto_pomo_left,
            pomo_count,
            focus_on_id,
            focus_on_type,
            focus_on_title,
        )

        operation = FocusOperation(
            id=operation_id,
            oId=focus_id,
            oType=0,
            op="start",
            duration=duration,
            firstFocusId=focus_id,
            focusOnId=focus_on_id or "",
            focusOnType=focus_on_type,
            focusOnTitle=focus_on_title,
            autoPomoLeft=auto_pomo_left,
            pomoCount=pomo_count,
            manual=manual,
            note=note or "",
            time=time_str,
            createdTime=int(datetime.utcnow().timestamp() * 1000),
        )

        payload = self._build_request_payload([operation], last_point)
        app_logger.debug("[focus_start] 请求 payload: {}", payload)
        result = await self.perform_focus_operations(auth_token, csrf_token, payload)
        self._update_focus_state_from_response(result)
        return result

    async def finish_focus(
        self,
        auth_token: str,
        csrf_token: str,
        *,
        manual: Optional[bool] = None,
        note: Optional[str] = None,
        focus_on_type: Optional[int] = None,
        focus_on_title: Optional[str] = None,
        last_point: Optional[int] = None,
    ) -> Dict[str, Any]:
        """完成番茄钟（finish 操作）"""
        if not await self._ensure_focus_context(auth_token, csrf_token, last_point):
            return {"error": "no_active_focus", "message": "当前没有正在运行的番茄钟"}

        try:
            operation = self._compose_operation("finish", manual=manual, note=note)
        except ValueError:
            return {"error": "no_active_focus", "message": "当前没有正在运行的番茄钟"}

        self._update_local_state(
            manual=manual,
            note=note,
            focus_on_type=focus_on_type,
            focus_on_title=focus_on_title,
        )

        payload = self._build_request_payload([operation], last_point)
        app_logger.debug("[focus_finish] 请求 payload: {}", payload)
        result = await self.perform_focus_operations(auth_token, csrf_token, payload)
        self._update_focus_state_from_response(result)
        return result

    async def pause_focus(
        self,
        auth_token: str,
        csrf_token: str,
        *,
        manual: Optional[bool] = None,
        note: Optional[str] = None,
        focus_on_type: Optional[int] = None,
        focus_on_title: Optional[str] = None,
        last_point: Optional[int] = None,
    ) -> Dict[str, Any]:
        """暂停当前番茄钟"""
        if not await self._ensure_focus_context(auth_token, csrf_token, last_point):
            return {"error": "no_active_focus", "message": "当前没有正在运行的番茄钟"}

        try:
            operation = self._compose_operation("pause", manual=manual, note=note)
        except ValueError:
            return {"error": "no_active_focus", "message": "当前没有正在运行的番茄钟"}

        self._update_local_state(
            manual=manual,
            note=note,
            focus_on_type=focus_on_type,
            focus_on_title=focus_on_title,
        )
        payload = self._build_request_payload([operation], last_point)
        app_logger.debug("[focus_pause] 请求 payload: {}", payload)
        result = await self.perform_focus_operations(auth_token, csrf_token, payload)
        self._update_focus_state_from_response(result)
        return result

    async def continue_focus(
        self,
        auth_token: str,
        csrf_token: str,
        *,
        manual: Optional[bool] = None,
        note: Optional[str] = None,
        focus_on_type: Optional[int] = None,
        focus_on_title: Optional[str] = None,
        last_point: Optional[int] = None,
    ) -> Dict[str, Any]:
        """继续已暂停的番茄钟"""
        if not await self._ensure_focus_context(auth_token, csrf_token, last_point):
            return {"error": "no_active_focus", "message": "当前没有可继续的番茄钟"}

        try:
            operation = self._compose_operation("continue", manual=manual, note=note)
        except ValueError:
            return {"error": "no_active_focus", "message": "当前没有可继续的番茄钟"}

        self._update_local_state(
            manual=manual,
            note=note,
            focus_on_type=focus_on_type,
            focus_on_title=focus_on_title,
        )
        payload = self._build_request_payload([operation], last_point)
        app_logger.debug("[focus_continue] 请求 payload: {}", payload)
        result = await self.perform_focus_operations(auth_token, csrf_token, payload)
        self._update_focus_state_from_response(result)
        return result

    async def stop_focus(
        self,
        auth_token: str,
        csrf_token: str,
        *,
        manual: Optional[bool] = None,
        note: Optional[str] = None,
        focus_on_type: Optional[int] = None,
        focus_on_title: Optional[str] = None,
        last_point: Optional[int] = None,
        include_exit: bool = True,
    ) -> Dict[str, Any]:
        """
        终止番茄钟（默认发送 drop + exit）

        Args:
            include_exit: 是否在 drop 之后追加 exit 操作
        """
        if not await self._ensure_focus_context(auth_token, csrf_token, last_point):
            return {"error": "no_active_focus", "message": "当前没有正在运行的番茄钟"}

        try:
            drop_operation = self._compose_operation(
                "drop",
                manual=manual,
                note=note,
                duration=0,
            )
        except ValueError:
            return {"error": "no_active_focus", "message": "当前没有正在运行的番茄钟"}

        operations: List[FocusOperation] = [drop_operation]

        if include_exit:
            try:
                exit_operation = self._compose_operation(
                    "exit",
                    manual=manual,
                    note=note,
                    duration=0,
                    auto_pomo_left=0,
                    pomo_count=0,
                )
                operations.append(exit_operation)
            except ValueError:
                # 如果 drop 之后状态已经清空，这里忽略
                pass

        payload = self._build_request_payload(operations, last_point)
        app_logger.debug("[focus_stop] 请求 payload: {}", payload)
        result = await self.perform_focus_operations(auth_token, csrf_token, payload)
        self._update_focus_state_from_response(result)
        return result
    
    async def get_focus_distribution(self, auth_token: str, csrf_token: str,
                                   start_date: str, end_date: str) -> dict:
        """获取专注详情分布，直接返回原始响应"""
        try:
            endpoint = f"{urls.DIDA_POMODORO_APIS['focus_distribution']}/{start_date}/{end_date}"
            url = urls.build_dida_api_url(endpoint)
            headers = self._build_auth_headers(auth_token, csrf_token)
            cookies = self._build_auth_cookies(auth_token, csrf_token)

            response = await self.client.get(url, headers=headers, cookies=cookies)

            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"HTTP {response.status_code}", "text": response.text}
        except Exception as e:
            return {"error": str(e)}
    
    async def get_focus_timeline(self, auth_token: str, csrf_token: str, to_timestamp: int = None) -> dict:
        """
        获取专注记录时间线，支持分页

        Args:
            auth_token: 认证令牌
            csrf_token: CSRF令牌
            to_timestamp: 可选的时间戳参数，用于分页获取更早的数据

        Returns:
            dict: 原始API响应
        """
        try:
            url = urls.build_dida_api_url(urls.DIDA_POMODORO_APIS["focus_timeline"])

            # 如果提供了时间戳参数，添加到URL中
            if to_timestamp is not None:
                url = f"{url}?to={to_timestamp}"

            headers = self._build_auth_headers(auth_token, csrf_token)
            cookies = self._build_auth_cookies(auth_token, csrf_token)

            response = await self.client.get(url, headers=headers, cookies=cookies)

            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"HTTP {response.status_code}", "text": response.text}
        except Exception as e:
            return {"error": str(e)}

    async def get_focus_heatmap(self, auth_token: str, csrf_token: str,
                               start_date: str, end_date: str) -> dict:
        """获取专注趋势热力图，直接返回原始响应"""
        try:
            endpoint = f"{urls.DIDA_POMODORO_APIS['focus_heatmap']}/{start_date}/{end_date}"
            url = urls.build_dida_api_url(endpoint)
            headers = self._build_auth_headers(auth_token, csrf_token)
            cookies = self._build_auth_cookies(auth_token, csrf_token)

            response = await self.client.get(url, headers=headers, cookies=cookies)

            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"HTTP {response.status_code}", "text": response.text}
        except Exception as e:
            return {"error": str(e)}

    async def get_focus_time_distribution(self, auth_token: str, csrf_token: str,
                                         start_date: str, end_date: str) -> dict:
        """获取专注时间分布（按时间段），直接返回原始响应"""
        try:
            endpoint = f"{urls.DIDA_POMODORO_APIS['focus_time_distribution']}/{start_date}/{end_date}"
            url = urls.build_dida_api_url(endpoint)
            headers = self._build_auth_headers(auth_token, csrf_token)
            cookies = self._build_auth_cookies(auth_token, csrf_token)

            response = await self.client.get(url, headers=headers, cookies=cookies)

            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"HTTP {response.status_code}", "text": response.text}
        except Exception as e:
            return {"error": str(e)}

    async def get_focus_hour_distribution(self, auth_token: str, csrf_token: str,
                                         start_date: str, end_date: str) -> dict:
        """获取专注时间按小时分布，直接返回原始响应"""
        try:
            endpoint = f"{urls.DIDA_POMODORO_APIS['focus_hour_distribution']}/{start_date}/{end_date}"
            url = urls.build_dida_api_url(endpoint)
            headers = self._build_auth_headers(auth_token, csrf_token)
            cookies = self._build_auth_cookies(auth_token, csrf_token)

            response = await self.client.get(url, headers=headers, cookies=cookies)

            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"HTTP {response.status_code}", "text": response.text}
        except Exception as e:
            return {"error": str(e)}
    
    async def query_focus_state(
        self,
        auth_token: str,
        csrf_token: str,
        *,
        last_point: Optional[int] = None,
    ) -> Dict[str, Any]:
        """查询当前番茄状态（不发送操作，仅同步最新信息）"""
        payload = self._build_request_payload([], last_point)
        app_logger.debug(f"[focus_current] 请求 payload: {payload}")
        result = await self.perform_focus_operations(auth_token, csrf_token, payload)
        self._update_focus_state_from_response(result)
        return result

    async def _ensure_focus_context(
        self,
        auth_token: str,
        csrf_token: str,
        last_point: Optional[int] = None,
    ) -> bool:
        """确保本地缓存中存在当前番茄会话信息，无则主动同步"""
        with self._state_lock:
            if self._focus_state.focus_id:
                return True

        app_logger.debug("[ensure_context] 缓存缺失，尝试同步当前番茄状态")
        await self.query_focus_state(auth_token, csrf_token, last_point=last_point)

        with self._state_lock:
            if self._focus_state.focus_id:
                app_logger.debug("[ensure_context] 同步成功，focusId={}", self._focus_state.focus_id)
            else:
                app_logger.warning("[ensure_context] 同步失败，仍未获取到 focusId")
            return self._focus_state.focus_id is not None
    
    async def close(self):
        """关闭HTTP客户端"""
        await self.client.aclose()


# 全局番茄专注服务实例
pomodoro_service = PomodoroService()
