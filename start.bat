@echo off
REM Supabase Backend - Startup Script für Windows
REM Startet Backend und Frontend

echo.
echo ========================================
echo  Supabase Backend System - Windows
echo ========================================
echo.

REM Überprüfe Python
python --version >nul 2>&1
if errorlevel 1 (
    echo Fehler: Python ist nicht installiert
    exit /b 1
)

echo [1/4] Installiere Abhängigkeiten...
pip install -q fastapi uvicorn supabase python-dotenv pydantic

echo [2/4] Starte Backend auf Port 8000...
start "Supabase Backend" cmd /k python main.py

echo [3/4] Warte auf Backend-Start...
timeout /t 3 /nobreak

echo [4/4] Starte Frontend auf Port 5000...
cd frontend
start "Supabase Frontend" cmd /k python -m http.server 5000

echo.
echo ========================================
echo  System läuft!
echo ========================================
echo.
echo Frontend:    http://localhost:5000
echo Backend API: http://localhost:8000
echo API Docs:    http://localhost:8000/docs
echo.
echo Drücken Sie eine Taste zum Schließen...
pause
