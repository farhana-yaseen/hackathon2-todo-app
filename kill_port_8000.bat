@echo off
taskkill /PID 9844 /F 2>nul
taskkill /PID 9156 /F 2>nul
timeout /t 3 /nobreak >nul
netstat -ano | findstr :8000
if errorlevel 1 echo Port 8000 is now free
