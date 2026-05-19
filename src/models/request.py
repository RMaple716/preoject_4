"""
请求模型定义
"""
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


# ============== 用户需求相关 ==============
class UserRequirement(BaseModel):
    """用户需求基础模型"""
    city_name: str = Field(..., description="目的地城市名称")
    travel_days: int = Field(..., ge=1, le=30, description="出行天数")
    total_budget: Optional[float] = Field(None, ge=0, description="总预算（元）")
    travel_type: Optional[str] = Field(None, description="出行类型: family/couple/friends/solo/business")
    start_date: Optional[str] = Field(None, description="出发日期 YYYY-MM-DD")
    preferences: Optional[List[str]] = Field(default_factory=list, description="用户偏好标签")


class RequirementSubmitRequest(BaseModel):
    """提交用户需求请求"""
    user_id: str = Field(..., description="用户ID")
    requirement: UserRequirement


class RequirementSubmitResponse(BaseModel):
    """提交用户需求响应"""
    requirement_id: str
    status: str = "pending"


class RequirementParseRequest(BaseModel):
    """需求预处理请求"""
    requirement_id: str


class ParsedKeywords(BaseModel):
    """解析后的关键词"""
    city_name: str
    travel_days: int
    total_budget: Optional[float] = None
    travel_type: Optional[str] = None
    preferences: List[str] = Field(default_factory=list)


class RequirementParseResponse(BaseModel):
    """需求预处理响应"""
    requirement_id: str
    parsed: bool = False
    keywords: Optional[ParsedKeywords] = None


# ============== 任务分发相关 ==============
class TaskDispatchRequest(BaseModel):
    """任务分发请求"""
    requirement_id: str
    agents: List[str] =Field(..., description="attractions/transport/hotel/food")


class TaskInfo(BaseModel):
    """任务信息"""
    task_id: str
    agent: str
    status: str  # pending/running/completed/failed
    result: Optional[dict] = None


class TaskDispatchResponse(BaseModel):
    """任务分发响应"""
    batch_id: str
    tasks: List[TaskInfo]


class TaskStatusResponse(BaseModel):
    """任务状态响应"""
    task_id: str
    agent: str
    status: str
    result: Optional[dict] = None
    error: Optional[str] = None


# ============== 智能体相关 ==============
class AttractionsAgentRequest(BaseModel):
    """景点智能体请求"""
    city_name: str
    travel_days: int = Field(..., ge=1)
    total_budget: Optional[float] = None
    preferences: List[str] = Field(default_factory=list)
    location_preference: Optional[str] = None


class AttractionsAgentResponse(BaseModel):
    """景点智能体响应"""
    attractions: List[dict] = Field(default_factory=list)


class TransportAgentRequest(BaseModel):
    """交通智能体请求"""
    from_city: str
    to_city: str
    travel_date: str
    transport_type: Optional[str] = None  # plane/train/bus


class TransportAgentResponse(BaseModel):
    """交通智能体响应"""
    transport_options: List[dict] = Field(default_factory=list)


class HotelAgentRequest(BaseModel):
    """住宿智能体请求"""
    city_name: str
    check_in_date: str
    check_out_date: str
    budget_per_night: Optional[float] = None
    location_preference: Optional[str] = None


class HotelAgentResponse(BaseModel):
    """住宿智能体响应"""
    hotels: List[dict] = Field(default_factory=list)


class FoodAgentRequest(BaseModel):
    """美食智能体请求"""
    city_name: str
    budget_per_meal: Optional[float] = None
    cuisine_type: Optional[str] = None


class FoodAgentResponse(BaseModel):
    """美食智能体响应"""
    restaurants: List[dict] = Field(default_factory=list)


# ============== 行程相关 ==============
class DayPlan(BaseModel):
    """每日行程"""
    day: int = Field(..., ge=1)
    date: str  # YYYY-MM-DD
    attractions: List[dict] = Field(default_factory=list)
    transport: Optional[dict] = None
    hotel: Optional[dict] = None
    meals: List[dict] = Field(default_factory=list)
    notes: Optional[str] = None


class ItineraryCreateRequest(BaseModel):
    """创建行程请求"""
    user_id: str
    requirement_id: str
    title: str
    city_name: str
    travel_days: int = Field(..., ge=1)
    total_budget: Optional[float] = None
    day_plans: List[DayPlan]


class ItineraryUpdateRequest(BaseModel):
    """更新行程请求"""
    title: Optional[str] = None
    day_plans: Optional[List[DayPlan]] = None


class ItineraryResponse(BaseModel):
    """行程响应"""
    itinerary_id: str
    user_id: str
    requirement_id: str
    title: str
    city_name: str
    travel_days: int
    total_budget: Optional[float] = None
    day_plans: List[dict]
    status: str  # draft/completed/archived
    created_at: str
    updated_at: str


# ============== 校验相关 ==============
class ConflictItem(BaseModel):
    """冲突项"""
    type: str  # time/location/budget
    description: str
    severity: str = "warning"  # warning/error


class ItineraryValidateRequest(BaseModel):
    """行程校验请求"""
    itinerary_id: Optional[str] = None
    day_plans: Optional[List[DayPlan]] = None
    structured_requirement: Optional[Dict[str, Any]] = None  # 添加结构化需求字段


class ItineraryValidateResponse(BaseModel):
    """行程校验响应"""
    valid: bool
    conflicts: List[ConflictItem] = Field(default_factory=list)
    suggestions: List[str] = Field(default_factory=list)


class TimeConflictRequest(BaseModel):
    """时间冲突检测请求"""
    schedule: List[dict]


class TimeConflictResponse(BaseModel):
    """时间冲突检测响应"""
    has_conflict: bool
    conflicts: List[dict] = Field(default_factory=list)