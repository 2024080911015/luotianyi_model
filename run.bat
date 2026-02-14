@echo off
chcp 65001 >nul
title 洛天依桌面助手

echo ========================================
echo       洛天依桌面助手 v1.0
echo ========================================
echo.

echo 检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python，请先安装Python 3.7+
    echo 下载地址: www.python.org/downloads/
    pause
    exit /b 1
)

echo.
echo 启动洛天依桌面助手...
echo 按ESC键可退出程序
echo.

python main.py

if errorlevel 1 (
    echo.
    echo 程序启动失败，请检查:
    echo 1. 是否已安装所有依赖
    echo 2. 是否以管理员身份运行
    echo 3. 系统是否支持透明窗口
    echo.
    pause
)

exit /b 0