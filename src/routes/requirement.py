"""用户需求相关路由"""
import uuid
from datetime import datetime
from fastapi import APIRouter
from src.models.response import success_response, error_response
from src.models.request import (
    RequirementSubmitRequest, RequirementSubmitResponse,
    RequirementParseRequest, RequirementParseResponse, ParsedKeywords
)

router = APIRouter(prefix="/api/v1/requirement", tags=["用户需求"])
requirements_store = {}

@router.post("/submit")
async def submit_requirement(request: RequirementSubmitRequest):
    requirement_id = str(uuid.uuid4())
    requirements_store[requirement_id] = {
        "requirement_id": requirement_id,
        "user_id": request.user_id,
        "requirement": request.requirement.model_dump(),
        "status": "pending",
        "created_at": datetime.now().isoformat()
    }
    return success_response(
        data=RequirementSubmitResponse(requirement_id=requirement_id, status="pending").model_dump(),
        msg="需求提交成功"
    )

@router.post("/parse")
async def parse_requirement(request: RequirementParseRequest):
    if request.requirement_id not in requirements_store:
        return error_response(code=404, msg="需求不存在")
    req = requirements_store[request.requirement_id]["requirement"]
    keywords = ParsedKeywords(
        city_name=req.get("city_name", ""),
        travel_days=req.get("travel_days", 1),
        total_budget=req.get("total_budget"),
        travel_type=req.get("travel_type"),
        preferences=req.get("preferences", [])
    )
    requirements_store[request.requirement_id]["status"] = "parsed"
    return success_response(
        data=RequirementParseResponse(requirement_id=request.requirement_id, parsed=True, keywords=keywords).model_dump(),
        msg="需求解析成功"
    )

@router.get("/{requirement_id}")
async def get_requirement(requirement_id: str):
    if requirement_id not in requirements_store:
        return error_response(code=404, msg="需求不存在")
    return success_response(data=requirements_store[requirement_id], msg="获取成功")