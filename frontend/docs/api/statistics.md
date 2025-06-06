# 获取用户排名统计

获取用户在滴答清单中的排名和基本统计信息。

## 接口信息

- **接口URL**: `https://api.dida365.com/api/v3/user/ranking`
- **请求方法**: `GET`
- **认证要求**: 需要登录认证
- **所属平台**: 滴答清单

## 请求参数

无需参数，使用当前认证会话。

## 响应格式

### 成功响应

```json
{
  "ranking": 85.6,
  "taskCount": 1250,
  "projectCount": 8,
  "dayCount": 365,
  "completedCount": 980,
  "score": 15420,
  "level": 12
}
```

## 响应字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| ranking | number | 排名百分比（你比X%的用户更勤奋） |
| taskCount | number | 总任务数量 |
| projectCount | number | 项目数量 |
| dayCount | number | 使用天数 |
| completedCount | number | 已完成任务数 |
| score | number | 成就值 |
| level | number | 账号等级 |




