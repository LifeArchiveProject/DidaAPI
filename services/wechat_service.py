"""微信登录服务模块"""
import re
import uuid
from typing import Optional, Dict, Any, Tuple
import httpx
from utils import app_logger
from core import config, db, urls
from models import WeChatQRResponse, WeChatValidateResponse, PasswordLoginRequest


class WeChatLoginService:
    """微信登录服务类"""
    
    def __init__(self):
        self.request_config = config.get('request_config', {})
        self.client = httpx.AsyncClient(timeout=self.request_config.get('timeout', 30.0))
    
    async def get_qr_code(self, state: str = "Lw==") -> Optional[WeChatQRResponse]:
        """
        获取微信登录二维码
        
        Args:
            state: 状态参数，默认为 "Lw=="
            
        Returns:
            WeChatQRResponse: 包含二维码URL和密钥的响应对象
        """
        try:
            # 使用统一的URL构建函数
            qr_url = urls.build_wechat_qr_url(state)
            
            app_logger.info(f"请求微信二维码: {qr_url}")
            
            # 发送请求
            response = await self.client.get(qr_url)
            response.raise_for_status()
            
            # 记录完整响应
            app_logger.debug(f"微信二维码响应状态: {response.status_code}")
            app_logger.debug(f"微信二维码响应头: {dict(response.headers)}")
            app_logger.debug(f"微信二维码响应内容长度: {len(response.text)}")
            
            # 解析HTML中的二维码图片链接
            qr_code_key = self._extract_qr_code_key(response.text)
            
            if not qr_code_key:
                app_logger.error("未能从响应中提取二维码密钥")
                return None
            
            # 构建完整的二维码图片URL
            qr_code_url = f"{urls.WECHAT_URLS['qr_image_base_url']}/{qr_code_key}"
            
            # 记录到数据库
            db.log_wechat_login(qr_code_key=qr_code_key, state=state)
            
            app_logger.info(f"成功获取二维码: {qr_code_url}")
            
            return WeChatQRResponse(
                qr_code_url=qr_code_url,
                qr_code_key=qr_code_key,
                state=state
            )
            
        except Exception as e:
            app_logger.error(f"获取微信二维码失败: {e}")
            return None
    
    def _extract_qr_code_key(self, html_content: str) -> Optional[str]:
        """
        从HTML内容中提取二维码密钥
        
        Args:
            html_content: HTML响应内容
            
        Returns:
            str: 16位二维码密钥，如果未找到则返回None
        """
        try:
            # 查找二维码图片标签
            pattern = r'<img[^>]*class="[^"]*qrcode[^"]*"[^>]*src="([^"]*)"'
            match = re.search(pattern, html_content)
            
            if match:
                src_url = match.group(1)
                app_logger.debug(f"找到二维码图片src: {src_url}")
                
                # 提取最后16位字符
                qr_code_key = src_url.split('/')[-1]
                
                if len(qr_code_key) >= 16:
                    qr_code_key = qr_code_key[-16:]
                    app_logger.info(f"提取到二维码密钥: {qr_code_key}")
                    return qr_code_key
                else:
                    app_logger.warning(f"二维码密钥长度不足16位: {qr_code_key}")
            
            # 如果上面的方法失败，尝试其他模式
            patterns = [
                r'/connect/qrcode/([a-zA-Z0-9]{16})',
                r'qrcode/([a-zA-Z0-9]{16})',
                r'src="[^"]*?([a-zA-Z0-9]{16})"'
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, html_content)
                if matches:
                    qr_code_key = matches[0]
                    app_logger.info(f"通过备用模式提取到二维码密钥: {qr_code_key}")
                    return qr_code_key
            
            app_logger.error("未能从HTML中提取二维码密钥")
            app_logger.debug(f"HTML内容片段: {html_content[:500]}...")
            return None
            
        except Exception as e:
            app_logger.error(f"提取二维码密钥时发生错误: {e}")
            return None

    async def poll_qr_status(self, qr_code_key: str, max_attempts: int = 60) -> Optional[WeChatValidateResponse]:
        """
        轮询二维码状态，检查是否已扫码登录

        Args:
            qr_code_key: 二维码密钥
            max_attempts: 最大轮询次数，默认60次（约5分钟）

        Returns:
            WeChatValidateResponse: 登录结果
        """
        import asyncio

        for attempt in range(max_attempts):
            try:
                app_logger.info(f"轮询二维码状态，第 {attempt + 1}/{max_attempts} 次")

                # 使用统一的URL构建函数
                poll_url = urls.build_wechat_poll_url(qr_code_key)

                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
                    'Referer': 'https://open.weixin.qq.com/',
                    'Accept': '*/*',
                    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
                }

                response = await self.client.get(poll_url, headers=headers)
                response_text = response.text
                app_logger.debug(f"轮询响应: {response_text}")

                # 解析微信轮询响应
                # 实际响应格式是: window.wx_errcode=405;window.wx_code='xxx';
                if "window.wx_errcode" in response_text:
                    import re

                    # 提取错误码
                    errcode_match = re.search(r'window\.wx_errcode\s*=\s*(\d+)', response_text)
                    code_match = re.search(r"window\.wx_code\s*=\s*'([^']*)'", response_text)

                    if errcode_match:
                        errcode = int(errcode_match.group(1))
                        wx_code = code_match.group(1) if code_match else ''

                        app_logger.info(f"轮询状态 - errcode: {errcode}, wx_code: {wx_code}")

                        if errcode == 405 and wx_code:
                            # 登录成功，获得了授权码
                            app_logger.info(f"检测到登录成功，获得授权码: {wx_code}")

                            # 使用获得的code进行验证
                            return await self.validate_wechat_login(wx_code)

                        elif errcode == 404:
                            app_logger.info("等待扫码...")
                        elif errcode == 403:
                            app_logger.info("二维码已扫描，等待用户确认")
                        elif errcode == 408:
                            app_logger.info("二维码已过期")
                            break
                        elif errcode == 400:
                            app_logger.info("二维码已失效")
                            break

                # 等待5秒后继续轮询
                await asyncio.sleep(5)

            except Exception as e:
                app_logger.error(f"轮询二维码状态失败: {e}")
                await asyncio.sleep(5)

        app_logger.warning("轮询超时，未检测到登录")
        return WeChatValidateResponse(
            success=False,
            message="轮询超时，请重新获取二维码",
            token=None,
            user_info=None,
            cookies=None,
            raw_response={"error": "polling_timeout"}
        )

    async def validate_wechat_login(self, code: str, state: str = "Lw==") -> Optional[WeChatValidateResponse]:
        """
        验证微信登录

        Args:
            code: 扫码后获得的验证码
            state: 状态参数

        Returns:
            WeChatValidateResponse: 验证响应对象
        """
        try:
            # 使用统一的URL构建函数
            validate_url = urls.build_wechat_validate_url(code, state)

            app_logger.info(f"验证微信登录: {validate_url}")

            # 设置请求头，模拟浏览器请求
            headers = {
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate, br, zstd',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
                'Content-Type': 'application/json',
                'Origin': 'https://dida365.com',
                'Referer': 'https://dida365.com/',
                'Sec-Ch-Ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
                'Sec-Ch-Ua-Mobile': '?0',
                'Sec-Ch-Ua-Platform': '"Windows"',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-site',
                'User-Agent': self.request_config.get('user_agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'),
                'X-Device': self.request_config.get('device_info', '{}')
            }

            # 发送验证请求
            response = await self.client.get(validate_url, headers=headers)

            # 记录详细的响应信息
            app_logger.info(f"验证响应状态码: {response.status_code}")
            app_logger.info(f"验证响应头: {dict(response.headers)}")

            # 提取cookies
            cookies = {}
            if hasattr(response, 'cookies') and response.cookies:
                for cookie_name, cookie_value in response.cookies.items():
                    cookies[cookie_name] = cookie_value

            # 同时从Set-Cookie头中解析cookies
            set_cookie_header = response.headers.get('set-cookie', '')
            if set_cookie_header:
                import re
                # 解析Set-Cookie头
                cookie_matches = re.findall(r'([^=]+)=([^;]+)', set_cookie_header)
                for name, value in cookie_matches:
                    cookies[name.strip()] = value.strip()

            app_logger.info(f"响应cookies: {cookies}")

            # 尝试解析JSON响应
            response_data = {}
            try:
                response_data = response.json()
                app_logger.info(f"验证响应JSON: {response_data}")
            except Exception as json_error:
                app_logger.warning(f"响应不是有效的JSON: {json_error}")
                app_logger.info(f"响应文本内容: {response.text}")
                response_data = {"raw_text": response.text}

            # 检查是否成功
            success = response.status_code == 200

            # 提取认证令牌
            token = cookies.get('t', '')
            csrf_token = cookies.get('_csrf_token', '')

            # 保存会话信息
            if success and token:
                session_id = str(uuid.uuid4())
                session_data = {
                    'session_id': session_id,
                    'token': token,
                    'csrf_token': csrf_token,
                    'cookies': cookies,
                    'is_active': True
                }
                db.save_user_session(session_data)

                # 自动设置滴答清单API认证会话
                try:
                    from services.dida_service import dida_service
                    dida_service.set_auth_session(token, csrf_token)
                    app_logger.info("已自动设置滴答清单API认证会话")
                except Exception as e:
                    app_logger.warning(f"自动设置滴答清单API认证会话失败: {e}")

            # 记录登录日志
            db.log_wechat_login(
                qr_code_key="",  # 这里可能需要从之前的记录中关联
                validation_code=code,
                state=state,
                response_data={
                    'status_code': response.status_code,
                    'headers': dict(response.headers),
                    'cookies': cookies,
                    'json_data': response_data
                },
                status='success' if success else 'failed'
            )

            return WeChatValidateResponse(
                success=success,
                message="登录成功" if success else "登录失败",
                token=token if token else None,
                user_info=response_data.get('user', {}),
                cookies=cookies,
                raw_response=response_data
            )

        except Exception as e:
            app_logger.error(f"验证微信登录失败: {e}")

            # 记录失败日志
            db.log_wechat_login(
                qr_code_key="",
                validation_code=code,
                state=state,
                response_data={'error': str(e)},
                status='failed'
            )

            return WeChatValidateResponse(
                success=False,
                message=f"验证失败: {str(e)}",
                token=None,
                user_info=None,
                cookies=None,
                raw_response={'error': str(e)}
            )

    async def password_login(self, username: str, password: str) -> dict:
        """
        密码登录滴答清单

        Args:
            username: 登录账户（邮箱或手机号）
            password: 登录密码

        Returns:
            dict: 原始响应数据
        """
        try:
            # 使用统一的URL构建函数
            login_url = urls.build_password_login_url(wc=True, remember=True)

            app_logger.info(f"密码登录请求: {login_url}")

            # 构建请求体
            login_data = {
                "username": username,
                "password": password
            }

            # 设置请求头，模拟浏览器请求
            headers = {
                'Accept': 'application/json, text/plain, */*',
                'Accept-Encoding': 'gzip, deflate, br, zstd',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
                'Content-Type': 'application/json',
                'Origin': 'https://dida365.com',
                'Referer': 'https://dida365.com/',
                'Sec-Ch-Ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
                'Sec-Ch-Ua-Mobile': '?0',
                'Sec-Ch-Ua-Platform': '"Windows"',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-site',
                'User-Agent': self.request_config.get('user_agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'),
                'X-Device': self.request_config.get('device_info', '{}')
            }

            # 发送POST请求
            response = await self.client.post(login_url, json=login_data, headers=headers)

            # 记录详细的响应信息
            app_logger.info(f"密码登录响应状态码: {response.status_code}")
            app_logger.info(f"密码登录响应头: {dict(response.headers)}")

            # 提取cookies
            cookies = {}
            if hasattr(response, 'cookies') and response.cookies:
                for cookie_name, cookie_value in response.cookies.items():
                    cookies[cookie_name] = cookie_value

            # 同时从Set-Cookie头中解析cookies
            set_cookie_header = response.headers.get('set-cookie', '')
            if set_cookie_header:
                import re
                # 解析Set-Cookie头
                cookie_matches = re.findall(r'([^=]+)=([^;]+)', set_cookie_header)
                for name, value in cookie_matches:
                    cookies[name.strip()] = value.strip()

            app_logger.info(f"密码登录响应cookies: {cookies}")

            # 尝试解析JSON响应
            response_data = {}
            try:
                response_data = response.json()
                app_logger.info(f"密码登录响应JSON: {response_data}")
            except Exception as json_error:
                app_logger.warning(f"响应不是有效的JSON: {json_error}")
                app_logger.info(f"响应文本内容: {response.text}")
                response_data = {"raw_text": response.text}

            # 检查是否成功
            success = response.status_code == 200 and 'token' in response_data

            # 如果成功，保存会话信息
            if success:
                token = response_data.get('token', '')
                if token:
                    session_id = str(uuid.uuid4())
                    session_data = {
                        'session_id': session_id,
                        'token': token,
                        'csrf_token': '',  # 密码登录可能不返回CSRF token
                        'cookies': cookies,
                        'is_active': True
                    }
                    db.save_user_session(session_data)

                    # 自动设置滴答清单API认证会话
                    try:
                        from services.dida_service import dida_service
                        dida_service.set_auth_session(token, '')
                        app_logger.info("已自动设置滴答清单API认证会话")
                    except Exception as e:
                        app_logger.warning(f"自动设置滴答清单API认证会话失败: {e}")

            # 直接返回原始响应
            return response_data

        except Exception as e:
            app_logger.error(f"密码登录失败: {e}")

            # 返回错误响应
            return {'error': str(e)}

    async def close(self):
        """关闭HTTP客户端"""
        await self.client.aclose()


# 全局微信登录服务实例
wechat_service = WeChatLoginService()
