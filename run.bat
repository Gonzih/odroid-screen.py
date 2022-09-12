@echo off
rem set cwd=%cd%
set cwd=\\wsl$\Ubuntu\home\gnzh\mydev\hw-monitor
@echo %cwd%
pushd %cwd%
C:\users\gnzh\appdata\roaming\Python\Scripts\poetry.exe install
C:\users\gnzh\appdata\roaming\Python\Scripts\poetry.exe run python main.py
pause
