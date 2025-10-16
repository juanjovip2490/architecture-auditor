@echo off
chcp 65001 >nul
echo ========================================
echo  Architecture Auditor - Installation
echo ========================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://python.org
    pause
    exit /b 1
)

echo [OK] Python detected
python --version

REM Check pip
pip --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: pip is not available
    echo Installing pip...
    python -m ensurepip --upgrade
)

echo [OK] pip available

REM Install dependencies
echo.
echo Installing dependencies...
pip install -r requirements.txt

if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo [OK] Dependencies installed

REM Verify installation
echo.
echo Verifying installation...
python auditor_simple.py --help >nul 2>&1
if errorlevel 1 (
    echo ERROR: Auditor is not working properly
    pause
    exit /b 1
)

echo [OK] Auditor working

echo.
echo ========================================
echo  INSTALLATION COMPLETED
echo ========================================
echo.
echo Basic usage:
echo   python auditor_simple.py --project C:\path\to\project
echo.
echo Advanced usage:
echo   python audit_runner_simple.py C:\path\to\project
echo.
echo Examples:
echo   python audit_runner_simple.py . 
echo   python audit_runner_simple.py C:\my-project web_app
echo.
echo For more info: README.md and EXAMPLES.md
echo.
pause