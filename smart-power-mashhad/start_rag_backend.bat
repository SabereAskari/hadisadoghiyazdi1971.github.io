@echo off
title RAG Backend Launcher
echo =========================================
echo    RAG Backend Launcher
echo =========================================
echo.

REM تعریف مسیرها
set "BACKEND_DIR=H:\HadiSadoghiYazdi\hadisadoghiyazdi1971.github.io\hadisadoghiyazdi1971.github.io\smart-power-mashhad"
set "VENV_PATH=G:\HadiEnv\rag_env\Scripts\activate.bat"

REM بررسی وجود پوشه بک‌اند
if not exist "%BACKEND_DIR%" (
    echo ❌ Backend directory not found:
    echo    %BACKEND_DIR%
    pause
    exit /b 1
)

REM بررسی وجود محیط مجازی
if not exist "%VENV_PATH%" (
    echo ❌ Virtual environment not found:
    echo    %VENV_PATH%
    pause
    exit /b 1
)

echo ✓ Backend directory found
echo ✓ Virtual environment found
echo.

REM باز کردن پنجره جدید و اجرای بک‌اند
echo Starting backend in new window...
start "RAG Backend" cmd /k "cd /d "%BACKEND_DIR%" && call "%BACKEND_DIR%\run_backend.bat""

REM صبر کوتاه برای اطمینان از شروع بک‌اند
echo Waiting for backend to initialize...
timeout /t 10 /nobreak >nul

echo.
echo -----------------------------------------
echo Managing tunnel with pm2...
echo -----------------------------------------

REM حذف تونل قبلی (در صورت وجود)
call pm2 delete tunnel >nul 2>&1

REM راه‌اندازی تونل جدید
if exist "%BACKEND_DIR%\tunnel.js" (
    echo Starting tunnel...
    call pm2 start "%BACKEND_DIR%\tunnel.js" --name "tunnel" --restart-delay 3000
    if errorlevel 1 (
        echo ⚠ Warning: Failed to start tunnel with pm2
    ) else (
        echo ✓ Tunnel started successfully
    )
) else (
    echo ⚠ Warning: tunnel.js not found, skipping...
)

echo.
echo =========================================
echo    Backend launcher completed
echo =========================================
echo.
echo Check the "RAG Backend" window for application logs.
echo.
echo   don't use VPN
echo   get password
start "" "https://loca.lt/mytunnelpassword"
echo run tunnel 
start "" "https://PowerGrid.loca.lt/"
pause

