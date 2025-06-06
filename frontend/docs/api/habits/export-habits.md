# 导出习惯数据

导出用户的习惯数据为Excel文件。

## 接口信息

- **接口URL**: `https://api.dida365.com/api/v2/data/export/habits`
- **请求方法**: `GET`
- **认证要求**: 需要登录认证
- **所属平台**: 滴答清单

## 请求参数

无需额外参数，使用当前登录会话的认证信息。

## 响应格式

### 成功响应

返回Excel文件下载，响应头包含：

```
Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet
Content-Disposition: attachment; filename=Habits_YYYYMMDD.xlsx
```



## 使用说明

1. 确保已完成认证获取会话
2. 调用接口将直接下载Excel文件
3. 文件包含用户的所有习惯数据和统计信息
4. 文件名格式为：`Habits_YYYYMMDD.xlsx` 或 `习惯_YYYYMMDD.xlsx`

## 文件内容

导出的Excel文件包含：
- 习惯基本信息（名称、图标、颜色等）
- 习惯打卡记录
- 统计数据（总打卡次数、连续天数等）
- 其他相关数据



