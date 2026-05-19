"""任务分发相关路由"""
import uuid
from datetime import datetime
from fastapi import APIRouter
from src.models.response import success_response, error_response
from src.models.request import TaskDispatchRequest, TaskDispatchResponse, TaskInfo, TaskStatusResponse

router = APIRouter(prefix="/api/v1/task", tags=["任务分发"])
tasks_store = {}

@router.post("/dispatch")
async def dispatch_tasks(request: TaskDispatchRequest):
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
    if task_id not in tasks_store:
        return error_response(code=404, msg="任务不存在")
    task = tasks_store[task_id]
    return success_response(data=TaskStatusResponse(task_id=task["task_id"], agent=task["agent"], status=task["status"], result=task.get("result"), error=task.get("error")).model_dump(), msg="获取成功")