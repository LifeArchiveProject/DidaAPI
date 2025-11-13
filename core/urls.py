"""
统一的URL和外部链接管理
所有外部API链接和相关URL都在此文件中统一管理
"""

# ================================
# 微信开放平台相关链接
# ================================

# 微信登录相关URL
WECHAT_URLS = {
    # 获取微信登录二维码的基础URL
    "qr_base_url": "https://open.weixin.qq.com/connect/qrconnect",
    
    # 微信二维码图片的基础URL
    "qr_image_base_url": "https://open.weixin.qq.com/connect/qrcode",
    
    # 微信长轮询检查登录状态的URL
    "poll_login_url": "https://long.open.weixin.qq.com/connect/l/qrconnect",
    
    # 微信登录重定向回调地址（滴答清单配置的）
    "redirect_uri": "https://dida365.com/sign/wechat",
}

# 微信应用配置
WECHAT_CONFIG = {
    # 滴答清单在微信开放平台的应用ID
    "app_id": "wxf1429a73d311aad4",
    
    # OAuth2.0授权类型
    "response_type": "code",
    
    # 授权作用域（网站应用微信登录）
    "scope": "snsapi_login",
    
    # 默认状态参数（用于防CSRF攻击）
    "default_state": "Lw==",
}

# ================================
# 滴答清单API相关链接
# ================================

# 滴答清单API基础配置
DIDA_API_BASE = {
    # 滴答清单API v2版本基础URL
    "base_url": "https://api.dida365.com/api/v2",
    
    # 滴答清单Web端主域名
    "web_domain": "https://dida365.com",
}

# 滴答清单微服务基础配置
DIDA_MS_BASE = {
    "base_url": "https://ms.dida365.com"
}

# 滴答清单认证相关API
DIDA_AUTH_APIS = {
    # 微信登录验证接口
    "wechat_validate": "/user/sign/wechat/validate",

    # 密码登录接口
    "password_login": "/user/signon",

    # 用户信息接口
    "user_profile": "/user/profile",
}

# 滴答清单任务管理API
DIDA_TASK_APIS = {
    # 批量检查/获取所有任务接口
    "get_all_tasks": "/batch/check/0",

    # 获取已完成任务接口（支持分页）
    "get_completed_tasks": "/project/all/closed",

    # 获取垃圾桶任务接口
    "get_trash_tasks": "/project/all/trash/page",

    # 任务搜索接口
    "task_search": "/task/search",

    # 任务统计接口（需要拼接日期范围）
    "task_statistics": "/task/statistics",  # /task/statistics/{start_date}/{end_date}
}

# 滴答清单项目管理API
DIDA_PROJECT_APIS = {
    # 获取所有项目列表
    "get_projects": "/projects",
}

# 滴答清单统计相关API
DIDA_STATISTICS_APIS = {
    # 用户排名统计
    "user_ranking": "/user/ranking",

    # 通用统计信息（概览、成就值、趋势）
    "general_statistics": "/statistics/general",

    # 任务统计（需要拼接日期范围）
    "task_statistics": "/task/statistics",  # /task/statistics/{start_date}/{end_date}
}

# 滴答清单番茄专注API
DIDA_POMODORO_APIS = {
    # 番茄专注概览（桌面版）
    "general_for_desktop": "/pomodoros/statistics/generalForDesktop",

    # 专注详情分布（需要拼接日期范围）
    "focus_distribution": "/pomodoros/statistics/dist",  # /pomodoros/statistics/dist/{start_date}/{end_date}

    # 专注记录时间线
    "focus_timeline": "/pomodoros/timeline",

    # 专注趋势热力图（需要拼接日期范围）
    "focus_heatmap": "/pomodoros/statistics/heatmap",  # /pomodoros/statistics/heatmap/{start_date}/{end_date}

    # 专注时间分布（按时间段，需要拼接日期范围）
    "focus_time_distribution": "/pomodoros/statistics/dist/clockByDay",  # /pomodoros/statistics/dist/clockByDay/{start_date}/{end_date}

    # 专注时间按小时分布（需要拼接日期范围）
    "focus_hour_distribution": "/pomodoros/statistics/dist/clock",  # /pomodoros/statistics/dist/clock/{start_date}/{end_date}
}

# 滴答清单番茄钟操作API
DIDA_FOCUS_APIS = {
    # 批量执行番茄钟操作（开始、暂停、继续、结束等）
    "focus_batch_operation": "/focus/batch/focusOp"
}

# 滴答清单习惯管理API
DIDA_HABIT_APIS = {
    # 获取所有习惯
    "get_habits": "/habits",

    # 本周习惯打卡统计
    "week_current_statistics": "/habits/statistics/week/current",

    # 导出习惯数据（Excel格式）
    "export_habits": "/data/export/habits",
}

# 滴答清单用户相关API
DIDA_USER_APIS = {
    # 用户信息
    "user_profile": "/user/profile",
}

# ================================
# 自定义接口API（本项目专属）
# ================================

# 自定义接口API
CUSTOM_APIS = {
    # 任务导出为Excel
    "export_tasks_excel": "/custom/export/tasks/excel",
    # 专注记录导出为Excel
    "export_focus_excel": "/custom/export/focus/excel",
}

# ================================
# 外部文档和参考链接
# ================================

# 官方文档链接
OFFICIAL_DOCS = {
    # 微信开放平台 - 网站应用微信登录开发指南
    "wechat_login_guide": "https://developers.weixin.qq.com/doc/oplatform/Website_App/WeChat_Login/Wechat_Login",
    
    # 微信开放平台 - OAuth2.0授权
    "wechat_oauth": "https://developers.weixin.qq.com/doc/oplatform/Website_App/WeChat_Login/Wechat_Login",
    
    # 滴答清单官网
    "dida_official": "https://dida365.com",
    
    # 滴答清单帮助中心
    "dida_help": "https://help.dida365.com",
}

# 技术参考链接
TECH_REFERENCES = {
    # FastAPI官方文档
    "fastapi_docs": "https://fastapi.tiangolo.com",
    
    # Pydantic官方文档
    "pydantic_docs": "https://docs.pydantic.dev",
    
    # HTTPX官方文档
    "httpx_docs": "https://www.python-httpx.org",
    
    # Loguru官方文档
    "loguru_docs": "https://loguru.readthedocs.io",
}

# ================================
# URL构建辅助函数
# ================================

def build_wechat_qr_url(state: str = None) -> str:
    """
    构建微信登录二维码URL
    
    Args:
        state: 状态参数，默认使用配置中的值
        
    Returns:
        str: 完整的微信登录二维码URL
    """
    if state is None:
        state = WECHAT_CONFIG["default_state"]
    
    params = {
        "appid": WECHAT_CONFIG["app_id"],
        "redirect_uri": WECHAT_URLS["redirect_uri"],
        "response_type": WECHAT_CONFIG["response_type"],
        "scope": WECHAT_CONFIG["scope"],
        "state": state
    }
    
    # 构建查询字符串
    query_string = "&".join([f"{k}={v}" for k, v in params.items()])
    return f"{WECHAT_URLS['qr_base_url']}?{query_string}"


def build_wechat_poll_url(uuid: str, timestamp: int = None) -> str:
    """
    构建微信登录状态轮询URL
    
    Args:
        uuid: 二维码密钥
        timestamp: 时间戳，用于防缓存
        
    Returns:
        str: 完整的轮询URL
    """
    import time
    if timestamp is None:
        timestamp = int(time.time() * 1000)
    
    return f"{WECHAT_URLS['poll_login_url']}?uuid={uuid}&_={timestamp}"


def build_dida_api_url(endpoint: str) -> str:
    """
    构建滴答清单API完整URL
    
    Args:
        endpoint: API端点路径
        
    Returns:
        str: 完整的API URL
    """
    # 确保endpoint以/开头
    if not endpoint.startswith('/'):
        endpoint = '/' + endpoint
    
    return f"{DIDA_API_BASE['base_url']}{endpoint}"


def build_dida_ms_url(endpoint: str) -> str:
    """
    构建滴答清单微服务API完整URL

    Args:
        endpoint: API端点路径

    Returns:
        str: 完整的微服务API URL
    """
    if not endpoint.startswith('/'):
        endpoint = '/' + endpoint

    return f"{DIDA_MS_BASE['base_url']}{endpoint}"


def build_wechat_validate_url(code: str, state: str = None) -> str:
    """
    构建微信登录验证URL

    Args:
        code: 微信授权码
        state: 状态参数

    Returns:
        str: 完整的验证URL
    """
    if state is None:
        state = WECHAT_CONFIG["default_state"]

    base_url = build_dida_api_url(DIDA_AUTH_APIS["wechat_validate"])
    return f"{base_url}?code={code}&state={state}"


def build_password_login_url(wc: bool = True, remember: bool = True) -> str:
    """
    构建密码登录URL

    Args:
        wc: Web客户端标识，默认为True
        remember: 记住登录状态，默认为True

    Returns:
        str: 完整的密码登录URL
    """
    base_url = build_dida_api_url(DIDA_AUTH_APIS["password_login"])
    params = []
    if wc:
        params.append("wc=true")
    if remember:
        params.append("remember=true")

    if params:
        return f"{base_url}?{'&'.join(params)}"
    return base_url


# ================================
# 链接验证和健康检查
# ================================

def get_all_external_urls() -> dict:
    """
    获取所有外部URL，用于健康检查
    
    Returns:
        dict: 包含所有外部URL的字典
    """
    return {
        "wechat_urls": WECHAT_URLS,
        "dida_base": DIDA_API_BASE,
        "dida_ms_base": DIDA_MS_BASE,
        "official_docs": OFFICIAL_DOCS,
        "tech_references": TECH_REFERENCES
    }


def get_api_endpoints() -> dict:
    """
    获取所有API端点

    Returns:
        dict: 包含所有API端点的字典
    """
    return {
        "auth_apis": DIDA_AUTH_APIS,
        "task_apis": DIDA_TASK_APIS,
        "project_apis": DIDA_PROJECT_APIS,
        "statistics_apis": DIDA_STATISTICS_APIS,
        "pomodoro_apis": DIDA_POMODORO_APIS,
        "focus_apis": DIDA_FOCUS_APIS,
        "habit_apis": DIDA_HABIT_APIS,
        "user_apis": DIDA_USER_APIS,
        "custom_apis": CUSTOM_APIS
    }
