# Vidleech

A modern GUI video downloader powered by yt-dlp.

## Features

- Clean, modern GUI interface
- Support for multiple video platforms
- Progress tracking and status updates
- Error handling with user-friendly messages
- Standalone Windows executable
- No external dependencies required

## Supported Platforms

Vidleech supports downloading from various platforms including:
- YouTube
- Vimeo
- Dailymotion
- And many more (see [yt-dlp supported sites](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md))

## Development Setup

### Prerequisites

- Python 3.11 or higher
- Poetry (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/vidleech.git
cd vidleech
```

2. Install dependencies using Poetry:
```bash
poetry install
```

3. Run the application:
```bash
poetry run python src/main.py
```

### Building

To create a standalone executable:

```bash
poetry run pyinstaller src/main.py --onefile --name vidleech
```

The executable will be created in the `dist` directory.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) for the core downloading functionality
- [PyQt6](https://www.riverbankcomputing.com/software/pyqt/) for the GUI framework
