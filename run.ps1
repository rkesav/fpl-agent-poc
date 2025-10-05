$env:PYTHONUNBUFFERED="1"
$env:PYTHONPATH = (Get-Location)
if (Test-Path ".venv\Scripts\python.exe") { .\.venv\Scripts\python -m uvicorn app_agent.server:app --reload --host 0.0.0.0 --port 8000 } else { python -m uvicorn app_agent.server:app --reload --host 0.0.0.0 --port 8000 }