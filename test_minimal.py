"""
最小化测试 - 定位list index out of range错误
"""
import sys
sys.path.insert(0, 'd:/memberB/preoject_4')

# 先测试餐厅索引计算
print("测试餐厅索引计算...")
restaurants_data = [{"name": f"餐厅{i}"} for i in range(3)]
travel_days = 3

for day in range(1, travel_days + 1):
    print(f"\n第{day}天:")
    for meal_idx in range(3):
        restaurant_index = ((day - 1) * 3 + meal_idx) % len(restaurants_data)
        print(f"  meal_idx={meal_idx}, 索引={restaurant_index}, 餐厅={restaurants_data[restaurant_index]['name']}")

print("\n✅ 餐厅索引计算正常")

# 现在测试完整的整合函数
print("\n" + "="*60)
print("测试完整整合功能...")
print("="*60)

from src.routes.integration import integrate_agent_results_to_daily_plans
import traceback

agent_results = {
    "attraction": {
        "attractions": [
            {"name": "故宫", "visit_time_slot": "morning", "ticket_price": 60, "location": {"lat": 39.916, "lng": 116.397}},
            {"name": "颐和园", "visit_time_slot": "afternoon", "ticket_price": 30, "location": {"lat": 39.998, "lng": 116.275}},
            {"name": "天坛", "visit_time_slot": "morning", "ticket_price": 15, "location": {"lat": 39.882, "lng": 116.407}},
            {"name": "圆明园", "visit_time_slot": "afternoon", "ticket_price": 25, "location": {"lat": 40.008, "lng": 116.298}},
            {"name": "北海公园", "visit_time_slot": "evening", "ticket_price": 10, "location": {"lat": 39.925, "lng": 116.389}},
            {"name": "景山公园", "visit_time_slot": "evening", "ticket_price": 2, "location": {"lat": 39.924, "lng": 116.397}}
        ]
    },
    "accommodation": {
        "hotels": [
            {"name": "王府井酒店", "price_per_night": 800.0}
        ]
    },
    "food": {
        "restaurants": [
            {"name": "四季民福", "avg_price_per_person": 150.0},
            {"name": "全聚德", "avg_price_per_person": 200.0},
            {"name": "炸酱面大王", "avg_price_per_person": 50.0}
        ]
    },
    "transport": {
        "transport_options": []
    }
}

structured_requirement = {
    "city_name": "北京",
    "travel_days": 3,
    "total_budget": 5000,
    "travel_date": "2026-05-20",
    "traveler_count": 2
}

try:
    day_plans = integrate_agent_results_to_daily_plans(agent_results, structured_requirement)
    print(f"\n✓ 整合成功！生成了 {len(day_plans)} 天的行程")
    
    for day_plan in day_plans:
        print(f"\n第{day_plan['day']}天 ({day_plan['date']})")
        print(f"  景点: {len(day_plan.get('attractions', []))}个")
        print(f"  餐饮: {len(day_plan.get('meals', []))}个")
        
except Exception as e:
    print(f"\n✗ 整合失败: {str(e)}")
    print("\n错误堆栈:")
    traceback.print_exc()
