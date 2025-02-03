"""
Main window implementation for the Vidleech application.
"""
from pathlib import Path
from PyQt6.QtCore import Qt, QSize, QThread, pyqtSignal
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QProgressBar,
    QLabel,
    QStatusBar,
    QComboBox,
    QFileDialog,
    QSizePolicy,
    QMenuBar,
    QMenu,
)

from gui.platforms_dialog import PlatformsDialog

from core.downloader import VideoDownloader, VideoFormat, DownloadProgress
from utils.url_utils import is_valid_url, get_platform, get_supported_platforms

class DownloadWorker(QThread):
    """Worker thread for handling downloads."""
    
    progress = pyqtSignal(DownloadProgress)
    finished = pyqtSignal(bool)
    
    def __init__(self, url: str, format: VideoFormat, download_path: Path):
        super().__init__()
        self.url = url
        self.format = format
        self.download_path = download_path
        
    def run(self):
        """Run the download operation."""
        downloader = VideoDownloader(
            progress_callback=self.progress.emit,
            download_path=self.download_path
        )
        downloader.set_format(self.format)
        success = downloader.download(self.url)
        self.finished.emit(success)

class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Vidleech")
        self.setMinimumSize(QSize(800, 500))
        self.resize(900, 600)
        
        # Create menu bar
        menu_bar = QMenuBar()
        self.setMenuBar(menu_bar)
        
        # Help menu
        help_menu = QMenu("Help", self)
        menu_bar.addMenu(help_menu)
        
        # Supported platforms action
        platforms_action = help_menu.addAction("Supported Platforms")
        platforms_action.triggered.connect(self.show_platforms)
        
        # Set application style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
                background-color: white;
                color: black;
            }
            QPushButton {
                padding: 8px 16px;
                background-color: #007bff;
                color: white !important;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:disabled {
                background-color: #ccc;
            }
            QComboBox {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
                background-color: white;
                min-width: 150px;
                color: black;
            }
            QComboBox:hover {
                border-color: #999;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                color: black;
                selection-background-color: #007bff;
                selection-color: white;
                border: none;
                margin: 0;
                padding: 0;
            }
            QProgressBar {
                border: 1px solid #ccc;
                border-radius: 4px;
                text-align: center;
                height: 20px;
                color: black;
            }
            QProgressBar::chunk {
                background-color: #007bff;
            }
            QLabel {
                color: black;
            }
            QLineEdit::placeholder {
                color: #999;
            }
            QStatusBar {
                color: black;
            }
            QWidget[accessibleName="group"] {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 8px;
            }
        """)
        
        # Create central widget and main layout
        central_widget = QWidget()
        central_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Title section
        title_label = QLabel("Vidleech")
        title_label.setFont(QFont(title_label.font().family(), 24, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #007bff; margin-bottom: 20px;")
        layout.addWidget(title_label)
        
        # URL input section
        url_layout = QHBoxLayout()
        url_layout.setSpacing(10)
        
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter video URL...")
        self.url_input.setFixedHeight(36)
        url_layout.addWidget(self.url_input)
        
        self.download_button = QPushButton("Download")
        self.download_button.setFixedSize(120, 36)
        self.download_button.clicked.connect(self.start_download)
        url_layout.addWidget(self.download_button)
        
        layout.addLayout(url_layout)
        
        # Options section
        options_group = QWidget()
        options_group.setAccessibleName("group")
        options_group.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        options_layout = QVBoxLayout(options_group)
        options_layout.setContentsMargins(20, 20, 20, 20)
        options_layout.setSpacing(15)
        
        # Format selection
        format_layout = QHBoxLayout()
        format_label = QLabel("Format:")
        format_layout.addWidget(format_label)
        
        self.format_combo = QComboBox()
        self.format_combo.addItems(["Best Quality", "720p", "480p", "Audio Only"])
        self.format_combo.setFixedHeight(36)
        format_layout.addWidget(self.format_combo)
        format_layout.addStretch()
        
        # Path selection
        path_layout = QHBoxLayout()
        path_label = QLabel("Save to:")
        path_layout.addWidget(path_label)
        
        self.path_input = QLineEdit(str(Path.home() / "Downloads"))
        self.path_input.setMinimumWidth(300)
        self.path_input.setFixedHeight(36)
        path_layout.addWidget(self.path_input, stretch=1)
        
        self.browse_button = QPushButton("Browse")
        self.browse_button.setFixedHeight(36)
        self.browse_button.clicked.connect(self.browse_path)
        path_layout.addWidget(self.browse_button)
        
        # Add layouts to options group
        options_layout.addLayout(format_layout)
        options_layout.addLayout(path_layout)
        
        # Add options group to main layout
        layout.addWidget(options_group)
        
        # Progress section (initially hidden)
        self.progress_group = QWidget()
        self.progress_group.setAccessibleName("group")
        self.progress_group.setFixedHeight(120)
        self.progress_group.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        progress_layout = QVBoxLayout(self.progress_group)
        progress_layout.setContentsMargins(20, 20, 20, 20)
        progress_layout.setSpacing(10)
        
        self.progress_label = QLabel("Ready")
        self.progress_label.setFixedHeight(24)
        progress_layout.addWidget(self.progress_label)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.progress_bar.setFixedHeight(24)
        progress_layout.addWidget(self.progress_bar)
        
        # Add progress group to main layout (initially hidden)
        layout.addWidget(self.progress_group)
        self.progress_group.hide()
        
        # Add spacer to maintain layout when progress is hidden
        self.progress_spacer = QWidget()
        self.progress_spacer.setFixedHeight(120)
        self.progress_spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        layout.addWidget(self.progress_spacer)
        
        # Add stretching space
        layout.addStretch()
        
        # Status bar
        self.status_bar = QStatusBar()
        self.status_bar.setStyleSheet("color: black;")
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready to download")
        
        # Initialize download state
        self.reset_progress()
    
    def show_platforms(self):
        """Show the supported platforms dialog."""
        dialog = PlatformsDialog(self)
        dialog.exec()
    
    def reset_progress(self):
        """Reset progress bar and labels to initial state."""
        self.progress_bar.setValue(0)
        self.progress_bar.setFormat("%p%")
        self.progress_label.setText("Ready")
        self.status_bar.showMessage("Ready to download")
        self.download_button.setEnabled(True)
        self.url_input.setEnabled(True)
        self.format_combo.setEnabled(True)
        self.browse_button.setEnabled(True)
        self.path_input.setEnabled(True)
        self.progress_group.hide()
        self.progress_spacer.show()
    
    def browse_path(self):
        """Open directory selection dialog."""
        path = QFileDialog.getExistingDirectory(
            self,
            "Select Download Directory",
            self.path_input.text(),
            QFileDialog.Option.ShowDirsOnly
        )
        if path:
            formatted_path = str(Path(path))
            self.path_input.setText(formatted_path)
    
    def _get_format(self) -> VideoFormat:
        """Get the selected video format."""
        format_map = {
            0: VideoFormat.BEST,
            1: VideoFormat.HD,
            2: VideoFormat.SD,
            3: VideoFormat.AUDIO
        }
        return format_map[self.format_combo.currentIndex()]
    
    def handle_progress(self, progress: DownloadProgress):
        """Handle download progress updates."""
        # Show progress group if hidden
        if not self.progress_group.isVisible():
            self.progress_group.show()
            self.progress_spacer.hide()
            
        if progress.status == "downloading":
            self.progress_bar.setValue(int(progress.percent))
            status = f"Downloading... "
            if progress.speed:
                status += f"Speed: {progress.speed} "
            if progress.eta:
                status += f"ETA: {progress.eta}"
            self.progress_label.setText(status)
            
        elif progress.status == "finished":
            self.progress_bar.setValue(100)
            self.progress_label.setText("Download complete!")
            self.status_bar.showMessage(
                f"Download complete: {Path(progress.filename or '').name}"
            )
            
        elif progress.status == "error":
            self.progress_label.setText("Error!")
            self.status_bar.showMessage(
                f"Download failed: {progress.filename}"
            )
    
    def handle_finished(self, success: bool):
        """Handle download completion."""
        if success:
            self.status_bar.showMessage("Download completed successfully")
        else:
            self.status_bar.showMessage("Download failed")
        self.reset_progress()
    
    def start_download(self):
        """Handle the download button click."""
        url = self.url_input.text().strip()
        if not url:
            self.status_bar.showMessage("Please enter a valid URL")
            return
            
        if not is_valid_url(url):
            self.status_bar.showMessage("Invalid URL format")
            return
            
        # Validate download path
        download_path = Path(self.path_input.text())
        if not download_path.exists():
            try:
                download_path.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                self.status_bar.showMessage(f"Invalid download path: {str(e)}")
                return
            
        platform = get_platform(url)
        if platform:
            self.status_bar.showMessage(f"Downloading from {platform.title()}...")
        else:
            self.status_bar.showMessage("Downloading from unknown platform...")
        
        # Show progress group and hide spacer
        self.progress_group.show()
        self.progress_spacer.hide()
        
        # Disable inputs during download
        self.download_button.setEnabled(False)
        self.url_input.setEnabled(False)
        self.format_combo.setEnabled(False)
        self.browse_button.setEnabled(False)
        self.path_input.setEnabled(False)
        
        # Start download in worker thread
        self.worker = DownloadWorker(
            url=url,
            format=self._get_format(),
            download_path=download_path
        )
        self.worker.progress.connect(self.handle_progress)
        self.worker.finished.connect(self.handle_finished)
        self.worker.start()
        
        self.status_bar.showMessage("Download started...")
        self.progress_label.setText("Preparing download...")
