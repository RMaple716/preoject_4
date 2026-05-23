"""
景点开放时间校验测试脚本
用于验证规划校验模块的景点开放时间检查功能
"""
import requests
import json

BASE_URL = "http://127.0.0.1:9091"


def test_opening_hours_validation():
    """测试1: 景点开放时间校验 - 游览时间超出开放范围"""
    print("\n=== 测试1: 景点开放时间校验（超出开放时间） ===")
    
    day_plans = [
        {
            "day": 1,
            "date": "2026-05-20",
            "attractions": [
                {
                    "name": "故宫博物院",
                    "start_time": "07:00",  # 早于开放时间08:30
                    "visit_duration": "2小时",
                    "opening_hours": "08:30-17:00",  # 开放时间
                    "ticket_price": 60,
                    "address": "北京市东城区"
                },
                {
                    "name": "颐和园",
                    "start_time": "14:00",
                    "visit_duration": "3小时",
                    "opening_hours": "06:30-18:00",  # 开放时间
                    "ticket_price": 30,
                    "address": "北京市海淀区"
                }
            ],
            "meals": [
                {
                    "name": "午餐",
                    "time": "12:00",
                    "duration": "1小时",
                    "avg_price_per_person": 80
                }
            ]
        }
    ]
    
    structured_requirement = {
        "city_name": "北京",
        "travel_days": 1,
        "total_budget": 5000,
        "travel_date": "2026-05-20",
        "traveler_count": 2
    }
    
    url = f"{BASE_URL}/api/v1/validation/itinerary"
    payload = {
        "day_plans": day_plans,
        "structured_requirement": structured_requirement
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        result = response.json()
        
        print(f"状态码: {result.get('code')}")
        print(f"消息: {result.get('msg')}")
        
        if result.get('code') == 200:
            data = result.get('data', {})
            valid = data.get('valid', False)
            conflicts = data.get('conflicts', [])
            
            print(f"\n✓ 校验完成")
            print(f"  是否有效: {valid}")
            print(f"  冲突数: {len(conflicts)}")
            
            # 查找开放时间相关的冲突
            opening_conflicts = [c for c in conflicts if 'opening_hours' in c.get('type', '')]
            
            if opening_conflicts:
                print(f"\n✓ 检测到开放时间冲突:")
                for conflict in opening_conflicts:
                    print(f"  - [{conflict['severity']}] {conflict['description']}")
                return True
            else:
                print("\n✗ 未检测到开放时间冲突（可能有问题）")
                print("  所有冲突:")
                for conflict in conflicts:
                    print(f"    - [{conflict['severity']}] {conflict['description']}")
                return False
        else:
            print(f"✗ 请求失败: {result.get('msg')}")
            return False
            
    except Exception as e:
        print(f"✗ 请求异常: {str(e)}")
        return False


def test_no_opening_hours_conflict():
    """测试2: 无开放时间冲突 - 游览时间在开放范围内"""
    print("\n=== 测试2: 无开放时间冲突（正常情况） ===")
    
    day_plans = [
        {
            "day": 1,
            "date": "2026-05-20",
            "attractions": [
                {
                    "name": "故宫博物院",
                    "start_time": "09:00",  # 在开放时间08:30-17:00内
                    "visit_duration": "3小时",
                    "opening_hours": "08:30-17:00",
                    "ticket_price": 60,
                    "address": "北京市东城区"
                },
                {
                    "name": "天坛公园",
                    "start_time": "14:00",  # 在开放时间06:00-22:00内
                    "visit_duration": "2小时",
                    "opening_hours": "06:00-22:00",
                    "ticket_price": 15,
                    "address": "北京市东城区"
                }
            ],
            "meals": []
        }
    ]
    
    structured_requirement = {
        "city_name": "北京",
        "travel_days": 1,
        "total_budget": 5000,
        "travel_date": "2026-05-20",
        "traveler_count": 2
    }
    
    url = f"{BASE_URL}/api/v1/validation/itinerary"
    payload = {
        "day_plans": day_plans,
        "structured_requirement": structured_requirement
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        result = response.json()
        
        if result.get('code') == 200:
            data = result.get('data', {})
            valid = data.get('valid', False)
            conflicts = data.get('conflicts', [])
            
            print(f"✓ 校验完成")
            print(f"  是否有效: {valid}")
            print(f"  冲突数: {len(conflicts)}")
            
            # 检查是否有开放时间冲突
            opening_conflicts = [c for c in conflicts if 'opening_hours' in c.get('type', '')]
            
            if not opening_conflicts:
                print("✓ 无开放时间冲突，游览时间安排合理")
                return True
            else:
                print("✗ 意外检测到开放时间冲突:")
                for conflict in opening_conflicts:
                    print(f"  - {conflict['description']}")
                return False
        else:
            print(f"✗ 请求失败: {result.get('msg')}")
            return False
            
    except Exception as e:
        print(f"✗ 请求异常: {str(e)}")
        return False


def test_budget_validation_with_opening_hours():
    """测试3: 预算校验 + 开放时间校验综合测试"""
    print("\n=== 测试3: 预算校验 + 开放时间校验综合测试 ===")
    
    day_plans = [
        {
            "day": 1,
            "date": "2026-05-20",
            "attractions": [
                {
                    "name": "故宫博物院",
                    "start_time": "18:00",  # 晚于关闭时间17:00
                    "visit_duration": "2小时",
                    "opening_hours": "08:30-17:00",
                    "ticket_price": 60,
                    "address": "北京市东城区"
                },
                {
                    "name": "长城",
                    "start_time": "10:00",
                    "visit_duration": "4小时",
                    "opening_hours": "06:00-18:00",
                    "ticket_price": 45,
                    "address": "北京市延庆区"
                }
            ],
            "meals": [
                {
                    "name": "高档餐厅",
                    "time": "12:00",
                    "duration": "2小时",
                    "avg_price_per_person": 500
                }
            ]
        }
    ]
    
    structured_requirement = {
        "city_name": "北京",
        "travel_days": 1,
        "total_budget": 500,  # 低预算，应该会超出
        "travel_date": "2026-05-20",
        "traveler_count": 2
    }
    
    url = f"{BASE_URL}/api/v1/validation/itinerary"
    payload = {
        "day_plans": day_plans,
        "structured_requirement": structured_requirement
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        result = response.json()
        
        if result.get('code') == 200:
            data = result.get('data', {})
            valid = data.get('valid', False)
            conflicts = data.get('conflicts', [])
            suggestions = data.get('suggestions', [])
            
            print(f"✓ 校验完成")
            print(f"  是否有效: {valid}")
            print(f"  冲突数: {len(conflicts)}")
            print(f"  建议数: {len(suggestions)}")
            
            # 分类显示冲突
            opening_conflicts = [c for c in conflicts if 'opening_hours' in c.get('type', '')]
            budget_conflicts = [c for c in conflicts if c.get('type') == 'budget_exceeded']
            
            if opening_conflicts:
                print(f"\n✓ 检测到开放时间冲突 ({len(opening_conflicts)}个):")
                for conflict in opening_conflicts:
                    print(f"  - [{conflict['severity']}] {conflict['description']}")
            
            if budget_conflicts:
                print(f"\n✓ 检测到预算超出:")
                for conflict in budget_conflicts:
                    print(f"  - [{conflict['severity']}] {conflict['description']}")
            
            if suggestions:
                print(f"\n建议:")
                for suggestion in suggestions:
                    print(f"  - {suggestion}")
            
            # 应该同时检测到两种冲突
            if opening_conflicts and budget_conflicts:
                print("\n✓ 成功检测到开放时间冲突和预算超出")
                return True
            else:
                print("\n✗ 未完全检测到预期冲突")
                return False
        else:
            print(f"✗ 请求失败: {result.get('msg')}")
            return False
            
    except Exception as e:
        print(f"✗ 请求异常: {str(e)}")
        return False


def test_missing_opening_hours():
    """测试4: 景点缺少开放时间信息 - 应跳过检查"""
    print("\n=== 测试4: 景点缺少开放时间信息 ===")
    
    day_plans = [
        {
            "day": 1,
            "date": "2026-05-20",
            "attractions": [
                {
                    "name": "未知景点",
                    "start_time": "09:00",
                    "visit_duration": "2小时",
                    # 没有opening_hours字段
                    "ticket_price": 50,
                    "address": "某地"
                }
            ],
            "meals": []
        }
    ]
    
    structured_requirement = {
        "city_name": "北京",
        "travel_days": 1,
        "total_budget": 5000,
        "travel_date": "2026-05-20",
        "traveler_count": 2
    }
    
    url = f"{BASE_URL}/api/v1/validation/itinerary"
    payload = {
        "day_plans": day_plans,
        "structured_requirement": structured_requirement
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        result = response.json()
        
        if result.get('code') == 200:
            data = result.get('data', {})
            conflicts = data.get('conflicts', [])
            
            # 检查是否有开放时间相关冲突
            opening_conflicts = [c for c in conflicts if 'opening_hours' in c.get('type', '')]
            
            if not opening_conflicts:
                print("✓ 正确跳过缺少开放时间信息的景点检查")
                return True
            else:
                print("✗ 意外检测到开放时间冲突:")
                for conflict in opening_conflicts:
                    print(f"  - {conflict['description']}")
                return False
        else:
            print(f"✗ 请求失败: {result.get('msg')}")
            return False
            
    except Exception as e:
        print(f"✗ 请求异常: {str(e)}")
        return False


if __name__ == "__main__":
    print("=" * 70)
    print("景点开放时间校验功能测试")
    print("=" * 70)
    
    # 检查服务是否运行
    try:
        health_response = requests.get(f"{BASE_URL}/api/v1/health", timeout=3)
        if health_response.status_code != 200:
            print("⚠ 警告: 服务可能未正常运行")
            exit(1)
        print("✓ 后端服务运行正常\n")
    except:
        print("⚠ 警告: 无法连接到服务，请先启动后端服务")
        print(f"  运行命令: python src/index.py")
        exit(1)
    
    # 执行测试
    tests = [
        ("开放时间超出检测", test_opening_hours_validation),
        ("正常开放时间", test_no_opening_hours_conflict),
        ("预算+开放时间综合测试", test_budget_validation_with_opening_hours),
        ("缺少开放时间信息", test_missing_opening_hours)
    ]
    
    results = []
    for test_name, test_func in tests:
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
        print("\n🎉 所有测试通过！景点开放时间校验功能正常")
    else:
        print(f"\n⚠ 有 {total - passed} 个测试失败，需要修复bug")
