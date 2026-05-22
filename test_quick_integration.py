"""
快速测试行程整合功能修复
"""
import sys
sys.path.insert(0, 'd:/memberB/preoject_4')

from src.routes.integration import integrate_agent_results_to_daily_plans

# 测试数据
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

print("测试行程整合功能...")
try:
    day_plans = integrate_agent_results_to_daily_plans(agent_results, structured_requirement)
    print(f"✓ 整合成功！生成了 {len(day_plans)} 天的行程")
    
    for day_plan in day_plans:
        print(f"\n第{day_plan['day']}天 ({day_plan['date']})")
        print(f"  景点数: {len(day_plan.get('attractions', []))}")
        print(f"  餐饮数: {len(day_plan.get('meals', []))}")
        print(f"  当日花费: {day_plan.get('daily_cost', 0)} 元")
        
        # 打印餐饮信息
        if day_plan.get('meals'):
            print(f"  餐饮安排:")
            for meal in day_plan['meals']:
                print(f"    - {meal['meal_time']}: {meal['name']}")
    
    print("\n✅ 所有测试通过！索引问题已修复")
except Exception as e:
    print(f"✗ 测试失败: {str(e)}")
    import traceback
    traceback.print_exc()
