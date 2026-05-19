"""校验相关路由"""
from fastapi import APIRouter
from src.models.response import success_response, error_response
from src.models.request import ItineraryValidateRequest, ItineraryValidateResponse, ConflictItem, TimeConflictRequest, TimeConflictResponse

router = APIRouter(prefix="/api/v1/validate", tags=["校验"])

@router.post("/itinerary")
async def validate_itinerary(request: ItineraryValidateRequest):
    if not request.itinerary_id and not request.day_plans:
        return error_response(code=400, msg="请提供行程ID或行程数据")
    conflicts = []
    suggestions = []
    if request.day_plans:
        for day_plan in request.day_plans:
            day_data = day_plan.model_dump() if hasattr(day_plan, 'model_dump') else day_plan
            attractions = day_data.get("attractions", [])
            if len(attractions) > 5:
                conflicts.append(ConflictItem(type="warning", description=f"第{day_data.get('day', '?')}天景点过多", severity="warning"))
                suggestions.append(f"第{day_data.get('day', '?')}天建议保留3-4个核心景点")
    valid = len([c for c in conflicts if c.severity == "error"]) == 0
    return success_response(data=ItineraryValidateResponse(valid=valid, conflicts=[c.model_dump() for c in conflicts], suggestions=suggestions).model_dump(), msg="校验完成")

@router.post("/time")
async def check_time_conflict(request: TimeConflictRequest):
    schedule = request.schedule
    conflicts = []
    for i, item1 in enumerate(schedule):
        for item2 in schedule[i + 1:]:
            if item1.get("start_time", "") < item2.get("end_time", "") and item2.get("start_time", "") < item1.get("end_time", ""):
                conflicts.append({"time1": f"{item1.get('start_time')}-{item1.get('end_time')}", "time2": f"{item2.get('start_time')}-{item2.get('end_time')}"})
    return success_response(data=TimeConflictResponse(has_conflict=len(conflicts) > 0, conflicts=conflicts).model_dump(), msg="时间冲突检测完成")