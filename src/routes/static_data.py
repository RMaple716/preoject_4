"""静态数据相关路由"""
from typing import List, Optional
from fastapi import APIRouter, Query
from src.models.response import success_response
from src.models.static_data import Attraction, City, Location, StaticAttractionsResponse, StaticCitiesResponse, StaticLocationsResponse

router = APIRouter(prefix="/api/v1/static", tags=["静态数据"])

SAMPLE_CITIES = [
    {"city_id": "c001", "city_name": "北京", "province": "北京", "country": "中国", "description": "中国的首都", "tags": ["历史文化", "政治中心"]},
    {"city_id": "c002", "city_name": "上海", "province": "上海", "country": "中国", "description": "国际化大都市", "tags": ["都市", "购物"]},
    {"city_id": "c003", "city_name": "成都", "province": "四川", "country": "中国", "description": "天府之国", "tags": ["美食", "大熊猫"]},
    {"city_id": "c004", "city_name": "杭州", "province": "浙江", "country": "中国", "description": "人间天堂", "tags": ["自然风光"]},
    {"city_id": "c005", "city_name": "西安", "province": "陕西", "country": "中国", "description": "千年古都", "tags": ["历史", "美食"]},
]

SAMPLE_ATTRACTIONS = [
    {"attraction_id": "a001", "name": "故宫", "city_name": "北京", "category": "scenic_spot", "ticket_price": 60.0, "rating": 4.8, "tags": ["历史", "建筑"]},
    {"attraction_id": "a002", "name": "天坛", "city_name": "北京", "category": "scenic_spot", "ticket_price": 34.0, "rating": 4.7, "tags": ["历史"]},
    {"attraction_id": "a003", "name": "外滩", "city_name": "上海", "category": "scenic_spot", "ticket_price": 0, "rating": 4.6, "tags": ["夜景"]},
    {"attraction_id": "a004", "name": "西湖", "city_name": "杭州", "category": "scenic_spot", "ticket_price": 0, "rating": 4.9, "tags": ["自然风光"]},
    {"attraction_id": "a005", "name": "宽窄巷子", "city_name": "成都", "category": "scenic_spot", "ticket_price": 0, "rating": 4.5, "tags": ["美食", "文化"]},
    {"attraction_id": "a006", "name": "兵马俑", "city_name": "西安", "category": "museum", "ticket_price": 120.0, "rating": 4.9, "tags": ["历史"]},
]

@router.get("/attractions")
async def get_attractions(category: Optional[str] = None, tags: Optional[List[str]] = Query(None)):
    attractions = SAMPLE_ATTRACTIONS
    if category:
        attractions = [a for a in attractions if a["category"] == category]
    cities = list(set(a["city_name"] for a in attractions))
    return success_response(data=StaticAttractionsResponse(total=len(attractions), cities=cities, attractions=[Attraction(**a) for a in attractions]).model_dump(), msg="获取成功")

@router.get("/attractions/{city_name}")
async def get_city_attractions(city_name: str):
    attractions = [a for a in SAMPLE_ATTRACTIONS if a["city_name"] == city_name]
    return success_response(data={"city_name": city_name, "total": len(attractions), "attractions": attractions}, msg="获取成功")

@router.get("/cities")
async def get_cities():
    return success_response(data=StaticCitiesResponse(total=len(SAMPLE_CITIES), cities=[City(**c) for c in SAMPLE_CITIES]).model_dump(), msg="获取成功")