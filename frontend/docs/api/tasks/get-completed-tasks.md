# 获取已完成/已放弃任务

获取用户的已完成或已放弃任务列表，支持分页获取。

## 接口信息

- **接口URL**: `https://api.dida365.com/api/v2/project/all/closed`
- **请求方法**: `GET`
- **认证要求**: 需要登录认证
- **所属平台**: 滴答清单

## 请求参数

### Query Parameters

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|--------|------|------|------|------|
| to | string | 否 | 分页参数，使用上次响应最后一个任务的completedTime | "2025-03-15T13:30:54.000+0000" |
| status | string | 否 | 任务状态，默认Completed | "Completed" 或 "Abandoned" |

### 状态参数说明

| 状态值 | 说明 |
|--------|------|
| Completed | 已完成的任务（默认） |
| Abandoned | 已放弃的任务 |

### 分页机制

**重要说明**: 此接口的分页机制需要严格按照以下步骤执行，否则无法获取全部数据。

**第一次请求（不携带to字段）**:
```
GET https://api.dida365.com/api/v2/project/all/closed?from=&status=Completed
```

**获取已放弃任务（第一次请求）**:
```
GET https://api.dida365.com/api/v2/project/all/closed?from=&status=Abandoned
```

**后续分页请求**:
```
GET https://api.dida365.com/api/v2/project/all/closed?from=&to=2025-03-15%2013:30:54&status=Completed
GET https://api.dida365.com/api/v2/project/all/closed?from=&to=2025-03-15%2013:30:54&status=Abandoned
```

**分页流程详解**:
1. **第一次请求**: 不携带`to`字段，直接请求
2. **获取分页参数**: 从响应中取最后一个任务的`completedTime`字段
3. **构造下次请求**: 将`completedTime`作为`to`参数
4. **重复请求**: 直到返回的任务数量少于50个为止

**to参数说明**:
- 使用上次响应最后一个任务的`completedTime`字段值（原始格式）
- 原始格式：`2025-03-15T13:30:54.000+0000`
- API转换格式：`2025-03-15 13:30:54`
- URL编码后：`2025-03-15%2013:30:54`
- **注意**: 传入原始的completedTime格式，API会自动转换为正确格式

**分页终止条件**:
- 当返回的任务数量少于50个时，表示已获取到最后一页
- 当返回空数组时，表示没有更多数据

## 响应格式

### 成功响应

返回已完成任务列表的原始数据：

```json
[
    {
        "id": "string",
        "projectId": "string",
        "sortOrder": 0,
        "title": "string",
        "content": "string",
        "desc": "string",
        "timeZone": "string",
        "isFloating": true,
        "isAllDay": true,
        "reminder": "string",
        "reminders": [
            {
                "id": "string",
                "trigger": "string"
            }
        ],
        "repeatFirstDate": "string",
        "exDate": [
            "string"
        ],
        "completedTime": "string",
        "completedUserId": 0,
        "repeatTaskId": "string",
        "priority": 0,
        "status": 0,
        "items": [
            "string"
        ],
        "progress": 0,
        "modifiedTime": "string",
        "etag": "string",
        "deleted": 0,
        "createdTime": "string",
        "creator": 0,
        "repeatFrom": "string",
        "attachments": [
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
                "stopwatchDuration": 0,
                "focuses": [
                    [
                        "string"
                    ]
                ]
            }
        ],
        "columnId": "string",
        "parentId": "string",
        "kind": "string",
        "pinnedTime": "string",
        "imgMode": 0,
        "startDate": "string",
        "dueDate": "string",
        "tags": [
            "string"
        ],
        "pomodoroSummaries": [
            {
                "userId": 0,
                "count": 0,
                "estimatedPomo": 0,
                "duration": 0
            }
        ],
        "repeatFlag": "string",
        "childIds": [
            "string"
        ]
    }
]
```



## 响应字段说明

### 核心字段

| 字段名 | 类型 | 说明 |
|--------|------|------|
| id | string | 任务唯一标识符 |
| projectId | string | 所属项目ID |
| title | string | 任务标题 |
| content | string | 任务内容 |
| completedTime | string | 完成时间（分页关键字段） |
| priority | number | 优先级 |
| status | number | 任务状态 |

### 时间字段

| 字段名 | 类型 | 说明 |
|--------|------|------|
| completedTime | string | 完成时间 |
| createdTime | string | 创建时间 |
| modifiedTime | string | 修改时间 |
| startDate | string | 开始日期 |
| dueDate | string | 截止日期 |

### 专注统计

| 字段名 | 类型 | 说明 |
|--------|------|------|
| focusSummaries | array | 专注统计摘要 |
| pomodoroSummaries | array | 番茄钟统计摘要 |


