#!/usr/bin/env bash
# One-click start for Mac / Linux: creates a virtual environment, installs packages, starts the app.
set -e
cd "$(dirname "$0")/backend"
if [ ! -d venv ]; then
  echo "Creating virtual environment..."
  python3 -m venv venv
fi
source venv/bin/activate
echo "Installing packages (first run takes a few minutes)..."
pip install -q -r requirements.txt
echo
echo " AI Resume Analyzer is starting..."
echo " Open http://127.0.0.1:5000 in your browser."
echo " Press Ctrl+C to stop."
echo
python app.py
