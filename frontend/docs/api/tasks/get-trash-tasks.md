# 获取垃圾桶任务

获取垃圾桶中的任务列表。

## 接口信息

- **接口URL**: `https://api.dida365.com/api/v2/project/all/trash/page`
- **请求方法**: `GET`
- **认证要求**: 需要登录认证
- **所属平台**: 滴答清单

## 请求参数

### Query Parameters

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|--------|------|------|------|------|
| limit | number | 否 | 每页任务数量，默认50 | 50 |
| task_type | number | 否 | 任务类型，默认1 | 1 |

## 响应格式

### 成功响应

返回垃圾桶任务的原始数据：

```json
{
    "tasks": [
        {
            "id": "string",
            "projectId": "string",
            "sortOrder": 0,
            "title": "string",
            "startDate": "string",
            "dueDate": "string",
            "timeZone": "string",
            "isFloating": true,
            "isAllDay": true,
            "reminders": [
                {
                    "id": "string",
                    "trigger": "string"
                }
            ],
            "exDate": [
                "string"
            ],
            "priority": 0,
            "status": 0,
            "items": [
                "string"
            ],
            "modifiedTime": "string",
            "etag": "string",
            "deleted": 0,
            "createdTime": "string",
            "creator": 0,
            "attachments": [
                "string"
            ],
            "columnId": "string",
            "parentId": "string",
            "childIds": [
                "string"
            ],
            "kind": "string",
            "pinnedTime": "string",
            "imgMode": 0,
            "deletedBy": 0,
            "deletedTime": 0,
            "repeatFirstDate": "string",
            "repeatTaskId": "string",
            "repeatFrom": "string",
            "tags": [
                "string"
            ],
            "commentCount": 0,
            "focusSummaries": [
                {
                    "userId": 0,
                    "pomoCount": 0,
                    "estimatedPomo": 0,
                    "estimatedDuration": 0,
                    "pomoDuration": 0,
                    "stopwatchDuration": 0
                }
            ],
            "repeatFlag": "string",
            "pomodoroSummaries": [
                {
                    "userId": 0,
                    "count": 0,
                    "estimatedPomo": 0,
                    "duration": 0
                }
            ]
        }
    ],
    "next": 0
}
```



## 响应字段说明

### 响应结构

| 字段名 | 类型 | 说明 |
|--------|------|------|
| tasks | array | 垃圾桶任务列表 |
| next | number | 下一页标识 |

### 任务对象核心字段

| 字段名 | 类型 | 说明 |
|--------|------|------|
| id | string | 任务唯一标识符 |
| projectId | string | 所属项目ID |
| title | string | 任务标题 |
| status | number | 任务状态 |
| priority | number | 优先级 |
| deleted | number | 删除标志 |
| deletedBy | number | 删除者ID |
| deletedTime | number | 删除时间 |

### 时间字段

| 字段名 | 类型 | 说明 |
|--------|------|------|
| createdTime | string | 创建时间 |
| modifiedTime | string | 修改时间 |
| startDate | string | 开始日期 |
| dueDate | string | 截止日期 |


