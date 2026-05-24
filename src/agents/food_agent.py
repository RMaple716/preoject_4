"""
美食推荐智能体
"""
from typing import Dict, Any, List
from .base_agent import BaseAgent

class FoodAgent(BaseAgent):
    """美食推荐智能体"""

    def __init__(self):
        super().__init__(
            agent_id="food_agent_001",
            name="美食推荐助手",
            description="为用户推荐当地特色美食和餐厅"
        )

    def get_capabilities(self) -> List[str]:
        return [
            "美食推荐",
            "餐厅推荐",
            "特色菜介绍",
            "价格查询"
        ]

    async def execute(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """执行美食推荐任务"""
        import time
        import uuid

        start_time = time.time()
        task_id = task_data.get("task_id", f"food_{uuid.uuid4().hex[:8]}")

        # 提取任务参数
        city_name = task_data.get("city_name", "")
        meal_type = task_data.get("meal_type")  # breakfast/lunch/dinner
        budget_per_person = task_data.get("budget_per_person")
        cuisine_preference = task_data.get("cuisine_preference")

        # 构建系统提示词
        system_prompt = """你是一个专业的美食推荐助手。请为用户推荐当地特色美食和餐厅。

要求：
1. 推荐的餐厅要符合用户预算和口味偏好
2. 包含当地特色菜品
3. 提供准确的价格和评分信息
4. 包含实用信息（位置、特色等）

返回格式：
{
  "restaurants": [
    {
      "restaurant_id": "rest_001",
      "name": "餐厅名称",
      "city_name": "城市名称",
      "location": "餐厅地址",
      "cuisine_type": "菜系类型",
      "avg_price": 人均消费（数字）,
      "rating": 评分（0-5）,
      "specialties": ["特色菜1", "特色菜2"]
    }
  ]
}"""

        # 构建用户提示词
        budget_hint = f"人均预算：{budget_per_person}元" if budget_per_person else "无预算限制"
        cuisine_hint = f"菜系偏好：{cuisine_preference}" if cuisine_preference else "推荐当地特色菜系"
        meal_hint = f"餐别：{meal_type}" if meal_type else "全天用餐"

        user_prompt = f"""请为以下美食需求推荐餐厅：

城市：{city_name}
{meal_hint}
{budget_hint}
{cuisine_hint}

请推荐5-8家不同特色的餐厅，包括当地知名餐厅和特色小店。
每个餐厅必须包含：
- 唯一ID（restaurant_id，rest_xxx格式）
- 餐厅名称
- 城市名称（与目的地一致）
- 餐厅地址（详细地址）
- 菜系类型
- 人均消费
- 评分（0-5）
- 特色菜品"""

        # 调用LLM
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        try:
            response_content = await self.call_llm(messages, max_tokens=1500)
            result = self._parse_json_response(response_content)

            processing_time = (time.time() - start_time) * 1000

            return {
                "task_id": task_id,
                "status": "success",
                "data": {
                    "items": result.get("restaurants", [])
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
