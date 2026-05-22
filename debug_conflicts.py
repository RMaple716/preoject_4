"""
调试脚本：查看详细的时间冲突信息
"""
import requests
import json

BASE_URL = "http://127.0.0.1:9091"

def debug_conflicts():
    """调试并显示详细的冲突信息"""
    
    # 构造模拟的智能体返回数据（与test_integration.py相同）
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
    
    url = f"{BASE_URL}/api/v1/integration/combine"
    payload = {
        "task_id": "debug_task_001",
        "agent_results": agent_results,
        "structured_requirement": structured_requirement
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        result = response.json()
        
        print("=" * 80)
        print("行程整合调试 - 详细冲突分析")
        print("=" * 80)
        
        if result.get('code') == 200:
            data = result.get('data', {})
            validation = data.get('validation', {})
            conflicts = validation.get('conflicts', [])
            
            print(f"\n总冲突数: {len(conflicts)}")
            print(f"是否有效: {validation.get('valid', False)}")
            print(f"总花费: {data.get('total_cost', 0)} 元\n")
            
            # 按类型分类统计
            conflict_types = {}
            for conflict in conflicts:
                ctype = conflict.get('type', 'unknown')
                if ctype not in conflict_types:
                    conflict_types[ctype] = []
                conflict_types[ctype].append(conflict)
            
            print("冲突类型统计:")
            for ctype, c_list in conflict_types.items():
                print(f"  - {ctype}: {len(c_list)} 个")
            
            print("\n" + "=" * 80)
            print("详细冲突列表:")
            print("=" * 80)
            
            for idx, conflict in enumerate(conflicts, 1):
                print(f"\n[{idx}] 类型: {conflict.get('type')}")
                print(f"    严重程度: {conflict.get('severity')}")
                print(f"    描述: {conflict.get('description')}")
                if conflict.get('day'):
                    print(f"    第{conflict['day']}天 ({conflict.get('date', '')})")
            
            print("\n" + "=" * 80)
            print("建议:")
            print("=" * 80)
            for suggestion in validation.get('suggestions', []):
                print(f"  • {suggestion}")
            
            # 打印每天的行程安排
            print("\n" + "=" * 80)
            print("每日行程详情:")
            print("=" * 80)
            
            day_plans = data.get('day_plans', [])
            for day_plan in day_plans:
                print(f"\n--- 第{day_plan['day']}天 ({day_plan['date']}) ---")
                print(f"当日花费: {day_plan.get('daily_cost', 0)} 元")
                
                print("\n景点安排:")
                for attr in day_plan.get('attractions', []):
                    print(f"  • {attr.get('name')}")
                    print(f"    时间: {attr.get('start_time', '?')}-{attr.get('end_time', '?')}")
                    print(f"    时段: {attr.get('visit_time', '?')}")
                
                print("\n餐饮安排:")
                for meal in day_plan.get('meals', []):
                    print(f"  • {meal.get('name')} ({meal.get('meal_type', '?')})")
                    print(f"    时间: {meal.get('time', '?')}")
                
                if day_plan.get('transport'):
                    t = day_plan['transport']
                    print(f"\n交通: {t.get('from')} → {t.get('to')}")
                    print(f"  方式: {t.get('mode')}, 耗时: {t.get('duration')}")
                
                if day_plan.get('hotel'):
                    print(f"\n住宿: {day_plan['hotel']['name']}")
                    print(f"  价格: {day_plan['hotel']['price_per_night']} 元/晚")
        
        else:
            print(f"✗ 请求失败: {result.get('msg')}")
            
    except Exception as e:
        print(f"✗ 异常: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    debug_conflicts()
