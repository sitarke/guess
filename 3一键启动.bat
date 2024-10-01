@echo off
REM 进入虚拟环境
call conda activate guess
if %errorlevel% neq 0 (
    echo 激活虚拟环境失败，请检查 Conda 是否正确安装。
    pause
    exit /b
)
echo ===========================
echo 虚拟环境激活成功，开始启动
echo ===========================

set /p choice="请输入 1 启动【机器人服务端】 或 2 【启动自动竞猜本地版】 "

if "%choice%"=="1" (
    call python server.py
) else if "%choice%"=="2" (
    call python start.py
) else (
    echo 输入无效，请输入 1 或 2。
)