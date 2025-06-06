# 获取用户信息

获取当前登录用户的详细信息。

## 接口信息

- **接口URL**: `https://api.dida365.com/api/v2/user/profile`
- **请求方法**: `GET`
- **认证要求**: 需要登录认证
- **所属平台**: 滴答清单

## 请求参数

无需参数，获取当前登录用户的信息。

## 响应格式

### 成功响应

```json
{
    "etimestamp": null,
    "username": "string",
    "siteDomain": "dida365.com",
    "createdCampaign": "string",
    "createdDeviceInfo": null,
    "filledPassword": true,
    "accountDomain": "string",
    "extenalId": "string",
    "email": "string",
    "verifiedEmail": true,
    "fakedEmail": false,
    "phone": null,
    "name": "string",
    "givenName": null,
    "familyName": null,
    "link": null,
    "picture": "string",
    "gender": "string",
    "locale": "zh_CN",
    "userCode": "string",
    "verCode": null,
    "verKey": null,
    "externalId": "string",
    "phoneWithoutCountryCode": null,
    "displayName": "string"
}
```

## 响应字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| etimestamp | null | 时间戳 |
| username | string | 用户名（通常是邮箱） |
| siteDomain | string | 站点域名 |
| createdCampaign | string | 创建活动 |
| createdDeviceInfo | null | 创建设备信息 |
| filledPassword | boolean | 是否已设置密码 |
| accountDomain | string | 账户域名 |
| extenalId | string | 外部ID |
| email | string | 邮箱地址 |
| verifiedEmail | boolean | 邮箱是否已验证 |
| fakedEmail | boolean | 是否为虚假邮箱 |
| phone | string/null | 手机号 |
| name | string | 姓名 |
| givenName | string/null | 名 |
| familyName | string/null | 姓 |
| link | string/null | 链接 |
| picture | string | 头像URL |
| gender | string | 性别（0-未知，1-男，2-女） |
| locale | string | 语言设置 |
| userCode | string | 用户代码 |
| verCode | string/null | 验证码 |
| verKey | string/null | 验证密钥 |
| externalId | string | 外部标识 |
| phoneWithoutCountryCode | string/null | 不含国家代码的手机号 |
| displayName | string | 显示名称 |



## 使用说明

1. 确保已完成认证获取会话
2. 直接调用接口即可获取当前用户信息
3. 返回的数据包含用户的完整个人资料信息
4. 头像URL可直接用于显示用户头像
5. 用户代码（userCode）是用户的唯一标识

## 应用场景

- **用户资料展示**: 在应用中显示用户的基本信息
- **头像显示**: 获取用户头像URL用于界面展示
- **用户身份验证**: 确认当前登录用户的身份
- **个人设置**: 获取用户的语言、性别等设置信息
- **账户管理**: 显示账户相关信息如邮箱验证状态


