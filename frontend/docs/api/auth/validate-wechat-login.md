# 验证微信登录

使用从轮询接口获得的授权码向滴答清单验证微信登录，获取认证令牌。

## 接口信息

- **接口URL**: `https://api.dida365.com/api/v2/user/sign/wechat/validate`
- **请求方法**: `GET`
- **认证要求**: 无需认证（此接口用于获取认证）
- **所属平台**: 滴答清单

## 请求参数

### Query Parameters

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| code | string | 是 | 微信授权码，从轮询接口获得 |
| state | string | 否 | 状态参数，需与获取二维码时一致 |

## 完整请求示例

```http
GET https://api.dida365.com/api/v2/user/sign/wechat/validate?code={authorization_code}&state={state} HTTP/1.1
Host: api.dida365.com
Accept: */*
Accept-Encoding: gzip, deflate, br, zstd
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7
Content-Type: application/json
Origin: https://dida365.com
Referer: https://dida365.com/
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36
X-Device: {"platform":"web","os":"Windows 10","device":"Chrome 136.0.0.0","name":"","version":6310,"id":"{device_id}","channel":"website","campaign":"","websocket":""}
```

## 响应格式

### 成功响应

**状态码**: `200 OK`

**Content-Type**: `application/json;charset=UTF-8`

### 响应头（重要）

响应头中包含认证相关的Cookie：

```http
Set-Cookie: t={auth_token}; Domain=.dida365.com; Expires={expires_date}; Path=/; Secure; HttpOnly; SameSite=None

Set-Cookie: _csrf_token={csrf_token}; Domain=.dida365.com; Expires={expires_date}; Path=/; Secure
```

### 响应体

```json
{
  "success": true,
  "message": "string",
  "user": {
    "id": "string",
    "username": "string",
    "email": "string"
  }
}
```

## 关键信息提取

### 认证令牌 (t cookie)

这是最重要的认证信息，用于后续所有API调用：

```
t={auth_token}
```

### CSRF令牌 (_csrf_token cookie)

用于防止跨站请求伪造攻击：

```
_csrf_token={csrf_token}
```

## Cookie解析

### 解析Set-Cookie头

```python
import re

def parse_cookies(set_cookie_header):
    """解析Set-Cookie头"""
    cookies = {}
    
    # 分割多个cookie
    cookie_parts = set_cookie_header.split(', ')
    
    for part in cookie_parts:
        # 提取cookie名称和值
        match = re.match(r'([^=]+)=([^;]+)', part)
        if match:
            name = match.group(1).strip()
            value = match.group(2).strip()
            
            # 处理空值cookie（用于删除）
            if value != '""':
                cookies[name] = value
    
    return cookies
```

## 后续API调用

获得认证令牌后，所有需要认证的API调用都需要包含：

### 必需的Cookie

```http
Cookie: t={认证令牌}; _csrf_token={CSRF令牌}
```

### 必需的请求头

```http
X-Csrftoken: {CSRF令牌}
X-Device: {"platform":"web","os":"Windows 10","device":"Chrome 136.0.0.0","name":"","version":6310,"id":"{device_id}","channel":"website","campaign":"","websocket":""}
```



## 相关接口

- [轮询登录状态](./poll-login-status.md) - 获取用于验证的授权码
- [获取所有任务](../tasks/get-all-tasks.md) - 使用认证令牌获取任务数据
