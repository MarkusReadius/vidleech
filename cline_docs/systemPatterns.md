# System Patterns: Vidleech

## Architecture Overview

Vidleech follows a simple layered architecture with clear separation of concerns:

```
┌─────────────────┐
│     GUI Layer   │ (PyQt6)
├─────────────────┤
│   Core Layer    │ (Video downloading logic)
├─────────────────┤
│ External Layer  │ (yt-dlp integration)
└─────────────────┘
```

## Key Technical Decisions

### 1. PyQt6 for GUI
- **Decision**: Use PyQt6 for the graphical user interface
- **Rationale**: Modern, well-maintained, cross-platform, and provides a native look and feel
- **Impact**: Enables a clean, responsive interface with good platform integration

### 2. yt-dlp as Download Backend
- **Decision**: Use yt-dlp instead of youtube-dl
- **Rationale**: More actively maintained, better performance, and supports more platforms
- **Impact**: More reliable downloads and broader platform support

### 3. Signal-Slot Pattern for UI Updates
- **Decision**: Use Qt's signal-slot mechanism for asynchronous UI updates
- **Rationale**: Prevents UI freezing during downloads and provides clean separation
- **Impact**: Responsive UI even during long-running operations

### 4. Single-File Executable
- **Decision**: Package as a single-file executable with PyInstaller
- **Rationale**: Simplifies distribution and installation for end users
- **Impact**: Users can run the application without installing Python or dependencies

## Code Organization

### Directory Structure
```
vidleech/
├── src/
│   ├── main.py           # Application entry point
│   ├── core/             # Core business logic
│   │   └── downloader.py # Video downloading functionality
│   ├── gui/              # User interface components
│   │   ├── main_window.py     # Main application window
│   │   └── platforms_dialog.py # Supported platforms dialog
│   ├── resources/        # Application resources
│   │   └── icon.svg      # Application icon
│   └── utils/            # Utility functions
│       └── url_utils.py  # URL validation and processing
├── tests/                # Test suite
└── build.py              # Build script for executable
```

### Design Patterns

1. **Model-View Pattern**
   - GUI components (View) are separated from download logic (Model)
   - Changes in download state are propagated to the UI via signals

2. **Factory Pattern**
   - Used in downloader.py to create appropriate download configurations based on format selection

3. **Observer Pattern**
   - Implemented via Qt's signal-slot mechanism
   - Download progress updates are observed by UI components

4. **Facade Pattern**
   - VideoDownloader class provides a simplified interface to the complex yt-dlp library
