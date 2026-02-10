@echo off
setlocal

echo ==========================================
echo    DocIntel Platform - Starting Services
echo ==========================================

:: Start Backend in a new window
echo [1/2] Starting Backend (FastAPI) on port 8000...
start "DocIntel Backend" cmd /k "cd backend && python main.py"

:: Start Frontend in a new window
echo [2/2] Starting Frontend (Next.js) on port 3000...
start "DocIntel Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo All services are launching!
echo ------------------------------------------
echo Backend API:  http://localhost:8000
echo Frontend Web: http://localhost:3000
echo ------------------------------------------
echo.
echo Close the individual windows to stop the services.
pause
