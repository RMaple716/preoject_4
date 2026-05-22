"""
行程整合功能测试脚本

测试场景:
1. 基本的行程整合（3天2夜）
2. 路线优化功能
3. 时间冲突检测集成
4. 边界情况处理（空数据、单天行程等）
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:9091"


def test_basic_integration():
    """测试基本的行程整合功能"""
    print("\n=== 测试1: 基本行程整合 ===")
    
    # 构造模拟的智能体返回数据
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
    
    # 结构化需求
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
    
    # 调用整合接口
    url = f"{BASE_URL}/api/v1/integration/combine"
    payload = {
        "task_id": "test_task_001",
        "agent_results": agent_results,
        "structured_requirement": structured_requirement
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        result = response.json()
        
        print(f"状态码: {result.get('code')}")
        print(f"消息: {result.get('msg')}")
        
        if result.get('code') == 200:
            data = result.get('data', {})
            day_plans = data.get('day_plans', [])
            
            print(f"\n✓ 整合成功！生成了 {len(day_plans)} 天的行程")
            print(f"总花费: {data.get('total_cost', 0)} 元")
            
            # 打印每天的简要信息
            for day_plan in day_plans:
                print(f"\n--- 第{day_plan['day']}天 ({day_plan['date']}) ---")
                print(f"  景点数: {len(day_plan.get('attractions', []))}")
                print(f"  餐饮数: {len(day_plan.get('meals', []))}")
                print(f"  当日花费: {day_plan.get('daily_cost', 0)} 元")
                
                if day_plan.get('hotel'):
                    print(f"  住宿: {day_plan['hotel']['name']}")
                
                if day_plan.get('transport'):
                    print(f"  交通: {day_plan['transport']['from']} → {day_plan['transport']['to']}")
            
            # 检查校验结果
            validation = data.get('validation', {})
            print(f"\n校验结果:")
            print(f"  是否有效: {validation.get('valid', False)}")
            print(f"  冲突数: {len(validation.get('conflicts', []))}")
            print(f"  建议数: {len(validation.get('suggestions', []))}")
            
            return True
        else:
            print(f"✗ 整合失败: {result.get('msg')}")
            return False
            
    except Exception as e:
        print(f"✗ 请求异常: {str(e)}")
        return False


def test_route_optimization():
    """测试路线优化功能"""
    print("\n=== 测试2: 路线优化 ===")
    
    attractions = [
        {"name": "故宫", "location": {"lat": 39.916, "lng": 116.397}},
        {"name": "颐和园", "location": {"lat": 39.998, "lng": 116.275}},
        {"name": "天坛", "location": {"lat": 39.882, "lng": 116.407}},
        {"name": "圆明园", "location": {"lat": 40.008, "lng": 116.298}},
        {"name": "北海公园", "location": {"lat": 39.925, "lng": 116.389}}
    ]
    
    url = f"{BASE_URL}/api/v1/integration/optimize-route"
    payload = {"attractions": attractions}
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        result = response.json()
        
        if result.get('code') == 200:
            optimized = result.get('data', {}).get('optimized_attractions', [])
            print(f"✓ 路线优化成功！优化后顺序:")
            for i, attr in enumerate(optimized, 1):
                print(f"  {i}. {attr['name']} (lat: {attr['location']['lat']:.3f})")
            return True
        else:
            print(f"✗ 优化失败: {result.get('msg')}")
            return False
            
    except Exception as e:
        print(f"✗ 请求异常: {str(e)}")
        return False


def test_edge_cases():
    """测试边界情况"""
    print("\n=== 测试3: 边界情况 ===")
    
    all_passed = True
    
    # 测试1: 单天行程
    print("\n子测试3.1: 单天行程")
    agent_results_minimal = {
        "attraction": {"attractions": [{"name": "故宫", "visit_time_slot": "morning", "ticket_price": 60}]},
        "accommodation": {"hotels": []},
        "food": {"restaurants": []},
        "transport": {"transport_options": []}
    }
    
    structured_req_minimal = {
        "city_name": "北京",
        "travel_days": 1,
        "travel_date": "2026-05-20",
        "traveler_count": 1
    }
    
    url = f"{BASE_URL}/api/v1/integration/combine"
    payload = {
        "task_id": "test_minimal",
        "agent_results": agent_results_minimal,
        "structured_requirement": structured_req_minimal
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        result = response.json()
        
        if result.get('code') == 200:
            print("  ✓ 单天行程整合成功")
        else:
            print(f"  ✗ 单天行程整合失败: {result.get('msg')}")
            all_passed = False
    except Exception as e:
        print(f"  ✗ 请求异常: {str(e)}")
        all_passed = False
    
    # 测试2: 缺少必要参数
    print("\n子测试3.2: 缺少必要参数")
    payload_invalid = {
        "task_id": "test_invalid",
        "agent_results": {}
    }
    
    try:
        response = requests.post(url, json=payload_invalid, timeout=10)
        result = response.json()
        
        if result.get('code') != 200:
            print(f"  ✓ 正确拒绝无效请求: {result.get('msg')}")
        else:
            print("  ✗ 应该拒绝无效请求但未拒绝")
            all_passed = False
    except Exception as e:
        print(f"  ✗ 请求异常: {str(e)}")
        all_passed = False
    
    return all_passed


if __name__ == "__main__":
    print("=" * 60)
    print("行程整合功能测试")
    print("=" * 60)
    
    # 检查服务是否运行
    try:
        health_response = requests.get(f"{BASE_URL}/api/v1/health", timeout=3)
        if health_response.status_code != 200:
            print("⚠ 警告: 服务可能未正常运行，请先启动后端服务")
            print(f"  运行命令: python src/index.py")
    except:
        print("⚠ 警告: 无法连接到服务，请先启动后端服务")
        print(f"  运行命令: python src/index.py")
        exit(1)
    
    # 执行测试
    results = []
    
    results.append(("基本行程整合", test_basic_integration()))
    results.append(("路线优化", test_route_optimization()))
    results.append(("边界情况", test_edge_cases()))
    
    # 总结
    print("\n" + "=" * 60)
    print("测试结果总结")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"{test_name}: {status}")
    
    print(f"\n总计: {passed}/{total} 测试通过")
    
    if passed == total:
        print("\n🎉 所有测试通过！行程整合功能正常工作")
    else:
        print(f"\n⚠ 有 {total - passed} 个测试失败，请检查日志")
