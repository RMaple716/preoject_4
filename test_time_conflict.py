"""
时间冲突检测算法测试脚本
用于验证行程校验模块的各项功能
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:9091"  # 修改为正确的端口号


def test_time_conflict_detection():
    """测试1: 基本时间冲突检测"""
    print("\n=== 测试1: 基本时间冲突检测 ===")
    
    # 构造有冲突的行程（两个活动时间重叠）
    schedule_with_conflict = [
        {
            "name": "故宫博物院",
            "start_time": "09:00",
            "end_time": "12:00",
            "activity_type": "attraction",
            "location": "北京市东城区"
        },
        {
            "name": "午餐",
            "start_time": "11:30",
            "duration": "1小时",
            "activity_type": "meal",
            "location": "王府井"
        }
    ]
    
    response = requests.post(
        f"{BASE_URL}/api/v1/validation/time-conflict",
        json={"schedule": schedule_with_conflict}
    )
    
    print(f"状态码: {response.status_code}")
    result = response.json()
    print(f"响应: {json.dumps(result, ensure_ascii=False, indent=2)}")
    
    assert result["code"] == 200
    assert result["data"]["has_conflict"] == True
    assert len(result["data"]["conflicts"]) > 0
    print("✓ 检测到时间冲突")


def test_no_time_conflict():
    """测试2: 无时间冲突的行程"""
    print("\n=== 测试2: 无时间冲突的行程 ===")
    
    schedule_without_conflict = [
        {
            "name": "故宫博物院",
            "start_time": "09:00",
            "end_time": "11:00",
            "activity_type": "attraction",
            "location": "北京市东城区"
        },
        {
            "name": "午餐",
            "start_time": "12:00",
            "duration": "1小时",
            "activity_type": "meal",
            "location": "王府井"
        },
        {
            "name": "颐和园",
            "start_time": "14:00",
            "end_time": "17:00",
            "activity_type": "attraction",
            "location": "海淀区"
        }
    ]
    
    response = requests.post(
        f"{BASE_URL}/api/v1/validation/time-conflict",
        json={"schedule": schedule_without_conflict}
    )
    
    print(f"状态码: {response.status_code}")
    result = response.json()
    print(f"响应: {json.dumps(result, ensure_ascii=False, indent=2)}")
    
    assert result["code"] == 200
    assert result["data"]["has_conflict"] == False
    print("✓ 无时间冲突，行程安排合理")


def test_time_slot_format():
    """测试3: 使用时间槽格式"""
    print("\n=== 测试3: 使用时间槽格式 ===")
    
    schedule_with_slots = [
        {
            "name": "上午景点游览",
            "start_time": "上午",
            "duration": "3小时",
            "activity_type": "attraction"
        },
        {
            "name": "下午景点游览",
            "start_time": "下午",
            "duration": "3小时",
            "activity_type": "attraction"
        }
    ]
    
    response = requests.post(
        f"{BASE_URL}/api/v1/validation/time-conflict",
        json={"schedule": schedule_with_slots}
    )
    
    print(f"状态码: {response.status_code}")
    result = response.json()
    print(f"响应: {json.dumps(result, ensure_ascii=False, indent=2)}")
    
    assert result["code"] == 200
    print("✓ 时间槽格式解析成功")


def test_unreasonable_time():
    """测试4: 不合理的时间安排"""
    print("\n=== 测试4: 不合理的时间安排 ===")
    
    unreasonable_schedule = [
        {
            "name": "凌晨活动",
            "start_time": "03:00",
            "end_time": "05:00",
            "activity_type": "attraction"
        },
        {
            "name": "深夜活动",
            "start_time": "23:30",
            "end_time": "01:00",
            "activity_type": "attraction"
        }
    ]
    
    response = requests.post(
        f"{BASE_URL}/api/v1/validation/time-conflict",
        json={"schedule": unreasonable_schedule}
    )
    
    print(f"状态码: {response.status_code}")
    result = response.json()
    print(f"响应: {json.dumps(result, ensure_ascii=False, indent=2)}")
    
    assert result["code"] == 200
    # 应该有警告级别的冲突
    warnings = [c for c in result["data"]["conflicts"] if c["severity"] == "warning"]
    print(f"✓ 检测到 {len(warnings)} 个时间合理性警告")


def test_duration_parsing():
    """测试5: 时长解析功能"""
    print("\n=== 测试5: 时长解析功能 ===")
    
    schedule_with_durations = [
        {
            "name": "短时游览",
            "start_time": "09:00",
            "duration": "30分钟",
            "activity_type": "attraction"
        },
        {
            "name": "长时间游览",
            "start_time": "10:00",
            "duration": "2-3小时",
            "activity_type": "attraction"
        }
    ]
    
    response = requests.post(
        f"{BASE_URL}/api/v1/validation/time-conflict",
        json={"schedule": schedule_with_durations}
    )
    
    print(f"状态码: {response.status_code}")
    result = response.json()
    print(f"响应: {json.dumps(result, ensure_ascii=False, indent=2)}")
    
    assert result["code"] == 200
    print("✓ 时长格式解析成功")


def test_overloaded_day():
    """测试6: 过度安排的检测"""
    print("\n=== 测试6: 过度安排的检测 ===")
    
    overloaded_schedule = [
        {
            "name": "早间活动",
            "start_time": "06:00",
            "end_time": "08:00",
            "activity_type": "attraction"
        },
        {
            "name": "上午活动",
            "start_time": "08:30",
            "end_time": "11:30",
            "activity_type": "attraction"
        },
        {
            "name": "中午活动",
            "start_time": "12:00",
            "end_time": "14:00",
            "activity_type": "meal"
        },
        {
            "name": "下午活动",
            "start_time": "14:30",
            "end_time": "17:30",
            "activity_type": "attraction"
        },
        {
            "name": "晚间活动",
            "start_time": "18:00",
            "end_time": "21:00",
            "activity_type": "attraction"
        }
    ]
    
    response = requests.post(
        f"{BASE_URL}/api/v1/validation/time-conflict",
        json={"schedule": overloaded_schedule}
    )
    
    print(f"状态码: {response.status_code}")
    result = response.json()
    print(f"响应: {json.dumps(result, ensure_ascii=False, indent=2)}")
    
    assert result["code"] == 200
    # 应该检测到过度安排
    overloaded_warnings = [c for c in result["data"]["conflicts"] if c["type"] == "overloaded_day"]
    if overloaded_warnings:
        print(f"✓ 检测到过度安排警告: {overloaded_warnings[0]['description']}")


def test_complete_itinerary_validation():
    """测试7: 完整行程校验"""
    print("\n=== 测试7: 完整行程校验 ===")
    
    day_plans = [
        {
            "day": 1,
            "date": "2026-05-20",
            "attractions": [
                {
                    "name": "故宫博物院",
                    "visit_time": "09:00",
                    "visit_duration": "3小时",
                    "ticket_price": 60,
                    "address": "北京市东城区"
                },
                {
                    "name": "天安门广场",
                    "visit_time": "14:00",
                    "visit_duration": "2小时",
                    "ticket_price": 0,
                    "address": "北京市东城区"
                }
            ],
            "meals": [
                {
                    "name": "全聚德烤鸭",
                    "meal_time": "12:00",
                    "avg_price": 150,
                    "address": "前门大街"
                }
            ],
            "transport": None
        }
    ]
    
    structured_requirement = {
        "total_budget": 5000,
        "city_name": "北京",
        "travel_days": 3
    }
    
    response = requests.post(
        f"{BASE_URL}/api/v1/validation/itinerary",
        json={
            "day_plans": day_plans,
            "structured_requirement": structured_requirement
        }
    )
    
    print(f"状态码: {response.status_code}")
    result = response.json()
    print(f"响应: {json.dumps(result, ensure_ascii=False, indent=2)}")
    
    assert result["code"] == 200
    print(f"✓ 行程校验完成，有效状态: {result['data']['valid']}")


def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("时间冲突检测算法测试套件")
    print("=" * 60)
    
    tests = [
        test_time_conflict_detection,
        test_no_time_conflict,
        test_time_slot_format,
        test_unreasonable_time,
        test_duration_parsing,
        test_overloaded_day,
        test_complete_itinerary_validation
    ]
    
    passed = 0
    failed = 0
    
    for test_func in tests:
        try:
            test_func()
            passed += 1
        except Exception as e:
            print(f"✗ 测试失败: {str(e)}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"测试结果: {passed} 通过, {failed} 失败")
    print("=" * 60)


if __name__ == "__main__":
    run_all_tests()
