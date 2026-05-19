"""
任务分解功能测试脚本
用于验证任务分解接口的正确性
"""
import requests
import json
from typing import Dict, Any

BASE_URL = "http://127.0.0.1:9091"


def test_budget_allocation():
    """测试预算分配逻辑"""
    print("=" * 60)
    print("测试1: 预算自动分配")
    print("=" * 60)
    
    url = f"{BASE_URL}/api/v1/task/decompose"
    
    payload = {
        "requirement_id": "req_test_budget",
        "structured_requirement": {
            "city_name": "北京",
            "travel_days": 3,
            "total_budget": 5000,
            "travel_date": "2026-05-20",
            "traveler_count": 3,
            "preferences": ["历史古迹"],
            "dislikes": []
        }
    }
    
    response = requests.post(url, json=payload)
    result = response.json()
    
    if result["code"] == 200:
        print("✅ 任务分解成功")
        print(f"任务ID: {result['data']['task_id']}")
        print(f"\n生成的子任务:")
        for subtask in result["data"]["subtasks"]:
            print(f"  - {subtask['agent']}: {subtask['task_id']}")
    else:
        print(f"❌ 任务分解失败: {result['msg']}")
    
    return result


def test_validation_rules():
    """测试业务规则验证"""
    print("\n" + "=" * 60)
    print("测试2: 业务规则验证")
    print("=" * 60)
    
    url = f"{BASE_URL}/api/v1/task/decompose"
    
    # 测试1: 预算过低
    print("\n测试2.1: 预算过低")
    payload = {
        "requirement_id": "req_test_low_budget",
        "structured_requirement": {
            "city_name": "北京",
            "travel_days": 3,
            "total_budget": 100,  # 过低
            "travel_date": "2026-05-20",
            "traveler_count": 3,
            "preferences": [],
            "dislikes": []
        }
    }
    
    response = requests.post(url, json=payload)
    result = response.json()
    
    if result["code"] != 200:
        print(f"✅ 正确拦截: {result['msg']}")
    else:
        print("❌ 未拦截低预算")
    
    # 测试2: 天数超限
    print("\n测试2.2: 出行天数超限")
    payload["structured_requirement"]["total_budget"] = 5000
    payload["structured_requirement"]["travel_days"] = 50  # 超过30天
    
    response = requests.post(url, json=payload)
    result = response.json()
    
    if result["code"] != 200:
        print(f"✅ 正确拦截: {result['msg']}")
    else:
        print("❌ 未拦截超期")


def test_task_status_query():
    """测试任务状态查询"""
    print("\n" + "=" * 60)
    print("测试3: 任务状态查询")
    print("=" * 60)
    
    # 先创建一个任务
    url_decompose = f"{BASE_URL}/api/v1/task/decompose"
    payload = {
        "requirement_id": "req_test_status",
        "structured_requirement": {
            "city_name": "上海",
            "travel_days": 2,
            "total_budget": 3000,
            "travel_date": "2026-06-01",
            "traveler_count": 2,
            "preferences": ["美食"],
            "dislikes": []
        }
    }
    
    response = requests.post(url_decompose, json=payload)
    result = response.json()
    
    if result["code"] == 200:
        task_id = result["data"]["task_id"]
        print(f"创建任务成功: {task_id}")
        
        # 查询任务状态
        url_status = f"{BASE_URL}/api/v1/task/{task_id}"
        status_response = requests.get(url_status)
        status_result = status_response.json()
        
        print(f"\n任务状态:")
        print(json.dumps(status_result, indent=2, ensure_ascii=False))
    else:
        print(f"❌ 创建任务失败: {result['msg']}")


def test_update_task_result():
    """测试更新任务结果"""
    print("\n" + "=" * 60)
    print("测试4: 更新任务结果")
    print("=" * 60)
    
    # 先创建一个任务
    url_decompose = f"{BASE_URL}/api/v1/task/decompose"
    payload = {
        "requirement_id": "req_test_update",
        "structured_requirement": {
            "city_name": "杭州",
            "travel_days": 2,
            "total_budget": 4000,
            "travel_date": "2026-07-01",
            "traveler_count": 2,
            "preferences": [],
            "dislikes": []
        }
    }
    
    response = requests.post(url_decompose, json=payload)
    result = response.json()
    
    if result["code"] == 200:
        subtask_id = result["data"]["subtasks"][0]["task_id"]
        print(f"获取第一个子任务ID: {subtask_id}")
        
        # 更新子任务结果
        url_update = f"{BASE_URL}/api/v1/task/update/{subtask_id}"
        update_payload = {
            "status": "success",
            "result": {
                "items": [
                    {
                        "id": "att_001",
                        "name": "西湖",
                        "category": "自然风光",
                        "suggested_duration": "3小时",
                        "visit_time_slot": "morning",
                        "ticket_price": 0,
                        "location": {"lat": 30.242, "lng": 120.155},
                        "tags": ["必去", "免费"]
                    }
                ]
            },
            "error": None
        }
        
        update_response = requests.post(url_update, json=update_payload)
        update_result = update_response.json()
        
        print(f"\n更新结果:")
        print(json.dumps(update_result, indent=2, ensure_ascii=False))
        
        # 再次查询主任务状态，看进度是否更新
        task_id = result["data"]["task_id"]
        url_status = f"{BASE_URL}/api/v1/task/{task_id}"
        status_response = requests.get(url_status)
        status_result = status_response.json()
        
        print(f"\n更新后的任务进度:")
        if status_result["code"] == 200:
            print(f"  进度: {status_result['data']['progress']}%")
            print(f"  状态: {status_result['data']['status']}")
    else:
        print(f"❌ 创建任务失败: {result['msg']}")


def main():
    """运行所有测试"""
    print("🚀 开始任务分解功能测试\n")
    
    try:
        test_budget_allocation()
        test_validation_rules()
        test_task_status_query()
        test_update_task_result()
        
        print("\n" + "=" * 60)
        print("✅ 所有测试完成")
        print("=" * 60)
    except Exception as e:
        print(f"\n❌ 测试出错: {str(e)}")
        print("请确保服务已启动: python src/index.py")


if __name__ == "__main__":
    main()