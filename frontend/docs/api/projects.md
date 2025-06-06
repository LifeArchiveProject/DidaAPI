# 获取清单列表

获取用户的所有清单列表。

## 接口信息

- **接口URL**: `https://api.dida365.com/api/v2/projects`
- **请求方法**: `GET`
- **认证要求**: 需要登录认证
- **所属平台**: 滴答清单

## 请求参数

无需参数，使用当前认证会话。

## 响应格式

### 成功响应
```json
[
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
]
```

## 响应字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | string | 清单唯一标识符 |
| `name` | string | 清单名称 |
| `isOwner` | boolean | 是否为拥有者 |
| `color` | string | 清单颜色 |
| `sortOrder` | number | 自定义排序值 |
| `sortOption` | object | 排序选项配置 |
| `sortType` | string | 排序类型 |
| `userCount` | number | 用户数量 |
| `etag` | string | 实体标签 |
| `modifiedTime` | string | 修改时间 |
| `inAll` | boolean | 是否在全部清单中显示 |
| `showType` | any | 显示类型 |
| `muted` | boolean | 是否静音 |
| `reminderType` | any | 提醒类型 |
| `closed` | any | 关闭状态 |
| `transferred` | any | 转移状态 |
| `groupId` | string/null | 分组ID |
| `viewMode` | string | 视图模式 |
| `notificationOptions` | array | 通知选项 |
| `teamId` | string/null | 团队ID |
| `permission` | string | 权限类型 |
| `kind` | string | 清单类型 |
| `timeline` | object | 时间线配置 |
| `needAudit` | boolean | 是否需要审核 |
| `barcodeNeedAudit` | boolean | 条码是否需要审核 |
| `openToTeam` | boolean | 是否对团队开放 |
| `teamMemberPermission` | any | 团队成员权限 |
| `source` | number | 来源标识 |


