# 获取本周习惯打卡统计

## 接口信息

- **接口路径**: `GET /habits/statistics/week/current`
- **接口描述**: 获取本周的习惯打卡统计信息
- **请求方式**: GET
- **认证要求**: 需要先完成微信登录获取认证会话

## 请求参数

无需参数

## 请求示例

```bash
curl -X GET "http://localhost:8000/habits/statistics/week/current"
```

## 响应格式

### 成功响应

```json
{
  "weekStart": "2023-12-04",
  "weekEnd": "2023-12-10",
  "totalHabits": 5,
  "completedDays": 4,
  "completionRate": 80.0,
  "dailyStats": [
    {
      "date": "2023-12-04",
      "dayOfWeek": "Monday",
      "completedHabits": 4,
      "totalHabits": 5,
      "completionRate": 80.0
    },
    {
      "date": "2023-12-05",
      "dayOfWeek": "Tuesday",
      "completedHabits": 5,
      "totalHabits": 5,
      "completionRate": 100.0
    }
  ],
  "habitDetails": [
    {
      "habitId": "habit123",
      "habitName": "早起",
      "targetDays": 7,
      "completedDays": 5,
      "completionRate": 71.4,
      "streak": 3,
      "dailyStatus": [
        {
          "date": "2023-12-04",
          "completed": true
        },
        {
          "date": "2023-12-05",
          "completed": true
        }
      ]
    }
  ]
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
  "message": "获取本周习惯打卡统计失败，请稍后重试"
}
```

## 响应字段说明

| 字段名 | 类型 | 描述 |
|--------|------|------|
| weekStart | string | 本周开始日期 |
| weekEnd | string | 本周结束日期 |
| totalHabits | integer | 总习惯数量 |
| completedDays | integer | 完成打卡的天数 |
| completionRate | float | 整体完成率（百分比） |
| dailyStats | array | 每日统计数据 |
| dailyStats[].date | string | 日期 |
| dailyStats[].dayOfWeek | string | 星期几 |
| dailyStats[].completedHabits | integer | 当日完成的习惯数 |
| dailyStats[].totalHabits | integer | 当日总习惯数 |
| dailyStats[].completionRate | float | 当日完成率 |
| habitDetails | array | 习惯详细信息 |
| habitDetails[].habitId | string | 习惯ID |
| habitDetails[].habitName | string | 习惯名称 |
| habitDetails[].targetDays | integer | 目标天数 |
| habitDetails[].completedDays | integer | 已完成天数 |
| habitDetails[].completionRate | float | 习惯完成率 |
| habitDetails[].streak | integer | 连续打卡天数 |
| habitDetails[].dailyStatus | array | 每日打卡状态 |

## 使用说明

1. **认证要求**: 需要先调用微信登录接口获取认证会话
2. **统计周期**: 统计当前自然周（周一到周日）的数据
3. **实时更新**: 数据实时更新，反映最新的打卡状态
4. **多维度统计**: 提供整体、每日、每个习惯的多维度统计

## 相关接口

- [获取所有习惯](../habits.md)
- [导出习惯数据](./export-habits.md)
- [微信登录流程](../auth/wechat-login-flow.md)

## 注意事项

- 需要先完成微信登录获取认证会话
- 统计数据基于当前自然周
- 完成率保留一位小数
- 连续打卡天数会在中断后重新计算
