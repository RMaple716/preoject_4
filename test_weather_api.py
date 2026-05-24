"""
测试天气API
"""
import asyncio
import sys
import os
from dotenv import load_dotenv

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

# 加载环境变量
env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(env_path)

from src.services.weather_service import WeatherService

async def test_weather_api():
    """测试天气API"""
    print("=" * 50)
    print("开始测试天气API")
    print("=" * 50)

    # 初始化天气服务,设置最小查询间隔为3秒
    weather_service = WeatherService(min_interval=3.0)

    # 测试城市列表
    test_cities = ["北京", "上海", "西安"]

    for city in test_cities:
        print(f"{'=' * 50}")
        print(f"测试城市: {city}")
        print(f"{'=' * 50}")

        # 测试实时天气
        print(f"1. 获取实时天气...")
        result = await weather_service.get_current_weather(city)

        if result['status'] == 'success':
            data = result['data']
            print("✅ 成功获取实时天气")
            print(f"   省份: {data.get('province')}")
            print(f"   城市: {data.get('city')}")
            print(f"   天气: {data.get('weather')}")
            print(f"   温度: {data.get('temperature')}°C")
            print(f"   风向: {data.get('winddirection')}")
            print(f"   风力: {data.get('windpower')}级")
            print(f"   湿度: {data.get('humidity')}%")
            print(f"   更新时间: {data.get('reporttime')}")
        else:
            print(f"❌ 获取失败: {result.get('message')}")

        # 城市之间添加延迟
        await asyncio.sleep(1)

        # 测试天气预报
        print(f"2. 获取天气预报...")
        result = await weather_service.get_forecast(city)

        if result['status'] == 'success':
            data = result['data']
            print("✅ 成功获取天气预报")
            print(f"   城市: {data.get('city')}")
            print(f"   更新时间: {data.get('reporttime')}")
            print("\n   未来几天天气:")
            for cast in data.get('casts', [])[:3]:  # 只显示前3天
                print(f"\n   {cast.get('date')} ({cast.get('week')})")
                print(f"   白天: {cast.get('dayweather')} {cast.get('daytemp')}°C")
                print(f"   晚上: {cast.get('nightweather')} {cast.get('nighttemp')}°C")
                print(f"   风向: {cast.get('daywind')} {cast.get('daypower')}级")
        else:
            print(f"❌ 获取失败: {result.get('message')}")

        # 城市之间添加延迟
        await asyncio.sleep(2)

    print(f"{'=' * 50}")
    print("测试完成")
    print(f"{'=' * 50}")

if __name__ == "__main__":
    # 检查是否配置了API密钥
    api_key = os.getenv('AMAP_API_KEY')
    print(f"{'=' * 50}")
    if not api_key:
        print("⚠️  警告: 未配置高德地图API密钥")
        print(f"{'=' * 50}")
        print("请按以下步骤配置:")
        print("1. 访问 https://lbs.amap.com/ 注册/登录")
        print("2. 创建应用并获取API密钥")
        print("3. 在项目根目录创建 .env 文件")
        print("4. 添加内容: AMAP_API_KEY=你的密钥")
        print(f"{'=' * 50}")
        print("或者直接在代码中设置API密钥:")
        print("weather_service = WeatherService(api_key='你的密钥')")
        print(f"{'=' * 50}")
        print(f"{'=' * 50}")
        print("现在将使用未配置密钥的服务进行测试...")
    else:
        print(f"✅ 已加载API密钥: {api_key[:10]}...{api_key[-4:]}")
    print(f"{'=' * 50}")

    asyncio.run(test_weather_api())
