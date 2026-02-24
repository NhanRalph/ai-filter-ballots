@echo off
REM Build script for Windows
REM Chạy file này trên Windows để tự động build .exe

echo ========================================
echo BALLOT VERIFICATION - BUILD SCRIPT
echo ========================================
echo.

REM Activate virtual environment nếu có
if exist venv\Scripts\activate.bat (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
)

REM Check Python
python --version
if errorlevel 1 (
    echo ERROR: Python not found!
    pause
    exit /b 1
)

REM Install requirements
echo.
echo Installing requirements...
pip install -r requirements.txt
pip install pyinstaller

REM Run build script
echo.
echo Starting build process...
python build.py

echo.
echo Build complete!
pause
