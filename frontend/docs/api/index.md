# 滴答清单API文档

本文档详细描述了滴答清单的原始API接口，帮助开发者了解如何直接调用滴答清单的服务。

## 接口分类

### 认证相关
- [微信登录流程](./auth/wechat-login-flow.md) - 完整的微信扫码登录流程
- [获取微信二维码](./auth/get-wechat-qrcode.md) - 获取微信登录二维码
- [轮询登录状态](./auth/poll-login-status.md) - 检查二维码扫码状态
- [验证微信登录](./auth/validate-wechat-login.md) - 验证微信登录并获取令牌
- [微信登录回调处理](./auth/wechat-callback.md) - 处理微信扫码后的回调，提取code参数
- [密码登录](./auth/password-login.md) - 使用用户名和密码进行登录

### 任务管理
- [获取所有任务](./tasks/get-all-tasks.md) - 获取用户的所有任务列表
- [获取已完成任务](./tasks/get-completed-tasks.md) - 获取已完成/已放弃的任务列表，支持分页
- [获取垃圾桶任务](./tasks/get-trash-tasks.md) - 获取垃圾桶中的任务列表
- [获取任务统计](./tasks/get-tasks-summary.md) - 获取任务的统计信息

### 清单管理
- [获取清单列表](./projects.md) - 获取用户的所有清单列表

### 统计分析
- [获取用户排名统计](./statistics.md) - 获取用户在滴答清单中的排名和基本统计信息
- [获取通用统计信息](./statistics/general-statistics.md) - 获取概览、成就值、趋势等通用统计信息
- [获取任务统计信息](./statistics/task-statistics.md) - 获取指定日期范围内的任务统计信息

### 番茄专注
- [获取番茄专注概览](./pomodoros.md) - 获取番茄专注的概览统计信息
- [执行番茄钟控制操作](./pomodoros/focus-operations.md) - 批量执行番茄钟的开始、暂停、继续、结束等操作
- [番茄钟自动操作接口](./pomodoros/focus-control-shortcuts.md) - 使用封装端点自动补齐 focusOp 所需字段

### 正计时专注
- [获取专注记录时间线](./pomodoros/focus-timeline.md) - 获取专注记录的时间线数据，支持分页
- [获取专注详情分布](./pomodoros/focus-distribution.md) - 获取指定日期范围内的专注时长分布统计
- [获取专注趋势热力图](./pomodoros/focus-heatmap.md) - 获取指定日期范围内的专注趋势热力图数据
- [获取专注时间按小时分布](./pomodoros/focus-hour-distribution.md) - 获取指定日期范围内按小时分布的专注时间统计
- [获取专注时间分布](./pomodoros/focus-time-distribution.md) - 获取指定日期范围内按时间段分布的专注数据

### 习惯管理
- [获取所有习惯](./habits.md) - 获取当前用户的所有习惯列表
- [获取本周习惯打卡统计](./habits/week-current-statistics.md) - 获取本周的习惯打卡统计信息
- [导出习惯数据](./habits/export-habits.md) - 导出用户的习惯数据为Excel文件

### 用户信息
- [获取用户信息](./users.md) - 获取当前登录用户的详细信息

### 自定义接口
- [导出任务到Excel](./custom/export-tasks-excel.md) - 导出所有任务到Excel文件，包含全部任务、已完成任务、垃圾桶任务三个工作表
- [导出专注记录到Excel](./custom/export-focus-excel.md) - 导出所有专注记录到Excel文件，包含完整的专注时间线数据


