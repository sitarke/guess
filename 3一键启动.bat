@echo off
REM �������⻷��
call conda activate guess
if %errorlevel% neq 0 (
    echo �������⻷��ʧ�ܣ����� Conda �Ƿ���ȷ��װ��
    pause
    exit /b
)
echo ===========================
echo ���⻷������ɹ�����ʼ����
echo ===========================

set /p choice="������ 1 �����������˷���ˡ� �� 2 �������Զ����±��ذ桿 "

if "%choice%"=="1" (
    call python server.py
) else if "%choice%"=="2" (
    call python start.py
) else (
    echo ������Ч�������� 1 �� 2��
)