# 番茄钟自动操作接口

为避免手动拼装 `focusOp` 请求体，本项目新增了一组封装接口，会根据本地缓存状态自动补齐滴答清单所需字段。

## 接口列表

| 方法 | 路径 | 说明 |
|------|------|------|
| `GET` | `/pomodoros/focus/current` | 查询当前番茄状态（不发送任何操作，返回滴答 `current` 原始数据） |
| `GET` | `/pomodoros/focus/start` | 生成 `start` 操作，自动创建 `id`、`firstFocusId`、`oId` 等字段；可通过 query 绑定任务（`focusOnId`/`focusOnType`/`focusOnTitle`） |
| `GET` | `/pomodoros/focus/pause` | 生成 `pause` 操作 |
| `GET` | `/pomodoros/focus/continue` | 生成 `continue` 操作 |
| `GET` | `/pomodoros/focus/finish` | 正常结束番茄（发送 `finish` 操作） |
| `GET` | `/pomodoros/focus/stop` | 不足 5 分钟时强制结束番茄（自动组合 drop + exit） |
| `POST` | `/pomodoros/focus/point/{point}` | 手动覆盖 `lastPoint` 缓存 |
| `POST` | `/pomodoros/focus/reset` | 重置本地缓存（保留 `lastPoint`） |
| `GET` | `/pomodoros/focus/state` | 查看当前缓存的番茄会话状态 |

> ⚠️ **注意**
> - 所有接口均依赖本地缓存的 `lastPoint`、`firstFocusId` 等信息，请在第一次调用前确认 `lastPoint` 已设置正确。
> - 若出现 `no_active_focus` 错误，表示当前没有缓存中的进行中番茄，需要先调用 `/focus/start`。

## 示例

### 启动番茄钟

```http
GET /pomodoros/focus/start?
  focusOnId=67867db6ebae1f00000000ea&
  focusOnType=1&
  focusOnTitle=%E5%AD%A6%E8%8B%B1%E8%AF%AD
```

> 说明：当 `focusOnId` 等字段存在时，会将番茄与任务/清单/习惯绑定，对应滴答返回中的 `focusTasks`、`focusOnLogs` 字段。

响应将返回滴答原始结构，并更新本地缓存的 `lastPoint`、`focusId` 等字段。

### 暂停番茄钟

```http
GET /pomodoros/focus/pause?note=%E7%A6%BB%E5%BC%80%E5%BA%A7%E4%BD%8D
```

若不传字段，则沿用上次缓存的 `manual`、`note` 值。

### 强制结束（drop + exit）

```http
GET /pomodoros/focus/stop?include_exit=true
```

该接口会依次发送 `drop` 和 `

### 结束番茄钟（正常完成）

```http
GET /pomodoros/focus/finish
```

> 说明：当番茄自然计时满 5 分钟后，滴答前端会发送 `finish` 操作。该接口复刻同样行为，用于同步并结束番茄。

### 查看当前番茄状态

```http
GET /pomodoros/focus/current
```

可选参数 `lastPoint` 用于覆盖本地缓存的指针值，例如 `GET /pomodoros/focus/current?lastPoint=1763039467240`。

• 基础参数
  - `duration`：番茄时长（分钟），默认 25
  - `autoPomoLeft` / `pomoCount`：自动番茄剩余次数与已完成次数
  - `manual`、`note`：手动触发、备注信息
  - `lastPoint`：覆盖本地缓存中的 `point`，一般无需填写
  - `focusOnId` / `focusOnType` / `focusOnTitle`：**绑定任务/清单/习惯** 时使用。实际测试表明只要提供 `focusOnId` 即可完成绑定，`focusOnType`、`focusOnTitle` 为辅助信息，可以留空。