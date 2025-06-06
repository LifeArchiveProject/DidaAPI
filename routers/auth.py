"""认证相关API路由"""
from fastapi import APIRouter, HTTPException, Query
from models import WeChatQRResponse, WeChatValidateResponse, ApiResponse, PasswordLoginRequest
from services import wechat_service
from utils import app_logger

router = APIRouter(prefix="/auth", tags=["认证"])


@router.get("/wechat/qrcode", 
           response_model=WeChatQRResponse,
           summary="获取微信登录二维码",
           description="获取微信登录二维码，用户扫码后可进行登录验证")
async def get_wechat_qrcode(
    state: str = Query(default="Lw==", description="状态参数，用于防止CSRF攻击")
) -> WeChatQRResponse:
    """
    获取微信登录二维码
    
    - **state**: 状态参数，默认为 "Lw=="，用于防止CSRF攻击
    
    返回包含二维码图片URL和密钥的响应
    """
    try:
        app_logger.info(f"请求获取微信二维码，state: {state}")
        
        qr_response = await wechat_service.get_qr_code(state)
        
        if not qr_response:
            raise HTTPException(
                status_code=500,
                detail="获取微信二维码失败，请稍后重试"
            )
        
        app_logger.info(f"成功返回微信二维码: {qr_response.qr_code_key}")
        return qr_response
        
    except HTTPException:
        raise
    except Exception as e:
        app_logger.error(f"获取微信二维码时发生未知错误: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"服务器内部错误: {str(e)}"
        )


@router.get("/wechat/validate",
           response_model=WeChatValidateResponse,
           summary="验证微信登录",
           description="使用扫码后获得的验证码进行微信登录验证")
async def validate_wechat_login(
    code: str = Query(..., description="扫码后获得的验证码"),
    state: str = Query(default="Lw==", description="状态参数，需与获取二维码时的参数一致")
) -> WeChatValidateResponse:
    """
    验证微信登录
    
    - **code**: 扫码后获得的验证码（必需）
    - **state**: 状态参数，需与获取二维码时的参数一致
    
    返回登录验证结果，包含用户信息和认证令牌
    """
    try:
        app_logger.info(f"请求验证微信登录，code: {code}, state: {state}")
        
        if not code:
            raise HTTPException(
                status_code=400,
                detail="验证码不能为空"
            )
        
        validate_response = await wechat_service.validate_wechat_login(code, state)
        
        if not validate_response:
            raise HTTPException(
                status_code=500,
                detail="验证微信登录失败，请稍后重试"
            )
        
        app_logger.info(f"微信登录验证完成，成功: {validate_response.success}")
        return validate_response
        
    except HTTPException:
        raise
    except Exception as e:
        app_logger.error(f"验证微信登录时发生未知错误: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"服务器内部错误: {str(e)}"
        )



@router.get("/wechat/poll",
           summary="轮询微信登录状态",
           description="轮询检查二维码是否已被扫码登录")
async def poll_wechat_login(
    qr_code_key: str = Query(..., description="二维码密钥（16位字符）"),
    max_attempts: int = Query(default=60, description="最大轮询次数，默认60次（约5分钟）")
) -> WeChatValidateResponse:
    """
    轮询微信登录状态

    - **qr_code_key**: 二维码密钥（16位字符）
    - **max_attempts**: 最大轮询次数，默认60次（约5分钟）

    这个接口会持续轮询微信服务器，检查二维码是否已被扫码登录
    """
    try:
        app_logger.info(f"开始轮询微信登录状态，qr_code_key: {qr_code_key}")

        result = await wechat_service.poll_qr_status(qr_code_key, max_attempts)

        if not result:
            raise HTTPException(
                status_code=500,
                detail="轮询微信登录状态失败"
            )

        app_logger.info(f"轮询完成，结果: {result.success}")
        return result

    except HTTPException:
        raise
    except Exception as e:
        app_logger.error(f"轮询微信登录状态时发生未知错误: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"服务器内部错误: {str(e)}"
        )


@router.get("/wechat/callback",
           summary="微信登录回调处理",
           description="处理微信扫码后的回调，提取code参数")
async def wechat_callback(
    code: str = Query(..., description="微信返回的授权码"),
    state: str = Query(default="Lw==", description="状态参数")
):
    """
    微信登录回调处理

    这个接口用于演示微信回调的处理流程。
    实际使用中，微信会重定向到配置的redirect_uri。

    - **code**: 微信返回的授权码
    - **state**: 状态参数
    """
    try:
        app_logger.info(f"收到微信回调，code: {code}, state: {state}")

        # 自动进行登录验证
        validate_response = await wechat_service.validate_wechat_login(code, state)

        if validate_response and validate_response.success:
            return {
                "message": "微信登录成功",
                "code": code,
                "state": state,
                "login_result": validate_response.dict(),
                "next_step": "用户已成功登录，可以访问受保护的资源"
            }
        else:
            return {
                "message": "微信登录失败",
                "code": code,
                "state": state,
                "error": validate_response.message if validate_response else "验证失败"
            }

    except Exception as e:
        app_logger.error(f"处理微信回调时发生错误: {e}")
        return {
            "message": "处理微信回调失败",
            "code": code,
            "state": state,
            "error": str(e)
        }


@router.post("/password/login",
            summary="密码登录",
            description="使用手机号/邮箱，密码进行登录")
async def password_login(
    login_request: PasswordLoginRequest
):
    """
    密码登录滴答清单

    - **username**: 登录账户（邮箱或手机号）
    - **password**: 登录密码

    返回登录结果，包含用户信息和认证令牌
    """
    try:
        app_logger.info(f"请求密码登录，用户名: {login_request.username}")

        if not login_request.username or not login_request.password:
            raise HTTPException(
                status_code=400,
                detail="用户名和密码不能为空"
            )

        login_response = await wechat_service.password_login(
            login_request.username,
            login_request.password
        )

        if not login_response:
            return {"error": "密码登录失败，请稍后重试"}

        # 记录日志
        if 'errorCode' in login_response:
            app_logger.info(f"密码登录失败，错误代码: {login_response.get('errorCode')}")
        else:
            user_id = login_response.get('userId', '')
            app_logger.info(f"密码登录成功，用户ID: {user_id}")

        # 直接返回原始响应，不进行任何封装
        return login_response

    except HTTPException:
        raise
    except Exception as e:
        app_logger.error(f"密码登录时发生未知错误: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"服务器内部错误: {str(e)}"
        )


@router.get("/health",
           response_model=ApiResponse,
           summary="健康检查",
           description="检查认证服务的健康状态")
async def health_check() -> ApiResponse:
    """
    健康检查接口

    返回服务的健康状态信息
    """
    return ApiResponse(
        code=200,
        message="认证服务运行正常",
        data={
            "service": "auth",
            "status": "healthy",
            "version": "1.0.0"
        }
    )
