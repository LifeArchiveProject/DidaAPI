# 获取专注详情分布

获取指定日期范围内的专注时长分布统计，包括按项目、标签、任务分布的专注时长。

## 接口信息

- **接口URL**: `https://api.dida365.com/api/v2/pomodoros/statistics/dist/{start_date}/{end_date}`
- **请求方法**: `GET`
- **认证要求**: 需要登录认证
- **所属平台**: 滴答清单官方API

## 请求参数

### 路径参数

| 参数名 | 类型 | 必填 | 描述 | 示例 |
|--------|------|------|------|------|
| start_date | string | 是 | 开始日期，格式: YYYYMMDD | 20231201 |
| end_date | string | 是 | 结束日期，格式: YYYYMMDD | 20231207 |

## 完整请求示例

```http
GET https://api.dida365.com/api/v2/pomodoros/statistics/dist/20231201/20231207 HTTP/1.1
Host: api.dida365.com
Cookie: t=string; _csrf_token=string
X-CSRFToken: string
```

## 响应格式

### 成功响应

**状态码**: `200 OK`

**响应体**:
```json
{
  "projectDurations": {
    "project_id_1": {
      "duration": 3600,
      "name": "工作项目",
      "color": "#FF5722"
    },
    "project_id_2": {
      "duration": 1800,
      "name": "学习项目", 
      "color": "#2196F3"
    }
  },
  "tagDurations": {
    "tag_id_1": {
      "duration": 2400,
      "name": "编程",
      "color": "#4CAF50"
    },
    "tag_id_2": {
      "duration": 1200,
      "name": "阅读",
      "color": "#FF9800"
    }
  },
  "taskDurations": {
    "task_id_1": {
      "duration": 1800,
      "title": "完成API文档",
      "projectId": "project_id_1"
    },
    "task_id_2": {
      "duration": 1200,
      "title": "学习新技术",
      "projectId": "project_id_2"
    }
  }
}
```

## 响应字段说明

### projectDurations (按项目分布)
- **类型**: Object
- **描述**: 按项目分组的专注时长统计
- **字段说明**:
  - `duration`: 专注时长（秒）
  - `name`: 项目名称
  - `color`: 项目颜色

### tagDurations (按标签分布)
- **类型**: Object
- **描述**: 按标签分组的专注时长统计
- **字段说明**:
  - `duration`: 专注时长（秒）
  - `name`: 标签名称
  - `color`: 标签颜色

### taskDurations (按任务分布)
- **类型**: Object
- **描述**: 按任务分组的专注时长统计
- **字段说明**:
  - `duration`: 专注时长（秒）
  - `title`: 任务标题
  - `projectId`: 所属项目ID

## 使用说明

1. **日期格式**: 必须使用 YYYYMMDD 格式
2. **时长单位**: 所有时长都以秒为单位
3. **数据范围**: 返回指定日期范围内的专注分布统计
4. **认证要求**: 需要有效的登录会话

## 相关接口

- [获取专注记录时间线](./focus-timeline.md) - 获取详细的专注记录
- [获取专注趋势热力图](./focus-heatmap.md) - 获取专注趋势数据
- [获取专注时间分布](./focus-time-distribution.md) - 获取时间段分布
- [获取专注时间按小时分布](./focus-hour-distribution.md) - 获取小时分布
