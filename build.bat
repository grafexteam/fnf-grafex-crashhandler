@echo off
title Building Grafex Crash Handler...
pyinstaller --noconsole --name="GrafexCrashHandler" --icon="./resources/icon.ico" --onefile --noupx main.py
echo Done
@echo on