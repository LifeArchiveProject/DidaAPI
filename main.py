"""滴答清单API主应用"""
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from contextlib import asynccontextmanager
from core import config, db
from utils import app_logger
from services import wechat_service
from routers import auth, tasks, system, projects, statistics, pomodoros, habits, users, export


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时执行
    app_logger.info("滴答清单API服务启动中...")

    # 初始化数据库
    db.init_database()
    app_logger.info("数据库初始化完成")

    yield

    # 关闭时执行
    app_logger.info("滴答清单API服务关闭中...")
    await wechat_service.close()
    app_logger.info("服务已关闭")


# 创建FastAPI应用
app = FastAPI(
    title=config.app.get('name', '滴答清单API'),
    version=config.app.get('version', '1.0.0'),
    description="""
## 滴答清单Web端API接口

这是一个滴答清单的Web端API接口项目，**在原始滴答清单API基础上进行了封装**，提供更简单易用的接口。
    """,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该限制具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 注册路由
app.include_router(auth.router)
app.include_router(tasks.router)
app.include_router(projects.router)
app.include_router(statistics.router)
app.include_router(pomodoros.router)
app.include_router(habits.router)
app.include_router(users.router)
app.include_router(export.router)
app.include_router(system.router)


@app.get("/", summary="根路径", description="API服务根路径，返回基本信息")
async def root():
    """根路径接口"""
    return {
        "message": "欢迎使用滴答清单API",
        "version": config.app.get('version', '1.0.0'),
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/auth/health",
        "auth_status": "/tasks/status",
        "url_management": "/system/urls",
        "system_info": "/system/info",
        "api_modules": {
            "authentication": "/auth/",
            "tasks": "/tasks/",
            "projects": "/projects/",
            "statistics": "/statistics/",
            "pomodoros": "/pomodoros/",
            "habits": "/habits/",
            "users": "/users/",
            "custom": "/custom/",
            "system": "/system/"
        }
    }


def main():
    """主函数，启动应用"""
    app_config = config.app

    uvicorn.run(
        "main:app",
        host=app_config.get('host', '127.0.0.1'),
        port=app_config.get('port', 8000),
        reload=app_config.get('debug', True),
        log_level="info"
    )


if __name__ == "__main__":
    main()
