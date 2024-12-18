@REM Author: Recogerous
@REM Version: v1.4
@REM Description: 该脚本用于初始化Python虚拟环境
@echo off & cls
chcp 65001 > nul

@REM 询问是否新建环境，默认为否，下面两个空行必须保留

echo 是否在当前目录下新建Python venv虚拟环境？

set /p create_env="这将覆盖已有的名为venv的环境(y/n)[n]:"
if "%create_env%" == "" (
    set create_env=n
)
if not "%create_env%" == "y" (
    echo 按任意键退出 & pause
    exit
)

@REM 设置虚拟环境的名称和位置
set VENV_NAME=venv
set VENV_DIR=%cd%\%VENV_NAME%
echo 即将创建的虚拟环境路径为：%VENV_DIR%

@REM 检查虚拟环境是否已存在，如果存在则删除
if exist "%VENV_DIR%" (
    echo 虚拟环境已存在，正在删除...
    rmdir /s /q "%VENV_DIR%"
    echo 虚拟环境已删除
)

@REM 创建新的虚拟环境
echo 正在创建虚拟环境...
python -m venv "%VENV_DIR%"
echo Python虚拟环境初始化完成

@REM 激活虚拟环境
call %VENV_DIR%\Scripts\activate.bat

@REM 检查并安装依赖库
if exist %cd%\requirements.txt (
    echo 正在安装依赖库...
    pip install -r "%~dp0requirements.txt"
    echo 安装完成！
) else (
    echo 未找到requirements.txt文件，无法安装依赖库
    echo 安装失败，请将requirements.txt文件放置在当前目录下
)

echo 按任意键退出 & pause
exit