<div align="center">
  <img src="frontend/docs/public/logo.png" alt="滴答清单API Logo" width="200">
</div>

# 滴答清单API接口

这是一个获取滴答清单API接口项目，提供包括任务管理、专注记录、习惯打卡、数据导出等功能。

## 🌐 在线文档

- **📖 API文档**: [https://lifearchiveproject.github.io/DidaAPI/](https://lifearchiveproject.github.io/DidaAPI/)
- **💻 项目地址**: [https://github.com/LifeArchiveProject/DidaAPI](https://github.com/LifeArchiveProject/DidaAPI)

## 📋 API接口清单

- [x] **🔐 认证相关 (/auth)**
  - [x] `GET /auth/wechat/qrcode` - 获取微信登录二维码
  - [x] `GET /auth/wechat/poll` - 轮询登录状态（自动检测）
  - [x] `GET /auth/wechat/validate` - 验证微信登录
  - [x] `POST /auth/password/login` - 密码登录
  - [x] `POST /tasks/set-auth` - 手动设置认证（通常不需要）

- [x] **📝 任务管理 (/tasks)**
  - [x] `GET /tasks/all` - 获取所有任务
  - [x] `GET /tasks/completed` - 获取已完成/已放弃任务（支持分页）
  - [x] `GET /tasks/trash` - 获取垃圾桶任务
  - [x] `GET /tasks/summary` - 获取任务统计

- [x] **📂 清单管理 (/projects)**
  - [x] `GET /projects/all` - 获取清单列表

- [x] **📊 统计分析 (/statistics)**
  - [x] `GET /statistics/ranking` - 获取用户排名统计
  - [x] `GET /statistics/general` - 获取通用统计信息
  - [x] `GET /statistics/tasks` - 获取任务统计信息

- [x] **🍅 专注记录 (/pomodoros)**
  - [x] `GET /pomodoros/general` - 获取番茄专注概览
  - [x] `GET /pomodoros/distribution` - 获取专注详情分布
  - [x] `GET /pomodoros/timeline` - 获取专注记录时间线

- [x] **🎯 习惯管理 (/habits)**
  - [x] `GET /habits/all` - 获取所有习惯
  - [x] `GET /habits/statistics/week/current` - 获取本周习惯打卡统计

- [x] **👤 用户信息 (/user)**
  - [x] `GET /user/info` - 获取用户信息

- [x] **📤 数据导出 (/custom/export)**
  - [x] `GET /custom/export/tasks/excel` - 导出任务到Excel
  - [x] `GET /custom/export/focus/excel` - 导出专注记录到Excel

## 📁 项目结构

```
DidaAPI/
├── main.py                    # 🎯 应用启动文件
├── config.toml               # 📝 配置文件
├── core/                     # 🔧 核心模块
│   ├── __init__.py
│   ├── config.py            # 配置管理
│   ├── database.py          # 数据库管理
│   └── urls.py              # URL和外部链接统一管理
├── models/                   # 📊 数据模型
│   ├── __init__.py
│   └── base.py             # 所有数据模型定义
├── services/                 # 🔄 业务服务
│   ├── __init__.py
│   ├── wechat_service.py   # 微信登录服务
│   ├── dida_service.py     # 滴答清单API服务
│   ├── pomodoro_service.py # 专注记录服务
│   └── export_service.py   # 数据导出服务
├── routers/                  # 🛣️ API路由
│   ├── __init__.py
│   ├── auth.py             # 认证相关路由
│   ├── tasks.py            # 任务管理路由
│   ├── projects.py         # 清单管理路由
│   ├── statistics.py       # 统计分析路由
│   ├── pomodoros.py        # 专注记录路由
│   ├── habits.py           # 习惯管理路由
│   ├── user.py             # 用户信息路由
│   └── export.py           # 数据导出路由
├── utils/                    # 🛠️ 工具模块
│   ├── __init__.py
│   └── logger.py           # 日志配置
├── frontend/                 # 🌐 前端项目（接口文档）
│   ├── docs/               # 📚 API文档
│   │   ├── index.md       # 文档首页
│   │   ├── api/           # API接口文档
│   │   │   ├── auth/      # 认证相关接口
│   │   │   ├── tasks/     # 任务管理接口
│   │   │   ├── projects/  # 清单管理接口
│   │   │   ├── statistics/ # 统计分析接口
│   │   │   ├── pomodoros/ # 专注记录接口
│   │   │   ├── habits/    # 习惯管理接口
│   │   │   ├── user/      # 用户信息接口
│   │   │   └── custom/    # 自定义接口
│   │   └── guide/         # 使用指南
│   ├── .vitepress/        # VitePress配置
│   └── package.json       # 前端依赖配置
└── output/                   # 📤 输出文件夹
    ├── databases/          # 数据库文件
    └── logs/              # 日志文件（按年/月/日组织）
```

## 🔧 安装和运行

### 环境要求
- Python 3.8+
- Node.js 16+ (用于前端文档)
- 推荐使用 uv 作为Python包管理器

## 📖 使用指南

### 完整使用流程

1. **启动后端服务**
   ```bash
   uv sync
   uv run main.py
   ```
2. **启动前端文档**
   ```bash
   cd frontend
   npm install
   npm run docs:dev 

3. **查看API文档**
   - 后端API文档: http://localhost:8000/docs
   - 前端接口文档: http://localhost:5173

## 🌐 前端项目介绍

### 文档结构
```
frontend/docs/
├── index.md              # 文档首页
├── api/                  # API接口文档
│   ├── auth/            # 认证相关接口
│   ├── tasks/           # 任务管理接口
│   ├── projects/        # 清单管理接口
│   ├── statistics/      # 统计分析接口
│   ├── pomodoros/       # 专注记录接口
│   ├── habits/          # 习惯管理接口
│   ├── user/            # 用户信息接口
│   └── custom/          # 自定义接口（导出等）
└── guide/               # 使用指南
    ├── getting-started.md
    ├── authentication.md
    └── best-practices.md
```

## ⚙️ 配置说明

### 后端配置 (`config.toml`)
```toml
[app]
name = "滴答清单API"
host = "127.0.0.1"
port = 8000
debug = true

[wechat]
app_id = "wxf1429a73d311aad4"
# 微信登录相关配置

[dida_api]
base_url = "https://api.dida365.com/api/v2"
# 滴答清单API配置

[database]
path = "output/databases/dida_api.db"
# 数据库配置

[logging]
level = "INFO"
path = "output/logs"
# 日志配置
```

### 前端配置 (`frontend/.vitepress/config.js`)
```javascript
export default {
  title: '滴答清单API文档',
  description: '完整的滴答清单API接口文档',
  themeConfig: {
    nav: [...],
    sidebar: {...},
    // 其他配置
  }
}
```

## 🔧 开发指南

### 添加新接口
1. 在 `services/` 中添加业务逻辑
2. 在 `routers/` 中添加路由定义
3. 在 `frontend/docs/api/` 中添加接口文档
4. 更新 README.md 中的接口清单

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

### 贡献指南
1. Fork 本项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

**注意**: 本项目仅用于学习和研究目的，请遵守滴答清单的服务条款和使用协议。