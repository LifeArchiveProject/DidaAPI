# 获取用户信息

获取当前登录用户的基本信息。

## 接口信息

- **原始API**: `https://api.dida365.com/api/v2/user/profile`
- **方法**: `GET`
- **认证**: 需要登录认证

## 请求参数

无需参数，使用当前认证会话。

## 响应格式

### 成功响应

```json
{
  "username": "string",
  "email": "string",
  "picture": "string",
  "locale": "zh_CN",
  "userCode": "string",
  "timezone": "Asia/Shanghai",
  "nickname": "string",
  "phone": "string",
  "createdTime": "string",
  "lastLoginTime": "string",
  "premium": false,
  "subscriptionType": "string",
  "subscriptionExpiry": "string"
}
```

## 响应字段说明

| 字段 | 类型 | 描述 |
|------|------|------|
| username | string | 用户名 |
| email | string | 邮箱地址 |
| picture | string | 头像URL |
| locale | string | 语言设置 |
| userCode | string | 用户代码 |
| timezone | string | 时区设置 |
| nickname | string | 昵称 |
| phone | string | 手机号 |
| createdTime | string | 注册时间 |
| lastLoginTime | string | 最后登录时间 |
| premium | boolean | 是否为高级用户 |
| subscriptionType | string | 订阅类型 |
| subscriptionExpiry | string | 订阅到期时间 |




