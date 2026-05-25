import requests
import json

url = "http://127.0.0.1:9091/api/v1/requirement/submit"
data = {
    "user_id": "test_user",
    "requirement": {
        "city_name": "北京",
        "travel_days": 3,
        "total_budget": 5000,
        "travel_type": "leisure",
        "travel_date": "2024-06-01",
        "preferences": ["历史古迹", "美食探索"]
    }
}

try:
    response = requests.post(url, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
except Exception as e:
    print(f"Error: {str(e)}")
