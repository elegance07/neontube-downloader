@echo off
title Neon-Tube Medya Konsolu
cd /d "%~dp0"
echo Gerekli kutuphaneler kontrol ediliyor (yt-dlp ve streamlit)...
py -m pip install --upgrade yt-dlp streamlit
echo.
echo Neon-Tube Medya Konsolu Baslatiliyor...
py -m streamlit run downloader.py
pause
