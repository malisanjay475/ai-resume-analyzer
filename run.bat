@echo off
REM One-click start for Windows: creates a virtual environment, installs packages, starts the app.
cd /d "%~dp0backend"
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)
call venv\Scripts\activate
echo Installing packages (first run takes a few minutes)...
pip install -q -r requirements.txt
echo.
echo  AI Resume Analyzer is starting...
echo  Open http://127.0.0.1:5000 in your browser.
echo  Press Ctrl+C to stop.
echo.
python app.py
pause
