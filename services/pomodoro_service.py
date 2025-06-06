"""番茄专注服务模块"""
import httpx
from datetime import datetime, timezone, timedelta
from core import urls


class PomodoroService:
    """番茄专注服务类"""
    
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=30.0)
    
    def _build_auth_headers(self, auth_token: str, csrf_token: str) -> dict:
        """构建认证请求头"""
        return {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'X-Tz': 'Asia/Shanghai',
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
    
    async def close(self):
        """关闭HTTP客户端"""
        await self.client.aclose()


# 全局番茄专注服务实例
pomodoro_service = PomodoroService()
