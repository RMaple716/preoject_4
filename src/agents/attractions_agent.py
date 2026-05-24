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
