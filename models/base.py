"""数据模型定义"""
from datetime import datetime, timezone, timedelta
from typing import Optional, Union
from pydantic import BaseModel, Field, ConfigDict

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


class FocusOperation(BaseModel):
    """番茄钟操作项模型"""
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
        json_schema_extra={
            "description": "番茄钟单个操作项，需和滴答清单桌面端保持一致。",
            "examples": [
                {
                    "id": "6915ae6838b6e20c76868c45",
                    "oId": "6915ae6838b6e20c76868c44",
                    "oType": 0,
                    "op": "start",
                    "duration": 25,
                    "firstFocusId": "6915ae6838b6e20c76868c44",
                    "focusOnId": "",
                    "autoPomoLeft": 5,
                    "pomoCount": 1,
                    "manual": True,
                    "note": "",
                    "time": "2025-11-13T10:09:44.765+0000"
                }
            ]
        }
    )

    id: str = Field(
        ...,
        description="【必填】操作唯一ID，建议复用官方返回的 id 或使用 UUID。",
        examples=["6915ae6838b6e20c76868c45"]
    )
    o_id: str = Field(
        ...,
        alias="oId",
        description="【必填】目标番茄钟 ID，通常与 firstFocusId 相同。",
        examples=["6915ae6838b6e20c76868c44"]
    )
    o_type: int = Field(
        ...,
        alias="oType",
        description="【必填】对象类型，番茄钟固定为 0。",
        examples=[0]
    )
    op: str = Field(
        ...,
        description="【必填】操作类型，例如 start、pause、continue、drop、exit。",
        examples=["start"]
    )
    duration: int = Field(
        ...,
        description="【必填】番茄钟总时长（分钟）。",
        examples=[25]
    )
    first_focus_id: str = Field(
        ...,
        alias="firstFocusId",
        description="【必填】首个番茄钟 ID，用于串联同一番茄会话。",
        examples=["6915ae6838b6e20c76868c44"]
    )
    focus_on_id: str = Field(
        "",
        alias="focusOnId",
        description="【选填】关联的专注任务 ID，没有可保持为空字符串。",
        examples=[""]
    )
    focus_on_type: Optional[int] = Field(
        None,
        alias="focusOnType",
        description="【选填】关联对象类型（0=任务，1=清单，2=习惯等）"
    )
    focus_on_title: Optional[str] = Field(
        None,
        alias="focusOnTitle",
        description="【选填】关联对象标题"
    )
    auto_pomo_left: int = Field(
        0,
        alias="autoPomoLeft",
        description="【选填】自动番茄剩余数量，保持与最新响应一致。",
        examples=[5]
    )
    pomo_count: int = Field(
        0,
        alias="pomoCount",
        description="【选填】当前番茄累计数量。",
        examples=[1]
    )
    manual: bool = Field(
        True,
        description="【选填】是否手动触发操作，桌面端默认 true。",
        examples=[True]
    )
    note: str = Field(
        "",
        description="【选填】备注信息，可留空。",
        examples=[""]
    )
    time: str = Field(
        ...,
        description="【必填】操作时间，ISO 字符串，示例：2025-11-13T10:09:44.765+0000。",
        examples=["2025-11-13T10:09:44.765+0000"]
    )
    created_time: Optional[int] = Field(
        None,
        alias="createdTime",
        description="【选填】操作创建时间戳（毫秒）"
    )


class FocusOperationRequest(BaseModel):
    """番茄钟操作请求模型"""
    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "description": "番茄钟批量操作请求体，lastPoint 与 opList 为必填字段。",
            "example": {
                "lastPoint": 1760632928097,
                "opList": [
                    {
                        "id": "6915ae6838b6e20c76868c45",
                        "oId": "6915ae6838b6e20c76868c44",
                        "oType": 0,
                        "op": "start",
                        "duration": 25,
                        "firstFocusId": "6915ae6838b6e20c76868c44",
                        "focusOnId": "",
                        "autoPomoLeft": 5,
                        "pomoCount": 1,
                        "manual": True,
                        "note": "",
                        "time": "2025-11-13T10:09:44.765+0000"
                    }
                ]
            }
        }
    )

    last_point: int = Field(
        ...,
        alias="lastPoint",
        description="【必填】最新 point 指针值，使用上一次响应中的 point。",
        examples=[1760632928097]
    )
    op_list: list[FocusOperation] = Field(
        ...,
        alias="opList",
        description="【必填】番茄钟操作项列表，可在一次请求中提交一个或多个操作。",
        examples=[[
            {
                "id": "6915ae6838b6e20c76868c45",
                "oId": "6915ae6838b6e20c76868c44",
                "oType": 0,
                "op": "start",
                "duration": 25,
                "firstFocusId": "6915ae6838b6e20c76868c44",
                "focusOnId": "",
                "autoPomoLeft": 5,
                "pomoCount": 1,
                "manual": True,
                "note": "",
                "time": "2025-11-13T10:09:44.765+0000"
            }
        ]]
    )


class FocusStartOptions(BaseModel):
    """番茄钟开始操作参数"""

    duration: int = Field(25, ge=1, le=360, description="番茄时长（分钟）")
    auto_pomo_left: int = Field(5, ge=0, alias="autoPomoLeft", description="自动番茄剩余数量")
    pomo_count: int = Field(1, ge=0, alias="pomoCount", description="当前番茄累计数量")
    manual: bool = Field(True, description="是否手动操作")
    note: str = Field("", description="备注信息", max_length=512)
    focus_on_id: str = Field("", alias="focusOnId", description="关联的任务 ID，可为空字符串")
    focus_on_type: Optional[int] = Field(None, alias="focusOnType", description="关联对象类型，例如 0=任务")
    focus_on_title: Optional[str] = Field(None, alias="focusOnTitle", description="关联对象标题")
    last_point: Optional[int] = Field(None, alias="lastPoint", ge=0, description="覆盖使用的同步指针，默认为缓存值")


class FocusControlOptions(BaseModel):
    """番茄钟控制操作参数（暂停、继续、完成等）"""

    manual: Optional[bool] = Field(None, description="是否手动操作（为空则沿用上次设置）")
    note: Optional[str] = Field(None, description="备注信息，不传则沿用上次记录", max_length=512)
    focus_on_type: Optional[int] = Field(None, alias="focusOnType", description="关联对象类型")
    focus_on_title: Optional[str] = Field(None, alias="focusOnTitle", description="关联对象标题")
    last_point: Optional[int] = Field(None, alias="lastPoint", ge=0, description="覆盖使用的同步指针")


class FocusStopOptions(FocusControlOptions):
    """番茄钟结束操作参数（drop/exit）"""

    include_exit: bool = Field(True, description="是否在 drop 后自动追加 exit 操作")


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
