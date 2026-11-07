@echo off
REM ==============================================================================
REM Anki Vector 2.0 Workstation Agent Launcher (Windows 11 / RTX 5070 + Intel NPU)
REM ==============================================================================

cd /d "%~dp0\.."

IF EXIST ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
)

SET PYTHONPATH=%CD%;%PYTHONPATH%

echo ====================================================================
echo Starting Vector PC Workstation Agent (RTX 5070 + Intel NPU)
echo Dashboard URL: http://localhost:8080/dashboard
echo FastMCP SSE URL: http://localhost:8080/sse
echo ====================================================================

python -m pc_agent.server
pause
