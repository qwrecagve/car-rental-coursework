@echo off
title Avtomobil Ijarasi Serveri
cd /d "%~dp0"
echo Server ishga tushmoqda...
py -m uvicorn backend.main:app --reload
pause
