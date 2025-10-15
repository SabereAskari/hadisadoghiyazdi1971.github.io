@echo off
REM --- run_backend.bat ---
REM این فایل باید در فولدر بک‌اند قرار بگیرد

echo -----------------------------------------
echo Starting backend from: %~dp0
echo -----------------------------------------

REM فعال کردن محیط مجازی
echo Activating virtual environment...
call "G:\HadiEnv\rag_env\Scripts\activate.bat"
if errorlevel 1 (
    echo ❌ Failed to activate virtual environment.
    pause
    exit /b 1
)

echo ✓ Virtual environment activated successfully
echo.

REM رفتن به پوشه بک‌اند
echo Changing directory to backend folder...
cd /d "%~dp0"
if errorlevel 1 (
    echo ❌ Failed to change directory.
    pause
    exit /b 1
)

echo ✓ Changed to: %CD%
echo.

REM بررسی وجود app.py
if not exist "app.py" (
    echo ❌ app.py not found in current directory!
    echo Current directory: %CD%
    dir app.py
    pause
    exit /b 1
)

echo ✓ app.py found
echo.
echo -----------------------------------------
echo Running: python app.py
echo -----------------------------------------
echo.

REM اجرای برنامه
python app.py

REM نمایش وضعیت خروج
echo.
echo -----------------------------------------
echo Python exited with code: %ERRORLEVEL%
echo -----------------------------------------
pause