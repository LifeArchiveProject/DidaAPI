"""项目管理服务模块"""
import httpx
from typing import Optional
from utils import app_logger
from core import urls
# 不再使用响应模型，直接返回原始响应


class ProjectService:
    """项目管理服务类"""
    
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def get_projects(self, auth_token: str, csrf_token: str) -> dict:
        """
        获取项目/清单列表

        Args:
            auth_token: 认证令牌
            csrf_token: CSRF令牌

        Returns:
            dict: 原始响应数据
        """
        try:
            # 构建请求URL
            url = urls.build_dida_api_url(urls.DIDA_PROJECT_APIS["get_projects"])
            
            # 构建请求头
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',
                'X-Tz': 'Asia/Shanghai',
            }
            
            # 构建cookies
            cookies = {
                't': auth_token,
                '_csrf_token': csrf_token
            }
            
            app_logger.info(f"请求获取项目列表: {url}")
            
            # 发送请求
            response = await self.client.get(url, headers=headers, cookies=cookies)
            
            if response.status_code == 200:
                response_data = response.json()
                app_logger.info(f"成功获取项目列表，项目数: {len(response_data) if isinstance(response_data, list) else 0}")

                # 直接返回原始响应
                return response_data
            else:
                app_logger.error(f"获取项目列表失败，状态码: {response.status_code}")
                return {"error": f"HTTP {response.status_code}", "text": response.text}
                
        except Exception as e:
            app_logger.error(f"获取项目列表时发生错误: {e}")
            return {"error": str(e)}

    async def close(self):
        """关闭HTTP客户端"""
        await self.client.aclose()


# 全局项目服务实例
project_service = ProjectService()
