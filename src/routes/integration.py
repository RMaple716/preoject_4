"""行程整合相关路由 - 将各智能体输出拼接为每日行程"""
import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from fastapi import APIRouter
from src.models.response import success_response, error_response

router = APIRouter(prefix="/api/v1/integration", tags=["行程整合"])


# ============== 核心整合逻辑 ==============

def calculate_route_optimization(attractions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    基础路线优化算法：根据景点位置排序，避免折返
    
    Args:
        attractions: 景点列表，每个景点包含 location {lat, lng}
    
    Returns:
        优化后的景点列表（按地理位置就近排序）
    """
    if not attractions or len(attractions) <= 1:
        return attractions
    
    # 简化版：按纬度排序（实际应使用更复杂的路径规划算法）
    sorted_attractions = sorted(
        attractions, 
        key=lambda x: x.get("location", {}).get("lat", 0)
    )
    
    return sorted_attractions


def estimate_transport_time(from_loc: Dict, to_loc: Dict) -> int:
    """
    估算两点之间的交通时间（分钟）
    
    Args:
        from_loc: 起点 {name, lat, lng}
        to_loc: 终点 {name, lat, lng}
    
    Returns:
        预计交通时间（分钟）
    """
    if not from_loc or not to_loc:
        return 30  # 默认30分钟
    
    # 简化判断：如果地点相同或很近，认为距离较近
    from_name = from_loc.get("name", "")
    to_name = to_loc.get("name", "")
    
    if from_name == to_name or from_name in to_name or to_name in from_name:
        return 15
    
    # 其他情况默认30分钟
    return 30


def integrate_agent_results_to_daily_plans(
    agent_results: Dict[str, Any],
    structured_requirement: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """
    将各智能体的输出整合为每日行程
    
    Args:
        agent_results: {
            "attraction": {"attractions": [...]},
            "accommodation": {"hotels": [...]},
            "food": {"restaurants": [...]},
            "transport": {"transport_options": [...]}
        }
        structured_requirement: 结构化需求对象
    
    Returns:
        day_plans列表，每个元素包含:
        - day: 第几天
        - date: 日期字符串
        - attractions: 当天景点列表
        - meals: 当天餐饮列表
        - transport: 交通信息
        - hotel: 住宿信息（仅第一天或换酒店时）
        - daily_cost: 当日总花费
    """
    # 提取基本信息
    travel_days = structured_requirement.get("travel_days", 1)
    travel_date_str = structured_requirement.get("travel_date", datetime.now().strftime("%Y-%m-%d"))
    traveler_count = structured_requirement.get("traveler_count", 1)
    
    # 解析起始日期
    try:
        start_date = datetime.strptime(travel_date_str, "%Y-%m-%d")
    except:
        start_date = datetime.now()
    
    # 提取各智能体数据
    attractions_data = agent_results.get("attraction", {}).get("attractions", [])
    hotels_data = agent_results.get("accommodation", {}).get("hotels", [])
    restaurants_data = agent_results.get("food", {}).get("restaurants", [])
    transport_data = agent_results.get("transport", {}).get("transport_options", [])

    # 为景点数据添加city_name字段
    for attraction in attractions_data:
        if "city_name" not in attraction:
            attraction["city_name"] = city_name

    # 为酒店数据添加city_name字段
    for hotel in hotels_data:
        if "city_name" not in hotel:
            hotel["city_name"] = city_name

    # 为餐厅数据添加city_name字段
    for restaurant in restaurants_data:
        if "city_name" not in restaurant:
            restaurant["city_name"] = city_name
    
    # 对景点进行路线优化
    optimized_attractions = calculate_route_optimization(attractions_data)
    
    # 按时间段分组景点（morning/afternoon/evening）
    morning_attractions = [a for a in optimized_attractions if a.get("visit_time_slot") == "morning"]
    afternoon_attractions = [a for a in optimized_attractions if a.get("visit_time_slot") == "afternoon"]
    evening_attractions = [a for a in optimized_attractions if a.get("visit_time_slot") == "evening"]
    
    # 按天数均匀分配各时间段的景点
    attractions_per_day = {
        "morning": max(1, len(morning_attractions) // travel_days) if morning_attractions else 0,
        "afternoon": max(1, len(afternoon_attractions) // travel_days) if afternoon_attractions else 0,
        "evening": max(1, len(evening_attractions) // travel_days) if evening_attractions else 0
    }
    
    attraction_indices = {
        "morning": 0,
        "afternoon": 0,
        "evening": 0
    }
    
    day_plans = []
    
    for day in range(1, travel_days + 1):
        # 计算当天日期
        current_date = start_date + timedelta(days=day - 1)
        date_str = current_date.strftime("%Y-%m-%d")
        
        # 分配当天的景点（按时间段分配，避免时间冲突）
        day_attractions = []
        
        # 上午景点（09:00-11:30）
        for i in range(attractions_per_day["morning"]):
            if attraction_indices["morning"] < len(morning_attractions):
                attraction = morning_attractions[attraction_indices["morning"]].copy()
                attraction["visit_time"] = "上午"
                attraction["start_time"] = "09:00"
                attraction["end_time"] = "11:30"
                attraction["visit_duration"] = "2.5小时"
                day_attractions.append(attraction)
                attraction_indices["morning"] += 1
        
        # 下午景点（14:00-16:30）
        for i in range(attractions_per_day["afternoon"]):
            if attraction_indices["afternoon"] < len(afternoon_attractions):
                attraction = afternoon_attractions[attraction_indices["afternoon"]].copy()
                attraction["visit_time"] = "下午"
                attraction["start_time"] = "14:00"
                attraction["end_time"] = "16:30"
                attraction["visit_duration"] = "2.5小时"
                day_attractions.append(attraction)
                attraction_indices["afternoon"] += 1
        
        # 晚上景点（18:30-20:00）
        for i in range(attractions_per_day["evening"]):
            if attraction_indices["evening"] < len(evening_attractions):
                attraction = evening_attractions[attraction_indices["evening"]].copy()
                attraction["visit_time"] = "晚上"
                attraction["start_time"] = "18:30"
                attraction["end_time"] = "20:00"
                attraction["visit_duration"] = "1.5小时"
                day_attractions.append(attraction)
                attraction_indices["evening"] += 1
        
        # 安排餐饮（早中晚三餐，时间与景点错开）
        day_meals = []
        meal_schedule = [
            {"meal_type": "breakfast", "meal_time": "早上", "time": "07:30", "duration": "30分钟"},
            {"meal_type": "lunch", "meal_time": "中午", "time": "12:00", "duration": "1小时"},
            {"meal_type": "dinner", "meal_time": "晚上", "time": "17:00", "duration": "1小时"}
        ]
        
        for meal_idx, meal_info in enumerate(meal_schedule):
            # 从餐厅列表中选择一个（简化：循环选择）
            if restaurants_data:
                # 使用取模运算确保索引不越界
                restaurant_index = ((day - 1) * 3 + meal_idx) % len(restaurants_data)
                restaurant = restaurants_data[restaurant_index].copy()
                restaurant["meal_type"] = meal_info["meal_type"]
                restaurant["meal_time"] = meal_info["meal_time"]
                restaurant["time"] = meal_info["time"]
                restaurant["start_time"] = meal_info["time"]
                restaurant["duration"] = meal_info["duration"]
                
                # 设置结束时间
                if meal_info["meal_type"] == "breakfast":
                    restaurant["end_time"] = "08:00"
                elif meal_info["meal_type"] == "lunch":
                    restaurant["end_time"] = "13:00"
                else:  # dinner
                    restaurant["end_time"] = "18:00"
                
                day_meals.append(restaurant)
        
        # 添加交通信息（景点之间）
        day_transport = None
        if len(day_attractions) >= 2:
            # 计算第一个景点到第二个景点的交通
            from_attr = day_attractions[0]
            to_attr = day_attractions[1]
            
            transport_time = estimate_transport_time(
                from_attr.get("location", {}),
                to_attr.get("location", {})
            )
            
            day_transport = {
                "from": from_attr.get("name", ""),
                "to": to_attr.get("name", ""),
                "mode": "transit",
                "duration": f"{transport_time}分钟",
                "cost": 5.0,  # 默认交通费
                "departure_time": "11:30"  # 上午景点结束后出发
            }
        
        # 添加住宿信息（仅第一天或需要换酒店时）
        day_hotel = None
        if day == 1 and hotels_data:
            day_hotel = hotels_data[0].copy()
            day_hotel["check_in_date"] = date_str
        
        # 计算当日花费
        daily_cost = 0
        for attr in day_attractions:
            daily_cost += attr.get("ticket_price", 0) * traveler_count
        for meal in day_meals:
            daily_cost += meal.get("avg_price", 0) * traveler_count
        if day_transport:
            daily_cost += day_transport.get("price", 0) * traveler_count
        if day_hotel:
            daily_cost += day_hotel.get("price_per_night", 0)
        
        # 构建当日行程
        day_plan = {
            "day": day,
            "date": date_str,
            "attractions": day_attractions,
            "meals": day_meals,
            "transport": day_transport,
            "hotel": day_hotel,
            "daily_cost": round(daily_cost, 2),
            "notes": f"第{day}天行程安排"
        }
        
        day_plans.append(day_plan)
    
    return day_plans


# ============== API 路由 ==============

@router.post("/combine")
async def combine_itinerary(request_data: Dict[str, Any]):
    """
    行程整合接口：将各智能体的输出拼接为每日行程
    
    请求参数:
    {
        "task_id": "xxx",
        "agent_results": {
            "attraction": {"attractions": [...]},
            "accommodation": {"hotels": [...]},
            "food": {"restaurants": [...]},
            "transport": {"transport_options": [...]}
        },
        "structured_requirement": {...}
    }
    
    响应:
    {
        "code": 200,
        "msg": "行程整合成功",
        "data": {
            "task_id": "xxx",
            "day_plans": [...],
            "validation": {...}
        }
    }
    """
    # 1. 提取参数
    task_id = request_data.get("task_id")
    agent_results = request_data.get("agent_results")
    structured_req = request_data.get("structured_requirement")
    
    if not agent_results or not structured_req:
        return error_response(code=400, msg="缺少必要参数：agent_results 或 structured_requirement")
    
    # 验证必填字段
    required_fields = ["city_name", "travel_days", "travel_date", "traveler_count"]
    for field in required_fields:
        if field not in structured_req:
            return error_response(code=400, msg=f"结构化需求缺少必填字段：{field}")
    
    # 2. 整合为每日行程
    try:
        day_plans = integrate_agent_results_to_daily_plans(agent_results, structured_req)
        
        # 3. 调用校验接口
        from src.routes.validate import check_itinerary_conflicts
        validation_result = check_itinerary_conflicts(day_plans, structured_req)
        
        # 4. 返回结果
        return success_response(
            data={
                "task_id": task_id,
                "day_plans": day_plans,
                "validation": validation_result,
                "total_cost": sum(day.get("daily_cost", 0) for day in day_plans)
            },
            msg="行程整合成功"
        )
    except Exception as e:
        return error_response(code=500, msg=f"行程整合失败: {str(e)}")


@router.post("/optimize-route")
async def optimize_route(request_data: Dict[str, Any]):
    """
    路线优化接口：对给定景点列表进行路径优化
    
    请求参数:
    {
        "attractions": [
            {"name": "故宫", "location": {"lat": 39.916, "lng": 116.397}},
            ...
        ]
    }
    """
    attractions = request_data.get("attractions", [])
    
    if not attractions:
        return error_response(code=400, msg="缺少景点数据")
    
    try:
        optimized = calculate_route_optimization(attractions)
        return success_response(
            data={"optimized_attractions": optimized},
            msg="路线优化完成"
        )
    except Exception as e:
        return error_response(code=500, msg=f"路线优化失败: {str(e)}")
