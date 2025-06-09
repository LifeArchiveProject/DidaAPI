# 获取任务统计

## 接口信息

- **接口路径**: `GET /tasks/summary`
- **接口描述**: 获取任务的统计信息
- **请求方式**: GET
- **认证要求**: 需要先完成微信登录获取认证会话

## 请求参数

无需参数

## 请求示例

```bash
curl -X GET "http://localhost:8000/tasks/summary"
```

## 响应格式

### 成功响应

```json
{
  "code": 200,
  "message": "获取任务统计成功",
  "data": {
    "total_tasks": 150,
    "completed_tasks": 120,
    "pending_tasks": 30,
    "completion_rate": 80.0
  }
}
```

### 错误响应

#### 未认证

```json
{
  "error": "获取任务统计失败",
  "details": {
    "error": "no_auth_session",
    "message": "未设置认证会话，请先完成微信登录"
  }
}
```

#### 服务错误

```json
{
  "detail": "服务器内部错误: 具体错误信息"
}
```

## 响应字段说明

| 字段名 | 类型 | 描述 |
|--------|------|------|
| code | integer | 响应状态码，200表示成功 |
| message | string | 响应消息 |
| data | object | 统计数据对象 |
| data.total_tasks | integer | 总任务数 |
| data.completed_tasks | integer | 已完成任务数 |
| data.pending_tasks | integer | 未完成任务数 |
| data.completion_rate | float | 完成率（百分比） |

## 使用说明

1. **认证要求**: 需要先调用微信登录接口获取认证会话
2. **统计范围**: 统计当前用户的所有任务
3. **实时数据**: 返回实时的任务统计信息
4. **完成率计算**: 完成率 = (已完成任务数 / 总任务数) × 100

## 相关接口

- [获取所有任务](./get-all-tasks.md)
- [获取已完成任务](./get-completed-tasks.md)
- [获取垃圾桶任务](./get-trash-tasks.md)
- [微信登录流程](../auth/wechat-login-flow.md)

## 注意事项

- 需要先完成微信登录获取认证会话
- 统计数据基于用户的所有任务
- 完成率保留两位小数
- 如果没有任务，完成率为0
