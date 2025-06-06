# 轮询微信登录状态

通过长轮询检查用户是否已扫码并确认微信登录。

## 接口信息

- **接口URL**: `https://long.open.weixin.qq.com/connect/l/qrconnect`
- **请求方法**: `GET`
- **认证要求**: 无需认证
- **所属平台**: 微信开放平台

## 请求参数

### Query Parameters

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| uuid | string | 是 | 二维码密钥，从获取二维码接口中提取的16位字符串 |
| _ | number | 是 | 时间戳，用于防止缓存，格式：毫秒级时间戳 |

## 完整请求示例

```http
GET https://long.open.weixin.qq.com/connect/l/qrconnect?uuid={qr_code_key}&_={timestamp} HTTP/1.1
Host: long.open.weixin.qq.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36
Accept: */*
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8
Referer: https://open.weixin.qq.com/
```

## 响应格式

### 响应类型

**Content-Type**: `text/javascript; charset=utf-8`

**响应体**: JavaScript代码片段

### 状态码说明

响应中包含 `window.wx_errcode` 表示不同的状态：

| errcode | 说明 | 后续操作 |
|---------|------|----------|
| 404 | 等待扫码 | 继续轮询 |
| 403 | 已扫码，等待用户确认 | 继续轮询 |
| 405 | 登录成功，获得授权码 | 停止轮询，提取授权码 |
| 408 | 二维码已过期 | 停止轮询，重新获取二维码 |
| 400 | 二维码已失效 | 停止轮询，重新获取二维码 |

## 响应示例

### 等待扫码 (errcode=404)
```javascript
window.wx_errcode=404;window.wx_code='';
```

### 已扫码等待确认 (errcode=403)
```javascript
window.wx_errcode=403;window.wx_code='';
```

### 登录成功 (errcode=405)
```javascript
window.wx_errcode=405;window.wx_code='{authorization_code}';
```

### 二维码过期 (errcode=408)
```javascript
window.wx_errcode=408;window.wx_code='';
```

## 响应解析

### 提取状态码和授权码

```javascript
// 解析响应文本
function parseWeChatResponse(responseText) {
    const errcodeMatch = responseText.match(/window\.wx_errcode\s*=\s*(\d+)/);
    const codeMatch = responseText.match(/window\.wx_code\s*=\s*'([^']*)'/);
    
    return {
        errcode: errcodeMatch ? parseInt(errcodeMatch[1]) : null,
        code: codeMatch ? codeMatch[1] : ''
    };
}
```



## 相关接口

- [获取微信二维码](./get-wechat-qrcode.md) - 获取用于轮询的二维码密钥
- [验证微信登录](./validate-wechat-login.md) - 使用获得的授权码进行登录验证
