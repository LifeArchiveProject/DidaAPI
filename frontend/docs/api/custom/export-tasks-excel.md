# 导出任务到Excel

将用户的所有任务导出为Excel文件，包含全部任务、已完成任务、放弃任务、垃圾桶任务四个工作表。

## 接口信息

- **接口URL**: `http://localhost:8000/custom/export/tasks/excel`
- **请求方法**: `GET`
- **认证要求**: 需要登录认证
- **所属平台**: 本项目自定义接口

## 功能说明

此接口会将用户的所有任务数据导出为Excel文件，包含以下四个工作表：

### 工作表1：全部任务
包含当前所有任务（未完成和已完成），数据来源于 `/api/v2/batch/check/0` 接口。

### 工作表2：已完成任务
包含历史已完成的任务，数据来源于 `/api/v2/project/all/closed?status=Completed` 接口。

**分页获取机制**:
- 第一次请求不携带`to`参数
- 后续请求使用上次响应最后一个任务的`completedTime`作为`to`参数
- 重复请求直到返回数据少于50条为止，确保获取所有历史数据

### 工作表3：放弃任务
包含历史放弃的任务，数据来源于 `/api/v2/project/all/closed?status=Abandoned` 接口。

**分页获取机制**:
- 第一次请求不携带`to`参数
- 后续请求使用上次响应最后一个任务的`completedTime`作为`to`参数
- 重复请求直到返回数据少于50条为止，确保获取所有历史数据

### 工作表4：垃圾桶任务
包含已删除的任务，数据来源于 `/api/v2/project/all/trash/page` 接口。

## 导出字段

每个工作表包含任务的完整字段信息（展平后），包括但不限于：

### 基本信息
- 任务ID
- 任务标题
- 任务内容
- 任务描述
- 项目ID
- 项目名称
- 排序顺序

### 状态信息
- 任务状态（文本描述）
- 状态代码（数字）
- 优先级
- 完成进度
- 删除状态

### 时间信息
- 创建时间
- 修改时间
- 开始日期
- 截止日期
- 置顶时间
- 完成时间
- 删除时间

### 时区和时间设置
- 时区
- 是否浮动时间
- 是否全天任务

### 重复设置
- 重复任务ID
- 重复标志
- 重复来源
- 首次重复日期

### 提醒设置
- 提醒设置
- 提醒列表
- 排除日期

### 层级关系
- 父任务ID
- 子任务ID列表

### 其他属性
- 标签列表
- 子项目
- 附件数量
- 评论数量
- 列ID
- 类型
- 图片模式
- 创建者ID
- 删除者ID
- 实体标签
- 番茄钟摘要
- 专注摘要
- 附件详情

## 请求示例

```http
GET http://localhost:8000/custom/export/tasks/excel HTTP/1.1
Host: localhost:8000
Accept: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet
```

## 响应格式

### 成功响应

**状态码**: `200 OK`

**Content-Type**: `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`

**响应头**:
```http
Content-Disposition: attachment; filename=滴答清单任务导出_20250106_143022.xlsx
```

**响应体**: Excel文件的二进制数据

### 错误响应

**状态码**: `401 Unauthorized`
```json
{
  "detail": "未设置认证会话，请先完成登录"
}
```

**状态码**: `500 Internal Server Error`
```json
{
  "detail": "导出失败: 具体错误信息"
}
```

## 使用说明

1. **认证要求**: 必须先完成认证，设置有效的会话
2. **文件格式**: 导出的Excel文件包含四个工作表
3. **文件命名**: 文件名格式为 `滴答清单任务导出_YYYYMMDD_HHMMSS.xlsx`
4. **数据完整性**: 包含任务的所有字段，无遗漏
5. **分页处理**: 自动处理已完成任务和放弃任务的分页，获取所有历史数据

## 辅助接口

### 获取导出信息

**接口URL**: `http://localhost:8000/custom/export/tasks/excel/info`

**请求方法**: `GET`

**功能**: 获取当前用户任务的统计信息，用于导出前预览

**响应示例**:
```json
{
  "auth_status": true,
  "all_tasks_count": 150,
  "completed_tasks_count": 89,
  "abandoned_tasks_count": 15,
  "trash_tasks_count": 12,
  "session_info": {
    "has_session": true,
    "session_id": "session_123",
    "created_at": "2025-01-06T14:30:22"
  }
}
```

## 注意事项

1. 导出过程可能需要一些时间，特别是当任务数量较多时
2. 已完成任务和放弃任务会通过分页获取所有历史数据，确保数据完整性
3. 如果某个数据源获取失败，对应的工作表将为空，但不影响其他工作表
4. 建议在网络状况良好时进行导出操作
5. 导出的Excel文件可以用Microsoft Excel、WPS Office等软件打开

## 相关接口

- [获取所有任务](../tasks/get-all-tasks.md) - 全部任务数据源
- [获取已完成任务](../tasks/get-completed-tasks.md) - 已完成任务数据源
- [获取已完成/已放弃任务](../tasks/get-completed-tasks.md) - 放弃任务数据源（使用status=Abandoned参数）
- [获取垃圾桶任务](../tasks/get-trash-tasks.md) - 垃圾桶任务数据源
