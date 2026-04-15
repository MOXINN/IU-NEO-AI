param(
    [switch]$db
)

$rootDir = $PSScriptRoot

Write-Host ""
Write-Host "=============================" -ForegroundColor Cyan
Write-Host " IU NWEO AI - Starting Up    " -ForegroundColor Cyan
Write-Host "=============================" -ForegroundColor Cyan
Write-Host ""

if ($db) {
    Write-Host "[1/3] Starting Docker databases..." -ForegroundColor Yellow
    docker compose -f "$rootDir\docker-compose.yml" up -d postgres neo4j chroma
    Write-Host "  Waiting 5s for databases..." -ForegroundColor DarkGray
    Start-Sleep -Seconds 5
} else {
    Write-Host "[1/3] Skipping databases (use -db flag to include)" -ForegroundColor DarkGray
}

Write-Host "[2/3] Starting Backend (FastAPI :8080)..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$rootDir\backend'; python -m uvicorn main:app --host 0.0.0.0 --port 8080 --reload"

Write-Host "[3/3] Starting Frontend (Next.js :3000)..." -ForegroundColor Blue
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
