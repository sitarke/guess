@echo off
@echo off

SET MINICONDA_INSTALLER_PATH=miniconda3_installer.exe
SET MINICONDA_URL=https://mirrors.tuna.tsinghua.edu.cn/anaconda/miniconda/Miniconda3-py39_24.7.1-0-Windows-x86_64.exe

where conda >nul 2>nul
if %errorlevel% neq 0 (
    echo "Conda is not installed"
    echo "Downloading Conda installer..."
    curl -o %MINICONDA_INSTALLER_PATH% %MINICONDA_URL%
    echo "Installing Conda..."
    start /wait "" %MINICONDA_INSTALLER_PATH% /InstallationType=JustMe  /AddToPath=1 /RegisterPython=0 /S /D=%UserProfile%\Miniconda3
    echo "Conda has been installed!"
) else (
    echo "Conda is already installed"
)
pause