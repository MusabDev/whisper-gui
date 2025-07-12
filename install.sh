#!/bin/bash

echo "🔧 Setting up Whisper Transcriber..."

# Detect OS
OS="$(uname)"
PY_CMD="python3"
PIP_CMD="pip3"

# Install Python & pip if needed
if ! command -v $PY_CMD &> /dev/null; then
    echo "❌ Python not found. Installing..."
    if [[ "$OS" == "Darwin" ]]; then
        # macOS
        if ! command -v brew &> /dev/null; then
            echo "❌ Homebrew not installed. Please install it from https://brew.sh"
            exit 1
        fi
        brew install python
    elif [[ "$OS" == "Linux" ]]; then
        sudo apt update
        sudo apt install -y python3 python3-pip
    fi
fi

# Install ffmpeg (required for whisper)
if ! command -v ffmpeg &> /dev/null; then
    echo "📦 Installing ffmpeg..."
    if [[ "$OS" == "Darwin" ]]; then
        brew install ffmpeg
    elif [[ "$OS" == "Linux" ]]; then
        sudo apt install -y ffmpeg
    fi
fi

# Upgrade pip and install dependencies
$PIP_CMD install --upgrade pip
$PIP_CMD install -r requirements.txt

mkdir -p models

echo "✅ Setup complete!"
