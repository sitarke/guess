@echo off
echo ===========================
echo 开始创建虚拟环境...
echo ===========================

REM 创建虚拟环境
call conda create -n guess python=3.10 -y
if %errorlevel% neq 0 (
    echo 创建虚拟环境失败，请检查 Conda 是否正确安装。
    pause
    exit /b
)

echo ===========================
echo 虚拟环境创建成功......
echo ===========================
REM 进入虚拟环境
call conda activate guess
if %errorlevel% neq 0 (
    echo 激活虚拟环境失败，请检查 Conda 是否正确安装。
    pause
    exit /b
)

echo ===========================
echo 虚拟环境激活成功，正在安装依赖...
echo ===========================

pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
if %errorlevel% neq 0 (
    echo 安装依赖失败，请检查 requirements.txt 文件。
    pause
    exit /b
)

echo ===========================
echo 环境创建和依赖安装完成。
echo ===========================
pause