"""统计服务模块"""
import httpx
from utils import app_logger
from core import urls


class StatisticsService:
    """统计服务类"""
    
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
    
    async def get_user_ranking(self, auth_token: str, csrf_token: str) -> dict:
        """获取用户排名统计，直接返回原始响应"""
        try:
            url = urls.build_dida_api_url(urls.DIDA_STATISTICS_APIS["user_ranking"]).replace('/v2/', '/v3/')
            headers = self._build_auth_headers(auth_token, csrf_token)
            cookies = self._build_auth_cookies(auth_token, csrf_token)
            
            response = await self.client.get(url, headers=headers, cookies=cookies)
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"HTTP {response.status_code}", "text": response.text}
        except Exception as e:
            return {"error": str(e)}
    
    async def get_general_statistics(self, auth_token: str, csrf_token: str) -> dict:
        """获取通用统计信息，直接返回原始响应"""
        try:
            url = urls.build_dida_api_url(urls.DIDA_STATISTICS_APIS["general_statistics"])
            headers = self._build_auth_headers(auth_token, csrf_token)
            cookies = self._build_auth_cookies(auth_token, csrf_token)
            
            response = await self.client.get(url, headers=headers, cookies=cookies)
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"HTTP {response.status_code}", "text": response.text}
        except Exception as e:
            return {"error": str(e)}
    
    async def get_task_statistics(self, auth_token: str, csrf_token: str, 
                                start_date: str, end_date: str) -> dict:
        """获取任务统计信息，直接返回原始响应"""
        try:
            endpoint = f"{urls.DIDA_STATISTICS_APIS['task_statistics']}/{start_date}/{end_date}"
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


# 全局统计服务实例
statistics_service = StatisticsService()
