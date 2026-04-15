@echo off
REM ============================================================================
REM IU NWEO AI — Start All Services (double-click friendly)
REM ============================================================================

echo.
echo =============================
echo  IU NWEO AI — Starting Up...
echo =============================
echo.

echo [1/2] Starting Backend (FastAPI on :8080)...
start "IU-Backend" cmd /k "cd /d %~dp0backend && python -m uvicorn main:app --host 0.0.0.0 --port 8080 --reload"

echo [2/2] Starting Frontend (Next.js on :3000)...
start "IU-Frontend" cmd /k "cd /d %~dp0frontend && npm run dev"

echo.
echo =============================
echo  All services launched!
echo =============================
echo.
echo   Backend:  http://localhost:8080
echo   Frontend: http://localhost:3000
echo   API Docs: http://localhost:8080/docs
echo.
echo Close the spawned windows to stop services.
pause
