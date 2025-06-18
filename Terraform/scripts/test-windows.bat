@echo off
REM Comprehensive test runner for Windows with menu

setlocal enabledelayedexpansion

:menu
cls
echo ╔══════════════════════════════════════════════════════╗
echo ║     Terraform Sublime Text Plugin - Test Suite       ║
echo ╚══════════════════════════════════════════════════════╝
echo.
echo   1. Run all tests
echo   2. Run unit tests only
echo   3. Run integration tests
echo   4. Run performance tests
echo   5. Run with coverage report
echo   6. Run specific test file
echo   7. Setup test environment
echo   8. Clean test artifacts
echo   9. Exit
echo.
set /p choice="Select option (1-9): "

if "%choice%"=="1" goto all_tests
if "%choice%"=="2" goto unit_tests
if "%choice%"=="3" goto integration_tests
if "%choice%"=="4" goto performance_tests
if "%choice%"=="5" goto coverage
if "%choice%"=="6" goto specific_test
if "%choice%"=="7" goto setup
if "%choice%"=="8" goto clean
if "%choice%"=="9" exit /b 0

echo Invalid choice. Please try again.
pause
goto menu

:all_tests
echo.
echo Running all tests...
cd /d %~dp0\..
python tests\run_tests.py -v
pause
goto menu

:unit_tests
echo.
echo Running unit tests...
cd /d %~dp0\..
python tests\run_tests.py -v --pattern "test_(?!integration|performance)*.py"
pause
goto menu

:integration_tests
echo.
echo Running integration tests...
cd /d %~dp0\..
python tests\run_tests.py --integration -v
pause
goto menu

:performance_tests
echo.
echo Running performance tests...
cd /d %~dp0\..
python tests\run_tests.py --performance -v
pause
goto menu

:coverage
echo.
echo Running tests with coverage...
cd /d %~dp0\..\tests
coverage run -m pytest -v
coverage report
coverage html
echo.
echo Coverage report generated in htmlcov\index.html
start htmlcov\index.html
pause
goto menu

:specific_test
echo.
set /p testname="Enter test name (e.g., test_plugin): "
cd /d %~dp0\..
python tests\run_tests.py %testname% -v
pause
goto menu

:setup
echo.
echo Setting up test environment...
cd /d %~dp0\..
python tests\setup_test_env.py
pause
goto menu

:clean
echo.
echo Cleaning test artifacts...
cd /d %~dp0\..
rmdir /s /q tests\__pycache__ 2>nul
rmdir /s /q tests\htmlcov 2>nul
rmdir /s /q tests\temp 2>nul
rmdir /s /q tests\.pytest_cache 2>nul
del /q tests\.coverage 2>nul
del /q tests\*.pyc 2>nul
echo Test artifacts cleaned.
pause
goto menu