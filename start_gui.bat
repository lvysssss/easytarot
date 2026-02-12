@echo off
chcp 65001 >nul 2>&1
setlocal EnableDelayedExpansion

REM ============================================================
REM GUI Application Launcher
REM ============================================================
set "SCRIPT_PATH=%~dp0"
set "SCRIPT_NAME=%~nx0"
set "LOG_DIR=%SCRIPT_PATH%logs"

REM Initialize log directory first
if not exist "%LOG_DIR%" (
    mkdir "%LOG_DIR%" 2>nul
    if errorlevel 1 (
        echo [ERROR] Cannot create log directory: %LOG_DIR%
    )
)

REM Generate simple timestamp for log filename using RANDOM
set "LOG_FILE=%LOG_DIR%\gui_%random%.log"

REM ============================================================
REM Main Script Logic
REM ============================================================

echo [%date% %time%] [INFO] ==========================================
echo [%date% %time%] [INFO] Launching GUI Application
echo [%date% %time%] [INFO] Script Path: %SCRIPT_PATH%
echo [%date% %time%] [INFO] Log File: %LOG_FILE%
echo [%date% %time%] [INFO] ==========================================

if not "%LOG_FILE%"=="" (
    echo [%date% %time%] [INFO] ========================================== >> "%LOG_FILE%" 2>nul
    echo [%date% %time%] [INFO] Launching GUI Application >> "%LOG_FILE%" 2>nul
    echo [%date% %time%] [INFO] Script Path: %SCRIPT_PATH% >> "%LOG_FILE%" 2>nul
    echo [%date% %time%] [INFO] Log File: %LOG_FILE% >> "%LOG_FILE%" 2>nul
    echo [%date% %time%] [INFO] ========================================== >> "%LOG_FILE%" 2>nul
)

echo [%date% %time%] [INFO] Checking Python environment...
if not "%LOG_FILE%"=="" (
    echo [%date% %time%] [INFO] Checking Python environment... >> "%LOG_FILE%" 2>nul
)

python --version >nul 2>&1
if errorlevel 1 (
    python3 --version >nul 2>&1
    if errorlevel 1 (
        echo [%date% %time%] [ERROR] Python not detected. Please install Python 3.7 or higher
        if not "%LOG_FILE%"=="" (
            echo [%date% %time%] [ERROR] Python not detected. Please install Python 3.7 or higher >> "%LOG_FILE%" 2>nul
        )
        echo.
        echo [ERROR] Python is not installed or not in PATH
        echo Please visit https://www.python.org/downloads/ to install Python
        echo.
        pause
        exit /b 1
    ) else (
        set "PYTHON_CMD=python3"
    )
) else (
    set "PYTHON_CMD=python"
)

for /f "tokens=*" %%a in ('%PYTHON_CMD% --version 2^>^&1') do set "PYTHON_VERSION=%%a"
echo [%date% %time%] [INFO] Python detected: %PYTHON_VERSION%
if not "%LOG_FILE%"=="" (
    echo [%date% %time%] [INFO] Python detected: %PYTHON_VERSION% >> "%LOG_FILE%" 2>nul
)

for /f "tokens=2 delims= " %%a in ("%PYTHON_VERSION%") do (
    for /f "tokens=1,2 delims=." %%b in ("%%a") do (
        set "PY_MAJOR=%%b"
        set "PY_MINOR=%%c"
    )
)

if %PY_MAJOR% LSS 3 (
    echo [%date% %time%] [ERROR] Python version too low. Requires 3.7 or higher
    if not "%LOG_FILE%"=="" (
        echo [%date% %time%] [ERROR] Python version too low. Requires 3.7 or higher >> "%LOG_FILE%" 2>nul
    )
    echo [ERROR] Python version too low
    pause
    exit /b 1
)
if %PY_MAJOR%==3 if %PY_MINOR% LSS 7 (
    echo [%date% %time%] [ERROR] Python version too low. Requires 3.7 or higher
    if not "%LOG_FILE%"=="" (
        echo [%date% %time%] [ERROR] Python version too low. Requires 3.7 or higher >> "%LOG_FILE%" 2>nul
    )
    echo [ERROR] Python version too low
    pause
    exit /b 1
)

set "VENV_PATH=%SCRIPT_PATH%venv"
set "VENV_SCRIPTS=%VENV_PATH%\Scripts"

if exist "%VENV_SCRIPTS%\activate.bat" (
    echo [%date% %time%] [INFO] Virtual environment detected, activating...
    if not "%LOG_FILE%"=="" (
        echo [%date% %time%] [INFO] Virtual environment detected, activating... >> "%LOG_FILE%" 2>nul
    )
    call "%VENV_SCRIPTS%\activate.bat" >nul 2>&1
    if errorlevel 1 (
        echo [%date% %time%] [WARN] Virtual environment activation failed, using system Python
        if not "%LOG_FILE%"=="" (
            echo [%date% %time%] [WARN] Virtual environment activation failed, using system Python >> "%LOG_FILE%" 2>nul
        )
    ) else (
        echo [%date% %time%] [INFO] Virtual environment activated
        if not "%LOG_FILE%"=="" (
            echo [%date% %time%] [INFO] Virtual environment activated >> "%LOG_FILE%" 2>nul
        )
        set "PYTHON_CMD=python"
    )
) else (
    echo [%date% %time%] [INFO] No virtual environment detected, using system Python
    if not "%LOG_FILE%"=="" (
        echo [%date% %time%] [INFO] No virtual environment detected, using system Python >> "%LOG_FILE%" 2>nul
    )
)

set "GUI_SCRIPT=%SCRIPT_PATH%gui.py"

if not exist "%GUI_SCRIPT%" (
    echo [%date% %time%] [ERROR] GUI main program not found: %GUI_SCRIPT%
    if not "%LOG_FILE%"=="" (
        echo [%date% %time%] [ERROR] GUI main program not found: %GUI_SCRIPT% >> "%LOG_FILE%" 2>nul
    )
    echo [ERROR] Main program file gui.py not found
    echo Please ensure the script is in the correct directory
    pause
    exit /b 1
)

echo [%date% %time%] [INFO] Main program file confirmed: %GUI_SCRIPT%
if not "%LOG_FILE%"=="" (
    echo [%date% %time%] [INFO] Main program file confirmed: %GUI_SCRIPT% >> "%LOG_FILE%" 2>nul
)

set "REQUIREMENTS=%SCRIPT_PATH%requirements.txt"
if exist "%REQUIREMENTS%" (
    echo [%date% %time%] [INFO] Checking Python dependencies...
    if not "%LOG_FILE%"=="" (
        echo [%date% %time%] [INFO] Checking Python dependencies... >> "%LOG_FILE%" 2>nul
    )
    %PYTHON_CMD% -c "import PyQt5" >nul 2>&1
    if errorlevel 1 (
        echo [%date% %time%] [WARN] Missing dependencies detected, attempting auto-install...
        if not "%LOG_FILE%"=="" (
            echo [%date% %time%] [WARN] Missing dependencies detected, attempting auto-install... >> "%LOG_FILE%" 2>nul
        )
        echo Installing dependencies, please wait...
        %PYTHON_CMD% -m pip install -r "%REQUIREMENTS%" --quiet
        if errorlevel 1 (
            echo [%date% %time%] [ERROR] Dependency installation failed
            if not "%LOG_FILE%"=="" (
                echo [%date% %time%] [ERROR] Dependency installation failed >> "%LOG_FILE%" 2>nul
            )
            echo [WARNING] Dependency installation failed, program may not run correctly
            timeout /t 3 /nobreak >nul
        ) else (
            echo [%date% %time%] [INFO] Dependencies installed
            if not "%LOG_FILE%"=="" (
                echo [%date% %time%] [INFO] Dependencies installed >> "%LOG_FILE%" 2>nul
            )
        )
    ) else (
        echo [%date% %time%] [INFO] Dependency check passed
        if not "%LOG_FILE%"=="" (
            echo [%date% %time%] [INFO] Dependency check passed >> "%LOG_FILE%" 2>nul
        )
    )
)

set "PYTHONIOENCODING=utf-8"
set "PYTHONUTF8=1"

echo [%date% %time%] [INFO] Starting GUI application...
echo [%date% %time%] [INFO] Command: %PYTHON_CMD% "%GUI_SCRIPT%"
if not "%LOG_FILE%"=="" (
    echo [%date% %time%] [INFO] Starting GUI application... >> "%LOG_FILE%" 2>nul
    echo [%date% %time%] [INFO] Command: %PYTHON_CMD% "%GUI_SCRIPT%" >> "%LOG_FILE%" 2>nul
)

echo.
echo ==========================================
echo    Starting AI Application GUI
echo    Do not close this window
echo ==========================================
echo.

%PYTHON_CMD% "%GUI_SCRIPT%" 2>&1
set "EXIT_CODE=%errorlevel%"

echo.
if %EXIT_CODE% equ 0 (
    echo [%date% %time%] [INFO] Application exited normally (Exit Code: %EXIT_CODE%)
    if not "%LOG_FILE%"=="" (
        echo [%date% %time%] [INFO] Application exited normally (Exit Code: %EXIT_CODE%) >> "%LOG_FILE%" 2>nul
    )
    echo [INFO] Application closed
) else (
    echo [%date% %time%] [ERROR] Application exited abnormally (Exit Code: %EXIT_CODE%)
    if not "%LOG_FILE%"=="" (
        echo [%date% %time%] [ERROR] Application exited abnormally (Exit Code: %EXIT_CODE%) >> "%LOG_FILE%" 2>nul
    )
    echo [ERROR] Application exited abnormally, Exit Code: %EXIT_CODE%
    echo.
    echo Press any key to view detailed logs...
    pause >nul
    if not "%LOG_FILE%"=="" (
        if exist "%LOG_FILE%" (
            type "%LOG_FILE%"
            echo.
            pause
        )
    )
)

echo [%date% %time%] [INFO] ==========================================
echo [%date% %time%] [INFO] Script execution completed
echo [%date% %time%] [INFO] ==========================================
if not "%LOG_FILE%"=="" (
    echo [%date% %time%] [INFO] ========================================== >> "%LOG_FILE%" 2>nul
    echo [%date% %time%] [INFO] Script execution completed >> "%LOG_FILE%" 2>nul
    echo [%date% %time%] [INFO] ========================================== >> "%LOG_FILE%" 2>nul
)

endlocal
timeout /t 2 /nobreak >nul
exit /b %EXIT_CODE%
