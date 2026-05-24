"""任务分发相关路由"""
import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.database import get_db
from src.models.response import success_response, error_response
from src.models.request import TaskDispatchRequest, TaskDispatchResponse, TaskInfo, TaskStatusResponse
from src.services.database_service import TaskService, RequirementService

router = APIRouter(prefix="/api/v1/task", tags=["任务分发"])

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
        "budget_per_person": round(food_budget / (travel_days * 3 * traveler_count), 2) if travel_days > 0 and traveler_count > 0 else 100,
        "cuisine_preference": "当地特色" if "美食" in preferences else None,
        "preferences": preferences,
        "dislikes": dislikes
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
        "travel_date": travel_date,
        "mode_preference": "transit"  # 默认公共交通
    }
    subtasks.append({
        "subtask_id": transport_subtask_id,
        "agent_type": "transport",
        "parameters": transport_params,
        "status": "pending",
        "result": None
    })
    
    return subtasks


# ============== API 路由 ==============

@router.post("/decompose")
async def decompose_task(request_data: Dict[str, Any], db: Session = Depends(get_db)):
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
    
    # 验证需求是否存在
    requirement = RequirementService.get_requirement(db, requirement_id)
    if not requirement:
        return error_response(code=404, msg="需求不存在")
    
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
    
    # 批量创建子任务到数据库
    tasks = TaskService.create_batch_tasks(
        db=db,
        batch_id=batch_id,
        requirement_id=requirement_id,
        subtasks=subtasks
    )
    
    # 构建响应数据
    tasks_info = [TaskInfo(
        task_id=task.task_id,
        agent=task.agent_type,
        status=task.status,
        result=None
    ) for task in tasks]
    
    return success_response(
        data={
            "task_id": batch_id,
            "batch_id": batch_id,
            "requirement_id": requirement_id,
            "subtasks": [t.model_dump() for t in tasks_info]
        },
        msg="任务分解成功"
    )


@router.post("/dispatch")
async def dispatch_tasks(request: TaskDispatchRequest, db: Session = Depends(get_db)):
    """
    旧版任务分发接口（保留兼容）
    """
    batch_id = str(uuid.uuid4())
    subtasks = []
    
    for agent in request.agents:
        subtasks.append({
            "agent_type": agent,
            "parameters": {}
        })
    
    tasks = TaskService.create_batch_tasks(
        db=db,
        batch_id=batch_id,
        requirement_id=request.requirement_id,
        subtasks=subtasks
    )
    
    tasks_info = [TaskInfo(
        task_id=task.task_id,
        agent=task.agent_type,
        status=task.status,
        result=None
    ) for task in tasks]
    
    return success_response(
        data=TaskDispatchResponse(
            batch_id=batch_id, 
            tasks=[t.model_dump() for t in tasks_info]
        ).model_dump(), 
        msg="任务分发成功"
    )


@router.get("/{task_id}")
async def get_task_status(task_id: str, db: Session = Depends(get_db)):
    """
    获取任务状态 - 从数据库查询
    """
    # 先尝试作为批次ID查询
    progress_info = TaskService.calculate_batch_progress(db, task_id)
    
    if progress_info["total"] > 0:
        # 是批次ID，返回总体进度
        return success_response(data={
            "task_id": task_id,
            "status": progress_info["status"],
            "progress": progress_info["progress"],
            "completed": progress_info["completed"],
            "failed": progress_info["failed"],
            "total": progress_info["total"],
            "message": f"已完成 {progress_info['completed']}/{progress_info['total']} 个子任务"
        }, msg="获取成功")
    
    # 尝试作为单个任务ID查询
    task = TaskService.get_task(db, task_id)
    
    if not task:
        return error_response(code=404, msg="任务不存在")
    
    return success_response(data=TaskStatusResponse(
        task_id=task.task_id,
        agent=task.agent_type,
        status=task.status,
        result=task.result,
        error=task.error
    ).model_dump(), msg="获取成功")


@router.post("/update/{task_id}")
async def update_task_result(task_id: str, result_data: Dict[str, Any], db: Session = Depends(get_db)):
    """
    更新任务结果（供智能体调用）- 保存到数据库
    
    请求参数:
    {
        "status": "success" | "failed",
        "result": { ... },  // 智能体返回的结果
        "error": null | "错误信息"
    }
    """
    task = TaskService.update_task_result(
        db=db,
        task_id=task_id,
        status=result_data.get("status", "success"),
        result=result_data.get("result"),
        error=result_data.get("error")
    )
    
    if not task:
        return error_response(code=404, msg="任务不存在")
    
    return success_response(
        data={"task_id": task_id, "status": task.status}, 
        msg="任务结果更新成功"
    )