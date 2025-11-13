# 执行番茄钟控制操作

透传滴答清单番茄钟批量操作接口，可执行开始、暂停、继续、结束等操作。

## 接口信息

- **接口URL**: `/pomodoros/focus/operations`
- **请求方法**: `POST`
- **认证要求**: 需要已成功设置滴答清单登录会话
- **所属平台**: 滴答清单

## 请求体

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| lastPoint | number | 是 | 最近一次操作返回的 `point`，用于保证状态递增 |
| opList | array | 是 | 番茄钟操作列表，可一次提交一个或多个操作 |

`opList` 中每个对象遵循滴答清单原生格式，关键字段如下：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | string | 是 | 操作记录ID，需唯一，可复用官方返回或自行生成 |
| oId | string | 是 | 当前番茄钟ID |
| oType | number | 是 | 对象类型，番茄钟固定为 `0` |
| op | string | 是 | 操作类型：`start`、`pause`、`continue`、`drop`、`exit` 等 |
| duration | number | 是 | 操作的番茄时长（分钟），如 `25` |
| firstFocusId | string | 是 | 首个番茄钟ID，通常与 `oId` 相同 |
| focusOnId | string | 否 | 关联任务ID，若无可留空字符串 |
| autoPomoLeft | number | 否 | 自动番茄剩余数量，保持与最新响应一致 |
| pomoCount | number | 否 | 已累计的番茄数 |
| manual | boolean | 否 | 是否为手动操作，Web 端默认 `true` |
| note | string | 否 | 备注，可留空 |
| time | string | 是 | 操作时间，ISO 字符串（示例：`2025-11-13T10:09:44.765+0000`） |

> ⚠️ **特别说明**  
> - 当番茄时长不足 5 分钟结束时，官方前端会发送 `drop` + `exit` 两个操作，用于提示“计时不足 5 分钟”。  
> - 建议始终复用官方接口返回的 ID、point 值，避免状态不同步。

## 任务绑定字段

将番茄与任务/清单/习惯关联时，需要同时携带下列字段：

| 字段 | 说明 |
|------|------|
| `focusOnId` | 关联对象 ID，例如任务 ID、清单 ID **（必填）** |
| `focusOnType` | 对象类型（常见值：`0`=任务、`1`=清单、`2`=习惯，可选） |
| `focusOnTitle` | 对象标题（可选） |

> 实际调用中，只要提供 `focusOnId` 即可完成绑定，其余字段属于补充信息。

对应响应体中的 `focusTasks`、`focusOnLogs` 字段。

## 请求示例

### 开始番茄钟

```json
{
  "lastPoint": 1760632928097,
  "opList": [
    {
      "id": "6915ae6838b6e20c76868c45",
      "oId": "6915ae6838b6e20c76868c44",
      "oType": 0,
      "op": "start",
      "duration": 25,
      "firstFocusId": "6915ae6838b6e20c76868c44",
      "focusOnId": "",
      "autoPomoLeft": 5,
      "pomoCount": 1,
      "manual": true,
      "note": "",
      "time": "2025-11-13T10:09:44.765+0000"
    }
  ]
}
```

### 暂停番茄钟

```json
{
  "lastPoint": 1763028586178,
  "opList": [
    {
      "id": "6915aef838b6e20c76868c48",
      "oId": "6915ae6838b6e20c76868c44",
      "oType": 0,
      "op": "pause",
      "duration": 25,
      "firstFocusId": "6915ae6838b6e20c76868c44",
      "focusOnId": "",
      "autoPomoLeft": 5,
      "pomoCount": 1,
      "manual": true,
      "note": "",
      "time": "2025-11-13T10:12:08.069+0000"
    }
  ]
}
```

### 继续番茄钟

```json
{
  "lastPoint": 1763028729470,
  "opList": [
    {
      "id": "6915af5638b6e20c76868c4c",
      "oId": "6915ae6838b6e20c76868c44",
      "oType": 0,
      "op": "continue",
      "duration": 25,
      "firstFocusId": "6915ae6838b6e20c76868c44",
      "focusOnId": "",
      "autoPomoLeft": 5,
      "pomoCount": 1,
      "manual": true,
      "note": "",
      "time": "2025-11-13T10:13:42.178+0000"
    }
  ]
}
```

### 不足 5 分钟结束（drop + exit）

```json
{
  "lastPoint": 1763028864202,
  "opList": [
    {
      "id": "6915af8738b6e20c76868c52",
      "oId": "6915ae6838b6e20c76868c44",
      "oType": 0,
      "op": "drop",
      "duration": 0,
      "firstFocusId": "6915ae6838b6e20c76868c44",
      "focusOnId": "",
      "autoPomoLeft": 5,
      "pomoCount": 1,
      "manual": true,
      "note": "",
      "time": "2025-11-13T10:14:31.897+0000"
    },
    {
      "id": "6915af8738b6e20c76868c53",
      "oId": "6915ae6838b6e20c76868c44",
      "oType": 0,
      "op": "exit",
      "duration": 0,
      "firstFocusId": "6915ae6838b6e20c76868c44",
      "focusOnId": "",
      "autoPomoLeft": 0,
      "pomoCount": 0,
      "manual": true,
      "note": "",
      "time": "2025-11-13T10:14:31.989+0000"
    }
  ]
}
```

## 成功响应

接口直接返回滴答清单原始响应，包含最新的 `point` 值、当前番茄钟状态及更新记录。例如：

```json
{
  "point": 1763028729470,
  "current": {
    "id": "6915ae6838b6e20c76868c44",
    "type": 0,
    "status": 1,
    "valid": true,
    "exited": false,
    "firstId": "6915ae6838b6e20c76868c44",
    "firstDid": "6915add138b6e20c76868ad8",
    "duration": 25,
    "startTime": "2025-11-13T10:09:44.765+0000",
    "endTime": "2025-11-13T10:34:44.765+0000",
    "autoPomoLeft": 5,
    "pomoCount": 1,
    "focusBreak": {},
    "focusOnLogs": [
      {
        "id": "",
        "time": "2025-11-13T10:09:44.765+0000"
      }
    ],
    "pauseLogs": [
      {
        "type": 0,
        "time": "2025-11-13T10:12:08.069+0000"
      }
    ],
    "focusTasks": [
      {
        "id": "",
        "startTime": "2025-11-13T10:09:44.765+0000",
        "endTime": "2025-11-13T10:12:08.069+0000"
      }
    ],
    "etag": "clvt5648",
    "autoStart": false
  },
  "updates": [
    {
      "id": "6915ae6838b6e20c76868c44",
      "type": 0,
      "status": 1,
      "valid": true,
      "exited": false,
      "firstId": "6915ae6838b6e20c76868c44",
      "firstDid": "6915add138b6e20c76868ad8",
      "duration": 25,
      "startTime": "2025-11-13T10:09:44.765+0000",
      "endTime": "2025-11-13T10:34:44.765+0000",
      "autoPomoLeft": 5,
      "pomoCount": 1,
      "focusBreak": {},
      "focusOnLogs": [
        {
          "id": "",
          "time": "2025-11-13T10:09:44.765+0000"
        }
      ],
      "pauseLogs": [
        {
          "type": 0,
          "time": "2025-11-13T10:12:08.069+0000"
        }
      ],
      "focusTasks": [
        {
          "id": "",
          "startTime": "2025-11-13T10:09:44.765+0000",
          "endTime": "2025-11-13T10:12:08.069+0000"
        }
      ],
      "etag": "clvt5648",
      "autoStart": false
    }
  ]
}
```

## 错误响应

若认证信息缺失或第三方接口返回错误，接口会返回错误描述，例如：

```json
{
  "error": "no_auth_session",
  "message": "未设置认证会话，请先完成微信登录"
}
```

