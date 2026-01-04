# NeMo Curator Data Processing

NVIDIA NeMo Curator notebooks for data curation and preprocessing for Large Language Models (LLMs).

## Overview

This project contains Jupyter notebooks demonstrating the use of NVIDIA NeMo Curator for preparing high-quality datasets for LLM training. NeMo Curator provides both GPU and CPU-based modules for efficient large-scale data processing.

## Features

### Notebook 01: Basics of Data Curation
- Text cleaning and unification
- Document size filtering
- Personally Identifiable Information (PII) detection and filtering

### Notebook 02: Advanced Data Processing
- Language detection and separation
- Domain/topic classification
- Document deduplication (exact and fuzzy matching)

## Requirements

### System Requirements
- **Python**: 3.12+
- **GPU**: CUDA-capable GPU (recommended for GPU-accelerated processing)
- **CUDA Toolkit**: CUDA 12.x installed on system
- **OS**: Linux (Ubuntu/Debian-based distributions)
  - ✅ Native Ubuntu/Debian
  - ✅ WSL2 (Windows Subsystem for Linux)
  - ✅ Docker containers
  - ✅ Cloud VMs (AWS, GCP, Azure)

### Pure Ubuntu Implementation

This project is implemented as a Ubuntu/Linux environment:

- **No Windows dependencies**: All code runs natively on Linux
- **POSIX-compliant scripts**: Uses standard bash/sh scripts
- **Linux Python environment**: All packages compiled for Linux
- **Portable**: Copy to any Linux system and it works identically

**Note**: While this was developed in WSL2, WSL2 uses a real Linux kernel (Microsoft's custom build of the Linux kernel), making it functionally identical to native Ubuntu for development purposes.

### Python Dependencies
All dependencies are listed in `requirements.txt`. Key packages:
- `nemo-curator` - Main data curation framework
- `dask` - Distributed computing
- `rapids` - GPU-accelerated data processing (optional)
- `presidio-analyzer` - PII detection

## Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/Aibeceles/Inferencing.git
cd Inferencing
```

### 2. Setup Environment

**Option A: Quick setup (recommended)**
```bash
chmod +x setup.sh
./setup.sh
```

**Option B: Manual setup**
```bash
# Create virtual environment
python3 -m venv .venv

# Activate environment
source .venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Download Language Detection Model (Optional)
```bash
cd data_curate
wget https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin
cd ..
```

### 4. Start Jupyter Notebook
```bash
# Activate CUDA environment
source activate_cuda.sh

# Start Jupyter
./start_jupyter.sh
```

Open your browser and navigate to the URL shown (typically http://localhost:8888)

## Usage

### Running Notebooks

1. **Basic Data Curation**: Open `data_curate/01_basics_curation (2).ipynb`
   - Follow cells sequentially to learn text cleaning, filtering, and PII detection

2. **Advanced Processing**: Open `data_curate/02_advanced_data_processing (1).ipynb`
   - Explore language separation, classification, and deduplication techniques

### Configuration

Edit `data_curate/languages-config.yaml` to customize:
- Language detection settings
- Filtering thresholds
- Domain classification parameters

## Project Structure

```
Inferencing/
├── .venv/                      # Virtual environment (not in Git)
├── .gitignore                  # Git ignore rules
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── setup.sh                    # Automated setup script
├── activate_cuda.sh            # CUDA environment activation
├── start_jupyter.sh            # Start Jupyter with CUDA
├── languages-config.yaml       # Language configuration (optional)
└── data_curate/               # Main working directory
    ├── 01_basics_curation (2).ipynb
    ├── 02_advanced_data_processing (1).ipynb
    ├── languages-config.yaml
    ├── languages-config.yml
    ├── original_data/          # Source data
    └── curated/                # Processed output data
```

## CPU vs GPU Processing

NeMo Curator supports both CPU and GPU-based processing:

- **CPU modules**: Use [Dask](https://www.dask.org/) for distributed computing across multi-node clusters
- **GPU modules**: Use [RAPIDS](https://rapids.ai/) for GPU-accelerated processing

The notebooks automatically detect available hardware and adjust accordingly.

## Troubleshooting

### CUDA Library Issues
If you encounter CUDA library errors:
```bash
# Check NVIDIA libraries are installed
find .venv -name "libnv*.so" | head -5

# Re-run activation script
source activate_cuda.sh
```

### Virtual Environment Issues
```bash
# Remove and recreate environment
rm -rf .venv
./setup.sh
```

### Jupyter Kernel Issues
```bash
# Install kernel manually
source .venv/bin/activate
python -m ipykernel install --user --name=nemo-curator
```

## Data Sources

The notebooks work with various data sources:
- Custom text datasets (JSON, JSONL, Parquet)
- Common Crawl
- Wikipedia dumps
- arXiv papers

## Performance Tips

1. **For large datasets**: Use GPU-accelerated modules with RAPIDS
2. **For distributed processing**: Configure Dask cluster
3. **Memory management**: Process data in chunks using Dask partitions

## Resources

- [NeMo Curator Documentation](https://docs.nvidia.com/nemo-framework/user-guide/latest/datacuration/index.html)
- [NVIDIA NeMo Framework](https://www.nvidia.com/en-us/ai-data-science/products/nemo/)
- [Dask Documentation](https://docs.dask.org/)
- [RAPIDS Documentation](https://docs.rapids.ai/)

## License

See LICENSE file for details.

## Acknowledgments

- NVIDIA for NeMo Curator framework
- Dask and RAPIDS communities
- Contributors and users of this project

