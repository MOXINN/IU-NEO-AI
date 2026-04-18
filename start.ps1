$rootDir = $PSScriptRoot

Write-Host ""
Write-Host "=============================" -ForegroundColor Cyan
Write-Host " IU NWEO AI - Starting Up    " -ForegroundColor Cyan
Write-Host "=============================" -ForegroundColor Cyan
Write-Host ""

Write-Host "[1/2] Starting Backend (FastAPI :8080)..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$rootDir\backend'; python run.py"

Write-Host "[2/2] Starting Frontend (Next.js :3000)..." -ForegroundColor Blue
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$rootDir\frontend'; npm run dev"

Write-Host ""
Write-Host "=============================" -ForegroundColor Cyan
Write-Host " All services launched!       " -ForegroundColor Cyan
Write-Host "=============================" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Backend:  http://localhost:8080" -ForegroundColor Green
Write-Host "  Frontend: http://localhost:3000" -ForegroundColor Blue
Write-Host "  API Docs: http://localhost:8080/docs" -ForegroundColor DarkGray
Write-Host ""
Write-Host "  Close the spawned windows to stop." -ForegroundColor DarkGray
