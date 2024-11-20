#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "🚀 Starting setup..."

# Step 1: Check for Python3
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Please install Python3 and try again."
    exit 1
fi

# Step 2: Create a virtual environment in the .env folder
echo "📁 Creating a virtual environment in .env..."
python3 -m venv .env

# Step 3: Activate the virtual environment
echo "🔗 Activating the virtual environment..."
source .env/bin/activate

# Step 4: Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Step 5: Install dependencies
if [ -f "requirements.txt" ]; then
    echo "📦 Installing dependencies from requirements.txt..."
    pip install -r requirements.txt
else
    echo "⚠️ requirements.txt not found. Skipping dependency installation."
fi

# Step 6: Download NLTK Brown corpus
echo "📥 Downloading NLTK Brown corpus..."
python -m nltk.downloader brown

echo "✅ Setup complete! To activate your virtual environment, run 'source .env/bin/activate'."
