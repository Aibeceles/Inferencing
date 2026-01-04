#!/bin/bash
# One-command setup script for NeMo Curator environment

set -e  # Exit on error

echo "================================================"
echo "NeMo Curator Environment Setup"
echo "================================================"
echo ""

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Check Python version
echo "Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Found Python $PYTHON_VERSION"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
if [ -d ".venv" ]; then
    echo "⚠ Virtual environment already exists at .venv"
    read -p "Do you want to recreate it? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf .venv
        python3 -m venv .venv
        echo "✓ Virtual environment recreated"
    else
        echo "Using existing virtual environment"
    fi
else
    python3 -m venv .venv
    echo "✓ Virtual environment created"
fi
echo ""

# Activate environment
echo "Activating environment..."
source .venv/bin/activate
echo "✓ Environment activated"
echo ""

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip --quiet
echo "✓ pip upgraded"
echo ""

# Install requirements
echo "Installing requirements..."
echo "(This may take several minutes...)"
pip install -r requirements.txt
echo "✓ Requirements installed"
echo ""

# Check for language model
echo "Checking for language detection model..."
if [ ! -f "data_curate/lid.176.bin" ]; then
    echo "⚠ Language detection model not found"
    echo ""
    echo "To download it, run:"
    echo "  cd data_curate"
    echo "  wget https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin"
    echo ""
else
    echo "✓ Language detection model found"
    echo ""
fi

echo "================================================"
echo "Setup Complete!"
echo "================================================"
echo ""
echo "Next steps:"
echo "  1. Run: source activate_cuda.sh"
echo "  2. Run: ./start_jupyter.sh"
echo ""
echo "Or in one command: source activate_cuda.sh && ./start_jupyter.sh"
echo ""

