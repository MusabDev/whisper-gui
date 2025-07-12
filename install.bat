@echo off
setlocal enabledelayedexpansion

echo 🔧 Whisper Transcriber Setup for Windows

:: === 1. Check Python ===
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo 🐍 Python not found. Installing Python 3.12...

    powershell -Command "Invoke-WebRequest -Uri https://www.python.org/ftp/python/3.12.2/python-3.12.2-amd64.exe -OutFile python-installer.exe"
    python-installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
    del python-installer.exe

    where python >nul 2>nul
    if %ERRORLEVEL% NEQ 0 (
        echo ❌ Failed to install Python. Please install it manually from https://python.org
        exit /b 1
    )
) else (
    echo ✅ Python is installed.
)

:: === 2. Check pip and upgrade it ===
echo 🔄 Installing or upgrading pip...
python -m ensurepip --upgrade
python -m pip install --upgrade pip

:: === 3. Check ffmpeg ===
where ffmpeg >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo 🎥 FFmpeg not found. Downloading and installing...

    powershell -Command "Invoke-WebRequest https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip -OutFile ffmpeg.zip"
    powershell -Command "Expand-Archive ffmpeg.zip -DestinationPath . -Force"
    set "FFMPEG_DIR="
    for /d %%D in (ffmpeg-*) do (
        set "FFMPEG_DIR=%%D"
        goto :break
    )
    :break
    move "!FFMPEG_DIR!\bin\ffmpeg.exe" . >nul
    rmdir /s /q "!FFMPEG_DIR!"
    del ffmpeg.zip
    echo ✅ FFmpeg installed locally.
) else (
    echo ✅ FFmpeg is already installed.
)

:: === 4. Install Python packages ===
echo 📦 Installing Python dependencies...
python -m pip install -r requirements.txt

:: === 5. Create models folder ===
mkdir models

echo.
echo ✅ Whisper Transcriber setup is complete!
pause
