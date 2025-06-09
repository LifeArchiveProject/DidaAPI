# 获取任务统计信息

## 接口信息

- **接口路径**: `GET /statistics/tasks`
- **接口描述**: 获取指定日期范围内的任务统计信息
- **请求方式**: GET
- **认证要求**: 需要先完成微信登录获取认证会话

## 请求参数

### Query参数

| 参数名 | 类型 | 必填 | 描述 | 示例值 |
|--------|------|------|------|--------|
| start_date | string | 是 | 开始日期，格式: YYYYMMDD | `20231201` |
| end_date | string | 是 | 结束日期，格式: YYYYMMDD | `20231207` |

## 请求示例

```bash
curl -X GET "http://localhost:8000/statistics/tasks?start_date=20231201&end_date=20231207"
```

## 响应格式

### 成功响应

```json
{
  "overdueCompletedCount": 2,
  "onTimeCompletedCount": 15,
  "noDateCompletedCount": 8,
  "uncompletedCount": 5,
  "projectStats": [
    {
      "projectId": "project123",
      "projectName": "工作项目",
      "completedCount": 10
    },
    {
      "projectId": "project456",
      "projectName": "个人项目",
      "completedCount": 5
    }
  ],
  "tagStats": [
    {
      "tagName": "重要",
      "completedCount": 8
    },
    {
      "tagName": "紧急",
      "completedCount": 4
    }
  ]
}
```

### 错误响应

#### 参数错误

```json
{
  "detail": [
    {
      "loc": ["query", "start_date"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

#### 未认证

```json
{
  "error": "no_auth_session",
  "message": "未设置认证会话，请先完成微信登录"
}
```

#### 服务错误

```json
{
  "error": "service_error",
  "message": "获取任务统计信息失败，请稍后重试"
}
```

## 响应字段说明

| 字段名 | 类型 | 描述 |
|--------|------|------|
| overdueCompletedCount | integer | 逾期完成任务数 |
| onTimeCompletedCount | integer | 按时完成任务数 |
| noDateCompletedCount | integer | 无日期任务完成数 |
| uncompletedCount | integer | 未完成任务数 |
| projectStats | array | 按项目的完成统计 |
| projectStats[].projectId | string | 项目ID |
| projectStats[].projectName | string | 项目名称 |
| projectStats[].completedCount | integer | 该项目完成任务数 |
| tagStats | array | 按标签的完成统计 |
| tagStats[].tagName | string | 标签名称 |
| tagStats[].completedCount | integer | 该标签完成任务数 |

## 使用说明

1. **认证要求**: 需要先调用微信登录接口获取认证会话
2. **日期格式**: 日期必须使用YYYYMMDD格式
3. **统计维度**: 提供多维度的任务完成统计
4. **时间范围**: 支持自定义时间范围查询

## 相关接口

- [获取通用统计信息](./general-statistics.md)
- [获取用户排名统计](../statistics.md)
- [获取任务统计](../tasks/get-tasks-summary.md)
- [微信登录流程](../auth/wechat-login-flow.md)

## 注意事项

- 需要先完成微信登录获取认证会话
- 日期格式必须正确，否则会返回参数错误
- 统计数据基于指定时间范围内的任务
- 项目和标签统计按完成数量降序排列
