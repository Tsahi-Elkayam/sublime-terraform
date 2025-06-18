@echo off
REM Terraform Sublime Text Plugin - Windows Test Runner
REM Usage: test.bat [options] [test_name]

setlocal enabledelayedexpansion

echo Terraform Plugin Test Runner for Windows
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found in PATH
    echo Please install Python 3.8+ from https://python.org
    exit /b 1
)

REM Change to script directory
cd /d %~dp0

REM Check if in virtual environment
if not defined VIRTUAL_ENV (
    if exist "venv\Scripts\activate.bat" (
        echo Activating virtual environment...
        call venv\Scripts\activate.bat
    )
)

REM Run tests
echo Running tests...
echo.
python tests\run_tests.py %*

REM Capture exit code
set EXIT_CODE=%ERRORLEVEL%

REM Show summary
echo.
if %EXIT_CODE%==0 (
    echo [32m✓ All tests passed![0m
) else (
    echo [31m✗ Some tests failed![0m
)

exit /b %EXIT_CODE%