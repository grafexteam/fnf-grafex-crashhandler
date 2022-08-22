@echo off
title Building Grafex Crash Handler...
echo Installing requirements...
python -m pip install --upgrade pip && pip install -r requirements.txt
echo Building code to .exe file
pyinstaller --noconsole --name="GrafexCrashHandler" --icon="./resources/icon.ico" --onefile --noupx main.py
echo Done
pause
@echo on