"""系统相关API路由"""
from fastapi import APIRouter
from typing import Dict, Any
from core import urls
from models import ApiResponse
from utils import app_logger

router = APIRouter(prefix="/system", tags=["系统管理"])


@router.get("/urls",
           response_model=ApiResponse,
           summary="获取所有URL配置",
           description="获取项目中管理的所有URL和外部链接配置")
async def get_all_urls() -> ApiResponse:
    """
    获取所有URL配置
    
    返回项目中统一管理的所有URL和外部链接
    """
    try:
        all_urls = urls.get_all_external_urls()
        api_endpoints = urls.get_api_endpoints()
        
        return ApiResponse(
            code=200,
            message="获取URL配置成功",
            data={
                "external_urls": all_urls,
                "api_endpoints": api_endpoints
            }
        )
        
    except Exception as e:
        app_logger.error(f"获取URL配置时发生错误: {e}")
        return ApiResponse(
            code=500,
            message=f"获取URL配置失败: {str(e)}",
            data=None
        )


@router.get("/urls/wechat",
           response_model=ApiResponse,
           summary="获取微信相关URL",
           description="获取微信开放平台相关的所有URL配置")
async def get_wechat_urls() -> ApiResponse:
    """
    获取微信相关URL
    
    返回微信开放平台相关的URL配置
    """
    try:
        return ApiResponse(
            code=200,
            message="获取微信URL配置成功",
            data={
                "wechat_urls": urls.WECHAT_URLS,
                "wechat_config": urls.WECHAT_CONFIG,
                "helper_functions": [
                    "build_wechat_qr_url(state)",
                    "build_wechat_poll_url(uuid, timestamp)",
                    "build_wechat_validate_url(code, state)"
                ]
            }
        )
        
    except Exception as e:
        app_logger.error(f"获取微信URL配置时发生错误: {e}")
        return ApiResponse(
            code=500,
            message=f"获取微信URL配置失败: {str(e)}",
            data=None
        )


@router.get("/urls/dida",
           response_model=ApiResponse,
           summary="获取滴答清单API URL",
           description="获取滴答清单API相关的所有URL配置")
async def get_dida_urls() -> ApiResponse:
    """
    获取滴答清单API URL
    
    返回滴答清单API相关的URL配置
    """
    try:
        return ApiResponse(
            code=200,
            message="获取滴答清单URL配置成功",
            data={
                "base_config": urls.DIDA_API_BASE,
                "auth_apis": urls.DIDA_AUTH_APIS,
                "task_apis": urls.DIDA_TASK_APIS,
                "project_apis": urls.DIDA_PROJECT_APIS,
                "statistics_apis": urls.DIDA_STATISTICS_APIS,
                "pomodoro_apis": urls.DIDA_POMODORO_APIS,
                "habit_apis": urls.DIDA_HABIT_APIS,
                "helper_functions": [
                    "build_dida_api_url(endpoint)"
                ]
            }
        )
        
    except Exception as e:
        app_logger.error(f"获取滴答清单URL配置时发生错误: {e}")
        return ApiResponse(
            code=500,
            message=f"获取滴答清单URL配置失败: {str(e)}",
            data=None
        )


@router.get("/urls/docs",
           response_model=ApiResponse,
           summary="获取文档链接",
           description="获取官方文档和技术参考链接")
async def get_doc_urls() -> ApiResponse:
    """
    获取文档链接
    
    返回官方文档和技术参考链接
    """
    try:
        return ApiResponse(
            code=200,
            message="获取文档链接成功",
            data={
                "official_docs": urls.OFFICIAL_DOCS,
                "tech_references": urls.TECH_REFERENCES,
                "project_docs": {
                    "frontend_docs": "http://localhost:3000",
                    "api_docs": "http://localhost:3000/api/",
                    "url_management": "http://localhost:3000/api/url-management",
                    "wechat_flow": "http://localhost:3000/api/auth/wechat-login-flow"
                }
            }
        )
        
    except Exception as e:
        app_logger.error(f"获取文档链接时发生错误: {e}")
        return ApiResponse(
            code=500,
            message=f"获取文档链接失败: {str(e)}",
            data=None
        )


@router.get("/info",
           response_model=ApiResponse,
           summary="获取系统信息",
           description="获取项目的基本信息和配置概览")
async def get_system_info() -> ApiResponse:
    """
    获取系统信息
    
    返回项目的基本信息和配置概览
    """
    try:
        from core import config
        
        return ApiResponse(
            code=200,
            message="获取系统信息成功",
            data={
                "project_name": "滴答清单Web端API接口",
                "version": "1.0.0",
                "description": "滴答清单原始API的封装层，提供简化的接口和完整的API文档",
                "features": [
                    "微信扫码登录",
                    "任务管理",
                    "会话持久化",
                    "统一URL管理",
                    "完整API文档"
                ],
                "url_management": {
                    "total_external_urls": len(urls.WECHAT_URLS) + len(urls.DIDA_API_BASE) + len(urls.OFFICIAL_DOCS) + len(urls.TECH_REFERENCES),
                    "total_api_endpoints": len(urls.DIDA_AUTH_APIS) + len(urls.DIDA_TASK_APIS) + len(urls.DIDA_PROJECT_APIS) + len(urls.DIDA_STATISTICS_APIS) + len(urls.DIDA_POMODORO_APIS) + len(urls.DIDA_HABIT_APIS),
                    "management_file": "core/urls.py"
                },
                "config": {
                    "app": config.app,
                    "request_config": config.get('request_config', {}),
                    "database": config.database
                }
            }
        )
        
    except Exception as e:
        app_logger.error(f"获取系统信息时发生错误: {e}")
        return ApiResponse(
            code=500,
            message=f"获取系统信息失败: {str(e)}",
            data=None
        )
