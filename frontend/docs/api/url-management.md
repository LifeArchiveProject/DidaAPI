# URL和外部链接管理

本项目采用统一的URL管理策略，所有外部链接和API端点都在 `core/urls.py` 文件中集中管理。

## 管理原则

### 为什么需要统一管理
1. **避免硬编码** - 防止URL散布在各个文件中
2. **便于维护** - 统一修改和更新链接
3. **提高可读性** - 清晰的分类和注释
4. **便于测试** - 集中的URL便于健康检查

### 分类管理
所有URL按功能分为以下几类：

#### 微信开放平台相关
- `WECHAT_URLS` - 微信API的基础URL
- `WECHAT_CONFIG` - 微信应用配置参数

#### 滴答清单API相关
- `DIDA_API_BASE` - 滴答清单API基础配置
- `DIDA_AUTH_APIS` - 认证相关API端点
- `DIDA_TASK_APIS` - 任务管理API端点
- `DIDA_PROJECT_APIS` - 项目管理API端点

#### 外部文档链接
- `OFFICIAL_DOCS` - 官方文档链接
- `TECH_REFERENCES` - 技术参考文档

## 使用方法

### 导入URL模块
```python
from core import urls
```

### 使用预定义的URL
```python
# 获取微信二维码基础URL
qr_base_url = urls.WECHAT_URLS["qr_base_url"]

# 获取滴答清单API基础URL
api_base = urls.DIDA_API_BASE["base_url"]
```

### 使用URL构建函数
```python
# 构建微信登录二维码URL
qr_url = urls.build_wechat_qr_url(state="Lw==")

# 构建滴答清单API完整URL
api_url = urls.build_dida_api_url("/batch/check/0")

# 构建微信登录验证URL
validate_url = urls.build_wechat_validate_url(code="xxx", state="Lw==")
```

## URL分类详情

### 微信相关URL
```python
WECHAT_URLS = {
    "qr_base_url": "https://open.weixin.qq.com/connect/qrconnect",
    "qr_image_base_url": "https://open.weixin.qq.com/connect/qrcode", 
    "poll_login_url": "https://long.open.weixin.qq.com/connect/l/qrconnect",
    "redirect_uri": "https://dida365.com/sign/wechat"
}
```

### 滴答清单API端点
```python
DIDA_TASK_APIS = {
    "get_all_tasks": "/batch/check/0",
    "task_crud": "/task",
    "task_search": "/task/search"
}
```

### 官方文档链接
```python
OFFICIAL_DOCS = {
    "wechat_login_guide": "https://developers.weixin.qq.com/doc/oplatform/Website_App/WeChat_Login/Wechat_Login",
    "dida_official": "https://dida365.com"
}
```

## 辅助函数

### URL构建函数
- `build_wechat_qr_url(state)` - 构建微信登录二维码URL
- `build_wechat_poll_url(uuid, timestamp)` - 构建轮询URL
- `build_dida_api_url(endpoint)` - 构建滴答清单API URL
- `build_wechat_validate_url(code, state)` - 构建验证URL

### 管理函数
- `get_all_external_urls()` - 获取所有外部URL
- `get_api_endpoints()` - 获取所有API端点

## 添加新URL的步骤

### 1. 确定分类
根据URL的用途选择合适的分类字典。

### 2. 添加URL
```python
# 在对应的字典中添加新URL
DIDA_TASK_APIS = {
    # 现有URL...
    "new_endpoint": "/new/api/endpoint"  # 新增
}
```

### 3. 添加注释
为新URL添加清晰的注释说明其用途。

### 4. 更新文档
在相关的API文档中引用新的URL配置。

## 相关文件

- `core/urls.py` - URL管理主文件
- `core/config.py` - 非URL配置管理
- `config.toml` - 配置文件（已移除URL配置）
