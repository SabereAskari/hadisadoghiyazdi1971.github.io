@echo off
cd /d "H:\HadiSadoghiYazdi\hadisadoghiyazdi1971.github.io\hadisadoghiyazdi1971.github.io\smart-repair-api"
title Smart Repair System

echo ========================================
echo 🚀 Starting System
echo ========================================

echo Step 1: Starting Flask...
echo "Flask Server" python app.py
echo python app.py
start "Flask Server" python3.14 app.py
timeout /t 8 >nul

echo Step 2: Stopping old tunnel (if exists)...
call pm2 delete tunnel >nul 2>&1
timeout /t 2 >nul

echo Step 3: Starting new tunnel with pm2...
call pm2 start tunnel.js --name "tunnel" --restart-delay 3000
timeout /t 8 >nul

echo Step 4: Getting password...
powershell -Command "(Invoke-WebRequest -Uri 'https://loca.lt/mytunnelpassword' -UseBasicParsing).Content.Trim()" > password.txt
set /p TUNNEL_PASSWORD=<password.txt

echo.
echo ✅ SYSTEM READY!
echo 📍 Flask: http://localhost:5000
echo 🌐 Tunnel: https://hadisadoghiyazdi.loca.lt
echo 🔑 Password: %TUNNEL_PASSWORD%
echo.
echo To view tunnel logs: pm2 logs tunnel
echo To stop tunnel: pm2 stop tunnel
echo.
cd /d "H:\HadiSadoghiYazdi\hadisadoghiyazdi1971.github.io\hadisadoghiyazdi1971.github.io\smart-repair-api"
call pm2 status
timeout /t 2 >nul
echo Help 
echo Free of ports
echo pm2 stop tunnel
echo pm2 delete tunnel
echo call  https://hadisadoghiyazdi.loca.lt
@echo off
start https://hadisadoghiyazdi.loca.lt
cmd
pause