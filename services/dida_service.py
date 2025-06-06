"""滴答清单API服务模块"""
import uuid
import time
from typing import Optional, Dict, Any, List
import httpx
from utils import app_logger
from core import config, db, urls
from models import TasksResponse, TaskItem


class DidaAPIService:
    """滴答清单API服务类"""
    
    def __init__(self):
        self.request_config = config.get('request_config', {})
        self.client = httpx.AsyncClient(timeout=self.request_config.get('timeout', 30.0))
        
        # 从数据库获取当前活跃的认证会话
        self.current_session = None
        self._load_active_session()
    
    def _load_active_session(self):
        """从数据库加载活跃的认证会话"""
        try:
            # 从数据库获取最新的活跃会话
            session_data = db.get_latest_active_session()
            if session_data:
                self.current_session = {
                    'session_id': session_data['session_id'],
                    'auth_token': session_data['token'],
                    'csrf_token': session_data['csrf_token'],
                    'is_active': session_data['is_active']
                }
                app_logger.info(f"已从数据库恢复认证会话: {session_data['session_id']}")
            else:
                app_logger.info("数据库中没有找到活跃的认证会话")
        except Exception as e:
            app_logger.error(f"加载认证会话失败: {e}")
    
    def set_auth_session(self, auth_token: str, csrf_token: str) -> str:
        """设置认证会话"""
        session_id = str(uuid.uuid4())
        self.current_session = {
            'session_id': session_id,
            'auth_token': auth_token,
            'csrf_token': csrf_token,
            'is_active': True
        }
        
        # 保存到数据库
        db.save_user_session({
            'session_id': session_id,
            'token': auth_token,
            'csrf_token': csrf_token,
            'is_active': True
        })
        
        app_logger.info(f"设置认证会话成功: {session_id}")
        return session_id

    def get_session_status(self) -> Dict[str, Any]:
        """获取当前会话状态"""
        if self.current_session:
            return {
                "has_session": True,
                "session_id": self.current_session.get('session_id'),
                "is_active": self.current_session.get('is_active', False)
            }
        else:
            return {
                "has_session": False,
                "session_id": None,
                "is_active": False
            }
    
    def _get_auth_headers(self) -> Dict[str, str]:
        """获取认证请求头"""
        if not self.current_session:
            raise ValueError("未设置认证会话，请先登录")
        
        # 生成traceid
        traceid = f"{int(time.time() * 1000):x}{uuid.uuid4().hex[:8]}"
        
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
            'Cache-Control': 'no-cache',
            'Origin': 'https://dida365.com',
            'Pragma': 'no-cache',
            'Referer': 'https://dida365.com/',
            'Sec-Ch-Ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': self.request_config.get('user_agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'),
            'X-Csrftoken': self.current_session['csrf_token'],
            'X-Device': self.request_config.get('device_info', '{}'),
            'Hl': self.request_config.get('language', 'zh_CN'),
            'X-Tz': self.request_config.get('timezone', 'Asia/Shanghai'),
            'Traceid': traceid
        }
        
        return headers
    
    def _get_auth_cookies(self) -> Dict[str, str]:
        """获取认证cookies"""
        if not self.current_session:
            raise ValueError("未设置认证会话，请先登录")
        
        cookies = {
            't': self.current_session['auth_token'],
            '_csrf_token': self.current_session['csrf_token']
        }
        
        return cookies

    async def get_all_tasks(self) -> dict:
        """
        获取所有任务

        Returns:
            dict: 原始响应数据
        """
        try:
            if not self.current_session:
                return {"error": "no_auth_session", "message": "未设置认证会话，请先登录"}

            # 使用统一的URL构建函数
            url = urls.build_dida_api_url(urls.DIDA_TASK_APIS["get_all_tasks"])

            # 获取认证头和cookies
            headers = self._get_auth_headers()
            cookies = self._get_auth_cookies()

            app_logger.info(f"请求获取所有任务: {url}")
            app_logger.debug(f"请求头: {headers}")

            # 发送请求
            response = await self.client.get(url, headers=headers, cookies=cookies)

            # 记录响应信息
            app_logger.info(f"任务响应状态码: {response.status_code}")
            app_logger.debug(f"任务响应头: {dict(response.headers)}")

            if response.status_code == 200:
                # 解析响应数据
                response_data = response.json()
                app_logger.info(f"成功获取任务数据，响应长度: {len(str(response_data))}")
                app_logger.debug(f"任务响应数据: {response_data}")

                # 直接返回原始响应
                return response_data

            else:
                app_logger.error(f"获取任务失败，状态码: {response.status_code}")
                return {"error": f"HTTP {response.status_code}", "text": response.text}

        except Exception as e:
            app_logger.error(f"获取任务时发生错误: {e}")
            return {"error": str(e)}

    async def get_completed_tasks(self, to: Optional[str] = None, status: str = "Completed") -> dict:
        """
        获取已完成或已放弃的任务（支持分页）

        Args:
            to: 分页参数，使用上次响应最后一个任务的completedTime字段
                如果为None，则获取第一页
                后续请求使用上次响应最后一个任务的completedTime字段（原始格式）
                原始格式：2025-03-15T13:30:54.000+0000
                API格式：2025-03-15 13:30:54
            status: 任务状态，支持以下值：
                   - "Completed": 已完成的任务
                   - "Abandoned": 已放弃的任务

        Returns:
            dict: 原始响应数据，包含任务列表

        Note:
            分页机制：
            - 第一次请求：不传to参数
            - 后续请求：使用上次响应最后一个任务的completedTime字段作为to参数
            - completedTime原始格式：2025-03-15T13:30:54.000+0000
            - API需要格式：2025-03-15 13:30:54
            - URL示例：https://api.dida365.com/api/v2/project/all/closed?from=&to=2025-03-15%2013:30:54&status=Completed
        """
        try:
            if not self.current_session:
                return {"error": "no_auth_session", "message": "未设置认证会话，请先登录"}

            # 构建URL
            base_url = urls.build_dida_api_url(urls.DIDA_TASK_APIS["get_completed_tasks"])

            # 构建查询参数
            params = {
                "from": "",  # 固定为空
                "status": status  # 支持Completed或Abandoned
            }

            # 如果提供了to参数，则添加到查询参数中
            if to:
                # 将completedTime格式转换为滴答清单API需要的格式
                # 从 2025-03-15T13:30:54.000+0000 转换为 2025-03-15 13:30:54
                formatted_to = to.replace('T', ' ').replace('.000+0000', '')
                params["to"] = formatted_to
            # 第一次请求不添加to参数

            # 获取认证头和cookies
            headers = self._get_auth_headers()
            cookies = self._get_auth_cookies()

            app_logger.info(f"请求获取已完成任务: {base_url}")
            app_logger.info(f"查询参数: {params}")
            app_logger.debug(f"请求头: {headers}")

            # 发送请求
            response = await self.client.get(base_url, headers=headers, cookies=cookies, params=params)

            # 记录响应信息
            app_logger.info(f"已完成任务响应状态码: {response.status_code}")
            app_logger.debug(f"已完成任务响应头: {dict(response.headers)}")

            if response.status_code == 200:
                # 解析响应数据
                response_data = response.json()
                task_count = len(response_data) if isinstance(response_data, list) else 0
                app_logger.info(f"成功获取已完成任务数据，任务数量: {task_count}")
                app_logger.debug(f"已完成任务响应数据: {response_data}")

                # 直接返回原始响应
                return response_data

            else:
                app_logger.error(f"获取已完成任务失败，状态码: {response.status_code}")
                return {"error": f"HTTP {response.status_code}", "text": response.text}

        except Exception as e:
            app_logger.error(f"获取已完成任务时发生错误: {e}")
            return {"error": str(e)}

    async def get_trash_tasks(self, limit: int = 50, task_type: int = 1) -> dict:
        """
        获取垃圾桶中的任务

        Args:
            limit: 每页任务数量，默认50
            task_type: 任务类型，默认1

        Returns:
            dict: 原始响应数据，包含垃圾桶任务列表

        Note:
            响应格式：
            {
                "tasks": [...],  # 任务列表
                "next": 0        # 下一页标识
            }
        """
        try:
            if not self.current_session:
                return {"error": "no_auth_session", "message": "未设置认证会话，请先登录"}

            # 构建URL
            base_url = urls.build_dida_api_url(urls.DIDA_TASK_APIS["get_trash_tasks"])

            # 构建查询参数
            params = {
                "limit": limit,
                "type": task_type
            }

            # 获取认证头和cookies
            headers = self._get_auth_headers()
            cookies = self._get_auth_cookies()

            app_logger.info(f"请求获取垃圾桶任务: {base_url}")
            app_logger.info(f"查询参数: {params}")
            app_logger.debug(f"请求头: {headers}")

            # 发送请求
            response = await self.client.get(base_url, headers=headers, cookies=cookies, params=params)

            # 记录响应信息
            app_logger.info(f"垃圾桶任务响应状态码: {response.status_code}")
            app_logger.debug(f"垃圾桶任务响应头: {dict(response.headers)}")

            if response.status_code == 200:
                # 解析响应数据
                response_data = response.json()
                task_count = len(response_data.get('tasks', [])) if isinstance(response_data, dict) else 0
                app_logger.info(f"成功获取垃圾桶任务数据，任务数量: {task_count}")
                app_logger.debug(f"垃圾桶任务响应数据: {response_data}")

                # 直接返回原始响应
                return response_data

            else:
                app_logger.error(f"获取垃圾桶任务失败，状态码: {response.status_code}")
                return {"error": f"HTTP {response.status_code}", "text": response.text}

        except Exception as e:
            app_logger.error(f"获取垃圾桶任务时发生错误: {e}")
            return {"error": str(e)}

    async def close(self):
        """关闭HTTP客户端"""
        await self.client.aclose()


# 全局滴答清单API服务实例
dida_service = DidaAPIService()
