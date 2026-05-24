"""任务分发相关路由"""
import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Any
from fastapi import APIRouter
from src.models.response import success_response, error_response
from src.models.request import TaskDispatchRequest, TaskDispatchResponse, TaskInfo, TaskStatusResponse

router = APIRouter(prefix="/api/v1/task", tags=["任务分发"])
tasks_store = {}
requirements_store = {}  # 用于存储需求信息，实际应从数据库获取

# ============== 任务分解核心逻辑 ==============

def calculate_budget_allocation(total_budget: float, travel_days: int, traveler_count: int) -> Dict[str, float]:
    """
    根据总预算自动分摊到各子类预算
    分摊算法：住宿占30%，餐饮25%，交通15%，门票20%，其他10%
    """
    if not total_budget:
        # 如果未指定总预算，按每人每天500元估算
        total_budget = traveler_count * travel_days * 500

    return {
        "accommodation_budget": round(total_budget * 0.30, 2),
        "food_budget": round(total_budget * 0.25, 2),
        "transport_budget": round(total_budget * 0.15, 2),
        "ticket_budget": round(total_budget * 0.20, 2),
        "other_budget": round(total_budget * 0.10, 2)
    }


def decompose_to_subtasks(requirement_id: str, structured_requirement: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    将结构化需求拆分为各智能体的子任务

    Args:
        requirement_id: 需求ID
        structured_requirement: 结构化需求对象

    Returns:
        子任务列表
    """
    # 提取基本信息
    city_name = structured_requirement.get("city_name", "")
    travel_days = structured_requirement.get("travel_days", 1)
    total_budget = structured_requirement.get("total_budget")
    travel_date = structured_requirement.get("travel_date", "")
    traveler_count = structured_requirement.get("traveler_count", 1)
    preferences = structured_requirement.get("preferences", [])
    dislikes = structured_requirement.get("dislikes", [])

    # 计算预算分配
    budget_allocation = calculate_budget_allocation(total_budget, travel_days, traveler_count)

    # 如果用户指定了具体预算，则使用用户的值
    accommodation_budget = structured_requirement.get("accommodation_budget") or budget_allocation["accommodation_budget"]
    food_budget = structured_requirement.get("food_budget") or budget_allocation["food_budget"]
    transport_budget = structured_requirement.get("transport_budget") or budget_allocation["transport_budget"]
    ticket_budget = structured_requirement.get("ticket_budget") or budget_allocation["ticket_budget"]

    subtasks = []

    # 1. 景点智能体子任务
    attraction_subtask_id = str(uuid.uuid4())
    attraction_params = {
        "city_name": city_name,
        "travel_days": travel_days,
        "preferences": preferences,
        "dislikes": dislikes,
        "ticket_budget": ticket_budget,
        "traveler_count": traveler_count
    }
    subtasks.append({
        "subtask_id": attraction_subtask_id,
        "agent_type": "attraction",
        "parameters": attraction_params,
        "status": "pending",
        "result": None
    })

    # 2. 住宿智能体子任务
    accommodation_subtask_id = str(uuid.uuid4())
    # 计算入住和退房日期
    check_in_date = travel_date if travel_date else datetime.now().strftime("%Y-%m-%d")
    check_out_date = (datetime.strptime(check_in_date, "%Y-%m-%d") + timedelta(days=travel_days)).strftime("%Y-%m-%d")

    accommodation_params = {
        "city_name": city_name,
        "check_in_date": check_in_date,
        "check_out_date": check_out_date,
        "nights": travel_days,
        "budget_per_night": round(accommodation_budget / travel_days, 2) if travel_days > 0 else accommodation_budget,
        "location_preference": "靠近景点" if preferences else None,
        "traveler_count": traveler_count
    }
    subtasks.append({
        "subtask_id": accommodation_subtask_id,
        "agent_type": "accommodation",
        "parameters": accommodation_params,
        "status": "pending",
        "result": None
    })

    # 3. 美食智能体子任务
    food_subtask_id = str(uuid.uuid4())
    food_params = {
        "city_name": city_name,
        "travel_days": travel_days,
        "preferences": preferences,
        "budget_per_person": round(food_budget / (travel_days * traveler_count), 2) if travel_days > 0 and traveler_count > 0 else food_budget,
        "traveler_count": traveler_count
    }
    subtasks.append({
        "subtask_id": food_subtask_id,
        "agent_type": "food",
        "parameters": food_params,
        "status": "pending",
        "result": None
    })

    # 4. 交通智能体子任务
    transport_subtask_id = str(uuid.uuid4())
    transport_params = {
        "city_name": city_name,
        "travel_days": travel_days,
        "budget": transport_budget,
        "mode_preference": "transit"
    }
    subtasks.append({
        "subtask_id": transport_subtask_id,
        "agent_type": "transport",
        "parameters": transport_params,
        "status": "pending",
        "result": None
    })

    return subtasks


@router.post("/decompose")
async def decompose_task(request_data: Dict[str, Any]):
    """
    任务分解接口：将结构化需求拆分为各智能体的子任务

    请求参数:
    {
        "requirement_id": "req_xxx",
        "structured_requirement": { ... }
    }
    """
    requirement_id = request_data.get("requirement_id")
    structured_requirement = request_data.get("structured_requirement")

    if not requirement_id or not structured_requirement:
        return error_response(code=400, msg="缺少必要参数：requirement_id 或 structured_requirement")

    # 验证必填字段
    required_fields = ["city_name", "travel_days", "total_budget", "travel_date", "traveler_count"]
    for field in required_fields:
        if field not in structured_requirement:
            return error_response(code=400, msg=f"缺少必填字段：{field}")

    # 执行业务规则验证
    travel_days = structured_requirement.get("travel_days", 0)
    traveler_count = structured_requirement.get("traveler_count", 0)
    total_budget = structured_requirement.get("total_budget", 0)

    if travel_days < 1 or travel_days > 30:
        return error_response(code=400001, msg="出行天数必须在1-30天之间")

    if traveler_count < 1 or traveler_count > 20:
        return error_response(code=400, msg="出行人数必须在1-20人之间")

    min_budget = traveler_count * 100
    if total_budget < min_budget:
        return error_response(code=400002, msg=f"预算过低，至少需要每人每天100元（最低{min_budget}元）")

    # 执行任务分解
    subtasks = decompose_to_subtasks(requirement_id, structured_requirement)

    # 生成任务批次ID
    batch_id = str(uuid.uuid4())
    task_id = batch_id  # 使用 batch_id 作为主任务ID

    # 存储所有子任务
    tasks_info = []
    for subtask in subtasks:
        task_id_local = subtask["subtask_id"]
        tasks_store[task_id_local] = {
            "task_id": task_id_local,
            "batch_id": batch_id,
            "requirement_id": requirement_id,
            "agent": subtask["agent_type"],
            "parameters": subtask["parameters"],
            "status": "pending",
            "result": None,
            "error": None,
            "created_at": datetime.now().isoformat()
        }
        tasks_info.append(TaskInfo(
            task_id=task_id_local,
            agent=subtask["agent_type"],
            status="pending",
            result=None
        ))

    # 存储主任务信息
    tasks_store[batch_id] = {
        "task_id": batch_id,
        "batch_id": batch_id,
        "requirement_id": requirement_id,
        "type": "main_task",
        "subtasks": [s["subtask_id"] for s in subtasks],
        "status": "pending",
        "progress": 0.0,
        "created_at": datetime.now().isoformat()
    }

    # 异步执行子任务
    import asyncio
    from src.agents import AttractionsAgent, HotelAgent, FoodAgent, TransportAgent

    async def execute_subtasks():
        """异步执行所有子任务"""
        try:
            # 更新主任务状态为运行中
            tasks_store[batch_id]["status"] = "running"

            # 初始化智能体
            attractions_agent = AttractionsAgent()
            hotel_agent = HotelAgent()
            food_agent = FoodAgent()
            transport_agent = TransportAgent()

            # 执行每个子任务
            for i, subtask in enumerate(subtasks):
                task_id_local = subtask["subtask_id"]
                agent_type = subtask["agent_type"]
                parameters = subtask["parameters"]

                # 更新子任务状态为处理中
                tasks_store[task_id_local]["status"] = "processing"

                try:
                    # 根据智能体类型执行相应的任务
                    if agent_type == "attraction":
                        result = await attractions_agent.execute({
                            "task_id": task_id_local,
                            **parameters
                        })
                    elif agent_type == "accommodation":
                        result = await hotel_agent.execute({
                            "task_id": task_id_local,
                            **parameters
                        })
                    elif agent_type == "food":
                        result = await food_agent.execute({
                            "task_id": task_id_local,
                            **parameters
                        })
                    elif agent_type == "transport":
                        result = await transport_agent.execute({
                            "task_id": task_id_local,
                            **parameters
                        })
                    else:
                        result = {"status": "failed", "error_message": f"未知的智能体类型: {agent_type}"}

                    # 更新子任务状态
                    if result["status"] == "success":
                        tasks_store[task_id_local]["status"] = "success"
                        tasks_store[task_id_local]["result"] = result.get("data", {})
                    else:
                        tasks_store[task_id_local]["status"] = "failed"
                        tasks_store[task_id_local]["error"] = result.get("error_message", "执行失败")

                    # 更新主任务进度
                    progress = ((i + 1) / len(subtasks)) * 100
                    tasks_store[batch_id]["progress"] = progress

                except Exception as e:
                    # 子任务执行失败
                    tasks_store[task_id_local]["status"] = "failed"
                    tasks_store[task_id_local]["error"] = str(e)
                    print(f"子任务 {task_id_local} 执行失败: {e}")

            # 所有子任务完成,更新主任务状态
            completed_count = sum(1 for sid in tasks_store[batch_id]["subtasks"] 
                                if tasks_store[sid]["status"] == "success")
            failed_count = sum(1 for sid in tasks_store[batch_id]["subtasks"] 
                             if tasks_store[sid]["status"] == "failed")

            if failed_count > 0:
                tasks_store[batch_id]["status"] = "failed"
            else:
                tasks_store[batch_id]["status"] = "success"

            tasks_store[batch_id]["progress"] = 100.0

        except Exception as e:
            print(f"执行子任务时出错: {e}")
            tasks_store[batch_id]["status"] = "failed"

    # 启动异步任务执行
    asyncio.create_task(execute_subtasks())

    return success_response(
        data={
            "task_id": task_id,
            "batch_id": batch_id,
            "requirement_id": requirement_id,
            "subtasks": [s.model_dump() for s in tasks_info]
        },
        msg="任务分解成功"
    )


@router.post("/dispatch")
async def dispatch_tasks(request: TaskDispatchRequest):
    """
    旧版任务分发接口（保留兼容）
    """
    batch_id = str(uuid.uuid4())
    tasks = []
    for agent in request.agents:
        task_id = str(uuid.uuid4())
        task_info = TaskInfo(task_id=task_id, agent=agent, status="pending", result=None)
        tasks.append(task_info)
        tasks_store[task_id] = {
            "task_id": task_id, "batch_id": batch_id, "requirement_id": request.requirement_id,
            "agent": agent, "status": "pending", "result": None, "created_at": datetime.now().isoformat()
        }
    return success_response(data=TaskDispatchResponse(batch_id=batch_id, tasks=[t.model_dump() for t in tasks]).model_dump(), msg="任务分发成功")


@router.get("/{task_id}")
async def get_task_status(task_id: str):
    """
    获取任务状态
    """
    if task_id not in tasks_store:
        return error_response(code=404, msg="任务不存在")

    task = tasks_store[task_id]

    # 如果是主任务，计算进度
    if task.get("type") == "main_task":
        subtask_ids = task.get("subtasks", [])
        completed_count = sum(1 for sid in subtask_ids if tasks_store.get(sid, {}).get("status") == "success")
        failed_count = sum(1 for sid in subtask_ids if tasks_store.get(sid, {}).get("status") == "failed")
        total = len(subtask_ids)

        progress = (completed_count / total * 100) if total > 0 else 0

        if failed_count > 0:
            status = "failed"
        elif completed_count == total:
            status = "success"
        else:
            status = "running"

        task["status"] = status
        task["progress"] = progress

        return success_response(data={
            "task_id": task_id,
            "status": status,
            "progress": progress,
            "failed_subtasks": [sid for sid in subtask_ids if tasks_store.get(sid, {}).get("status") == "failed"],
            "message": f"已完成 {completed_count}/{total} 个子任务"
        }, msg="获取成功")

    # 子任务直接返回
    return success_response(data=TaskStatusResponse(
        task_id=task["task_id"],
        agent=task["agent"],
        status=task["status"],
        result=task.get("result"),
        error=task.get("error")
    ).model_dump(), msg="获取成功")


@router.post("/update/{task_id}")
async def update_task_result(task_id: str, result_data: Dict[str, Any]):
    """
    更新任务结果（供智能体调用）

    请求参数:
    {
        "status": "success" | "failed",
        "result": { ... },  // 智能体返回的结果
        "error": null | "错误信息"
    }
    """
    if task_id not in tasks_store:
        return error_response(code=404, msg="任务不存在")

    task = tasks_store[task_id]
    task["status"] = result_data.get("status", "success")
    task["result"] = result_data.get("result")
    task["error"] = result_data.get("error")
    task["updated_at"] = datetime.now().isoformat()

    # 如果是子任务，更新主任务的进度
    batch_id = task.get("batch_id")
    if batch_id and batch_id in tasks_store:
        main_task = tasks_store[batch_id]
        if main_task.get("type") == "main_task":
            subtask_ids = main_task.get("subtasks", [])
            completed_count = sum(1 for sid in subtask_ids if tasks_store.get(sid, {}).get("status") == "success")
            total = len(subtask_ids)
            main_task["progress"] = (completed_count / total * 100) if total > 0 else 0

    return success_response(data={"task_id": task_id}, msg="更新成功")


@router.get("/{task_id}")
async def get_task_status(task_id: str):
    """
    获取任务状态
    """
    if task_id not in tasks_store:
        return error_response(code=404, msg="任务不存在")

    task = tasks_store[task_id]

    # 如果是主任务，计算进度
    if task.get("type") == "main_task":
        subtask_ids = task.get("subtasks", [])
        completed_count = sum(1 for sid in subtask_ids if tasks_store.get(sid, {}).get("status") == "success")
        failed_count = sum(1 for sid in subtask_ids if tasks_store.get(sid, {}).get("status") == "failed")
        total = len(subtask_ids)

        progress = (completed_count / total * 100) if total > 0 else 0

        if failed_count > 0:
            status = "failed"
        elif completed_count == total:
            status = "success"
        else:
            status = "running"

        task["status"] = status
        task["progress"] = progress

        return success_response(data={
            "task_id": task_id,
            "status": status,
            "progress": progress,
            "failed_subtasks": [sid for sid in subtask_ids if tasks_store.get(sid, {}).get("status") == "failed"],
            "message": f"已完成 {completed_count}/{total} 个子任务"
        }, msg="获取成功")

    # 子任务直接返回
    return success_response(data=TaskStatusResponse(
        task_id=task["task_id"],
        agent=task["agent"],
        status=task["status"],
        result=task.get("result"),
        error=task.get("error")
    ).model_dump(), msg="获取成功")
