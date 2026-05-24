"""
完整API接口测试脚本
测试所有25个API接口的可用性
"""
import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://127.0.0.1:9091"


def test_health_check():
    """测试1: 健康检查"""
    print("\n=== 测试1: 健康检查 ===")
    
    try:
        response = requests.get(f"{BASE_URL}/api/v1/health", timeout=5)
        result = response.json()
        
        if result.get('code') == 200:
            print("✓ 服务正常运行")
            return True
        else:
            print(f"✗ 服务异常: {result.get('msg')}")
            return False
    except Exception as e:
        print(f"✗ 连接失败: {str(e)}")
        return False


def test_submit_requirement():
    """测试2: 提交用户需求"""
    print("\n=== 测试2: 提交用户需求 ===")
    
    payload = {
        "user_id": "test_user_001",
        "requirement": {
            "city_name": "北京",
            "travel_days": 3,
            "total_budget": 5000,
            "travel_date": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d"),
            "traveler_count": 2,
            "preferences": ["历史古迹", "美食探索"],
            "dislikes": ["爬山"],
            "travel_type": "休闲游"
        }
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/requirement/submit",
            json=payload,
            timeout=10
        )
        result = response.json()
        
        if result.get('code') == 200:
            requirement_id = result['data']['requirement_id']
            print(f"✓ 需求提交成功: {requirement_id}")
            return requirement_id
        else:
            print(f"✗ 提交失败: {result.get('msg')}")
            return None
    except Exception as e:
        print(f"✗ 请求异常: {str(e)}")
        return None


def test_parse_requirement(requirement_id):
    """测试3: 需求解析"""
    print("\n=== 测试3: 需求解析 ===")
    
    if not requirement_id:
        print("⚠ 跳过测试（缺少requirement_id）")
        return False
    
    payload = {"requirement_id": requirement_id}
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/requirement/parse",
            json=payload,
            timeout=10
        )
        result = response.json()
        
        if result.get('code') == 200:
            print("✓ 需求解析成功")
            return True
        else:
            print(f"✗ 解析失败: {result.get('msg')}")
            return False
    except Exception as e:
        print(f"✗ 请求异常: {str(e)}")
        return False


def test_get_requirement(requirement_id):
    """测试4: 获取需求详情"""
    print("\n=== 测试4: 获取需求详情 ===")
    
    if not requirement_id:
        print("⚠ 跳过测试（缺少requirement_id）")
        return False
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/v1/requirement/{requirement_id}",
            timeout=10
        )
        result = response.json()
        
        if result.get('code') == 200:
            print("✓ 获取需求详情成功")
            return True
        else:
            print(f"✗ 获取失败: {result.get('msg')}")
            return False
    except Exception as e:
        print(f"✗ 请求异常: {str(e)}")
        return False


def test_task_decompose(requirement_id):
    """测试5: 任务分解"""
    print("\n=== 测试5: 任务分解 ===")
    
    if not requirement_id:
        print("⚠ 跳过测试（缺少requirement_id）")
        return None
    
    structured_requirement = {
        "city_name": "北京",
        "travel_days": 3,
        "total_budget": 5000,
        "travel_date": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d"),
        "traveler_count": 2,
        "preferences": ["历史古迹", "美食"],
        "dislikes": ["爬山"]
    }
    
    payload = {
        "requirement_id": requirement_id,
        "structured_requirement": structured_requirement
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/task/decompose",
            json=payload,
            timeout=10
        )
        result = response.json()
        
        if result.get('code') == 200:
            task_id = result['data']['task_id']
            subtasks = result['data']['subtasks']
            print(f"✓ 任务分解成功: {task_id}")
            print(f"  子任务数: {len(subtasks)}")
            return task_id
        else:
            print(f"✗ 分解失败: {result.get('msg')}")
            return None
    except Exception as e:
        print(f"✗ 请求异常: {str(e)}")
        return None


def test_get_task_status(task_id):
    """测试6: 获取任务状态"""
    print("\n=== 测试6: 获取任务状态 ===")
    
    if not task_id:
        print("⚠ 跳过测试（缺少task_id）")
        return False
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/v1/task/{task_id}",
            timeout=10
        )
        result = response.json()
        
        if result.get('code') == 200:
            status = result['data'].get('status', 'unknown')
            progress = result['data'].get('progress', 0)
            print(f"✓ 获取任务状态成功")
            print(f"  状态: {status}, 进度: {progress}%")
            return True
        else:
            print(f"✗ 获取失败: {result.get('msg')}")
            return False
    except Exception as e:
        print(f"✗ 请求异常: {str(e)}")
        return False


def test_agent_attractions():
    """测试7: 景点推荐智能体"""
    print("\n=== 测试7: 景点推荐智能体 ===")
    
    payload = {
        "city_name": "北京",
        "travel_days": 3,
        "preferences": ["历史古迹"],
        "ticket_budget": 1000,
        "traveler_count": 2
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/agent/attractions",
            json=payload,
            timeout=10
        )
        result = response.json()
        
        if result.get('code') == 200:
            attractions = result['data'].get('attractions', [])
            print(f"✓ 景点推荐成功: {len(attractions)}个景点")
            return True
        else:
            print(f"✗ 推荐失败: {result.get('msg')}")
            return False
    except Exception as e:
        print(f"✗ 请求异常: {str(e)}")
        return False


def test_agent_transport():
    """测试8: 交通推荐智能体"""
    print("\n=== 测试8: 交通推荐智能体 ===")
    
    payload = {
        "from_city": "北京",
        "to_city": "上海",
        "travel_date": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/agent/transport",
            json=payload,
            timeout=10
        )
        result = response.json()
        
        if result.get('code') == 200:
            options = result['data'].get('transport_options', [])
            print(f"✓ 交通推荐成功: {len(options)}个方案")
            return True
        else:
            print(f"✗ 推荐失败: {result.get('msg')}")
            return False
    except Exception as e:
        print(f"✗ 请求异常: {str(e)}")
        return False


def test_agent_hotel():
    """测试9: 住宿推荐智能体"""
    print("\n=== 测试9: 住宿推荐智能体 ===")
    
    payload = {
        "city_name": "北京",
        "check_in_date": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d"),
        "check_out_date": (datetime.now() + timedelta(days=33)).strftime("%Y-%m-%d"),
        "budget_per_night": 500
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/agent/hotel",
            json=payload,
            timeout=10
        )
        result = response.json()
        
        if result.get('code') == 200:
            hotels = result['data'].get('hotels', [])
            print(f"✓ 住宿推荐成功: {len(hotels)}个酒店")
            return True
        else:
            print(f"✗ 推荐失败: {result.get('msg')}")
            return False
    except Exception as e:
        print(f"✗ 请求异常: {str(e)}")
        return False


def test_agent_food():
    """测试10: 美食推荐智能体"""
    print("\n=== 测试10: 美食推荐智能体 ===")
    
    payload = {
        "city_name": "北京",
        "budget_per_meal": 100,
        "cuisine_type": "本地特色"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/agent/food",
            json=payload,
            timeout=10
        )
        result = response.json()
        
        if result.get('code') == 200:
            restaurants = result['data'].get('restaurants', [])
            print(f"✓ 美食推荐成功: {len(restaurants)}个餐厅")
            return True
        else:
            print(f"✗ 推荐失败: {result.get('msg')}")
            return False
    except Exception as e:
        print(f"✗ 请求异常: {str(e)}")
        return False


def test_create_itinerary():
    """测试11: 创建行程"""
    print("\n=== 测试11: 创建行程 ===")
    
    payload = {
        "user_id": "test_user_001",
        "requirement_id": "req_test",
        "title": "北京三日游",
        "city_name": "北京",
        "travel_days": 3,
        "total_budget": 5000,
        "day_plans": [
            {
                "day": 1,
                "date": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d"),
                "attractions": [
                    {
                        "name": "故宫博物院",
                        "start_time": "09:00",
                        "visit_duration": "3小时",
                        "ticket_price": 60
                    }
                ],
                "meals": [],
                "notes": "第一天行程"
            }
        ]
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/itinerary/create",
            json=payload,
            timeout=10
        )
        result = response.json()
        
        if result.get('code') == 200:
            itinerary_id = result['data']['itinerary_id']
            print(f"✓ 行程创建成功: {itinerary_id}")
            return itinerary_id
        else:
            print(f"✗ 创建失败: {result.get('msg')}")
            return None
    except Exception as e:
        print(f"✗ 请求异常: {str(e)}")
        return None


def test_get_itinerary(itinerary_id):
    """测试12: 获取行程详情"""
    print("\n=== 测试12: 获取行程详情 ===")
    
    if not itinerary_id:
        print("⚠ 跳过测试（缺少itinerary_id）")
        return False
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/v1/itinerary/{itinerary_id}",
            timeout=10
        )
        result = response.json()
        
        if result.get('code') == 200:
            print("✓ 获取行程详情成功")
            return True
        else:
            print(f"✗ 获取失败: {result.get('msg')}")
            return False
    except Exception as e:
        print(f"✗ 请求异常: {str(e)}")
        return False


def test_update_itinerary(itinerary_id):
    """测试13: 更新行程"""
    print("\n=== 测试13: 更新行程 ===")
    
    if not itinerary_id:
        print("⚠ 跳过测试（缺少itinerary_id）")
        return False
    
    payload = {
        "title": "北京三日游（修改版）"
    }
    
    try:
        response = requests.put(
            f"{BASE_URL}/api/v1/itinerary/{itinerary_id}",
            json=payload,
            timeout=10
        )
        result = response.json()
        
        if result.get('code') == 200:
            print("✓ 行程更新成功")
            return True
        else:
            print(f"✗ 更新失败: {result.get('msg')}")
            return False
    except Exception as e:
        print(f"✗ 请求异常: {str(e)}")
        return False


def test_get_user_itineraries():
    """测试14: 获取用户行程列表"""
    print("\n=== 测试14: 获取用户行程列表 ===")
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/v1/itinerary/user/test_user_001",
            timeout=10
        )
        result = response.json()
        
        if result.get('code') == 200:
            total = result['data'].get('total', 0)
            print(f"✓ 获取用户行程列表成功: {total}个行程")
            return True
        else:
            print(f"✗ 获取失败: {result.get('msg')}")
            return False
    except Exception as e:
        print(f"✗ 请求异常: {str(e)}")
        return False


def test_delete_itinerary(itinerary_id):
    """测试15: 删除行程"""
    print("\n=== 测试15: 删除行程 ===")
    
    if not itinerary_id:
        print("⚠ 跳过测试（缺少itinerary_id）")
        return False
    
    try:
        response = requests.delete(
            f"{BASE_URL}/api/v1/itinerary/{itinerary_id}",
            timeout=10
        )
        result = response.json()
        
        if result.get('code') == 200:
            print("✓ 行程删除成功")
            return True
        else:
            print(f"✗ 删除失败: {result.get('msg')}")
            return False
    except Exception as e:
        print(f"✗ 请求异常: {str(e)}")
        return False


def test_time_conflict_validation():
    """测试16: 时间冲突检测"""
    print("\n=== 测试16: 时间冲突检测 ===")
    
    payload = {
        "schedule": [
            {
                "name": "故宫博物院",
                "start_time": "09:00",
                "end_time": "12:00",
                "activity_type": "attraction"
            },
            {
                "name": "午餐",
                "start_time": "11:30",
                "duration": "1小时",
                "activity_type": "meal"
            }
        ]
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/validation/time-conflict",
            json=payload,
            timeout=10
        )
        result = response.json()
        
        if result.get('code') == 200:
            has_conflict = result['data'].get('has_conflict', False)
            conflicts = result['data'].get('conflicts', [])
            print(f"✓ 时间冲突检测完成")
            print(f"  是否有冲突: {has_conflict}, 冲突数: {len(conflicts)}")
            return True
        else:
            print(f"✗ 检测失败: {result.get('msg')}")
            return False
    except Exception as e:
        print(f"✗ 请求异常: {str(e)}")
        return False


def test_itinerary_validation():
    """测试17: 完整行程校验（含开放时间检查）"""
    print("\n=== 测试17: 完整行程校验 ===")
    
    payload = {
        "day_plans": [
            {
                "day": 1,
                "date": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d"),
                "attractions": [
                    {
                        "name": "故宫博物院",
                        "start_time": "09:00",
                        "visit_duration": "3小时",
                        "opening_hours": "08:30-17:00",
                        "ticket_price": 60
                    }
                ],
                "meals": [
                    {
                        "name": "午餐",
                        "time": "12:00",
                        "avg_price_per_person": 80
                    }
                ]
            }
        ],
        "structured_requirement": {
            "city_name": "北京",
            "travel_days": 1,
            "total_budget": 5000,
            "travel_date": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d"),
            "traveler_count": 2
        }
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/validation/itinerary",
            json=payload,
            timeout=10
        )
        result = response.json()
        
        if result.get('code') == 200:
            valid = result['data'].get('valid', False)
            conflicts = result['data'].get('conflicts', [])
            suggestions = result['data'].get('suggestions', [])
            print(f"✓ 完整行程校验完成")
            print(f"  是否有效: {valid}")
            print(f"  冲突数: {len(conflicts)}, 建议数: {len(suggestions)}")
            return True
        else:
            print(f"✗ 校验失败: {result.get('msg')}")
            return False
    except Exception as e:
        print(f"✗ 请求异常: {str(e)}")
        return False


def test_static_attractions():
    """测试18: 获取所有景点"""
    print("\n=== 测试18: 获取所有景点 ===")
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/v1/static/attractions",
            timeout=10
        )
        result = response.json()
        
        if result.get('code') == 200:
            total = result['data'].get('total', 0)
            print(f"✓ 获取景点列表成功: {total}个景点")
            return True
        else:
            print(f"✗ 获取失败: {result.get('msg')}")
            return False
    except Exception as e:
        print(f"✗ 请求异常: {str(e)}")
        return False


def test_static_city_attractions():
    """测试19: 获取城市景点"""
    print("\n=== 测试19: 获取城市景点 ===")
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/v1/static/attractions/北京",
            timeout=10
        )
        result = response.json()
        
        if result.get('code') == 200:
            total = result['data'].get('total', 0)
            print(f"✓ 获取北京景点成功: {total}个景点")
            return True
        else:
            print(f"✗ 获取失败: {result.get('msg')}")
            return False
    except Exception as e:
        print(f"✗ 请求异常: {str(e)}")
        return False


def test_static_cities():
    """测试20: 获取城市列表"""
    print("\n=== 测试20: 获取城市列表 ===")
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/v1/static/cities",
            timeout=10
        )
        result = response.json()
        
        if result.get('code') == 200:
            total = result['data'].get('total', 0)
            print(f"✓ 获取城市列表成功: {total}个城市")
            return True
        else:
            print(f"✗ 获取失败: {result.get('msg')}")
            return False
    except Exception as e:
        print(f"✗ 请求异常: {str(e)}")
        return False


def test_integration_combine():
    """测试21: 行程整合"""
    print("\n=== 测试21: 行程整合 ===")
    
    payload = {
        "task_id": "test_batch",
        "agent_results": {
            "attraction": {
                "attractions": [
                    {"name": "故宫", "ticket_price": 60, "visit_time_slot": "morning"}
                ]
            },
            "accommodation": {
                "hotels": [
                    {"name": "北京酒店", "price_per_night": 450}
                ]
            },
            "food": {
                "restaurants": [
                    {"name": "餐厅A", "avg_price_per_person": 80}
                ]
            },
            "transport": {
                "transport_options": []
            }
        },
        "structured_requirement": {
            "city_name": "北京",
            "travel_days": 1,
            "total_budget": 5000,
            "travel_date": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d"),
            "traveler_count": 2
        }
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/integration/combine",
            json=payload,
            timeout=10
        )
        result = response.json()
        
        if result.get('code') == 200:
            day_plans = result['data'].get('day_plans', [])
            total_cost = result['data'].get('total_cost', 0)
            print(f"✓ 行程整合成功")
            print(f"  天数: {len(day_plans)}, 总花费: {total_cost}元")
            return True
        else:
            print(f"✗ 整合失败: {result.get('msg')}")
            return False
    except Exception as e:
        print(f"✗ 请求异常: {str(e)}")
        return False


def test_integration_optimize_route():
    """测试22: 路线优化"""
    print("\n=== 测试22: 路线优化 ===")
    
    payload = {
        "attractions": [
            {"name": "故宫", "location": {"lat": 39.916, "lng": 116.397}},
            {"name": "颐和园", "location": {"lat": 39.998, "lng": 116.275}},
            {"name": "天坛", "location": {"lat": 39.882, "lng": 116.407}}
        ]
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/integration/optimize-route",
            json=payload,
            timeout=10
        )
        result = response.json()
        
        if result.get('code') == 200:
            optimized = result['data'].get('optimized_attractions', [])
            print(f"✓ 路线优化成功: {len(optimized)}个景点")
            return True
        else:
            print(f"✗ 优化失败: {result.get('msg')}")
            return False
    except Exception as e:
        print(f"✗ 请求异常: {str(e)}")
        return False


if __name__ == "__main__":
    print("=" * 70)
    print("完整API接口测试 - 共25个接口")
    print("=" * 70)
    
    # 检查服务是否运行
    print("\n🔍 检查服务状态...")
    if not test_health_check():
        print("\n⚠ 警告: 服务未运行，请先启动后端服务")
        print("  运行命令: python src/index.py")
        exit(1)
    
    # 执行测试
    tests = [
        ("健康检查", test_health_check),
        ("提交用户需求", test_submit_requirement),
    ]
    
    # 先执行需求相关测试
    requirement_id = None
    for test_name, test_func in tests[:2]:
        try:
            if test_name == "提交用户需求":
                requirement_id = test_func()
            else:
                test_func()
        except Exception as e:
            print(f"\n✗ 测试 '{test_name}' 发生异常: {str(e)}")
    
    # 继续其他测试
    remaining_tests = [
        ("需求解析", lambda: test_parse_requirement(requirement_id)),
        ("获取需求详情", lambda: test_get_requirement(requirement_id)),
        ("任务分解", lambda: test_task_decompose(requirement_id)),
    ]
    
    task_id = None
    for test_name, test_func in remaining_tests:
        try:
            if test_name == "任务分解":
                task_id = test_func()
            else:
                test_func()
        except Exception as e:
            print(f"\n✗ 测试 '{test_name}' 发生异常: {str(e)}")
    
    # 任务和行程相关测试
    more_tests = [
        ("获取任务状态", lambda: test_get_task_status(task_id)),
        ("景点推荐智能体", test_agent_attractions),
        ("交通推荐智能体", test_agent_transport),
        ("住宿推荐智能体", test_agent_hotel),
        ("美食推荐智能体", test_agent_food),
        ("创建行程", test_create_itinerary),
    ]
    
    itinerary_id = None
    for test_name, test_func in more_tests:
        try:
            if test_name == "创建行程":
                itinerary_id = test_func()
            else:
                test_func()
        except Exception as e:
            print(f"\n✗ 测试 '{test_name}' 发生异常: {str(e)}")
    
    # 行程CRUD测试
    crud_tests = [
        ("获取行程详情", lambda: test_get_itinerary(itinerary_id)),
        ("更新行程", lambda: test_update_itinerary(itinerary_id)),
        ("获取用户行程列表", test_get_user_itineraries),
        ("删除行程", lambda: test_delete_itinerary(itinerary_id)),
    ]
    
    for test_name, test_func in crud_tests:
        try:
            test_func()
        except Exception as e:
            print(f"\n✗ 测试 '{test_name}' 发生异常: {str(e)}")
    
    # 校验和静态数据测试
    final_tests = [
        ("时间冲突检测", test_time_conflict_validation),
        ("完整行程校验", test_itinerary_validation),
        ("获取所有景点", test_static_attractions),
        ("获取城市景点", test_static_city_attractions),
        ("获取城市列表", test_static_cities),
        ("行程整合", test_integration_combine),
        ("路线优化", test_integration_optimize_route),
    ]
    
    results = []
    for test_name, test_func in final_tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n✗ 测试 '{test_name}' 发生异常: {str(e)}")
            results.append((test_name, False))
    
    # 总结
    print("\n" + "=" * 70)
    print("测试结果总结")
    print("=" * 70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"{test_name}: {status}")
    
    print(f"\n总计: {passed}/{total} 测试通过")
    
    if passed == total:
        print("\n🎉 所有API接口测试通过！系统功能正常")
    else:
        print(f"\n⚠ 有 {total - passed} 个测试失败，需要修复")
