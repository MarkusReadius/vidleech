# Technical Context: Vidleech

## Technologies Used

### Core Technologies
- **Python 3.11+**: Main programming language
- **PyQt6 (6.6.1+)**: GUI framework for the application interface
- **yt-dlp (2025.01.26+)**: Backend for video downloading functionality
- **Poetry**: Dependency management and packaging

### Development Tools
- **Black**: Code formatting
- **isort**: Import sorting
- **flake8**: Linting
- **pytest**: Testing framework
- **PyInstaller**: Used to create standalone executable

## Development Setup

### Local Development Environment
1. Python 3.11+ installed
2. Poetry installed for dependency management
3. Git for version control
4. IDE with Python support (e.g., VSCode)

### Building from Source
```bash
# Clone repository
git clone https://github.com/maread2/vidleech.git
cd vidleech

# Install dependencies with Poetry
poetry install

# Run the application
poetry run python src/main.py
```

### Building Executable
```bash
# Using Poetry and PyInstaller
poetry run pyinstaller src/main.py --name=vidleech --onefile --noconsole
```

## Technical Constraints

### Dependencies
- Requires PyQt6 for GUI rendering
- Relies on yt-dlp for video downloading functionality
- Needs ffmpeg for media processing (bundled with executable)

### Platform Support
- Primary focus on Windows support
- Can run on macOS and Linux from source

### Performance Considerations
- Download speed limited by network and platform restrictions
- GUI responsiveness maintained during downloads via threading

### Security Considerations
- No authentication or API keys required
- Downloads performed directly without proxies
- User data not stored or transmitted
