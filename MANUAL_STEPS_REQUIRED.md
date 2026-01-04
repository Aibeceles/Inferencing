# Manual Steps Required

## Completed ✅

1. ✅ Renamed root directory: `lession_01_wsl` → `inferencing`
2. ✅ Created `start_jupyter.sh` (with updated paths)
3. ✅ Deleted old `start_jupyter_cuda.sh`
4. ✅ Created `.gitignore`
5. ✅ Created `requirements.txt`
6. ✅ Created `activate_cuda.sh`
7. ✅ Created `setup.sh`
8. ✅ Created `README.md`

## Manual Steps Needed

Please run the following commands in your WSL terminal:

### 1. Rename the data directory

```bash
cd /home/aibeceles/inferencing
mv lession_01 data_curate
```

### 2. Make scripts executable

```bash
cd /home/aibeceles/inferencing
chmod +x activate_cuda.sh
chmod +x setup.sh
chmod +x start_jupyter.sh
```

### 3. Initialize Git repository and push to GitHub

```bash
cd /home/aibeceles/inferencing

# Initialize Git
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Pure Ubuntu NeMo Curator implementation

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

## Verification

After completing the manual steps, verify the structure:

```bash
cd /home/aibeceles/inferencing
ls -la
```

You should see:
- ✅ `activate_cuda.sh` (executable)
- ✅ `setup.sh` (executable)
- ✅ `start_jupyter.sh` (executable)
- ✅ `data_curate/` directory (renamed from lession_01)
- ✅ `.gitignore`
- ✅ `requirements.txt`
- ✅ `README.md`

## Next Steps

Once the manual steps are complete:

1. **Test the setup:**
   ```bash
   cd /home/aibeceles/inferencing
   ./setup.sh
   source activate_cuda.sh
   ./start_jupyter.sh
   ```

2. **Verify Git push:**
   - Visit https://github.com/Aibeceles/Inferencing
   - Verify all files are present

3. **Clean up:**
   - Delete this file: `rm MANUAL_STEPS_REQUIRED.md`
   - Optionally delete: `setup-git-repository_plan.md` (or keep for reference)

