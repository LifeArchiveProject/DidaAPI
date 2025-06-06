"""数据库管理模块"""
import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any
from utils import app_logger
from core.config import config


class Database:
    """SQLite数据库管理类"""
    
    def __init__(self, db_path: str = "output/databases/dida_api.db"):
        self.db_path = Path(db_path)
        # 确保数据库目录存在
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.init_database()
    
    def get_connection(self) -> sqlite3.Connection:
        """获取数据库连接"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # 使结果可以通过列名访问
        return conn
    
    def init_database(self) -> None:
        """初始化数据库表"""
        with self.get_connection() as conn:
            # 用户会话表
            conn.execute("""
                CREATE TABLE IF NOT EXISTS user_sessions (
                    session_id TEXT PRIMARY KEY,
                    user_id TEXT,
                    token TEXT,
                    csrf_token TEXT,
                    cookies TEXT,  -- JSON格式存储cookies
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    expires_at TIMESTAMP,
                    is_active BOOLEAN DEFAULT 1
                )
            """)
            
            # 微信登录日志表
            conn.execute("""
                CREATE TABLE IF NOT EXISTS wechat_login_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    qr_code_key TEXT,
                    validation_code TEXT,
                    state TEXT,
                    response_data TEXT,  -- JSON格式存储响应数据
                    status TEXT,  -- 'pending', 'success', 'failed'
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.commit()
            app_logger.info("数据库初始化完成")
    
    def save_user_session(self, session_data: Dict[str, Any]) -> bool:
        """保存用户会话"""
        try:
            with self.get_connection() as conn:
                cookies_json = json.dumps(session_data.get('cookies', {}))
                
                conn.execute("""
                    INSERT OR REPLACE INTO user_sessions 
                    (session_id, user_id, token, csrf_token, cookies, updated_at, expires_at, is_active)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    session_data['session_id'],
                    session_data.get('user_id'),
                    session_data.get('token'),
                    session_data.get('csrf_token'),
                    cookies_json,
                    datetime.now(),
                    session_data.get('expires_at'),
                    session_data.get('is_active', True)
                ))
                
                conn.commit()
                app_logger.info(f"用户会话已保存: {session_data['session_id']}")
                return True
                
        except Exception as e:
            app_logger.error(f"保存用户会话失败: {e}")
            return False
    
    def get_user_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """获取用户会话"""
        try:
            with self.get_connection() as conn:
                cursor = conn.execute(
                    "SELECT * FROM user_sessions WHERE session_id = ? AND is_active = 1",
                    (session_id,)
                )
                row = cursor.fetchone()

                if row:
                    session_data = dict(row)
                    # 解析cookies JSON
                    if session_data['cookies']:
                        session_data['cookies'] = json.loads(session_data['cookies'])
                    return session_data

                return None

        except Exception as e:
            app_logger.error(f"获取用户会话失败: {e}")
            return None

    def get_latest_active_session(self) -> Optional[Dict[str, Any]]:
        """获取最新的活跃用户会话"""
        try:
            with self.get_connection() as conn:
                cursor = conn.execute("""
                    SELECT * FROM user_sessions
                    WHERE is_active = 1
                    ORDER BY updated_at DESC
                    LIMIT 1
                """)
                row = cursor.fetchone()

                if row:
                    session_data = dict(row)
                    # 解析cookies JSON
                    if session_data['cookies']:
                        session_data['cookies'] = json.loads(session_data['cookies'])
                    return session_data

                return None

        except Exception as e:
            app_logger.error(f"获取最新活跃会话失败: {e}")
            return None

    def log_wechat_login(self, qr_code_key: str, validation_code: str = None,
                        state: str = None, response_data: Dict = None,
                        status: str = 'pending') -> bool:
        """记录微信登录日志"""
        try:
            with self.get_connection() as conn:
                response_json = json.dumps(response_data) if response_data else None

                conn.execute("""
                    INSERT INTO wechat_login_logs
                    (qr_code_key, validation_code, state, response_data, status)
                    VALUES (?, ?, ?, ?, ?)
                """, (qr_code_key, validation_code, state, response_json, status))

                conn.commit()
                app_logger.info(f"微信登录日志已记录: {qr_code_key}")
                return True

        except Exception as e:
            app_logger.error(f"记录微信登录日志失败: {e}")
            return False


# 全局数据库实例
db = Database()
