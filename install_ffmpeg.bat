@echo off
title Installing FFmpeg...

:: Check if FFmpeg is already installed
where ffmpeg >nul 2>&1
if %errorlevel%==0 (
    echo FFmpeg is already installed.
    goto :eof
)

echo FFmpeg not found. Installing...

:: Download FFmpeg static build
curl -L https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip -o ffmpeg.zip

:: Extract using PowerShell
powershell -Command "Expand-Archive -Path ffmpeg.zip -DestinationPath ."

:: Find the extracted folder (assuming it starts with ffmpeg)
for /d %%i in (ffmpeg*) do set FOLDER=%%i

:: Move to ffmpeg folder
if defined FOLDER (
    if exist ffmpeg\ (
        rmdir /s /q ffmpeg
    )
    rename %FOLDER% ffmpeg
)

:: Add to user PATH
setx PATH "%PATH%;%cd%\ffmpeg\bin"

:: Clean up
del ffmpeg.zip

echo FFmpeg installed successfully. Please restart your command prompt for PATH changes to take effect.
pause
