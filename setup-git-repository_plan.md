# Setup Git Repository Plan

## Overview

This plan outlines the steps to prepare the NeMo Curator project for Git version control and push it to GitHub at https://github.com/Aibeceles/Inferencing.git

The project will be renamed to match the GitHub repository name, transforming the local working directory from `lession_01_wsl` to `inferencing`.

## Evolution: Windows → WSL → Pure Ubuntu

### Project History

This project evolved through three phases:

1. **Windows Phase**: Initially developed on Windows
   - Evidence: Checkpoint notebooks show Windows-specific errors (`'lscpu' is not recognized...`)
   - Used Windows Python environment

2. **WSL Phase**: Migrated to Windows Subsystem for Linux (WSL2)
   - Directory name `lession_01_wsl` indicates this transition
   - Hybrid environment with access to both Windows and Linux
   - CUDA support through WSL2's GPU passthrough

3. **Pure Ubuntu Phase** (Current): Now a fully native Linux environment
   - Running on Ubuntu via WSL2 kernel (`linux 6.6.87.2-microsoft-standard-WSL2`)
   - Uses native Linux paths and conventions
   - Shell scripts written for bash (`/bin/bash`)
   - Virtual environments use Linux Python binaries
   - All dependencies installed via pip for Linux
   - No Windows-specific code or dependencies

### Why This Is "Pure Ubuntu"

Despite running on WSL2, this setup is **functionally pure Ubuntu**:

- ✅ **Native Linux kernel**: Uses Linux system calls, file permissions, and process management
- ✅ **Ubuntu package ecosystem**: Can use apt, snap, and other Ubuntu tools
- ✅ **POSIX-compliant**: All scripts use bash/sh with standard Unix commands
- ✅ **Linux file paths**: Uses `/home/aibeceles/` not Windows paths
- ✅ **ELF binaries**: Python and all extensions are compiled for Linux
- ✅ **No Windows dependencies**: Doesn't rely on Windows Python, PowerShell, or Windows-specific tools
- ✅ **Portable to native Ubuntu**: Can be copied to a native Ubuntu machine and work identically

**The WSL2 difference**: WSL2 provides a real Linux kernel, making it indistinguishable from native Ubuntu for most development purposes. The Microsoft kernel is just a repackaged Linux kernel.

### Repository Naming

Renaming `lession_01_wsl` → `inferencing`:
- Removes the "wsl" reference (no longer relevant to users)
- Matches GitHub repository name
- Describes what the project does (data curation for inferencing/LLMs)
- Makes the project platform-agnostic (works on any Ubuntu/Linux system)

## Changes Summary

### Complete Transformation

**Before:**
```
/home/aibeceles/lession_01_wsl/     # WSL-specific naming
├── start_jupyter_cuda.sh           # CUDA-explicit naming
├── nemo_env_clean/                 # Large env not portable
└── lession_01/                     # Generic "lesson" naming
    ├── notebooks...
    └── data...
```

**After:**
```
/home/aibeceles/inferencing/        # Clean, descriptive name
├── start_jupyter.sh                # Simple, clean naming
├── .venv/                          # Standard Python convention
├── requirements.txt                # Reproducible dependencies
├── activate_cuda.sh                # Modular CUDA activation
├── setup.sh                        # One-command setup
├── README.md                       # Complete documentation
└── data_curate/                    # Descriptive purpose
    ├── notebooks...
    └── data...
```

### Renaming Operations
1. **`lession_01_wsl/` → `inferencing/`** - Root directory matches GitHub repo
2. **`start_jupyter_cuda.sh` → `start_jupyter.sh`** - Cleaner naming (CUDA still supported)
3. **`lession_01/` → `data_curate/`** - Descriptive of actual purpose
4. All path references updated to use `inferencing` root

---

## Quick Reference: Execution Steps

```bash
# 1. Rename root directory
mv /home/aibeceles/lession_01_wsl /home/aibeceles/inferencing
cd /home/aibeceles/inferencing

# 2. Rename files and directories
mv start_jupyter_cuda.sh start_jupyter.sh
mv lession_01 data_curate

# 3. Create configuration files
# (Create .gitignore, requirements.txt, README.md, activate_cuda.sh, setup.sh)

# 4. Make scripts executable
chmod +x activate_cuda.sh start_jupyter.sh setup.sh

# 5. Initialize Git and push
git init
git add .
git commit -m "Initial commit: Pure Ubuntu NeMo Curator implementation"
git remote add origin https://github.com/Aibeceles/Inferencing.git
git branch -M main
git push -u origin main
```

---

## Files to Create

### 1. `.gitignore`

**Purpose:** Exclude large files, virtual environments, and generated files from Git

**Location:** `/home/aibeceles/inferencing/.gitignore`

```gitignore
# Virtual Environment
.venv/
venv/
env/
nemo_env/
nemo_env_clean/

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python

# Jupyter
.ipynb_checkpoints/
*.ipynb_checkpoints

# Large model files
*.bin

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Optional: Uncomment to exclude data directories
# data_curate/original_data/
# data_curate/curated/
```

---

### 2. `requirements.txt`

**Purpose:** List all Python dependencies for reproducible environment

**Location:** `/home/aibeceles/inferencing/requirements.txt`

```
# Core NeMo Curator
nemo-curator>=0.9.0

# PII Detection
presidio-analyzer

# Jupyter Environment
jupyter>=1.0.0
jupyterlab>=4.0.0
notebook>=7.0.0
ipykernel>=6.0.0

# Data Processing
dask[complete]>=2024.1.0
numpy>=1.24.0
pandas>=2.0.0

# ML Dependencies
transformers>=4.30.0
torch>=2.0.0

# Language Detection (fasttext model downloaded separately)
# Model: https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin

# Optional: Uncomment for specific versions
# dask-cuda>=25.4.0
# cudf>=25.4.0
# rapids>=25.4.0
```

---

### 3. `activate_cuda.sh`

**Purpose:** Activate virtual environment and set CUDA library paths

**Location:** `/home/aibeceles/inferencing/activate_cuda.sh`

```bash
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
```

---

### 4. `start_jupyter.sh` (Updated)

**Purpose:** Start Jupyter Notebook with CUDA environment

**Location:** `/home/aibeceles/inferencing/start_jupyter.sh` (renamed from start_jupyter_cuda.sh)

```bash
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
```

---

### 5. `setup.sh`

**Purpose:** One-command setup script for new users

**Location:** `/home/aibeceles/inferencing/setup.sh`

```bash
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
```

---

### 6. `README.md`

**Purpose:** Project documentation and setup instructions

**Location:** `/home/aibeceles/inferencing/README.md`

```markdown
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

This project is implemented as a **pure Ubuntu/Linux environment**:

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

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

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
```

---

## Operations to Perform

### Step 0: Rename Root Directory

```bash
# Rename the project root directory to match GitHub repository name
mv /home/aibeceles/lession_01_wsl /home/aibeceles/inferencing
cd /home/aibeceles/inferencing
```

**Why**: This aligns the local directory name with the GitHub repository name and removes the "wsl" reference, making it clear this is a pure Ubuntu/Linux project.

### Step 1: Rename Files and Directories

```bash
# Rename script
mv start_jupyter_cuda.sh start_jupyter.sh

# Rename data directory
mv lession_01 data_curate
```

### Step 2: Create New Files

1. Create `.gitignore`
2. Create `requirements.txt`
3. Create `activate_cuda.sh` (make executable)
4. Update `start_jupyter.sh` with new paths (make executable)
5. Create `setup.sh` (make executable)
6. Create `README.md`

### Step 3: Make Scripts Executable

```bash
cd /home/aibeceles/inferencing
chmod +x activate_cuda.sh
chmod +x start_jupyter.sh
chmod +x setup.sh
```

### Step 4: Initialize Git Repository

```bash
cd /home/aibeceles/inferencing

# Initialize Git
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: NeMo Curator data processing notebooks

- Added basic and advanced data curation notebooks
- Created environment setup scripts (activate_cuda.sh, setup.sh)
- Added comprehensive README with setup instructions
- Configured .gitignore for Python/Jupyter projects
- Pure Ubuntu/Linux implementation (portable across Linux systems)"

# Add remote repository
git remote add origin https://github.com/Aibeceles/Inferencing.git

# Rename branch to main
git branch -M main

# Push to GitHub
git push -u origin main
```

---

## Final Repository Structure

```
inferencing/                   # ✓ Renamed from lession_01_wsl
├── .git/                      # Git repository data
├── .venv/                     # Virtual environment (not in Git)
├── .gitignore                 # ✓ Created
├── requirements.txt           # ✓ Created
├── README.md                  # ✓ Created
├── setup.sh                   # ✓ Created (executable)
├── activate_cuda.sh           # ✓ Created (executable)
├── start_jupyter.sh           # ✓ Renamed & updated (executable)
├── languages-config.yaml      # Existing file
├── nemo_env_clean/            # Not tracked (in .gitignore)
└── data_curate/               # ✓ Renamed from lession_01
    ├── 01_basics_curation (2).ipynb
    ├── 02_advanced_data_processing (1).ipynb
    ├── languages-config.yaml
    ├── languages-config.yml
    ├── original_data/         # Optional (can exclude in .gitignore)
    └── curated/               # Optional (can exclude in .gitignore)
```

### Local Path Structure

```
/home/aibeceles/
└── inferencing/               # Project root (was lession_01_wsl)
    └── data_curate/           # Working directory (was lession_01)
```

This structure is **pure Ubuntu/Linux** - it will work identically on:
- WSL2 (current environment)
- Native Ubuntu installation
- Ubuntu Docker container
- Any Debian-based Linux distribution

---

## Verification Checklist

After completing all steps, verify:

- [ ] **Root directory renamed**: `lession_01_wsl/` → `inferencing/`
- [ ] **Script renamed**: `start_jupyter_cuda.sh` → `start_jupyter.sh`
- [ ] **Data directory renamed**: `lession_01/` → `data_curate/`
- [ ] All new files created (`.gitignore`, `requirements.txt`, `README.md`, etc.)
- [ ] Scripts are executable (`chmod +x`)
- [ ] All path references updated to use `inferencing` root
- [ ] Git repository initialized
- [ ] Remote repository added
- [ ] Files committed to Git
- [ ] Successfully pushed to GitHub

## Test the Setup

To verify everything works for new users:

```bash
# In a new directory, clone and test
cd /tmp
git clone https://github.com/Aibeceles/Inferencing.git
cd Inferencing
./setup.sh
source activate_cuda.sh
./start_jupyter.sh
```

---

## Notes

- **Virtual environments** (`.venv/`, `nemo_env/`, `nemo_env_clean/`) are excluded from Git
- **Large model files** (`lid.176.bin`) are excluded; users download them separately
- **Data directories** can be optionally excluded by uncommenting lines in `.gitignore`
- **Root directory renamed**: Local directory now matches GitHub repository name (`inferencing`)
- **Pure Ubuntu environment**: Despite running on WSL2, this is functionally identical to native Ubuntu
  - Uses Linux kernel, file system, and conventions
  - No Windows dependencies
  - Fully portable to any Linux system
- **Platform independence**: The code can run on:
  - WSL2 (current)
  - Native Ubuntu/Debian
  - Docker containers
  - Cloud Linux VMs
  - Any CUDA-capable Linux system

---

## Summary: Pure Ubuntu Implementation

### What Makes This "Pure Ubuntu"?

Despite its journey through Windows → WSL → Current state, this is now a **pure Ubuntu/Linux implementation**:

| Aspect | Pure Ubuntu ✓ | Why |
|--------|---------------|-----|
| **Kernel** | Linux 6.6.87.2 | Real Linux kernel, not emulated |
| **File System** | ext4 via WSL2 | Native Linux filesystem |
| **Binaries** | ELF format | All executables compiled for Linux |
| **Shell** | bash (/bin/bash) | POSIX-compliant scripting |
| **Python** | Linux CPython | Native Linux Python interpreter |
| **Paths** | /home/aibeceles/ | Unix-style paths, not Windows |
| **Dependencies** | pip/apt packages | Linux package ecosystem |
| **Permissions** | Unix permissions | chmod, user/group/other |
| **Processes** | Linux processes | Native Linux process management |

### Portability

This exact repository can be cloned and run on:

1. **Native Ubuntu** desktop or server
2. **Debian** or other Debian-based distros
3. **Docker** containers based on Ubuntu
4. **Cloud VMs** (AWS EC2, GCP Compute, Azure VM)
5. **HPC clusters** running Linux
6. **WSL2** (current environment)

**No modifications needed** - it's pure Linux code.

### The WSL2 Advantage

WSL2 provides the best of both worlds:
- Full Linux kernel and environment (pure Ubuntu)
- Access to Windows tools and file systems when needed
- Native GPU passthrough for CUDA
- Seamless integration with Windows development tools

But the **code itself is 100% Linux** - WSL2 is just where it happens to be running right now.

---

## Next Steps After Git Push

1. Add a `LICENSE` file to the repository
2. Consider adding GitHub Actions for CI/CD
3. Add badges to README (build status, license, etc.)
4. Create release tags for versions
5. Add CONTRIBUTING.md for contributors
6. Consider adding example data samples
7. Test cloning and setup on a native Ubuntu machine to verify portability

