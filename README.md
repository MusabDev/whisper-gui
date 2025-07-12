# Whisper Transcriber GUI

A sleek Python desktop application built with `customtkinter` that leverages OpenAI's [Whisper](https://github.com/openai/whisper) model for accurate speech-to-text transcription of audio and video files.

## Features
- 🎛 User-friendly GUI using `customtkinter`
- 🎚 Choose from all Whisper models (tiny → large)
- 📂 Load audio/video files (MP3, MP4, WAV, etc.)
- 📋 Copy and 💾 Save transcription with a click
- 🌐 Multilingual transcription support

## Tech Stack
- Python 3.10+
- customtkinter
- OpenAI Whisper
- ffmpeg (for media decoding)

## Installation

Run the provided installation script **once** to set up Python, dependencies, and required programs:

### On macOS / Linux
```bash
./install.sh
```

On Windows (PowerShell or CMD)
```bash
install.bat
```

This script will install Python, pip, and all required Python packages from requirements.txt.

## Running the Application
After installation, start the application using the run script:

On macOS / Linux
```bash
./run.sh
```

On Windows (PowerShell or CMD)
```bash
run.bat
```
This will launch the Whisper Transcriber GUI.

## 🧠 Model Info
Whisper models supported:
- `tiny` (39 MB)
- `base` (74 MB)
- `small` (244 MB)
- `medium` (769 MB)
- `large` (1550 MB)
- `large-v2` (1550 MB)
- `large-v3` (1550 MB)
- `turbo` (809 MB)

---

Contributions welcome! ⭐
