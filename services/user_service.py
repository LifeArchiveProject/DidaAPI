"""用户信息服务模块"""
import httpx
from core import urls
from utils import app_logger


class UserService:
    """用户信息服务类"""
    
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=30.0)
    
    def _build_auth_headers(self, auth_token: str, csrf_token: str) -> dict:
        """构建认证headers"""
        return {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Content-Type': 'application/json;charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'x-csrftoken': csrf_token,
            'Referer': 'https://dida365.com/',
            'Origin': 'https://dida365.com'
        }
    
    def _build_auth_cookies(self, auth_token: str, csrf_token: str) -> dict:
        """构建认证cookies"""
        return {
            't': auth_token,
            '_csrf_token': csrf_token
        }
    
    async def get_user_profile(self, auth_token: str, csrf_token: str) -> dict:
        """
        获取用户信息，直接返回原始响应
        
        Args:
            auth_token: 认证令牌
            csrf_token: CSRF令牌
            
        Returns:
            dict: 原始API响应
        """
        try:
            url = urls.build_dida_api_url(urls.DIDA_AUTH_APIS["user_profile"])
            headers = self._build_auth_headers(auth_token, csrf_token)
            cookies = self._build_auth_cookies(auth_token, csrf_token)
            
            app_logger.info(f"请求获取用户信息: {url}")
            
            response = await self.client.get(url, headers=headers, cookies=cookies)
            
            if response.status_code == 200:
                response_data = response.json()
                app_logger.info(f"成功获取用户信息，用户名: {response_data.get('username', 'N/A')}")
                
                # 直接返回原始响应
                return response_data
            else:
                app_logger.error(f"获取用户信息失败，状态码: {response.status_code}")
                return {"error": f"HTTP {response.status_code}", "text": response.text}
                
        except Exception as e:
            app_logger.error(f"获取用户信息时发生错误: {e}")
            return {"error": str(e)}
    
    async def close(self):
        """关闭HTTP客户端"""
        await self.client.aclose()


# 全局用户服务实例
user_service = UserService()
