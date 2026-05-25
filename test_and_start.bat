@echo off
chcp 65001 >nul
echo ========================================
echo   旅游行程规划系统 - 前端API测试
echo ========================================
echo.

echo [步骤1] 检查后端服务...
curl -s http://127.0.0.1:9091/api/v1/health >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 后端服务未启动!
    echo.
    echo 请先在另一个终端窗口运行:
    echo    python src/index.py
    echo.
    pause
    exit /b 1
)
echo ✅ 后端服务正常运行
echo.

echo [步骤2] 运行API集成测试...
python frontend/test_api_integration.py
echo.

echo [步骤3] 启动前端开发服务器...
echo.
echo 前端将运行在: http://localhost:3000
echo 后端API代理: http://127.0.0.1:9091
echo.
echo 按 Ctrl+C 停止前端服务
echo.
cd frontend
npm run dev