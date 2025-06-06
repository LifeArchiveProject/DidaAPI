# 获取微信登录二维码

获取微信扫码登录的二维码，这是微信登录流程的第一步。

## 接口信息

- **接口URL**: `https://open.weixin.qq.com/connect/qrconnect`
- **请求方法**: `GET`
- **认证要求**: 无需认证
- **所属平台**: 微信开放平台

## 请求参数

### Query Parameters

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| appid | string | 是 | 微信应用ID |
| redirect_uri | string | 是 | 授权后重定向的回调地址 |
| response_type | string | 是 | 返回类型，固定值：`code` |
| scope | string | 是 | 应用授权作用域，固定值：`snsapi_login` |
| state | string | 否 | 重定向后会带上state参数，开发者可以填写a-zA-Z0-9的参数值，最多128字节 |

## 完整请求示例

```http
GET https://open.weixin.qq.com/connect/qrconnect?appid={appid}&redirect_uri={redirect_uri}&response_type=code&scope=snsapi_login&state={state} HTTP/1.1
Host: open.weixin.qq.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7
Accept-Encoding: gzip, deflate, br, zstd
```

## 响应格式

### 成功响应

**状态码**: `200 OK`

**Content-Type**: `text/html; charset=utf-8`

**响应体**: HTML页面，包含二维码图片

### 关键HTML结构

```html
<!DOCTYPE html>
<html>
<head>
    <title>微信登录</title>
</head>
<body>
    <!-- 其他HTML内容 -->
    <img class="qrcode lightBorder js_qrcode_img" src="/connect/qrcode/{qr_code_key}">
    <!-- 其他HTML内容 -->
</body>
</html>
```

## 响应解析

### 提取二维码密钥

从响应HTML中提取二维码图片的src属性：

```javascript
// 正则表达式匹配
const pattern = /<img[^>]*class="[^"]*qrcode[^"]*"[^>]*src="([^"]*)"/;
const match = html.match(pattern);

if (match) {
    const srcUrl = match[1]; // "/connect/qrcode/{qr_code_key}"
    const qrCodeKey = srcUrl.split('/').pop(); // "{qr_code_key}"
}
```

### 构建完整二维码URL

```javascript
const qrCodeUrl = `https://open.weixin.qq.com${srcUrl}`;
// 结果: https://open.weixin.qq.com/connect/qrcode/{qr_code_key}
```

## 响应头示例

```http
HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
Cache-Control: no-cache, must-revalidate
Content-Encoding: gzip
Content-Length: 17543
X-Wx-Fj: 001,018,0000001024
```

## 后续步骤

获取二维码后，需要：

1. 显示二维码供用户扫描
2. 使用二维码密钥进行[轮询登录状态](./poll-login-status.md)
3. 获取授权码后进行[验证微信登录](./validate-wechat-login.md)
