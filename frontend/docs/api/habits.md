# 获取所有习惯

获取当前用户的所有习惯列表。

## 接口信息

- **接口URL**: `https://api.dida365.com/api/v2/habits`
- **请求方法**: `GET`
- **认证要求**: 需要登录认证
- **所属平台**: 滴答清单

## 请求参数

无需参数，使用当前认证会话。

## 响应格式

### 成功响应

```json
[
  {
    "id": "string",
    "name": "string",
    "iconRes": "string",
    "color": "string",
    "status": 1,
    "encouragement": "string",
    "totalCheckIns": 0,
    "createdTime": "string",
    "modifiedTime": "string",
    "type": "string",
    "goal": 0.0
  },
  {
    "id": "string",
    "name": "string",
    "iconRes": "string",
    "color": "string",
    "status": 0,
    "encouragement": "string",
    "totalCheckIns": 0,
    "createdTime": "string",
    "modifiedTime": "string",
    "type": "string",
    "goal": 0.0
  }
]
```

## 响应字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| id | string | 习惯ID |
| name | string | 习惯名称 |
| iconRes | string | 图标资源名称 |
| color | string | 习惯颜色（十六进制） |
| status | number | 状态（0=未完成，1=已完成） |
| encouragement | string | 激励语句 |
| totalCheckIns | number | 总打卡次数 |
| createdTime | string | 创建时间 |
| modifiedTime | string | 修改时间 |
| type | string | 习惯类型（daily/weekly等） |
| goal | number | 目标值 |






