$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

.\ml-service\.venv\Scripts\python.exe scripts\prepare_data.py
.\ml-service\.venv\Scripts\python.exe scripts\train_baseline.py
.\ml-service\.venv\Scripts\python.exe -m uvicorn app.main:app --app-dir ml-service --reload --port 8000

