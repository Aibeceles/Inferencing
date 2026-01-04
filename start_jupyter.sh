#!/bin/bash
# Script to start Jupyter with CUDA environment properly configured

cd ~/inferencing/data_curate

# Activate environment with CUDA paths
source ~/inferencing/activate_cuda.sh

# Check if activation was successful
if [ $? -ne 0 ]; then
    echo "Failed to activate CUDA environment"
    exit 1
fi

# Start Jupyter
jupyter notebook --no-browser --port=8888

