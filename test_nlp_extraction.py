"""
测试NLP提取功能
"""
from src.services.travel_extractor import TravelExtractor
import sys
sys.path.insert(0, '.')

def test_extraction():
    extractor = TravelExtractor()
    
    # 测试用例1
    text1 = "我想一个人大后天去上海玩一天，预算是2000"
    result1 = extractor.extract(text1)
    
    print("=" * 60)
    print("测试用例1:")
    print(f"输入: {text1}")
    print(f"结果: {result1}")
    print(f"期望: city=上海, people=1, depart_time=大后天, travel_days=1, budget=2000")
    print()
    
    # 验证
    assert result1['city'] == '上海', f"城市错误: {result1['city']}"
    assert result1['people'] == 1, f"人数错误: {result1['people']}"
    assert result1['depart_time'] == '大后天', f"日期错误: {result1['depart_time']}"
    assert result1['travel_days'] == 1, f"天数错误: {result1['travel_days']}"
    assert result1['budget'] == 2000, f"预算错误: {result1['budget']}"
    print("✅ 测试用例1通过!")
    print()
    
    # 测试用例2 - 包含景点
    text2 = "两个人后天去北京看故宫玩三天，预算五千"
    result2 = extractor.extract(text2)
    
    print("=" * 60)
    print("测试用例2（含景点）:")
    print(f"输入: {text2}")
    print(f"结果: {result2}")
    print(f"期望: city=北京, attraction=故宫, people=2, depart_time=后天, travel_days=3, budget=5000")
    print()
    
    assert result2['city'] == '北京', f"城市错误: {result2['city']}"
    assert result2['attraction'] == '故宫', f"景点错误: {result2['attraction']}（不应包含'玩三天'）"
    assert result2['people'] == 2, f"人数错误: {result2['people']}"
    assert result2['depart_time'] == '后天', f"日期错误: {result2['depart_time']}"
    assert result2['travel_days'] == 3, f"天数错误: {result2['travel_days']}"
    assert result2['budget'] == 5000, f"预算错误: {result2['budget']}"
    print("✅ 测试用例2通过!")
    print()
    
    # 测试用例3 - 混合短语提取
    text3 = "我想去西安参观兵马俑待两天"
    result3 = extractor.extract(text3)
    
    print("=" * 60)
    print("测试用例3（混合短语）:")
    print(f"输入: {text3}")
    print(f"结果: {result3}")
    print(f"期望: city=西安, attraction=兵马俑, travel_days=2")
    print()
    
    assert result3['city'] == '西安', f"城市错误: {result3['city']}"
    assert result3['attraction'] == '兵马俑', f"景点错误: {result3['attraction']}（不应包含'待两天'）"
    assert result3['travel_days'] == 2, f"天数错误: {result3['travel_days']}"
    print("✅ 测试用例3通过!")
    print()
    
    print("=" * 60)
    print("所有基础测试通过! 🎉")
    print()
    
    # 测试用例4 - "我"的语义识别
    text4 = "我想大后天去上海玩一天，预算是2000"
    result4 = extractor.extract(text4)
    
    print("=" * 60)
    print("测试用例4（'我想'语义）:")
    print(f"输入: {text4}")
    print(f"结果: people={result4['people']}")
    print(f"期望: people=1")
    print()
    
    assert result4['people'] == 1, f"人数错误: {result4['people']}（'我想'应识别为1人）"
    print("✅ 测试用例4通过!")
    print()
    
    # 测试用例5 - "我和朋友"的语义识别
    text5 = "我和朋友下周末去北京玩三天，预算五千"
    result5 = extractor.extract(text5)
    
    print("=" * 60)
    print("测试用例5（'我和朋友'语义）:")
    print(f"输入: {text5}")
    print(f"结果: people={result5['people']}")
    print(f"期望: people=2")
    print()
    
    assert result5['people'] == 2, f"人数错误: {result5['people']}（'我和朋友'应识别为2人）"
    print("✅ 测试用例5通过!")
    print()
    
    # 测试用例6 - "我一个人"的语义识别
    text6 = "我一个人明天去杭州玩两天"
    result6 = extractor.extract(text6)
    
    print("=" * 60)
    print("测试用例6（'我一个人'语义）:")
    print(f"输入: {text6}")
    print(f"结果: people={result6['people']}")
    print(f"期望: people=1")
    print()
    
    assert result6['people'] == 1, f"人数错误: {result6['people']}（'我一个人'应识别为1人）"
    print("✅ 测试用例6通过!")
    print()
    
    # 测试用例7 - "我们"的语义识别
    text7 = "我们后天去西安看兵马俑"
    result7 = extractor.extract(text7)
    
    print("=" * 60)
    print("测试用例7（'我们'语义）:")
    print(f"输入: {text7}")
    print(f"结果: people={result7['people']}")
    print(f"期望: people=2")
    print()
    
    assert result7['people'] == 2, f"人数错误: {result7['people']}（'我们'应识别为2人）"
    print("✅ 测试用例7通过!")
    print()
    
    print("=" * 60)
    print("所有测试通过! 🎉")
    print()
    print("⚠️  注意：前端日期解析已修复，请刷新浏览器后重新测试")
    print("   后端提取的 depart_time='大后天' 是正确的")
    print("   前端 parseNaturalDate('大后天') 应该返回 today + 3天")

if __name__ == "__main__":
    test_extraction()
