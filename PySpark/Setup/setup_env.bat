@echo off
echo ==========================================================
echo  Setting up Milestone 2 PySpark Environment (Windows CMD)
echo ==========================================================

:: Change directory to Milestone 2\PySpark Setup
cd /d "%~dp0PySpark Setup"

:: Create virtual environment if it doesn't exist
if not exist ".venv\Scripts\python.exe" (
    echo Creating virtual environment at .venv...
    python -m venv .venv
)

:: Install requirements
echo Installing PySpark and dependencies...
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

:: Download Hadoop WinUtils and MySQL connector
echo Downloading Hadoop WinUtils and JARs...
python download_assets.py

echo.
echo ==========================================================
echo  Setup Complete!
echo  To run tests, open VS Code and click 'Run Python File'
echo  on 'Milestone 2\PySpark Practice\solution.py'
echo ==========================================================
pause
