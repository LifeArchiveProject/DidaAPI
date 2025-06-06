"""习惯管理服务模块"""
import httpx
from typing import Optional
from utils import app_logger
from core import urls
# 不再使用响应模型，直接返回原始响应


class HabitService:
    """习惯管理服务类"""
    
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
    
    async def get_habits(self, auth_token: str, csrf_token: str) -> dict:
        """
        获取习惯列表

        Args:
            auth_token: 认证令牌
            csrf_token: CSRF令牌

        Returns:
            dict: 原始响应数据
        """
        try:
            url = urls.build_dida_api_url(urls.DIDA_HABIT_APIS["get_habits"])
            
            headers = self._build_auth_headers(auth_token, csrf_token)
            cookies = self._build_auth_cookies(auth_token, csrf_token)
            
            app_logger.info(f"请求获取习惯列表: {url}")
            
            response = await self.client.get(url, headers=headers, cookies=cookies)
            
            if response.status_code == 200:
                response_data = response.json()
                app_logger.info(f"成功获取习惯列表，习惯数: {len(response_data) if isinstance(response_data, list) else 0}")

                # 直接返回原始响应
                return response_data
            else:
                app_logger.error(f"获取习惯列表失败，状态码: {response.status_code}")
                return {"error": f"HTTP {response.status_code}", "text": response.text}
                
        except Exception as e:
            app_logger.error(f"获取习惯列表时发生错误: {e}")
            return {"error": str(e)}
    
    async def get_week_current_statistics(self, auth_token: str, csrf_token: str) -> dict:
        """
        获取本周习惯打卡统计

        Args:
            auth_token: 认证令牌
            csrf_token: CSRF令牌

        Returns:
            dict: 原始响应数据
        """
        try:
            url = urls.build_dida_api_url(urls.DIDA_HABIT_APIS["week_current_statistics"])

            headers = self._build_auth_headers(auth_token, csrf_token)
            cookies = self._build_auth_cookies(auth_token, csrf_token)

            app_logger.info(f"请求获取本周习惯打卡统计: {url}")

            response = await self.client.get(url, headers=headers, cookies=cookies)

            if response.status_code == 200:
                response_data = response.json()
                app_logger.info("成功获取本周习惯打卡统计")

                # 直接返回原始响应
                return response_data
            else:
                app_logger.error(f"获取本周习惯打卡统计失败，状态码: {response.status_code}")
                return {"error": f"HTTP {response.status_code}", "text": response.text}

        except Exception as e:
            app_logger.error(f"获取本周习惯打卡统计时发生错误: {e}")
            return {"error": str(e)}

    async def export_habits(self, auth_token: str, csrf_token: str) -> dict:
        """
        导出习惯数据（Excel格式）

        Args:
            auth_token: 认证令牌
            csrf_token: CSRF令牌

        Returns:
            dict: 包含文件内容和元数据的响应
        """
        try:
            url = urls.build_dida_api_url(urls.DIDA_HABIT_APIS["export_habits"])

            # 对于文件下载，需要修改Accept头
            headers = self._build_auth_headers(auth_token, csrf_token)
            headers['Accept'] = '*/*'
            headers['X-CSRFToken'] = csrf_token

            cookies = self._build_auth_cookies(auth_token, csrf_token)

            app_logger.info(f"请求导出习惯数据: {url}")

            response = await self.client.get(url, headers=headers, cookies=cookies)

            if response.status_code == 200:
                # 获取文件名
                content_disposition = response.headers.get('content-disposition', '')
                filename = 'habits_export.xlsx'
                if 'filename=' in content_disposition:
                    filename = content_disposition.split('filename=')[1].split(';')[0].strip('"')

                app_logger.info(f"成功导出习惯数据，文件名: {filename}")

                # 返回文件内容和元数据
                return {
                    "filename": filename,
                    "content_type": response.headers.get('content-type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                    "content": response.content,
                    "size": len(response.content)
                }
            else:
                app_logger.error(f"导出习惯数据失败，状态码: {response.status_code}")
                return {"error": f"HTTP {response.status_code}", "text": response.text}

        except Exception as e:
            app_logger.error(f"导出习惯数据时发生错误: {e}")
            return {"error": str(e)}
    
    async def close(self):
        """关闭HTTP客户端"""
        await self.client.aclose()


# 全局习惯服务实例
habit_service = HabitService()
