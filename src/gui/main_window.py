import os
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLineEdit, QPushButton, QProgressBar, QComboBox,
    QLabel, QFileDialog, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QPalette, QColor
from src.core.downloader import VideoDownloader

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Vidleech")
        self.setMinimumWidth(600)
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
        """)

        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # URL input
        url_layout = QHBoxLayout()
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter video URL")
        url_layout.addWidget(self.url_input)
        layout.addLayout(url_layout)

        # Format selection
        format_layout = QHBoxLayout()
        format_label = QLabel("Format:")
        self.format_combo = QComboBox()
        self.format_combo.addItems(["Best", "HD (1080p)", "SD (480p)", "Audio Only"])
        format_layout.addWidget(format_label)
        format_layout.addWidget(self.format_combo)
        layout.addLayout(format_layout)

        # Output directory selection
        dir_layout = QHBoxLayout()
        self.dir_input = QLineEdit()
        self.dir_input.setPlaceholderText("Output directory")
        self.dir_input.setText(os.path.expanduser("~/Downloads"))
        self.browse_btn = QPushButton("Browse")
        self.browse_btn.clicked.connect(self.browse_directory)
        dir_layout.addWidget(self.dir_input)
        dir_layout.addWidget(self.browse_btn)
        layout.addLayout(dir_layout)

        # Download button
        self.download_btn = QPushButton("Download")
        self.download_btn.clicked.connect(self.start_download)
        layout.addWidget(self.download_btn)

        # Progress bar
        self.progress = QProgressBar()
        self.progress.setTextVisible(True)
        # Set progress bar text color to white
        palette = self.progress.palette()
        palette.setColor(QPalette.ColorRole.Text, QColor('white'))
        self.progress.setPalette(palette)
        layout.addWidget(self.progress)

        # Status label
        self.status_label = QLabel()
        layout.addWidget(self.status_label)

        # Initialize downloader
        self.downloader = VideoDownloader()
        self.downloader.progress.connect(self.update_progress)
        self.downloader.error.connect(self.show_error)
        self.downloader.complete.connect(self.download_complete)

    def browse_directory(self):
        dir_path = QFileDialog.getExistingDirectory(
            self, "Select Output Directory",
            self.dir_input.text(),
            QFileDialog.Option.ShowDirsOnly
        )
        if dir_path:
            self.dir_input.setText(dir_path)

    def start_download(self):
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
        self.progress.setValue(0)
        self.status_label.setText("Starting download...")
        self.downloader.download(url, output_path, format_selection)

    def update_progress(self, percent: float, status: str):
        self.progress.setValue(int(percent))
        self.status_label.setText(status)

    def show_error(self, message: str):
        self.download_btn.setEnabled(True)
        self.status_label.setText("Error")
        QMessageBox.critical(self, "Error", message)

    def download_complete(self):
        self.download_btn.setEnabled(True)
        self.status_label.setText("Download complete!")
        QMessageBox.information(self, "Success", "Download completed successfully!")
