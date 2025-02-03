#!/usr/bin/env python3
"""
Build script for creating the Vidleech standalone executable.
"""
import os
import shutil
import subprocess
from pathlib import Path

def clean_build():
    """Clean previous build artifacts."""
    print("Cleaning build directories...")
    dirs_to_clean = ['build', 'dist']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
    
    # Clean PyInstaller spec file
    spec_file = 'vidleech.spec'
    if os.path.exists(spec_file):
        os.remove(spec_file)

def build_executable():
    """Build the standalone executable."""
    print("Building Vidleech executable...")
    
    # PyInstaller command
    cmd = [
        'pyinstaller',
        '--name=vidleech',
        '--onefile',
        '--noconsole',
        '--clean',
        '--add-data=LICENSE;.',
        '--hidden-import=PyQt6.sip',
        'src/main.py'
    ]
    
    # Add Windows-specific options
    if os.name == 'nt':
        cmd.extend([
            '--icon=src/resources/icon.ico',
            '--version-file=version_info.txt'
        ])
    
    try:
        subprocess.run(cmd, check=True)
        print("\nBuild successful!")
        print(f"Executable created at: {os.path.abspath('dist/vidleech.exe')}")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"\nBuild failed with error: {e}")
        return False

def main():
    """Main build process."""
    # Clean previous builds
    clean_build()
    
    # Create build
    if build_executable():
        print("\nBuild completed successfully!")
    else:
        print("\nBuild failed!")
        exit(1)

if __name__ == '__main__':
    main()
