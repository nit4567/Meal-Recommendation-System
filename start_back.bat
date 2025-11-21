@echo off
cd backend
echo Starting FastAPI server...
call venv\Scripts\activate
uvicorn main:app --reload --host 127.0.0.1 --port 8000
pause
