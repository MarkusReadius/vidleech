import os
from pathlib import Path
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLineEdit, QPushButton, QProgressBar, QComboBox,
    QLabel, QFileDialog, QMessageBox, QFrame, QSizePolicy,
    QListWidget, QListWidgetItem, QToolButton, QMenu
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QPalette, QColor, QFont, QPixmap, QAction
from src.core.downloader import VideoDownloader
from src.gui.platforms_dialog import PlatformsDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Vidleech")
        self.setMinimumWidth(700)
        self.setMinimumHeight(600)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2b2b2b;
            }
            QWidget {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                background-color: #363636;
                color: #ffffff;
            }
            QComboBox {
                padding: 8px;
                padding-right: 20px;
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                background-color: #363636;
                color: #ffffff;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
                background-color: #444444;
                border-top-right-radius: 4px;
                border-bottom-right-radius: 4px;
            }
                QComboBox::down-arrow {
                    width: 14px;
                    height: 14px;
                    image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 14 14'%3E%3Cpath fill='%23ffffff' d='M7 9L2 4h10z'/%3E%3C/svg%3E");
                    margin-right: 8px;
                }
            QComboBox::drop-down:hover {
                background-color: #505050;
            }
            QComboBox QAbstractItemView {
                background-color: #363636;
                border: 1px solid #3d3d3d;
                selection-background-color: #505050;
                selection-color: white;
            }
            QPushButton {
                padding: 8px 16px;
                border: none;
                border-radius: 4px;
                background-color: #0d6efd;
                color: white;
            }
            QPushButton:hover {
                background-color: #0b5ed7;
            }
            QPushButton:disabled {
                background-color: #6c757d;
            }
            QProgressBar {
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                text-align: center;
                background-color: #363636;
            }
            QProgressBar::chunk {
                background-color: #0d6efd;
            }
        """)

        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # Header with logo and title
        header_layout = QHBoxLayout()
        
        # Try to load the icon as a logo
        icon_path = Path(__file__).parent.parent / "resources" / "icon.svg"
        logo_label = QLabel()
        if icon_path.exists():
            logo_pixmap = QPixmap(str(icon_path))
            logo_label.setPixmap(logo_pixmap.scaled(48, 48, Qt.AspectRatioMode.KeepAspectRatio))
        logo_label.setFixedSize(48, 48)
        header_layout.addWidget(logo_label)
        
        # Title and version
        title_layout = QVBoxLayout()
        title_label = QLabel("Потребує інтернету")
        title_label.setFont(QFont(title_label.font().family(), 18, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #0d6efd;")
        
        version_label = QLabel("v0.1.3")
        version_label.setStyleSheet("color: #6c757d;")
        
        title_layout.addWidget(title_label)
        title_layout.addWidget(version_label)
        header_layout.addLayout(title_layout)
        
        # Add spacer to push help button to the right
        header_layout.addStretch()
        
        # Help button
        self.help_btn = QPushButton("Supported Platforms")
        self.help_btn.setIcon(QIcon.fromTheme("help-about"))
        self.help_btn.clicked.connect(self.show_platforms)
        header_layout.addWidget(self.help_btn)
        
        # Theme toggle
        self.theme_btn = QPushButton()
        self.theme_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
            }
        """)
        self.theme_btn.setIcon(QIcon.fromTheme("weather-clear-night"))
        self.theme_btn.setToolTip("Toggle Dark/Light Theme")
        self.theme_btn.setFixedSize(36, 36)
        self.theme_btn.clicked.connect(self.toggle_theme)
        header_layout.addWidget(self.theme_btn)
        
        layout.addLayout(header_layout)
        
        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator.setStyleSheet("background-color: #3d3d3d;")
        layout.addWidget(separator)
        
        # Main content
        content_layout = QVBoxLayout()
        content_layout.setSpacing(15)
        
        # URL input with clear button
        url_layout = QHBoxLayout()
        url_label = QLabel("Video URL:")
        url_label.setFixedWidth(80)
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter video URL (YouTube, Vimeo, etc.)")
        
        # Clear button for URL input
        clear_btn = QPushButton("Clear")
        clear_btn.clicked.connect(self.url_input.clear)
        
        url_layout.addWidget(url_label)
        url_layout.addWidget(self.url_input)
        url_layout.addWidget(clear_btn)
        content_layout.addLayout(url_layout)

        # Format selection
        format_layout = QHBoxLayout()
        format_label = QLabel("Format:")
        format_label.setFixedWidth(80)
        self.format_combo = QComboBox()
        self.format_combo.addItems(["Best", "HD (1080p)", "SD (480p)", "Audio Only"])
        format_layout.addWidget(format_label)
        format_layout.addWidget(self.format_combo)
        format_layout.addStretch()
        content_layout.addLayout(format_layout)

        # Output directory selection
        dir_layout = QHBoxLayout()
        dir_label = QLabel("Save to:")
        dir_label.setFixedWidth(80)
        self.dir_input = QLineEdit()
        self.dir_input.setPlaceholderText("Output directory")
        self.dir_input.setText(os.path.expanduser("~/Downloads"))
        self.browse_btn = QPushButton("Browse")
        self.browse_btn.clicked.connect(self.browse_directory)
        dir_layout.addWidget(dir_label)
        dir_layout.addWidget(self.dir_input)
        dir_layout.addWidget(self.browse_btn)
        content_layout.addLayout(dir_layout)

        # Download and cancel buttons
        buttons_layout = QHBoxLayout()
        self.download_btn = QPushButton("Download")
        self.download_btn.setIcon(QIcon.fromTheme("download"))
        self.download_btn.clicked.connect(self.start_download)
        self.download_btn.setMinimumHeight(40)
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setIcon(QIcon.fromTheme("process-stop"))
        self.cancel_btn.clicked.connect(self.cancel_download)
        self.cancel_btn.setEnabled(False)
        
        buttons_layout.addWidget(self.download_btn)
        buttons_layout.addWidget(self.cancel_btn)
        content_layout.addLayout(buttons_layout)

        # Progress section
        progress_frame = QFrame()
        progress_frame.setFrameShape(QFrame.Shape.StyledPanel)
        progress_frame.setStyleSheet("""
            QFrame {
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                background-color: #363636;
            }
        """)
        progress_layout = QVBoxLayout(progress_frame)
        
        # Progress bar
        self.progress = QProgressBar()
        self.progress.setTextVisible(True)
        self.progress.setMinimumHeight(25)
        # Set progress bar text color to white
        palette = self.progress.palette()
        palette.setColor(QPalette.ColorRole.Text, QColor('white'))
        self.progress.setPalette(palette)
        progress_layout.addWidget(self.progress)

        # Status label
        self.status_label = QLabel("Ready")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        progress_layout.addWidget(self.status_label)
        
        content_layout.addWidget(progress_frame)
        
        # Recent downloads section
        recent_label = QLabel("Recent Downloads")
        recent_label.setFont(QFont(recent_label.font().family(), 12, QFont.Weight.Bold))
        content_layout.addWidget(recent_label)
        
        self.downloads_list = QListWidget()
        self.downloads_list.setMinimumHeight(150)
        self.downloads_list.setAlternatingRowColors(True)
        self.downloads_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                background-color: #363636;
                alternate-background-color: #2b2b2b;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #3d3d3d;
            }
            QListWidget::item:selected {
                background-color: #0d6efd;
            }
        """)
        # Connect double-click event to open file
        self.downloads_list.itemDoubleClicked.connect(self.open_downloaded_file)
        content_layout.addWidget(self.downloads_list)
        
        layout.addLayout(content_layout)

        # Initialize downloader
        self.downloader = VideoDownloader()
        self.downloader.progress.connect(self.update_progress)
        self.downloader.error.connect(self.show_error)
        self.downloader.complete.connect(self.download_complete)
        
        # Initialize state
        self.is_downloading = False
        self.current_download = None
        self.dark_mode = True  # Start with dark mode by default

    def show_platforms(self):
        """Show the supported platforms dialog."""
        dialog = PlatformsDialog(self)
        dialog.exec()
    
    def toggle_theme(self):
        """Toggle between dark and light theme."""
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #2b2b2b;
                }
                QWidget {
                    background-color: #2b2b2b;
                    color: #ffffff;
                }
                QLineEdit {
                    padding: 8px;
                    border: 1px solid #3d3d3d;
                    border-radius: 4px;
                    background-color: #363636;
                    color: #ffffff;
                }
                QComboBox {
                    padding: 8px;
                    padding-right: 20px;
                    border: 1px solid #3d3d3d;
                    border-radius: 4px;
                    background-color: #363636;
                    color: #ffffff;
                }
                QComboBox::drop-down {
                    border: none;
                    width: 20px;
                    background-color: #444444;
                    border-top-right-radius: 4px;
                    border-bottom-right-radius: 4px;
                }
                QComboBox::down-arrow {
                    image: none;
                    border-left: 5px solid transparent;
                    border-right: 5px solid transparent;
                    border-top: 5px solid #ffffff;
                    width: 0;
                    height: 0;
                    margin-right: 8px;
                }
                QComboBox::drop-down:hover {
                    background-color: #505050;
                }
                QComboBox QAbstractItemView {
                    background-color: #363636;
                    border: 1px solid #3d3d3d;
                    selection-background-color: #505050;
                    selection-color: white;
                }
                QPushButton {
                    padding: 8px 16px;
                    border: none;
                    border-radius: 4px;
                    background-color: #0d6efd;
                    color: white;
                }
                QPushButton:hover {
                    background-color: #0b5ed7;
                }
                QPushButton:disabled {
                    background-color: #6c757d;
                }
                QProgressBar {
                    border: 1px solid #3d3d3d;
                    border-radius: 4px;
                    text-align: center;
                    background-color: #363636;
                }
                QProgressBar::chunk {
                    background-color: #0d6efd;
                }
                QListWidget {
                    border: 1px solid #3d3d3d;
                    border-radius: 4px;
                    background-color: #363636;
                    alternate-background-color: #2b2b2b;
                }
                QListWidget::item {
                    padding: 8px;
                    border-bottom: 1px solid #3d3d3d;
                }
                QListWidget::item:selected {
                    background-color: #0d6efd;
                }
                QFrame {
                    border: 1px solid #3d3d3d;
                    border-radius: 4px;
                    background-color: #363636;
                }
            """)
            self.theme_btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    border: none;
                }
            """)
            self.theme_btn.setIcon(QIcon.fromTheme("weather-clear"))
            self.theme_btn.setToolTip("Switch to Light Theme")
        else:
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #f8f9fa;
                }
                QWidget {
                    background-color: #f8f9fa;
                    color: #212529;
                }
                QLineEdit {
                    padding: 8px;
                    border: 1px solid #ced4da;
                    border-radius: 4px;
                    background-color: #ffffff;
                    color: #212529;
                }
                QComboBox {
                    padding: 8px;
                    padding-right: 20px;
                    border: 1px solid #ced4da;
                    border-radius: 4px;
                    background-color: #ffffff;
                    color: #212529;
                }
                QComboBox::drop-down {
                    border: none;
                    width: 20px;
                    background-color: #e9ecef;
                    border-top-right-radius: 4px;
                    border-bottom-right-radius: 4px;
                }
                QComboBox::down-arrow {
                    width: 14px;
                    height: 14px;
                    image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 14 14'%3E%3Cpath fill='%23212529' d='M7 9L2 4h10z'/%3E%3C/svg%3E");
                    margin-right: 8px;
                }
                QComboBox::drop-down:hover {
                    background-color: #dee2e6;
                }
                QComboBox QAbstractItemView {
                    background-color: #ffffff;
                    border: 1px solid #ced4da;
                    selection-background-color: #0d6efd;
                    selection-color: white;
                }
                QPushButton {
                    padding: 8px 16px;
                    border: none;
                    border-radius: 4px;
                    background-color: #0d6efd;
                    color: white;
                }
                QPushButton:hover {
                    background-color: #0b5ed7;
                }
                QPushButton:disabled {
                    background-color: #6c757d;
                }
                QProgressBar {
                    border: 1px solid #ced4da;
                    border-radius: 4px;
                    text-align: center;
                    background-color: #ffffff;
                }
                QProgressBar::chunk {
                    background-color: #0d6efd;
                }
                QListWidget {
                    border: 1px solid #ced4da;
                    border-radius: 4px;
                    background-color: #ffffff;
                    alternate-background-color: #f8f9fa;
                }
                QListWidget::item {
                    padding: 8px;
                    border-bottom: 1px solid #ced4da;
                }
                QListWidget::item:selected {
                    background-color: #0d6efd;
                    color: white;
                }
                QFrame {
                    border: 1px solid #ced4da;
                    border-radius: 4px;
                    background-color: #ffffff;
                }
            """)
            self.theme_btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    border: none;
                }
            """)
            self.theme_btn.setIcon(QIcon.fromTheme("weather-clear-night"))
            self.theme_btn.setToolTip("Switch to Dark Theme")
            
            # Update progress bar text color for light theme
            palette = self.progress.palette()
            palette.setColor(QPalette.ColorRole.Text, QColor('black'))
            self.progress.setPalette(palette)

    def browse_directory(self):
        """Open file dialog to select output directory."""
        dir_path = QFileDialog.getExistingDirectory(
            self, "Select Output Directory",
            self.dir_input.text(),
            QFileDialog.Option.ShowDirsOnly
        )
        if dir_path:
            self.dir_input.setText(dir_path)

    def start_download(self):
        """Start downloading the video."""
        url = self.url_input.text().strip()
        if not url:
            self.show_error("Please enter a video URL")
            return

        output_path = self.dir_input.text()
        if not os.path.exists(output_path):
            try:
                os.makedirs(output_path)
            except Exception as e:
                self.show_error(f"Could not create output directory: {str(e)}")
                return

        format_map = {
            "Best": "best",
            "HD (1080p)": "hd",
            "SD (480p)": "sd",
            "Audio Only": "audio"
        }
        format_selection = format_map[self.format_combo.currentText()]

        self.download_btn.setEnabled(False)
        self.cancel_btn.setEnabled(True)
        self.progress.setValue(0)
        self.status_label.setText("Starting download...")
        self.is_downloading = True
        self.current_download = {
            "url": url,
            "format": self.format_combo.currentText(),
            "path": output_path
        }
        self.downloader.download(url, output_path, format_selection)
    
    def cancel_download(self):
        """Cancel the current download."""
        if self.is_downloading:
            # Currently there's no direct way to cancel a download in yt-dlp
            # This is a placeholder for future implementation
            self.status_label.setText("Cancelling download...")
            self.download_btn.setEnabled(True)
            self.cancel_btn.setEnabled(False)
            self.is_downloading = False

    def update_progress(self, percent: float, status: str):
        """Update the progress bar and status label."""
        self.progress.setValue(int(percent))
        self.status_label.setText(status)

    def show_error(self, message: str):
        """Show error message."""
        self.download_btn.setEnabled(True)
        self.cancel_btn.setEnabled(False)
        self.is_downloading = False
        self.status_label.setText("Error")
        QMessageBox.critical(self, "Error", message)

    def open_downloaded_file(self, item):
        """Open the downloaded file or its containing folder."""
        # Extract the file path from the tooltip
        tooltip = item.toolTip()
        path_line = next((line for line in tooltip.split('\n') if line.startswith('Saved to:')), None)
        
        if path_line:
            file_path = path_line.replace('Saved to:', '').strip()
            
            # Check if the file exists
            if os.path.exists(file_path):
                # On Windows, use the default file association to open the file
                os.startfile(file_path)
            else:
                # If file doesn't exist, try to open the containing folder
                folder_path = os.path.dirname(file_path)
                if os.path.exists(folder_path):
                    os.startfile(folder_path)
                else:
                    QMessageBox.warning(self, "File Not Found", 
                                       f"The file or folder no longer exists:\n{file_path}")

    def download_complete(self, filename=""):
        """Handle download completion."""
        self.download_btn.setEnabled(True)
        self.cancel_btn.setEnabled(False)
        self.is_downloading = False
        self.status_label.setText("Download complete!")
        
        # Add to recent downloads list
        if self.current_download:
            path = self.current_download['path']
            
            # Use the actual filename if provided, otherwise use a default
            if not filename:
                format_ext = ".mp3" if self.current_download['format'] == "Audio Only" else ".mp4"
                filename = f"video{format_ext}"  # Default filename
            
            # Create full path to the file
            full_path = os.path.join(path, filename)
            
            # Create list item with the actual filename
            item_text = f"{filename} - {self.current_download['format']}"
            item = QListWidgetItem(item_text)
            item.setToolTip(f"URL: {self.current_download['url']}\nFormat: {self.current_download['format']}\nSaved to: {full_path}")
            # Store the full path as item data for easy access
            item.setData(Qt.ItemDataRole.UserRole, full_path)
            self.downloads_list.insertItem(0, item)
            
            # Limit list to 10 items
            if self.downloads_list.count() > 10:
                self.downloads_list.takeItem(self.downloads_list.count() - 1)
        
        # No popup message - just update the status label
