# 获取专注时间分布

获取指定日期范围内按时间段分布的专注数据。

## 接口信息

- **接口URL**: `https://api.dida365.com/api/v2/pomodoros/statistics/dist/clockByDay/{start_date}/{end_date}`
- **请求方法**: `GET`
- **认证要求**: 需要登录认证
- **所属平台**: 滴答清单

## 请求参数

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|--------|------|------|------|------|
| start_date | string | 是 | 开始日期，格式: YYYYMMDD | 20250526 |
| end_date | string | 是 | 结束日期，格式: YYYYMMDD | 20250601 |

## 响应格式

### 成功响应

```json
[
    {
        "day": "20250526",
        "timezone": "Asia/Shanghai"
    },
    {
        "timeDurations": {
            "15": 60,
            "22": 60,
            "23": 60
        },
        "day": "20250601",
        "timezone": "Asia/Shanghai"
    }
]
```

### 响应字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| day | string | 日期（YYYYMMDD格式） |
| timezone | string | 时区 |
| timeDurations | object | 时间段专注分布（可选字段） |
| timeDurations.{hour} | number | 指定小时的专注时长（分钟），hour为24小时制 |




