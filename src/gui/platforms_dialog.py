"""
Dialog to display supported platforms.
"""
import webbrowser
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QWidget,
    QFrame,
    QGridLayout,
)

class PlatformsDialog(QDialog):
    """Dialog showing all supported platforms."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Supported Platforms")
        self.setMinimumSize(700, 500)
        
        # Inherit parent's dark/light mode
        if parent and hasattr(parent, 'dark_mode'):
            self.dark_mode = parent.dark_mode
        else:
            self.dark_mode = True
            
        # Set dialog style based on theme
        self.apply_theme()
        
        # Create layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Header
        header_layout = QHBoxLayout()
        
        # Title
        title = QLabel("Supported Platforms")
        title.setFont(QFont(title.font().family(), 20, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        title.setStyleSheet("color: #0d6efd;")
        header_layout.addWidget(title)
        
        # Add spacer to push close button to the right
        header_layout.addStretch()
        
        layout.addLayout(header_layout)
        
        # Description
        desc = QLabel(
            "Vidleech supports downloading from many platforms through yt-dlp. "
            "Below is a list of popular supported sites. For a complete list, click the button at the bottom."
        )
        desc.setWordWrap(True)
        desc.setStyleSheet("font-size: 14px;")
        layout.addWidget(desc)
        
        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(separator)
        
        # Create scrollable area for platforms
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        
        # Container for platforms grid
        container = QWidget()
        container_layout = QGridLayout(container)
        container_layout.setContentsMargins(10, 10, 10, 10)
        container_layout.setSpacing(15)
        
        # Add platforms in a grid layout
        platforms = [
            {"name": "YouTube", "icon": "video"},
            {"name": "Vimeo", "icon": "video"},
            {"name": "Dailymotion", "icon": "video"},
            {"name": "Facebook", "icon": "share"},
            {"name": "Twitter", "icon": "share"},
            {"name": "Instagram", "icon": "image"},
            {"name": "TikTok", "icon": "video"},
            {"name": "Reddit", "icon": "share"},
            {"name": "Twitch", "icon": "video"},
            {"name": "SoundCloud", "icon": "audio"},
            {"name": "Bandcamp", "icon": "audio"},
            {"name": "Bilibili", "icon": "video"},
            {"name": "BitChute", "icon": "video"},
            {"name": "Flickr", "icon": "image"},
            {"name": "Imgur", "icon": "image"},
            {"name": "LinkedIn", "icon": "share"},
            {"name": "Mashable", "icon": "share"},
            {"name": "Mixcloud", "icon": "audio"},
            {"name": "Odysee", "icon": "video"},
            {"name": "Patreon", "icon": "share"},
            {"name": "PeerTube", "icon": "video"},
            {"name": "Pinterest", "icon": "image"},
            {"name": "Rumble", "icon": "video"},
            {"name": "Streamable", "icon": "video"},
            {"name": "Telegram", "icon": "share"},
            {"name": "TED", "icon": "video"},
            {"name": "Tumblr", "icon": "share"},
            {"name": "Udemy", "icon": "video"},
            {"name": "VK", "icon": "share"},
            {"name": "Voot", "icon": "video"},
            {"name": "Wistia", "icon": "video"},
        ]
        
        # Create platform cards in a 3-column grid
        for i, platform in enumerate(platforms):
            row = i // 3
            col = i % 3
            
            # Platform name with icon
            name_label = QLabel(f"  {platform['name']}")
            name_label.setFont(QFont(name_label.font().family(), 12))
            name_label.setStyleSheet("""
                QLabel {
                    padding: 8px;
                    border-radius: 4px;
                }
                QLabel:hover {
                    background-color: rgba(13, 110, 253, 0.1);
                }
            """)
            
            # Add to grid
            container_layout.addWidget(name_label, row, col)
        
        # Add "And many more..." label at the end
        more_label = QLabel("And many more...")
        more_label.setFont(QFont(more_label.font().family(), 12, QFont.Weight.Bold))
        more_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        more_label.setStyleSheet("color: #0d6efd;")
        container_layout.addWidget(more_label, (len(platforms) // 3) + 1, 0, 1, 3)
        
        # Add container to scroll area
        scroll.setWidget(container)
        layout.addWidget(scroll)
        
        # Buttons row
        buttons_layout = QHBoxLayout()
        
        # Close button
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)
        
        # Full list button
        link_btn = QPushButton("View Full List of Supported Sites")
        link_btn.setIcon(QIcon.fromTheme("web-browser"))
        link_btn.clicked.connect(self.open_full_list)
        
        buttons_layout.addWidget(close_btn)
        buttons_layout.addStretch()
        buttons_layout.addWidget(link_btn)
        
        layout.addLayout(buttons_layout)
    
    def apply_theme(self):
        """Apply the current theme to the dialog."""
        if self.dark_mode:
            self.setStyleSheet("""
                QDialog {
                    background-color: #2b2b2b;
                    color: #ffffff;
                }
                QLabel {
                    color: #ffffff;
                }
                QPushButton {
                    padding: 8px 16px;
                    background-color: #0d6efd;
                    color: white;
                    border: none;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #0b5ed7;
                }
                QScrollArea {
                    border: none;
                    background-color: transparent;
                }
                QFrame {
                    border: 1px solid #3d3d3d;
                    border-radius: 8px;
                    background-color: #363636;
                }
            """)
        else:
            self.setStyleSheet("""
                QDialog {
                    background-color: #f8f9fa;
                    color: #212529;
                }
                QLabel {
                    color: #212529;
                }
                QPushButton {
                    padding: 8px 16px;
                    background-color: #0d6efd;
                    color: white;
                    border: none;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #0b5ed7;
                }
                QScrollArea {
                    border: none;
                    background-color: transparent;
                }
                QFrame {
                    border: 1px solid #ced4da;
                    border-radius: 8px;
                    background-color: #ffffff;
                }
            """)
    
    def open_full_list(self):
        """Open the full list of supported sites in browser."""
        webbrowser.open("https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md")
