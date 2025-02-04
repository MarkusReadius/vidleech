"""
Dialog to display supported platforms.
"""
import webbrowser
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QWidget,
)

class PlatformsDialog(QDialog):
    """Dialog showing all supported platforms."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Supported Platforms")
        self.setMinimumSize(600, 400)
        
        # Set dialog style
        self.setStyleSheet("""
            QDialog {
                background-color: #f5f5f5;
            }
            QPushButton {
                padding: 8px 16px;
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """)
        
        # Create layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Title
        title = QLabel("Supported Platforms")
        title.setFont(QFont(title.font().family(), 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #007bff;")
        layout.addWidget(title)
        
        # Description
        desc = QLabel(
            "Vidleech supports downloading from many platforms through yt-dlp. "
            "Here's a comprehensive list of supported sites:"
        )
        desc.setWordWrap(True)
        desc.setStyleSheet("color: #444; font-size: 13px;")
        layout.addWidget(desc)
        
        # Create scrollable area for platforms
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        
        # Container for platforms list
        container = QWidget()
        container.setStyleSheet("""
            QWidget {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 8px;
            }
        """)
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(20, 20, 20, 20)
        container_layout.setSpacing(5)
        
        # Add platforms
        platforms = [
            "YouTube", "Vimeo", "Dailymotion", "Facebook", "Twitter", "Instagram",
            "TikTok", "Reddit", "Twitch", "SoundCloud", "Bandcamp", "Bilibili",
            "BitChute", "Flickr", "Imgur", "LinkedIn", "Mashable", "Mixcloud",
            "Odysee", "Patreon", "PeerTube", "Pinterest", "Rumble", "Streamable",
            "Telegram", "TED", "Tumblr", "Udemy", "VK", "Voot", "Wistia",
            "And many more..."
        ]
        
        for platform in platforms:
            label = QLabel(f"• {platform}")
            label.setStyleSheet("""
                padding: 4px 10px;
                color: #333;
                font-size: 13px;
                background: none;
            """)
            container_layout.addWidget(label)
        
        # Add container to scroll area
        scroll.setWidget(container)
        layout.addWidget(scroll)
        
        # Add link to full list
        link_btn = QPushButton("View Full List of Supported Sites")
        link_btn.clicked.connect(self.open_full_list)
        layout.addWidget(link_btn)
    
    def open_full_list(self):
        """Open the full list of supported sites in browser."""
        webbrowser.open("https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md")
