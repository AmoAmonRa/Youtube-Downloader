@echo off
echo Installing PyInstaller...
pip install pyinstaller

echo Building executable...
pyinstaller --onefile --windowed --icon=icon128.png yt_downloader.py

echo Build complete! Check the 'dist' folder for yt_downloader.exe.
