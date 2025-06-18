@echo off
REM ========================================
REM  Terraform Plugin - Quick Test Runner
REM  Just double-click this file to run tests!
REM ========================================

color 0A
title Terraform Plugin Tests

echo.
echo  =====================================
echo   Terraform Sublime Text Plugin Tests
echo  =====================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    color 0C
    echo  [ERROR] Python not found!
    echo.
    echo  Please install Python 3.8 or higher from:
    echo  https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo  Running tests...
echo  ________________
echo.

REM Run the tests
python tests\run_tests.py -v

REM Check result
if errorlevel 1 (
    color 0C
    echo.
    echo  =====================================
    echo   SOME TESTS FAILED!
    echo  =====================================
) else (
    color 0A
    echo.
    echo  =====================================
    echo   ALL TESTS PASSED!
    echo  =====================================
)

echo.
echo  Press any key to exit...
pause >nul