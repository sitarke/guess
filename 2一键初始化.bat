@echo off
echo ===========================
echo ��ʼ�������⻷��...
echo ===========================

REM �������⻷��
call conda create -n guess python=3.10 -y
if %errorlevel% neq 0 (
    echo �������⻷��ʧ�ܣ����� Conda �Ƿ���ȷ��װ��
    pause
    exit /b
)

echo ===========================
echo ���⻷�������ɹ�......
echo ===========================
REM �������⻷��
call conda activate guess
if %errorlevel% neq 0 (
    echo �������⻷��ʧ�ܣ����� Conda �Ƿ���ȷ��װ��
    pause
    exit /b
)

echo ===========================
echo ���⻷������ɹ������ڰ�װ����...
echo ===========================

pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
if %errorlevel% neq 0 (
    echo ��װ����ʧ�ܣ����� requirements.txt �ļ���
    pause
    exit /b
)

echo ===========================
echo ����������������װ��ɡ�
echo ===========================
pause