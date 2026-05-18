"""智能体相关路由"""
from fastapi import APIRouter
from src.models.response import success_response
from src.models.request import (
    AttractionsAgentRequest, AttractionsAgentResponse,
    TransportAgentRequest, TransportAgentResponse,
    HotelAgentRequest, HotelAgentResponse,
    FoodAgentRequest, FoodAgentResponse
)

router = APIRouter(prefix="/api/v1/agent", tags=["智能体"])

@router.post("/attractions")
async def attractions_agent(request: AttractionsAgentRequest):
    # TODO: 实现景点推荐逻辑
    attractions = [{"name": "示例景点", "duration": "2-3小时", "fee": 50.0, "location": "市中心"}]
    return success_response(data=AttractionsAgentResponse(attractions=attractions).model_dump(), msg="景点推荐成功")

@router.post("/transport")
async def transport_agent(request: TransportAgentRequest):
    transport_options = [{"type": "高铁", "departure_time": "08:00", "arrival_time": "12:30", "price": 500.0}]
    return success_response(data=TransportAgentResponse(transport_options=transport_options).model_dump(), msg="交通推荐成功")

@router.post("/hotel")
async def hotel_agent(request: HotelAgentRequest):
    hotels = [{"name": "示例酒店", "address": "市中心", "price_per_night": 300.0, "rating": 4.5}]
    return success_response(data=HotelAgentResponse(hotels=hotels).model_dump(), msg="住宿推荐成功")

@router.post("/food")
async def food_agent(request: FoodAgentRequest):
    restaurants = [{"name": "示例餐厅", "cuisine": "本地特色", "avg_price": 80.0, "rating": 4.6}]
    return success_response(data=FoodAgentResponse(restaurants=restaurants).model_dump(), msg="美食推荐成功")