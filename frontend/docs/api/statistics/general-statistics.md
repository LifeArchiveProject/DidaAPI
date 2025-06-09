# 获取通用统计信息

## 接口信息

- **接口路径**: `GET /statistics/general`
- **接口描述**: 获取概览、成就值、趋势等通用统计信息
- **请求方式**: GET
- **认证要求**: 需要先完成微信登录获取认证会话

## 请求参数

无需参数

## 请求示例

```bash
curl -X GET "http://localhost:8000/statistics/general"
```

## 响应格式

### 成功响应

```json
{
  "score": 1250,
  "level": 5,
  "yesterdayCompletedCount": 8,
  "todayCompletedCount": 12,
  "totalCompletedCount": 1580,
  "todayPomoCount": 6,
  "yesterdayPomoCount": 4,
  "totalPomoCount": 320,
  "todayFocusTime": 150,
  "yesterdayFocusTime": 100,
  "totalFocusTime": 8000,
  "targetPomoCount": 8,
  "targetFocusTime": 200
}
```

### 错误响应

#### 未认证

```json
{
  "error": "no_auth_session",
  "message": "未设置认证会话，请先完成微信登录"
}
```

#### 服务错误

```json
{
  "error": "service_error",
  "message": "获取通用统计信息失败，请稍后重试"
}
```

## 响应字段说明

| 字段名 | 类型 | 描述 |
|--------|------|------|
| score | integer | 成就值 |
| level | integer | 账号等级 |
| yesterdayCompletedCount | integer | 昨日完成任务数 |
| todayCompletedCount | integer | 今日完成任务数 |
| totalCompletedCount | integer | 总完成任务数 |
| todayPomoCount | integer | 今日番茄数 |
| yesterdayPomoCount | integer | 昨日番茄数 |
| totalPomoCount | integer | 总番茄数 |
| todayFocusTime | integer | 今日专注时长（分钟） |
| yesterdayFocusTime | integer | 昨日专注时长（分钟） |
| totalFocusTime | integer | 总专注时长（分钟） |
| targetPomoCount | integer | 目标番茄数 |
| targetFocusTime | integer | 目标专注时长（分钟） |

## 使用说明

1. **认证要求**: 需要先调用微信登录接口获取认证会话
2. **统计范围**: 包含任务完成和番茄专注的综合统计
3. **时间维度**: 提供昨日、今日和总计三个维度的数据
4. **目标对比**: 包含目标设置，便于进度对比

## 相关接口

- [获取用户排名统计](../statistics.md)
- [获取任务统计信息](./task-statistics.md)
- [获取番茄专注概览](../pomodoros.md)
- [微信登录流程](../auth/wechat-login-flow.md)

## 注意事项

- 需要先完成微信登录获取认证会话
- 时间以分钟为单位
- 数据实时更新
- 成就值和等级基于用户活跃度计算
