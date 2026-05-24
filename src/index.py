"""
旅游行程规划后端服务 - FastAPI 主入口

统一接口规范：
- 响应格式：{code: int, msg: str, data: any}
- 命名规范：英文小写下划线
- 时间格式：HH:mm
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from dotenv import load_dotenv

# 加载环境变量
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

import src.routes

# 创建 FastAPI 应用
app = FastAPI(
    title="旅游行程规划后端服务",
    description="统一接口规范 | 响应格式: {code, msg, data}",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 全局异常处理
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "code": 500,
            "msg": f"服务器内部错误: {str(exc)}",
            "data": None
        }
    )

# 注册路由
app.include_router(src.routes.health_router)
app.include_router(src.routes.requirement_router)
app.include_router(src.routes.task_router)
app.include_router(src.routes.agent_router)
app.include_router(src.routes.itinerary_router)
app.include_router(src.routes.validate_router)
app.include_router(src.routes.static_data_router)
app.include_router(src.routes.integration_router)
app.include_router(src.routes.nlp_router)
app.include_router(src.routes.weather_router)

# 根路径
@app.get("/")
async def root():
    return {
        "service": "travel-planner-backend",
        "version": "1.0.0",
        "docs": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=9091)