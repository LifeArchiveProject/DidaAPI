"""日志配置模块"""
import sys
import os
from datetime import datetime
from loguru import logger


def setup_logger():
    """配置日志系统"""
    # 移除默认的日志处理器
    logger.remove()

    # 使用默认配置
    level = 'DEBUG'
    format_str = '{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} - {message}'
    rotation = '1 day'
    retention = '7 days'

    # 控制台输出
    logger.add(
        sys.stdout,
        format=format_str,
        level=level,
        colorize=True
    )

    # 获取当前日期，用于创建日志文件夹结构
    now = datetime.now()
    year = now.strftime('%Y')
    month = now.strftime('%m')
    day = now.strftime('%d')
    
    # 创建日志文件夹结构: output/logs/年/月/日/
    log_dir = f"output/logs/{year}/{month}/{day}"
    os.makedirs(log_dir, exist_ok=True)

    # 应用日志文件
    logger.add(
        f"{log_dir}/app.log",
        format=format_str,
        level=level,
        rotation=rotation,
        retention=retention,
        encoding="utf-8"
    )

    # 错误日志单独文件
    logger.add(
        f"{log_dir}/error.log",
        format=format_str,
        level="ERROR",
        rotation=rotation,
        retention=retention,
        encoding="utf-8"
    )

    return logger


# 初始化日志
app_logger = setup_logger()
