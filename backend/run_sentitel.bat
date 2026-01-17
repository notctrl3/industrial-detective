@echo off
REM ====================================================
REM  Industrial Detective - Safran Sentinel Launcher
REM  Fixes WinError 1114 (DLL init) on Windows
REM ====================================================

REM 1️⃣ 临时禁止 CUDA 初始化
set USE_CUDA=0

REM 2️⃣ 使用 Python 运行 Safran Sentinel
python safran_sentinel.py

REM 3️⃣ 提示完成
echo.
echo ✅ Safran Sentinel finished running
pause
