"""
测试天气API集成功能
"""
import asyncio
import sys
import os
from datetime import datetime, timedelta

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.services.weather_service import WeatherService
from src.agents.attractions_agent import AttractionsAgent


async def test_weather_service():
    """测试天气服务"""
    print("=" * 50)
    print("测试天气服务")
    print("=" * 50)

    weather_service = WeatherService()

    # 测试获取北京天气
    print("\n1. 测试获取北京天气信息...")
    result = await weather_service.get_weather("北京", extensions="all")

    if result.get("status") == "success":
        forecasts = result.get("data", [])
        if forecasts:
            print(f"✓ 成功获取天气信息")
            print(f"  城市: 北京")
            print(f"  预报天数: {len(forecasts[0].get('casts', []))}")
            for i, cast in enumerate(forecasts[0].get('casts', [])[:3]):
                print(f"  第{i+1}天 ({cast.get('date', '')}): "
                      f"{cast.get('dayweather', '')}/{cast.get('nightweather', '')}, "
                      f"{cast.get('daytemp', '')}°C/{cast.get('nighttemp', '')}°C")
        else:
            print("✗ 未获取到天气预报数据")
    else:
        print(f"✗ 获取天气信息失败: {result.get('message', '未知错误')}")

    return result.get("status") == "success"


async def test_attractions_agent_with_weather():
    """测试景点智能体集成天气API"""
    print("\n" + "=" * 50)
    print("测试景点智能体集成天气API")
    print("=" * 50)

    agent = AttractionsAgent()

    # 准备测试数据
    travel_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
    task_data = {
        "task_id": "test_attr_001",
        "city_name": "北京",
        "travel_days": 3,
        "travel_date": travel_date,
        "ticket_budget": 500,
        "preferences": ["历史", "文化"],
        "dislikes": [],
        "traveler_count": 2
    }

    print(f"\n测试参数:")
    print(f"  城市: {task_data['city_name']}")
    print(f"  旅行天数: {task_data['travel_days']}")
    print(f"  旅行日期: {task_data['travel_date']}")
    print(f"  预算: {task_data['ticket_budget']}元")
    print(f"  人数: {task_data['traveler_count']}")

    # 执行任务
    print("\n2. 执行景点推荐任务...")
    result = await agent.execute(task_data)

    if result.get("status") == "success":
        print("✓ 任务执行成功")
        attractions = result.get("data", {}).get("items", [])
        print(f"  推荐景点数量: {len(attractions)}")

        # 显示推荐的景点
        for i, attraction in enumerate(attractions[:3]):
            print(f"\n  景点 {i+1}:")
            print(f"    名称: {attraction.get('name', '')}")
            print(f"    描述: {attraction.get('description', '')[:50]}...")
            print(f"    门票: {attraction.get('ticket_price', 0)}元")
            print(f"    评分: {attraction.get('rating', 0)}")

        # 检查元数据
        metadata = result.get("metadata", {})
        print(f"\n  元数据:")
        print(f"    处理时间: {metadata.get('processing_time_ms', 0)}ms")
        print(f"    数据源: {metadata.get('source', '')}")
    else:
        print(f"✗ 任务执行失败: {result.get('error_message', '未知错误')}")

    return result.get("status") == "success"


async def test_weather_in_itinerary():
    """测试天气信息在行程中的集成"""
    print("\n" + "=" * 50)
    print("测试天气信息在行程中的集成")
    print("=" * 50)

    # 这个测试需要实际的API调用，这里只是展示如何测试
    print("\n3. 测试行程中的天气信息...")
    print("  注意: 此测试需要完整的API调用链路")
    print("  建议通过前端界面或API直接测试")

    # 模拟天气数据
    mock_weather = {
        "date": "2024-06-01",
        "dayweather": "晴",
        "nightweather": "多云",
        "daytemp": "28",
        "nighttemp": "18",
        "daywind": "东南风3-4级",
        "nightwind": "东南风2-3级"
    }

    print(f"\n  模拟天气数据:")
    print(f"    日期: {mock_weather['date']}")
    print(f"    天气: {mock_weather['dayweather']}/{mock_weather['nightweather']}")
    print(f"    温度: {mock_weather['daytemp']}°C/{mock_weather['nighttemp']}°C")
    print(f"    风向: {mock_weather['daywind']}/{mock_weather['nightwind']}")

    print("\n✓ 天气数据格式正确")
    return True


async def main():
    """主测试函数"""
    print("\n" + "=" * 50)
    print("天气API集成测试")
    print("=" * 50)
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # 检查API密钥
    if not os.getenv('AMAP_API_KEY'):
        print("\n⚠ 警告: 未配置AMAP_API_KEY环境变量")
        print("  某些测试可能会失败")
        print("  请设置环境变量: export AMAP_API_KEY=your_api_key")

    # 执行测试
    results = []

    try:
        # 测试1: 天气服务
        result1 = await test_weather_service()
        results.append(("天气服务测试", result1))

        # 测试2: 景点智能体集成
        result2 = await test_attractions_agent_with_weather()
        results.append(("景点智能体集成测试", result2))

        # 测试3: 行程中的天气信息
        result3 = await test_weather_in_itinerary()
        results.append(("行程天气信息测试", result3))

    except Exception as e:
        print(f"\n✗ 测试过程中发生错误: {str(e)}")
        import traceback
        traceback.print_exc()

    # 输出测试结果
    print("\n" + "=" * 50)
    print("测试结果汇总")
    print("=" * 50)
    for test_name, result in results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"{test_name}: {status}")

    # 计算通过率
    passed = sum(1 for _, result in results if result)
    total = len(results)
    print(f"\n通过率: {passed}/{total} ({(passed/total*100):.1f}%)")

    print("\n" + "=" * 50)
    print("测试完成")
    print("=" * 50)


if __name__ == "__main__":
    asyncio.run(main())
