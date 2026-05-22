"""
调试测试 - 查看详细错误信息
"""
import sys
sys.path.insert(0, 'd:/memberB/preoject_4')

from src.routes.integration import integrate_agent_results_to_daily_plans
import traceback

# 测试数据 - 完全模拟test_integration.py中的数据
agent_results = {
    "attraction": {
        "attractions": [
            {
                "id": "att_001",
                "name": "故宫博物院",
                "category": "历史古迹",
                "suggested_duration": "4小时",
                "visit_time_slot": "morning",
                "ticket_price": 60.0,
                "location": {"lat": 39.916, "lng": 116.397},
                "tags": ["必去", "室内"]
            },
            {
                "id": "att_002",
                "name": "颐和园",
                "category": "皇家园林",
                "suggested_duration": "3小时",
                "visit_time_slot": "afternoon",
                "ticket_price": 30.0,
                "location": {"lat": 39.998, "lng": 116.275},
                "tags": ["自然", "户外"]
            },
            {
                "id": "att_003",
                "name": "天坛公园",
                "category": "历史古迹",
                "suggested_duration": "2小时",
                "visit_time_slot": "morning",
                "ticket_price": 15.0,
                "location": {"lat": 39.882, "lng": 116.407},
                "tags": ["历史"]
            },
            {
                "id": "att_004",
                "name": "圆明园",
                "category": "遗址公园",
                "suggested_duration": "3小时",
                "visit_time_slot": "afternoon",
                "ticket_price": 25.0,
                "location": {"lat": 40.008, "lng": 116.298},
                "tags": ["历史", "户外"]
            },
            {
                "id": "att_005",
                "name": "北海公园",
                "category": "皇家园林",
                "suggested_duration": "2小时",
                "visit_time_slot": "evening",
                "ticket_price": 10.0,
                "location": {"lat": 39.925, "lng": 116.389},
                "tags": ["休闲"]
            },
            {
                "id": "att_006",
                "name": "景山公园",
                "category": "城市公园",
                "suggested_duration": "1.5小时",
                "visit_time_slot": "evening",
                "ticket_price": 2.0,
                "location": {"lat": 39.924, "lng": 116.397},
                "tags": ["观景"]
            }
        ]
    },
    "accommodation": {
        "hotels": [
            {
                "id": "hotel_001",
                "name": "北京王府井希尔顿酒店",
                "address": "东城区王府井大街8号",
                "price_per_night": 800.0,
                "rating": 4.8,
                "distance_to_center_km": 1.5,
                "amenities": ["早餐", "WiFi", "停车场"]
            }
        ]
    },
    "food": {
        "restaurants": [
            {
                "id": "rest_001",
                "name": "四季民福烤鸭店",
                "cuisine": "京菜",
                "avg_price_per_person": 150.0,
                "rating": 4.7,
                "recommended_dishes": ["酥香嫩烤鸭", "贝勒烤肉"],
                "location": {"lat": 39.910, "lng": 116.400}
            },
            {
                "id": "rest_002",
                "name": "全聚德",
                "cuisine": "京菜",
                "avg_price_per_person": 200.0,
                "rating": 4.5,
                "recommended_dishes": ["烤鸭"],
                "location": {"lat": 39.900, "lng": 116.395}
            },
            {
                "id": "rest_003",
                "name": "老北京炸酱面大王",
                "cuisine": "小吃",
                "avg_price_per_person": 50.0,
                "rating": 4.3,
                "recommended_dishes": ["炸酱面"],
                "location": {"lat": 39.905, "lng": 116.402}
            }
        ]
    },
    "transport": {
        "transport_options": [
            {
                "from": "故宫博物院",
                "to": "颐和园",
                "mode": "transit",
                "duration_minutes": 50,
                "cost": 5.0
            }
        ]
    }
}

structured_requirement = {
    "city_name": "北京",
    "travel_days": 3,
    "total_budget": 5000,
    "travel_date": "2026-05-20",
    "traveler_count": 2,
    "preferences": ["历史古迹", "美食"],
    "dislikes": ["爬山"],
    "accommodation_budget": 1500,
    "food_budget": 1200,
    "transport_budget": 800,
    "ticket_budget": 1000
}

print("=" * 60)
print("调试测试 - 行程整合功能")
print("=" * 60)

try:
    print("\n开始整合...")
    day_plans = integrate_agent_results_to_daily_plans(agent_results, structured_requirement)
    
    print(f"\n✓ 整合成功！生成了 {len(day_plans)} 天的行程\n")
    
    for day_plan in day_plans:
        print(f"第{day_plan['day']}天 ({day_plan['date']})")
        print(f"  景点数: {len(day_plan.get('attractions', []))}")
        print(f"  餐饮数: {len(day_plan.get('meals', []))}")
        print(f"  当日花费: {day_plan.get('daily_cost', 0)} 元")
        
        if day_plan.get('meals'):
            print(f"  餐饮安排:")
            for meal in day_plan['meals']:
                print(f"    - {meal['meal_time']}: {meal['name']} (¥{meal.get('avg_price_per_person', 0)})")
        print()
    
    print("=" * 60)
    print("✅ 测试通过！索引问题已修复")
    print("=" * 60)
    
except Exception as e:
    print(f"\n✗ 测试失败: {str(e)}")
    print("\n详细错误信息:")
    traceback.print_exc()
    print("\n" + "=" * 60)
