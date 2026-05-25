"""
景点推荐智能体
"""
from typing import Dict, Any, List
from .base_agent import BaseAgent

class AttractionsAgent(BaseAgent):
    """景点推荐智能体"""

    def __init__(self):
        super().__init__(
            agent_id="attractions_agent_001",
            name="景点推荐助手",
            description="基于用户偏好推荐合适的旅游景点"
        )

    def get_capabilities(self) -> List[str]:
        return [
            "景点推荐",
            "行程规划",
            "景点信息查询",
            "游览时间建议"
        ]

    async def execute(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """执行景点推荐任务"""
        import time
        import uuid
        import os

        start_time = time.time()
        task_id = task_data.get("task_id", f"attr_{uuid.uuid4().hex[:8]}")

        # 提取任务参数
        city_name = task_data.get("city_name", "")
        travel_days = task_data.get("travel_days", 1)
        ticket_budget = task_data.get("ticket_budget")
        preferences = task_data.get("preferences", [])
        dislikes = task_data.get("dislikes", [])
        location_preference = task_data.get("location_preference")
        traveler_count = task_data.get("traveler_count", 1)

        # 如果没有配置API密钥，返回模拟数据
        if not os.getenv("DEEPSEEK_API_KEY"):
            return self._get_mock_data(task_id, city_name, travel_days, start_time)

        # 构建系统提示词
        system_prompt = """你是一个专业的景点推荐助手。请根据用户需求推荐合适的旅游景点。

要求：
1. 推荐的景点要符合用户偏好和预算
2. 合理安排游览时间
3. 提供准确的费用信息
4. 包含实用信息（位置、最佳游览时间等）

返回格式：
{
  "attractions": [
    {
      "attraction_id": "att_001",
      "name": "景点名称",
      "city_name": "城市名称",
      "location": "景点地址",
      "description": "景点描述",
      "recommended_duration": "游览时长（如：4小时）",
      "visit_time_slot": "morning/afternoon/evening",
      "ticket_price": 门票价格（数字）,
      "rating": 评分（0-5）,
      "opening_hours": "营业时间",
      "tags": ["标签1", "标签2"]
    }
  ]
}"""

        # 构建用户提示词
        user_prompt = f"""请为以下旅行需求推荐景点：

目的地：{city_name}
旅行天数：{travel_days}天
门票预算：{ticket_budget}元（如未指定则不考虑预算）
偏好：{', '.join(preferences) if preferences else '无特殊偏好'}
不喜欢的：{', '.join(dislikes) if dislikes else '无'}
区域偏好：{location_preference if location_preference else '无特殊要求'}
旅行人数：{traveler_count}人

请推荐{travel_days * 3}个左右的景点，确保每天有合理的游览安排。
每个景点必须包含：
- 唯一ID（attraction_id，att_xxx格式）
- 景点名称
- 城市名称（与目的地一致）
- 景点地址（详细地址）
- 景点描述（简要介绍）
- 建议游览时长
- 建议游览时段（morning/afternoon/evening）
- 门票价格
- 评分（0-5）
- 营业时间
- 标签"""

        # 调用LLM
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        try:
            response_content = await self.call_llm(messages, max_tokens=2000)
            result = self._parse_json_response(response_content)

            processing_time = (time.time() - start_time) * 1000

            return {
                "task_id": task_id,
                "status": "success",
                "data": {
                    "items": result.get("attractions", [])
                },
                "metadata": {
                    "processing_time_ms": processing_time,
                    "source": "ai_generated",
                    "model_used": "deepseek-chat",
                    "over_budget": False
                },
                "error_message": None
            }
        except Exception as e:
            processing_time = (time.time() - start_time) * 1000
            return {
                "task_id": task_id,
                "status": "failed",
                "data": {"items": []},
                "metadata": {
                    "processing_time_ms": processing_time,
                    "source": "ai_generated",
                    "model_used": "deepseek-chat",
                    "over_budget": False
                },
                "error_message": str(e)
            }

    def _get_mock_data(self, task_id: str, city_name: str, travel_days: int, start_time: float) -> Dict[str, Any]:
        """生成模拟景点数据"""
        import time

        # 根据城市名称生成不同的景点
        city_attractions = {
            "北京": [
                {"attraction_id": "att_001", "name": "故宫博物院", "city_name": city_name, "location": "北京市东城区景山前街4号", "description": "中国明清两代的皇家宫殿,世界文化遗产", "recommended_duration": "4小时", "visit_time_slot": "morning", "ticket_price": 60, "rating": 4.8, "opening_hours": "8:30-17:00", "tags": ["历史", "文化", "世界遗产"]},
                {"attraction_id": "att_002", "name": "天坛公园", "city_name": city_name, "location": "北京市东城区天坛路甲1号", "description": "明清两代皇帝祭天的场所,中国古代建筑杰作", "recommended_duration": "3小时", "visit_time_slot": "afternoon", "ticket_price": 35, "rating": 4.7, "opening_hours": "6:00-22:00", "tags": ["历史", "建筑", "公园"]},
                {"attraction_id": "att_003", "name": "颐和园", "city_name": city_name, "location": "北京市海淀区新建宫门路19号", "description": "中国古典园林之首,皇家园林博物馆", "recommended_duration": "4小时", "visit_time_slot": "morning", "ticket_price": 50, "rating": 4.8, "opening_hours": "6:30-18:00", "tags": ["园林", "历史", "皇家"]},
                {"attraction_id": "att_004", "name": "长城(八达岭)", "city_name": city_name, "location": "北京市延庆区八达岭镇", "description": "世界文化遗产,中国古代军事防御工程", "recommended_duration": "5小时", "visit_time_slot": "morning", "ticket_price": 40, "rating": 4.9, "opening_hours": "7:30-16:00", "tags": ["历史", "世界遗产", "徒步"]},
                {"attraction_id": "att_005", "name": "南锣鼓巷", "city_name": city_name, "location": "北京市东城区南锣鼓巷", "description": "北京最古老的街区之一,胡同文化体验地", "recommended_duration": "2小时", "visit_time_slot": "afternoon", "ticket_price": 0, "rating": 4.5, "opening_hours": "全天", "tags": ["文化", "购物", "美食"]},
                {"attraction_id": "att_006", "name": "798艺术区", "city_name": city_name, "location": "北京市朝阳区酒仙桥路4号", "description": "当代艺术聚集地,工业遗址改造的艺术区", "recommended_duration": "3小时", "visit_time_slot": "afternoon", "ticket_price": 0, "rating": 4.6, "opening_hours": "10:00-18:00", "tags": ["艺术", "文化", "摄影"]},
            ],
            "上海": [
                {"attraction_id": "att_001", "name": "外滩", "city_name": city_name, "location": "上海市黄浦区中山东一路", "description": "上海标志性景点,万国建筑博览群", "recommended_duration": "2小时", "visit_time_slot": "evening", "ticket_price": 0, "rating": 4.8, "opening_hours": "全天", "tags": ["历史", "建筑", "夜景"]},
                {"attraction_id": "att_002", "name": "东方明珠", "city_name": city_name, "location": "上海市浦东新区世纪大道1号", "description": "上海地标建筑,登高俯瞰城市全景", "recommended_duration": "2小时", "visit_time_slot": "evening", "ticket_price": 220, "rating": 4.7, "opening_hours": "9:00-21:30", "tags": ["地标", "观景", "夜景"]},
                {"attraction_id": "att_003", "name": "豫园", "city_name": city_name, "location": "上海市黄浦区福佑路168号", "description": "明代私家园林,江南古典园林代表", "recommended_duration": "2小时", "visit_time_slot": "morning", "ticket_price": 40, "rating": 4.6, "opening_hours": "8:30-17:00", "tags": ["园林", "历史", "文化"]},
                {"attraction_id": "att_004", "name": "田子坊", "city_name": city_name, "location": "上海市黄浦区泰康路210弄", "description": "艺术创意园区,石库门建筑群", "recommended_duration": "2小时", "visit_time_slot": "afternoon", "ticket_price": 0, "rating": 4.5, "opening_hours": "10:00-21:00", "tags": ["艺术", "文化", "购物"]},
                {"attraction_id": "att_005", "name": "南京路步行街", "city_name": city_name, "location": "上海市黄浦区南京东路", "description": "中华商业第一街,购物天堂", "recommended_duration": "3小时", "visit_time_slot": "afternoon", "ticket_price": 0, "rating": 4.6, "opening_hours": "全天", "tags": ["购物", "美食", "商业"]},
                {"attraction_id": "att_006", "name": "上海博物馆", "city_name": city_name, "location": "上海市黄浦区人民大道201号", "description": "中国古代艺术博物馆,文物收藏丰富", "recommended_duration": "3小时", "visit_time_slot": "morning", "ticket_price": 0, "rating": 4.7, "opening_hours": "9:00-17:00", "tags": ["博物馆", "历史", "文化"]},
            ],
            "杭州": [
                {"attraction_id": "att_001", "name": "西湖", "city_name": city_name, "location": "浙江省杭州市西湖区", "description": "世界文化遗产,中国最美湖泊之一", "recommended_duration": "4小时", "visit_time_slot": "morning", "ticket_price": 0, "rating": 4.9, "opening_hours": "全天", "tags": ["自然", "文化", "世界遗产"]},
                {"attraction_id": "att_002", "name": "灵隐寺", "city_name": city_name, "location": "浙江省杭州市西湖区灵隐路法云弄1号", "description": "中国著名佛教寺院,千年古刹", "recommended_duration": "2小时", "visit_time_slot": "morning", "ticket_price": 75, "rating": 4.7, "opening_hours": "7:00-18:00", "tags": ["宗教", "历史", "文化"]},
                {"attraction_id": "att_003", "name": "雷峰塔", "city_name": city_name, "location": "浙江省杭州市西湖区南山路15号", "description": "西湖十景之一,白娘子传说发源地", "recommended_duration": "2小时", "visit_time_slot": "afternoon", "ticket_price": 40, "rating": 4.6, "opening_hours": "8:00-20:00", "tags": ["历史", "传说", "观景"]},
                {"attraction_id": "att_004", "name": "宋城", "city_name": city_name, "location": "浙江省杭州市西湖区之江路148号", "description": "大型文化主题公园,宋城千古情演出", "recommended_duration": "4小时", "visit_time_slot": "afternoon", "ticket_price": 310, "rating": 4.5, "opening_hours": "10:00-21:00", "tags": ["主题公园", "演出", "文化"]},
                {"attraction_id": "att_005", "name": "西溪湿地", "city_name": city_name, "location": "浙江省杭州市西湖区天目山路518号", "description": "国家湿地公园,城市绿肺", "recommended_duration": "3小时", "visit_time_slot": "morning", "ticket_price": 80, "rating": 4.7, "opening_hours": "7:30-18:30", "tags": ["自然", "生态", "休闲"]},
                {"attraction_id": "att_006", "name": "龙井村", "city_name": city_name, "location": "浙江省杭州市西湖区龙井村", "description": "西湖龙井茶产地,茶文化体验", "recommended_duration": "2小时", "visit_time_slot": "afternoon", "ticket_price": 0, "rating": 4.6, "opening_hours": "全天", "tags": ["茶文化", "乡村", "自然"]},
            ],
            "成都": [
                {"attraction_id": "att_001", "name": "大熊猫繁育研究基地", "city_name": city_name, "location": "四川省成都市成华区熊猫大道1375号", "description": "世界著名的大熊猫迁地保护基地", "recommended_duration": "3小时", "visit_time_slot": "morning", "ticket_price": 58, "rating": 4.8, "opening_hours": "7:30-18:00", "tags": ["动物", "自然", "亲子"]},
                {"attraction_id": "att_002", "name": "宽窄巷子", "city_name": city_name, "location": "四川省成都市青羊区宽窄巷子", "description": "成都历史文化街区,体验老成都生活", "recommended_duration": "2小时", "visit_time_slot": "afternoon", "ticket_price": 0, "rating": 4.6, "opening_hours": "全天", "tags": ["文化", "美食", "历史"]},
                {"attraction_id": "att_003", "name": "锦里古街", "city_name": city_name, "location": "四川省成都市武侯区武侯祠大街231号", "description": "仿古商业街,三国文化体验地", "recommended_duration": "2小时", "visit_time_slot": "afternoon", "ticket_price": 0, "rating": 4.5, "opening_hours": "全天", "tags": ["文化", "购物", "美食"]},
                {"attraction_id": "att_004", "name": "武侯祠", "city_name": city_name, "location": "四川省成都市武侯区武侯祠大街231号", "description": "中国唯一的君臣合祀祠庙,三国圣地", "recommended_duration": "2小时", "visit_time_slot": "morning", "ticket_price": 60, "rating": 4.7, "opening_hours": "8:00-18:00", "tags": ["历史", "文化", "三国"]},
                {"attraction_id": "att_005", "name": "杜甫草堂", "city_name": city_name, "location": "四川省成都市青羊区青华路37号", "description": "唐代诗人杜甫的故居,文学圣地", "recommended_duration": "2小时", "visit_time_slot": "morning", "ticket_price": 60, "rating": 4.6, "opening_hours": "8:00-18:30", "tags": ["历史", "文化", "文学"]},
                {"attraction_id": "att_006", "name": "春熙路", "city_name": city_name, "location": "四川省成都市锦江区春熙路", "description": "成都最繁华的商业街,购物美食天堂", "recommended_duration": "2小时", "visit_time_slot": "evening", "ticket_price": 0, "rating": 4.5, "opening_hours": "全天", "tags": ["购物", "美食", "商业"]},
            ]
        }

        # 获取对应城市的景点,如果没有则使用通用景点
        attractions = city_attractions.get(city_name, [
            {"attraction_id": "att_001", "name": f"{city_name}博物馆", "city_name": city_name, "location": f"{city_name}市中心", "description": f"了解{city_name}历史文化的好去处", "recommended_duration": "2小时", "visit_time_slot": "morning", "ticket_price": 50, "rating": 4.5, "opening_hours": "9:00-17:00", "tags": ["历史", "文化"]},
            {"attraction_id": "att_002", "name": f"{city_name}公园", "city_name": city_name, "location": f"{city_name}市中心", "description": f"{city_name}市民休闲的好去处", "recommended_duration": "2小时", "visit_time_slot": "afternoon", "ticket_price": 0, "rating": 4.4, "opening_hours": "6:00-22:00", "tags": ["自然", "休闲"]},
            {"attraction_id": "att_003", "name": f"{city_name}古街", "city_name": city_name, "location": f"{city_name}老城区", "description": f"体验{city_name}传统文化", "recommended_duration": "2小时", "visit_time_slot": "afternoon", "ticket_price": 0, "rating": 4.5, "opening_hours": "全天", "tags": ["文化", "历史"]},
        ])

        # 根据天数选择景点数量
        num_attractions = min(len(attractions), travel_days * 3)
        selected_attractions = attractions[:num_attractions]

        processing_time = (time.time() - start_time) * 1000

        return {
            "task_id": task_id,
            "status": "success",
            "data": {
                "items": selected_attractions
            },
            "metadata": {
                "processing_time_ms": processing_time,
                "source": "mock_data",
                "model_used": None,
                "over_budget": False
            },
            "error_message": None
        }
