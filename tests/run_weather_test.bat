@echo off
chcp 65001
echo ====================================
echo 天气API集成测试
echo ====================================
echo.

REM 检查Python环境
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: 未找到Python环境
    echo 请先安装Python 3.8或更高版本
    pause
    exit /b 1
)

REM 检查环境变量
if not defined AMAP_API_KEY (
    echo 警告: 未配置AMAP_API_KEY环境变量
    echo 某些测试可能会失败
    echo 请设置环境变量: set AMAP_API_KEY=your_api_key
    echo.
)

REM 运行测试
echo 开始运行测试...
echo.
python tests\test_weather_integration.py

if %errorlevel% neq 0 (
    echo.
    echo 测试执行失败
    pause
    exit /b 1
)

echo.
echo 测试执行完成
pause
