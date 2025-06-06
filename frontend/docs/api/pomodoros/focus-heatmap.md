# 获取专注趋势热力图

获取指定日期范围内的专注趋势热力图数据。

## 接口信息

- **接口URL**: `https://api.dida365.com/api/v2/pomodoros/statistics/heatmap/{start_date}/{end_date}`
- **请求方法**: `GET`
- **认证要求**: 需要登录认证
- **所属平台**: 滴答清单

## 请求参数

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|--------|------|------|------|------|
| start_date | string | 是 | 开始日期，格式: YYYYMMDD | 20231201 |
| end_date | string | 是 | 结束日期，格式: YYYYMMDD | 20231207 |

## 响应格式

### 成功响应

```json
[
  {
    "duration": 0,
    "day": "20231126",
    "timezone": "Asia/Shanghai"
  },
  {
    "duration": 25,
    "day": "20231128",
    "timezone": "Asia/Shanghai"
  }
]
```

### 响应字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| duration | number | 专注时长（分钟） |
| day | string | 日期（YYYYMMDD格式） |
| timezone | string | 时区 |




