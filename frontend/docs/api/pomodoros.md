# 获取番茄专注概览

获取番茄专注的概览统计信息（桌面版）。

## 接口信息

- **接口URL**: `https://api.dida365.com/api/v2/pomodoros/statistics/generalForDesktop`
- **请求方法**: `GET`
- **认证要求**: 需要登录认证
- **所属平台**: 滴答清单

## 请求参数

无需参数，使用当前认证会话。

## 响应格式

### 成功响应

```json
{
  "todayPomoCount": 6,
  "todayPomoDuration": 150,
  "totalPomoCount": 450,
  "totalPomoDuration": 11250
}
```

## 响应字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| todayPomoCount | number | 今日番茄数量 |
| todayPomoDuration | number | 今日专注时长（分钟） |
| totalPomoCount | number | 总番茄数量 |
| totalPomoDuration | number | 总专注时长（分钟） |




