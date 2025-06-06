# 获取所有任务

获取当前用户的所有任务列表，包括任务详情、状态、优先级等信息。

## 接口信息

- **接口URL**: `https://api.dida365.com/api/v2/batch/check/0`
- **请求方法**: `GET`
- **认证要求**: 需要登录认证
- **所属平台**: 滴答清单

## 认证要求

此接口需要完整的认证信息，包括：

### 必需的Cookie
```http
Cookie: t={auth_token}; _csrf_token={csrf_token}; AWSALB={load_balancer_cookie}; AWSALBCORS={load_balancer_cookie}
```

### 必需的请求头
```http
Accept: application/json, text/plain, */*
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7
Cache-Control: no-cache
Origin: https://dida365.com
Pragma: no-cache
Referer: https://dida365.com/
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36
X-Csrftoken: {csrf_token}
X-Device: {"platform":"web","os":"Windows 10","device":"Chrome 136.0.0.0","name":"","version":6310,"id":"{device_id}","channel":"website","campaign":"","websocket":""}
Hl: zh_CN
X-Tz: Asia/Shanghai
Traceid: {trace_id}
```

## 完整请求示例

```http
GET https://api.dida365.com/api/v2/batch/check/0 HTTP/1.1
Host: api.dida365.com
Accept: application/json, text/plain, */*
Accept-Encoding: gzip, deflate, br, zstd
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7
Cache-Control: no-cache
Cookie: t={auth_token}; _csrf_token={csrf_token}
Hl: zh_CN
Origin: https://dida365.com
Pragma: no-cache
Referer: https://dida365.com/
Traceid: {trace_id}
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36
X-Csrftoken: {csrf_token}
X-Device: {"platform":"web","os":"Windows 10","device":"Chrome 136.0.0.0","name":"","version":6310,"id":"{device_id}","channel":"website","campaign":"","websocket":"{websocket_id}"}
X-Tz: Asia/Shanghai
```

## 响应格式

### 成功响应

**状态码**: `200 OK`

**Content-Type**: `application/json;charset=UTF-8`

### 响应体结构

```json
{
    "checkPoint": 0,
    "syncTaskBean": {
        "update": [
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
                "exDate": [
                    "string"
                ],
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
                    {
                        "id": "string",
                        "refId": "string",
                        "path": "string",
                        "size": 0,
                        "fileName": "string",
                        "fileType": "string",
                        "status": 0,
                        "createdTime": "string"
                    }
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
                "kind": "string",
                "imgMode": 0,
                "startDate": "string",
                "dueDate": "string",
                "repeatFlag": "string",
                "pomodoroSummaries": [
                    {
                        "userId": 0,
                        "count": 0,
                        "estimatedPomo": 0,
                        "duration": 0
                    }
                ],
                "childIds": [
                    "string"
                ],
                "pinnedTime": "string",
                "repeatFirstDate": "string",
                "tags": [
                    "string"
                ],
                "parentId": "string",
                "deletedBy": 0,
                "deletedTime": 0
            }
        ],
        "tagUpdate": [
            "string"
        ],
        "delete": [
            "string"
        ],
        "add": [
            "string"
        ],
        "empty": true
    },
    "projectProfiles": [
        {
            "id": "string",
            "name": "string",
            "isOwner": true,
            "color": "string",
            "sortOrder": 0,
            "sortOption": {
                "groupBy": "string",
                "orderBy": "string"
            },
            "sortType": "string",
            "userCount": 0,
            "etag": "string",
            "modifiedTime": "string",
            "inAll": true,
            "showType": null,
            "muted": true,
            "reminderType": null,
            "closed": null,
            "transferred": null,
            "groupId": null,
            "viewMode": "string",
            "notificationOptions": [
                "string"
            ],
            "teamId": null,
            "permission": "string",
            "kind": "string",
            "timeline": {
                "range": null,
                "sortType": "string",
                "sortOption": {
                    "groupBy": "string",
                    "orderBy": "string"
                }
            },
            "needAudit": true,
            "barcodeNeedAudit": true,
            "openToTeam": true,
            "teamMemberPermission": null,
            "source": 0
        }
    ],
    "projectGroups": [
        "string"
    ],
    "filters": null,
    "tags": [
        "string"
    ],
    "syncTaskOrderBean": {
        "taskOrderByDate": {},
        "taskOrderByPriority": {},
        "taskOrderByProject": {}
    },
    "syncOrderBean": {
        "orderByType": {
            "taskPinned": {
                "{project_id_1}": {
                    "changed": [
                        {
                            "id": "string",
                            "order": 0,
                            "type": 0
                        }
                    ],
                    "deleted": [
                        {
                            "id": "string",
                            "order": 0,
                            "type": 0
                        }
                    ]
                },
                "{project_id_2}": {
                    "changed": [
                        {
                            "id": "string",
                            "order": 0,
                            "type": 0
                        }
                    ],
                    "deleted": [
                        {
                            "id": "string",
                            "order": 0,
                            "type": 0
                        }
                    ]
                }
            }
        }
    },
    "syncOrderBeanV3": {
        "orderByType": {}
    },
    "inboxId": "string",
    "checks": null,
    "remindChanges": [
        "string"
    ]
}
```

## 响应字段说明

### 根级字段

| 字段名 | 类型 | 说明 |
|--------|------|------|
| checkPoint | number | 检查点 |
| syncTaskBean | object | 任务同步数据 |
| projectProfiles | array | 项目配置列表 |
| projectGroups | array | 项目分组 |
| filters | null | 过滤器 |
| tags | array | 标签列表 |
| syncTaskOrderBean | object | 任务排序数据 |
| syncOrderBean | object | 排序数据 |
| syncOrderBeanV3 | object | 排序数据V3 |
| inboxId | string | 收件箱ID |
| checks | null | 检查项 |
| remindChanges | array | 提醒变更 |

### 任务字段 (syncTaskBean.update)

| 字段名 | 类型 | 说明 |
|--------|------|------|
| id | string | 任务唯一标识符 |
| projectId | string | 所属项目ID |
| sortOrder | number | 排序顺序 |
| title | string | 任务标题 |
| content | string | 任务内容 |
| desc | string | 任务描述 |
| timeZone | string | 时区 |
| isFloating | boolean | 是否浮动时间 |
| isAllDay | boolean | 是否全天任务 |
| reminder | string | 提醒设置 |
| reminders | array | 提醒列表 |
| exDate | array | 排除日期 |
| repeatTaskId | string | 重复任务ID |
| priority | number | 优先级 |
| status | number | 任务状态 |
| items | array | 子项目 |
| progress | number | 完成进度 |
| modifiedTime | string | 修改时间 |
| etag | string | 实体标签 |
| deleted | number | 删除状态 |
| createdTime | string | 创建时间 |
| creator | number | 创建者ID |
| repeatFrom | string | 重复来源 |
| attachments | array | 附件列表 |
| commentCount | number | 评论数量 |
| focusSummaries | array | 专注摘要 |
| columnId | string | 列ID |
| kind | string | 类型 |
| imgMode | number | 图片模式 |
| startDate | string | 开始日期 |
| dueDate | string | 截止日期 |
| repeatFlag | string | 重复标志 |
| pomodoroSummaries | array | 番茄钟摘要 |
| childIds | array | 子任务ID列表 |
| pinnedTime | string | 置顶时间 |
| repeatFirstDate | string | 首次重复日期 |
| tags | array | 标签列表 |
| parentId | string | 父任务ID |
| deletedBy | number | 删除者ID |
| deletedTime | number | 删除时间 |

### 项目配置字段 (projectProfiles)

| 字段名 | 类型 | 说明 |
|--------|------|------|
| id | string | 项目ID |
| name | string | 项目名称 |
| isOwner | boolean | 是否为所有者 |
| color | string | 项目颜色 |
| sortOrder | number | 排序顺序 |
| sortOption | object | 排序选项 |
| sortType | string | 排序类型 |
| userCount | number | 用户数量 |
| etag | string | 实体标签 |
| modifiedTime | string | 修改时间 |
| inAll | boolean | 是否在全部中显示 |
| showType | null | 显示类型 |
| muted | boolean | 是否静音 |
| reminderType | null | 提醒类型 |
| closed | null | 是否关闭 |
| transferred | null | 是否转移 |
| groupId | null | 分组ID |
| viewMode | string | 查看模式 |
| notificationOptions | array | 通知选项 |
| teamId | null | 团队ID |
| permission | string | 权限 |
| kind | string | 类型 |
| timeline | object | 时间线配置 |
| needAudit | boolean | 是否需要审核 |
| barcodeNeedAudit | boolean | 条码是否需要审核 |
| openToTeam | boolean | 是否对团队开放 |
| teamMemberPermission | null | 团队成员权限 |
| source | number | 来源 |

### 附件字段 (attachments)

| 字段名 | 类型 | 说明 |
|--------|------|------|
| id | string | 附件ID |
| refId | string | 引用ID |
| path | string | 文件路径 |
| size | number | 文件大小 |
| fileName | string | 文件名 |
| fileType | string | 文件类型 |
| status | number | 状态 |
| createdTime | string | 创建时间 |

### 专注摘要字段 (focusSummaries)

| 字段名 | 类型 | 说明 |
|--------|------|------|
| userId | number | 用户ID |
| pomoCount | number | 番茄钟数量 |
| estimatedPomo | number | 预估番茄钟 |
| estimatedDuration | number | 预估时长 |
| pomoDuration | number | 番茄钟时长 |
| stopwatchDuration | number | 秒表时长 |
| focuses | array | 专注记录 |



## 相关接口

- [验证微信登录](../auth/validate-wechat-login.md) - 获取认证令牌
- [创建任务](./create-task.md) - 创建新任务
- [更新任务](./update-task.md) - 更新任务信息
