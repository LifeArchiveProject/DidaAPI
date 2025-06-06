# 密码登录

使用用户名（邮箱或手机号）和密码进行滴答清单登录认证。

## 接口信息

- **接口URL**: `https://api.dida365.com/api/v2/user/signon?wc=true&remember=true`
- **请求方法**: `POST`
- **认证要求**: 无需认证
- **所属平台**: 滴答清单

## 请求参数

### 请求体

| 参数名   | 类型   | 必需 | 说明                     |
|----------|--------|------|--------------------------|
| username | string | 是   | 登录账户（邮箱或手机号） |
| password | string | 是   | 登录密码                 |

### 请求示例

```json
{
  "username": "string",
  "password": "string"
}
```

## 响应格式

### 成功响应

**HTTP状态码**: `200 OK`

```json
{
  "token": "string",
  "userId": "string",
  "userCode": "string",
  "username": "string",
  "teamPro": false,
  "proStartDate": "string",
  "proEndDate": "string",
  "subscribeType": "string",
  "subscribeFreq": "string",
  "needSubscribe": false,
  "freq": "string",
  "inboxId": "string",
  "teamUser": false,
  "activeTeamUser": false,
  "freeTrial": false,
  "gracePeriod": false,
  "pro": true,
  "ds": false
}
```



## 响应字段说明

| 字段名           | 类型    | 说明                   |
|------------------|---------|------------------------|
| token            | string  | 认证令牌，用于后续API调用 |
| userId           | string  | 用户唯一ID             |
| userCode         | string  | 用户代码               |
| username         | string  | 用户名（邮箱或手机号） |
| teamPro          | boolean | 是否为团队专业版       |
| proStartDate     | string  | 专业版开始日期         |
| proEndDate       | string  | 专业版结束日期         |
| subscribeType    | string  | 订阅类型（如：wxpay_subscribe） |
| subscribeFreq    | string  | 订阅频率（如：Month）   |
| needSubscribe    | boolean | 是否需要订阅           |
| freq             | string  | 频率                   |
| inboxId          | string  | 默认任务添加清单ID     |
| teamUser         | boolean | 是否为团队用户         |
| activeTeamUser   | boolean | 是否为活跃团队用户     |
| freeTrial        | boolean | 是否为免费试用         |
| gracePeriod      | boolean | 是否在宽限期           |
| pro              | boolean | 是否为专业版           |
| ds               | boolean | 数据同步状态           |