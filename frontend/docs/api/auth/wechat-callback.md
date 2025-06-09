# 微信登录回调处理

## 接口信息

- **接口路径**: `GET /auth/wechat/callback`
- **接口描述**: 处理微信扫码后的回调，提取code参数
- **请求方式**: GET
- **认证要求**: 无需认证

## 请求参数

### Query参数

| 参数名 | 类型 | 必填 | 描述 | 示例值 |
|--------|------|------|------|--------|
| code | string | 是 | 微信返回的授权码 | `001uZIkl2urXGf4qrmml2mAIWz4uZIkW` |
| state | string | 否 | 状态参数 | `Lw==` |

## 请求示例

```bash
curl -X GET "http://localhost:8000/auth/wechat/callback?code=001uZIkl2urXGf4qrmml2mAIWz4uZIkW&state=Lw=="
```

## 响应格式

### 成功响应

```json
{
  "message": "微信登录成功",
  "code": "001uZIkl2urXGf4qrmml2mAIWz4uZIkW",
  "state": "Lw==",
  "login_result": {
    "success": true,
    "message": "微信登录验证成功",
    "user_info": {
      "username": "用户名",
      "email": "user@example.com"
    },
    "session_info": {
      "auth_token": "43A001113F9610FFC85AA97B18A297A4...",
      "csrf_token": "rMwhKGWevLOhHIhFv6hHjAziGDbkpnuY..."
    }
  },
  "next_step": "用户已成功登录，可以访问受保护的资源"
}
```

### 失败响应

```json
{
  "message": "微信登录失败",
  "code": "001uZIkl2urXGf4qrmml2mAIWz4uZIkW",
  "state": "Lw==",
  "error": "验证失败"
}
```

## 使用说明

1. **回调处理**: 这个接口用于演示微信回调的处理流程
2. **自动验证**: 接收到回调后会自动进行登录验证
3. **会话建立**: 验证成功后会建立用户会话
4. **实际使用**: 在实际使用中，微信会重定向到配置的redirect_uri

## 相关接口

- [微信登录流程](./wechat-login-flow.md)
- [获取微信二维码](./get-wechat-qrcode.md)
- [轮询登录状态](./poll-login-status.md)
- [验证微信登录](./validate-wechat-login.md)

## 注意事项

- 这是微信OAuth流程的最后一步
- code参数只能使用一次，有效期很短
- 成功后会自动建立认证会话
- 可以直接用于后续API调用
