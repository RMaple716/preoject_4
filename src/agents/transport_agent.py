"""
交通推荐智能体
"""
from typing import Dict, Any, List
from .base_agent import BaseAgent

class TransportAgent(BaseAgent):
    """交通推荐智能体"""

    def __init__(self):
        super().__init__(
            agent_id="transport_agent_001",
            name="交通规划助手",
            description="为用户提供交通方案推荐"
        )

    def get_capabilities(self) -> List[str]:
        return [
            "交通方案推荐",
            "路线规划",
            "票价查询",
            "时刻表查询"
        ]

    async def execute(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """执行交通推荐任务"""
        import time
        import uuid

        start_time = time.time()
        task_id = task_data.get("task_id", f"trans_{uuid.uuid4().hex[:8]}")

        # 提取任务参数
        from_location = task_data.get("from_location", {})
        to_location = task_data.get("to_location", {})
        mode_preference = task_data.get("mode_preference")  # walking/transit/driving

        # 构建系统提示词
        system_prompt = """你是一个专业的交通规划助手。请为用户推荐合适的交通方案。

要求：
1. 提供详细的交通步骤
2. 包含准确的距离和时间信息
3. 考虑不同交通方式
4. 提供实用建议

返回格式：
{
  "transport_options": [
    {
      "transport_id": "trans_001",
      "type": "flight/train/bus/subway/taxi",
      "from": "起点名称",
      "to": "终点名称",
      "departure_time": "出发时间（HH:mm）",
      "arrival_time": "到达时间（HH:mm）",
      "duration": "预计时长（如：30分钟）",
      "price": 价格（数字）
    }
  ]
}"""

        # 构建用户提示词
        from_name = from_location.get("name", "")
        to_name = to_location.get("name", "")
        mode_hint = f"优先使用{mode_preference}" if mode_preference else "推荐所有可用交通方式"

        user_prompt = f"""请为以下行程推荐交通方案：

起点：{from_name}
终点：{to_name}
要求：{mode_hint}

请提供2-3个不同的交通方案供用户选择。
每个方案必须包含：
- 唯一ID（transport_id，trans_xxx格式）
- 交通类型（flight/train/bus/subway/taxi）
- 起点名称
- 终点名称
- 出发时间（格式：HH:mm）
- 到达时间（格式：HH:mm）
- 预计时长
- 价格"""

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
                    "items": result.get("transport_options", [])
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
