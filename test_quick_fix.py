"""
快速测试脚本 - 仅测试基本整合功能
"""
import requests
import json

BASE_URL = "http://127.0.0.1:9091"

def quick_test():
    """快速测试行程整合"""
    
    agent_results = {
        "attraction": {
            "attractions": [
                {"id": "att_001", "name": "故宫博物院", "visit_time_slot": "morning", "ticket_price": 60.0, "location": {"lat": 39.916, "lng": 116.397}},
                {"id": "att_002", "name": "颐和园", "visit_time_slot": "afternoon", "ticket_price": 30.0, "location": {"lat": 39.998, "lng": 116.275}},
                {"id": "att_003", "name": "天坛公园", "visit_time_slot": "morning", "ticket_price": 15.0, "location": {"lat": 39.882, "lng": 116.407}},
                {"id": "att_004", "name": "圆明园", "visit_time_slot": "afternoon", "ticket_price": 25.0, "location": {"lat": 40.008, "lng": 116.298}}
            ]
        },
        "accommodation": {
            "hotels": [
                {"id": "hotel_001", "name": "北京王府井希尔顿酒店", "price_per_night": 800.0}
            ]
        },
        "food": {
            "restaurants": [
                {"id": "rest_001", "name": "四季民福烤鸭店", "avg_price_per_person": 150.0},
                {"id": "rest_002", "name": "全聚德", "avg_price_per_person": 200.0}
            ]
        },
        "transport": {"transport_options": []}
    }
    
    structured_requirement = {
        "city_name": "北京",
        "travel_days": 2,
        "total_budget": 5000,
        "travel_date": "2026-05-20",
        "traveler_count": 2
    }
    
    url = f"{BASE_URL}/api/v1/integration/combine"
    payload = {
        "task_id": "quick_test_001",
        "agent_results": agent_results,
        "structured_requirement": structured_requirement
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        result = response.json()
        
        print("=" * 60)
        print("快速测试结果")
        print("=" * 60)
        print(f"状态码: {result.get('code')}")
        print(f"消息: {result.get('msg')}")
        
        if result.get('code') == 200:
            data = result.get('data', {})
            validation = data.get('validation', {})
            
            print(f"\n✓ 整合成功！")
            print(f"天数: {len(data.get('day_plans', []))}")
            print(f"总花费: {data.get('total_cost', 0)} 元")
            print(f"\n校验结果:")
            print(f"  是否有效: {validation.get('valid', False)}")
            print(f"  冲突数: {len(validation.get('conflicts', []))}")
            
            if validation.get('conflicts'):
                print(f"\n冲突详情:")
                for conflict in validation['conflicts']:
                    print(f"  - [{conflict.get('severity')}] {conflict.get('description')}")
            
            # 打印每天的简要信息
            print(f"\n每日行程:")
            for day_plan in data.get('day_plans', []):
                print(f"\n第{day_plan['day']}天 ({day_plan['date']})")
                print(f"  景点: {len(day_plan.get('attractions', []))}个")
                print(f"  餐饮: {len(day_plan.get('meals', []))}个")
                
                # 打印时间安排
                print(f"  时间安排:")
                for attr in day_plan.get('attractions', []):
                    print(f"    {attr.get('start_time', '?')}-{attr.get('end_time', '?')}: {attr.get('name')}")
                for meal in day_plan.get('meals', []):
                    print(f"    {meal.get('start_time', '?')}-{meal.get('end_time', '?')}: {meal.get('name')} ({meal.get('meal_type')})")
        else:
            print(f"✗ 失败: {result.get('msg')}")
            
    except Exception as e:
        print(f"✗ 异常: {str(e)}")


if __name__ == "__main__":
    quick_test()
