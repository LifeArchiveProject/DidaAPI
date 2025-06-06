"""数据模型定义"""
from datetime import datetime, timezone, timedelta
from typing import Optional, Union
from pydantic import BaseModel, Field

# 中国时区
CHINA_TZ = timezone(timedelta(hours=8))

def get_china_time() -> datetime:
    """获取中国时区的当前时间"""
    return datetime.now(CHINA_TZ)


class WeChatQRResponse(BaseModel):
    """微信二维码响应模型"""
    qr_code_url: str = Field(..., description="二维码图片URL")
    qr_code_key: str = Field(..., description="二维码密钥（16位字符）")
    state: str = Field(..., description="状态参数")


class WeChatValidateRequest(BaseModel):
    """微信验证请求模型"""
    code: str = Field(..., description="扫码后获得的验证码")
    state: str = Field(..., description="状态参数")


class PasswordLoginRequest(BaseModel):
    """密码登录请求模型"""
    username: str = Field(..., description="登录账户（邮箱或手机号）")
    password: str = Field(..., description="登录密码")


# 密码登录直接返回原始响应，不使用Pydantic模型


class WeChatValidateResponse(BaseModel):
    """微信验证响应模型"""
    success: bool = Field(..., description="是否成功")
    message: str = Field(..., description="响应消息")
    token: Optional[str] = Field(None, description="认证令牌")
    user_info: Optional[dict] = Field(None, description="用户信息")
    cookies: Optional[dict] = Field(None, description="响应cookies")
    raw_response: Optional[Union[dict, list]] = Field(None, description="原始响应数据")


class UserSession(BaseModel):
    """用户会话模型"""
    session_id: str = Field(..., description="会话ID")
    user_id: Optional[str] = Field(None, description="用户ID")
    token: Optional[str] = Field(None, description="认证令牌")
    csrf_token: Optional[str] = Field(None, description="CSRF令牌")
    cookies: Optional[dict] = Field(None, description="会话cookies")
    created_at: datetime = Field(default_factory=get_china_time, description="创建时间")
    updated_at: datetime = Field(default_factory=get_china_time, description="更新时间")
    expires_at: Optional[datetime] = Field(None, description="过期时间")
    is_active: bool = Field(True, description="是否活跃")


class ApiResponse(BaseModel):
    """通用API响应模型"""
    code: int = Field(..., description="响应代码")
    message: str = Field(..., description="响应消息")
    data: Optional[dict] = Field(None, description="响应数据")
    timestamp: datetime = Field(default_factory=get_china_time, description="响应时间")


class TaskItem(BaseModel):
    """任务项模型"""
    id: str = Field(..., description="任务ID")
    title: str = Field(..., description="任务标题")
    content: Optional[str] = Field(None, description="任务内容")
    status: int = Field(..., description="任务状态（0=未完成，2=已完成）")
    priority: int = Field(default=0, description="优先级")
    created_time: Optional[str] = Field(None, description="创建时间")
    modified_time: Optional[str] = Field(None, description="修改时间")
    project_id: Optional[str] = Field(None, description="项目ID")
    tags: Optional[list] = Field(default_factory=list, description="标签列表")


class TasksResponse(BaseModel):
    """获取任务响应模型"""
    success: bool = Field(..., description="是否成功")
    message: str = Field(..., description="响应消息")
    tasks: Optional[list[TaskItem]] = Field(None, description="任务列表")
    total_count: int = Field(default=0, description="任务总数")
    raw_response: Optional[Union[dict, list]] = Field(None, description="原始响应数据")


class AuthSession(BaseModel):
    """认证会话模型"""
    session_id: str = Field(..., description="会话ID")
    auth_token: str = Field(..., description="认证令牌")
    csrf_token: str = Field(..., description="CSRF令牌")
    is_active: bool = Field(True, description="是否活跃")
    created_at: datetime = Field(default_factory=get_china_time, description="创建时间")
    expires_at: Optional[datetime] = Field(None, description="过期时间")


# ================================
# 项目管理相关模型
# ================================

class ProjectItem(BaseModel):
    """项目/清单项模型"""
    id: str = Field(..., description="项目ID")
    name: str = Field(..., description="项目名称")
    is_owner: bool = Field(..., description="是否为拥有者")
    color: Optional[str] = Field(None, description="项目颜色")
    in_all: bool = Field(True, description="是否在全部清单中显示")
    sort_order: int = Field(..., description="排序顺序")
    user_count: int = Field(1, description="用户数量")
    permission: str = Field("write", description="权限")
    kind: str = Field("TASK", description="类型")
    created_time: Optional[str] = Field(None, description="创建时间")
    modified_time: Optional[str] = Field(None, description="修改时间")


class ProjectsResponse(BaseModel):
    """获取项目列表响应模型"""
    success: bool = Field(..., description="是否成功")
    message: str = Field(..., description="响应消息")
    projects: Optional[list[ProjectItem]] = Field(None, description="项目列表")
    total_count: int = Field(default=0, description="项目总数")
    raw_response: Optional[Union[dict, list]] = Field(None, description="原始响应数据")


# ================================
# 统计相关模型
# ================================

class UserRankingResponse(BaseModel):
    """用户排名统计响应模型"""
    success: bool = Field(..., description="是否成功")
    message: str = Field(..., description="响应消息")
    ranking: float = Field(..., description="排名百分比（你比X%的用户更勤奋）")
    task_count: int = Field(..., description="任务数量")
    project_count: int = Field(..., description="项目数量")
    day_count: int = Field(..., description="使用天数")
    completed_count: int = Field(..., description="已完成任务数")
    score: int = Field(..., description="成就值")
    level: int = Field(..., description="账号等级")
    raw_response: Optional[Union[dict, list]] = Field(None, description="原始响应数据")


class GeneralStatisticsResponse(BaseModel):
    """通用统计信息响应模型"""
    success: bool = Field(..., description="是否成功")
    message: str = Field(..., description="响应消息")
    score: int = Field(..., description="成就值")
    level: int = Field(..., description="账号等级")
    yesterday_completed: int = Field(..., description="昨日完成任务数")
    today_completed: int = Field(..., description="今日完成任务数")
    total_completed: int = Field(..., description="总完成任务数")
    today_pomo_count: int = Field(..., description="今日番茄数")
    yesterday_pomo_count: int = Field(..., description="昨日番茄数")
    total_pomo_count: int = Field(..., description="总番茄数")
    today_pomo_duration: int = Field(..., description="今日专注时长（分钟）")
    yesterday_pomo_duration: int = Field(..., description="昨日专注时长（分钟）")
    total_pomo_duration: int = Field(..., description="总专注时长（分钟）")
    pomo_goal: int = Field(..., description="目标番茄数")
    pomo_duration_goal: int = Field(..., description="目标专注时长")
    raw_response: Optional[Union[dict, list]] = Field(None, description="原始响应数据")


class TaskStatisticsResponse(BaseModel):
    """任务统计响应模型"""
    success: bool = Field(..., description="是否成功")
    message: str = Field(..., description="响应消息")
    statistics: Optional[list] = Field(None, description="统计数据列表")
    raw_response: Optional[Union[dict, list]] = Field(None, description="原始响应数据")


# ================================
# 番茄专注相关模型
# ================================

class PomodoroGeneralResponse(BaseModel):
    """番茄专注概览响应模型"""
    success: bool = Field(..., description="是否成功")
    message: str = Field(..., description="响应消息")
    today_pomo_count: int = Field(..., description="今日番茄数量")
    today_pomo_duration: int = Field(..., description="今日专注时长（分钟）")
    total_pomo_count: int = Field(..., description="总番茄数量")
    total_pomo_duration: int = Field(..., description="总专注时长（分钟）")
    raw_response: Optional[Union[dict, list]] = Field(None, description="原始响应数据")


class PomodoroDistributionResponse(BaseModel):
    """番茄专注分布响应模型"""
    success: bool = Field(..., description="是否成功")
    message: str = Field(..., description="响应消息")
    project_durations: Optional[dict] = Field(None, description="按项目分布")
    tag_durations: Optional[dict] = Field(None, description="按标签分布")
    task_durations: Optional[dict] = Field(None, description="按任务分布")
    raw_response: Optional[Union[dict, list]] = Field(None, description="原始响应数据")


class PomodoroTimelineResponse(BaseModel):
    """番茄专注时间线响应模型"""
    success: bool = Field(..., description="是否成功")
    message: str = Field(..., description="响应消息")
    timeline: Optional[list] = Field(None, description="专注记录时间线")
    raw_response: Optional[Union[dict, list]] = Field(None, description="原始响应数据")


# ================================
# 习惯管理相关模型
# ================================

class HabitItem(BaseModel):
    """习惯项模型"""
    id: str = Field(..., description="习惯ID")
    name: str = Field(..., description="习惯名称")
    icon_res: Optional[str] = Field(None, description="图标资源")
    color: Optional[str] = Field(None, description="颜色")
    status: int = Field(..., description="状态（0=未完成，1=已完成）")
    encouragement: Optional[str] = Field(None, description="激励语句")
    total_check_ins: int = Field(0, description="总打卡次数")
    created_time: Optional[str] = Field(None, description="创建时间")
    modified_time: Optional[str] = Field(None, description="修改时间")
    type: Optional[str] = Field(None, description="类型")
    goal: float = Field(1.0, description="目标值")


class HabitsResponse(BaseModel):
    """获取习惯列表响应模型"""
    success: bool = Field(..., description="是否成功")
    message: str = Field(..., description="响应消息")
    habits: Optional[list[HabitItem]] = Field(None, description="习惯列表")
    total_count: int = Field(default=0, description="习惯总数")
    raw_response: Optional[Union[dict, list]] = Field(None, description="原始响应数据")


class HabitWeekStatisticsResponse(BaseModel):
    """习惯本周统计响应模型"""
    success: bool = Field(..., description="是否成功")
    message: str = Field(..., description="响应消息")
    week_statistics: Optional[dict] = Field(None, description="本周打卡统计")
    raw_response: Optional[Union[dict, list]] = Field(None, description="原始响应数据")
