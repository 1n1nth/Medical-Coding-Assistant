#!/usr/bin/env python3
"""
Setup script to download required data files for Medical Coding Assistant
"""

import os
import requests
import zipfile
from pathlib import Path
import sys

# Data file URLs (replace with your actual URLs)
DATA_URLS = {
    "cleaned_icd.csv": "https://drive.google.com/uc?id=YOUR_CSV_FILE_ID",
    "description_embeddings.npy": "https://drive.google.com/uc?id=YOUR_NPY_FILE_ID", 
    "icd_index.faiss": "https://drive.google.com/uc?id=YOUR_FAISS_FILE_ID"
}

# Alternative: Single zip file approach
# DATASET_ZIP_URL = "https://drive.google.com/uc?id=YOUR_ZIP_FILE_ID"

def download_file(url, destination):
    """Download a file with progress bar"""
    print(f"Downloading {destination}...")
    
    response = requests.get(url, stream=True)
    response.raise_for_status()
    
    total_size = int(response.headers.get('content-length', 0))
    downloaded = 0
    
    with open(destination, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
                downloaded += len(chunk)
                
                if total_size > 0:
                    percent = (downloaded / total_size) * 100
                    print(f"\rProgress: {percent:.1f}%", end='', flush=True)
    
    print(f"\n✓ Downloaded {destination}")

def setup_data_directory():
    """Create data directory and download required files"""
    
    # Create data directory
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    print("Setting up Medical Coding Assistant data files...")
    print("This may take a few minutes depending on your internet connection.\n")
    
    # Check if files already exist
    missing_files = []
    for filename in DATA_URLS.keys():
        filepath = data_dir / filename
        if not filepath.exists():
            missing_files.append(filename)
        else:
            print(f"✓ {filename} already exists")
    
    if not missing_files:
        print("\nAll data files are already present")
        return
    
    # Download missing files
    for filename in missing_files:
        try:
            url = DATA_URLS[filename]
            destination = data_dir / filename
            download_file(url, destination)
        except Exception as e:
            print(f"\nError downloading {filename}: {e}")
            print("Please check the URL or download manually from the README")
            sys.exit(1)
    
    print(f"\nSetup complete. Downloaded {len(missing_files)} files.")
    print("You can now run: python app.py")

def verify_installation():
    """Verify all required files are present"""
    data_dir = Path("data")
    required_files = list(DATA_URLS.keys())
    
    missing = []
    for filename in required_files:
        if not (data_dir / filename).exists():
            missing.append(filename)
    
    if missing:
        print(f"Missing files: {', '.join(missing)}")
        print("Run: python setup.py")
        return False
    
    print("All data files present")
    return True

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "verify":
        verify_installation()
    else:
        setup_data_directory()
