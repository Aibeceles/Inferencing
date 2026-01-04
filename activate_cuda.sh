#!/bin/bash
# Activate the virtual environment and set CUDA library paths

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Activate the virtual environment
if [ -f "$SCRIPT_DIR/.venv/bin/activate" ]; then
    source "$SCRIPT_DIR/.venv/bin/activate"
    echo "✓ Virtual environment activated"
else
    echo "✗ Error: Virtual environment not found at $SCRIPT_DIR/.venv"
    echo "  Run './setup.sh' to create it first"
    return 1
fi

# Set CUDA library paths - add all NVIDIA library directories
NVIDIA_LIB_DIRS=$(find "$SCRIPT_DIR/.venv/lib/python3.12/site-packages/nvidia" -type d -name "lib" 2>/dev/null | tr '\n' ':')

if [ -n "$NVIDIA_LIB_DIRS" ]; then
    export LD_LIBRARY_PATH="${NVIDIA_LIB_DIRS}${LD_LIBRARY_PATH}"
    echo "✓ CUDA library paths set"
else
    echo "⚠ Warning: No NVIDIA CUDA libraries found in virtual environment"
    echo "  GPU acceleration may not be available"
fi

echo ""
echo "Environment ready! Run './start_jupyter.sh' to start Jupyter Notebook"

