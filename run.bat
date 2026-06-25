@echo off
cd /d "C:\Users\batha\OneDrive\Desktop\Student ManagementSystem"

if not exist "venv\Scripts\activate.bat" (
    echo ERROR: venv not found!
    pause
    exit /b
)

call venv\Scripts\activate.bat

if not exist "app.py" (
    echo ERROR: app.py not found!
    pause
    exit /b
)

python app.py

pause