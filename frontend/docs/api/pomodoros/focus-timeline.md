# 获取专注记录时间线

获取专注记录的时间线数据，支持分页获取历史记录。

## 接口信息

- **接口URL**: `https://api.dida365.com/api/v2/pomodoros/timeline`
- **请求方法**: `GET`
- **认证要求**: 需要登录认证
- **所属平台**: 滴答清单

## 请求参数

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|--------|------|------|------|------|
| to | string | 否 | 分页参数：上一页最后一条记录的startTime，用于获取更早的数据 | 2025-04-22T08:43:31.000+0000 |

## 响应格式

### 成功响应

```json
[
    {
        "id": "string",
        "tasks": [
            {
                "taskId": "string",
                "title": "string",
                "projectName": "string",
                "startTime": "2025-04-22T08:43:31.000+0000",
                "endTime": "2025-04-22T09:38:58.000+0000"
            }
        ],
        "startTime": "2025-04-22T08:43:31.000+0000",
        "endTime": "2025-04-22T09:38:58.000+0000",
        "pauseDuration": 0,
        "etag": "string",
        "type": 1,
        "added": false
    }
]
```

### 响应字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| id | string | 专注记录ID |
| tasks | array | 关联的任务列表 |
| tasks[].taskId | string | 任务ID |
| tasks[].title | string | 任务标题 |
| tasks[].projectName | string | 项目名称 |
| tasks[].startTime | string | 任务开始时间 |
| tasks[].endTime | string | 任务结束时间 |
| startTime | string | 专注开始时间 |
| endTime | string | 专注结束时间 |
| pauseDuration | number | 暂停时长（毫秒） |
| etag | string | 版本标识 |
| type | number | 专注类型（0=番茄专注，1=正计时专注） |
| added | boolean | 是否已添加 |

## 分页说明

1. **首次请求**：不传 `to` 参数，获取最新的专注记录（约31条）
2. **获取更多**：使用上一页最后一条记录的 `startTime` 作为 `to` 参数
3. **时间格式**：`to` 参数使用ISO 8601格式，如 `2025-04-22T08:43:31.000+0000`
4. **自动转换**：系统会自动将时间转换为时间戳并调整时区




