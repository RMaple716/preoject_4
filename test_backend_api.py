import requests
import json

BASE_URL = "http://127.0.0.1:9091/api/v1"

def test_health():
    """测试健康检查接口"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"健康检查: {response.status_code}")
        print(f"响应: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"健康检查失败: {e}")
        return False

def test_requirement_submit():
    """测试需求提交接口"""
    try:
        data = {
            "user_id": "test_user_001",
            "requirement": {
                "city_name": "北京",
                "travel_days": 3,
                "total_budget": 5000,
                "travel_type": "family",
                "start_date": "2024-02-01",
                "preferences": ["历史古迹", "美食探索"]
            }
        }
        response = requests.post(f"{BASE_URL}/requirement/submit", json=data)
        print(f"需求提交: {response.status_code}")
        print(f"响应: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"需求提交失败: {e}")
        return False

def test_task_decompose():
    """测试任务分解接口"""
    try:
        data = {
            "requirement_id": "test_req_001",
            "structured_requirement": {
                "city_name": "北京",
                "travel_days": 3,
                "total_budget": 5000,
                "travel_date": "2024-02-01",
                "traveler_count": 2,
                "preferences": ["历史古迹", "美食探索"]
            }
        }
        response = requests.post(f"{BASE_URL}/task/decompose", json=data)
        print(f"任务分解: {response.status_code}")
        print(f"响应: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"任务分解失败: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("开始测试后端API")
    print("=" * 50)

    # 测试健康检查
    print("
1. 测试健康检查接口")
    health_ok = test_health()

    # 测试需求提交
    print("
2. 测试需求提交接口")
    submit_ok = test_requirement_submit()

    # 测试任务分解
    print("
3. 测试任务分解接口")
    decompose_ok = test_task_decompose()

    print("
" + "=" * 50)
    print("测试结果:")
    print(f"健康检查: {'OK' if health_ok else 'FAIL'}")
    print(f"需求提交: {'OK' if submit_ok else 'FAIL'}")
    print(f"任务分解: {'OK' if decompose_ok else 'FAIL'}")
    print("=" * 50)
