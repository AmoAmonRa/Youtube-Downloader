@echo off
echo Installing PyInstaller...
pip install pyinstaller

echo Building executable...
pyinstaller --onefile --windowed yt_downloader.py

echo Build complete! Check the 'dist' folder for yt_downloader.exe.
