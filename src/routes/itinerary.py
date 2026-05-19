"""行程相关路由"""
import uuid
from datetime import datetime
from fastapi import APIRouter
from src.models.response import success_response, error_response
from src.models.request import ItineraryCreateRequest, ItineraryUpdateRequest

router = APIRouter(prefix="/api/v1/itinerary", tags=["行程"])
itineraries_store = {}

@router.post("/create")
async def create_itinerary(request: ItineraryCreateRequest):
    itinerary_id = str(uuid.uuid4())
    now = datetime.now().isoformat()
    itinerary_data = {
        "itinerary_id": itinerary_id, "user_id": request.user_id, "requirement_id": request.requirement_id,
        "title": request.title, "city_name": request.city_name, "travel_days": request.travel_days,
        "total_budget": request.total_budget, "day_plans": [day.model_dump() for day in request.day_plans],
        "status": "draft", "created_at": now, "updated_at": now
    }
    itineraries_store[itinerary_id] = itinerary_data
    return success_response(data=itinerary_data, msg="行程创建成功")

@router.get("/{itinerary_id}")
async def get_itinerary(itinerary_id: str):
    if itinerary_id not in itineraries_store:
        return error_response(code=404, msg="行程不存在")
    return success_response(data=itineraries_store[itinerary_id], msg="获取成功")

@router.put("/{itinerary_id}")
async def update_itinerary(itinerary_id: str, request: ItineraryUpdateRequest):
    if itinerary_id not in itineraries_store:
        return error_response(code=404, msg="行程不存在")
    itinerary = itineraries_store[itinerary_id]
    if request.title is not None:
        itinerary["title"] = request.title
    if request.day_plans is not None:
        itinerary["day_plans"] = [day.model_dump() for day in request.day_plans]
    itinerary["updated_at"] = datetime.now().isoformat()
    return success_response(data=itinerary, msg="行程更新成功")

@router.delete("/{itinerary_id}")
async def delete_itinerary(itinerary_id: str):
    if itinerary_id not in itineraries_store:
        return error_response(code=404, msg="行程不存在")
    del itineraries_store[itinerary_id]
    return success_response(data={"deleted": True}, msg="行程删除成功")

@router.get("/user/{user_id}")
async def get_user_itineraries(user_id: str):
    user_itineraries = [it for it in itineraries_store.values() if it["user_id"] == user_id]
    return success_response(data={"total": len(user_itineraries), "itineraries": user_itineraries}, msg="获取成功")