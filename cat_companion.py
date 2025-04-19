import sys
import os
import json
import win32api
import win32con
import random
from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QMenu, 
                           QSystemTrayIcon, QWidget, QDialog, QVBoxLayout,
                           QPushButton, QFileDialog, QLineEdit, QSpinBox,
                           QFormLayout, QCheckBox, QColorDialog, QMessageBox,
                           QHBoxLayout, QGroupBox)
from PyQt6.QtCore import Qt, QTimer, QSize, QPropertyAnimation, QEasingCurve, QUrl, QPoint, QRectF, QTime, QPointF
from PyQt6.QtGui import QIcon, QMovie, QAction, QColor, QPainter, QPainterPath, QPen, QBrush, QCursor, QShortcut, QKeySequence, QPixmap, QImage
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle("Settings")
        self.setMinimumWidth(400)
        self.setMinimumHeight(600)  # Increased height for stats
        
        # Set pink theme for dialog
        self.setStyleSheet(f"""
            QDialog {{
                background-color: #FFF0F5;
            }}
            QLabel {{
                color: {parent.theme_color};
                font-size: 12px;
                font-weight: bold;
            }}
            QPushButton {{
                background-color: {parent.theme_color};
                color: white;
                border-radius: 8px;
                padding: 8px 16px;
                border: none;
                font-weight: bold;
                min-width: 100px;
            }}
            QPushButton:hover {{
                background-color: #FF1493;
            }}
            QLineEdit, QSpinBox {{
                border: 2px solid {parent.theme_color};
                border-radius: 8px;
                padding: 6px;
                background-color: white;
                color: #333;
                font-size: 12px;
            }}
            QLineEdit:focus, QSpinBox:focus {{
                border: 2px solid #FF1493;
            }}
            QCheckBox {{
                color: {parent.theme_color};
                font-size: 12px;
                font-weight: bold;
            }}
            QCheckBox::indicator {{
                width: 18px;
                height: 18px;
                border: 2px solid {parent.theme_color};
                border-radius: 4px;
            }}
            QCheckBox::indicator:checked {{
                background-color: {parent.theme_color};
            }}
            QSpinBox::up-button, QSpinBox::down-button {{
                width: 20px;
                border: none;
                background-color: {parent.theme_color};
                border-radius: 4px;
            }}
            QSpinBox::up-button:hover, QSpinBox::down-button:hover {{
                background-color: #FF1493;
            }}
            QGroupBox {{
                border: 2px solid {parent.theme_color};
                border-radius: 8px;
                margin-top: 1em;
                padding-top: 10px;
                color: {parent.theme_color};
                font-weight: bold;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px;
            }}
        """)
        
        # Create main layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Create form layout for settings
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        
        # Add title
        title_label = QLabel("Cat Companion Settings")
        title_label.setStyleSheet(f"""
            font-size: 18px;
            font-weight: bold;
            color: {parent.theme_color};
            padding-bottom: 10px;
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Create personalization group
        personalization_group = QGroupBox("Personalization")
        personalization_layout = QFormLayout()
        
        # Cat name
        self.cat_name = QLineEdit()
        self.cat_name.setText(parent.cat_name)
        self.cat_name.setPlaceholderText("Enter your cat's name")
        personalization_layout.addRow("Cat's Name:", self.cat_name)
        
        # Theme color
        color_layout = QHBoxLayout()
        self.theme_color_button = QPushButton()
        self.theme_color_button.setFixedSize(30, 30)
        self.theme_color = parent.theme_color
        self.update_color_button()
        self.theme_color_button.clicked.connect(self.choose_color)
        color_layout.addWidget(self.theme_color_button)
        personalization_layout.addRow("Theme Color:", color_layout)
        
        personalization_group.setLayout(personalization_layout)
        main_layout.addWidget(personalization_group)
        
        # Create reminder group
        reminder_group = QGroupBox("Reminders")
        reminder_layout = QFormLayout()
        
        # Reminder interval
        interval_layout = QHBoxLayout()
        self.interval_spinbox = QSpinBox()
        self.interval_spinbox.setRange(1, 240)
        self.interval_spinbox.setValue(parent.reminder_interval // 60000)  # Convert ms to minutes
        self.interval_spinbox.setSuffix(" minutes")
        interval_layout.addWidget(self.interval_spinbox)
        reminder_layout.addRow("Reminder Interval:", interval_layout)
        
        # Custom reminder message
        self.reminder_message = QLineEdit()
        self.reminder_message.setText(parent.reminder_message)
        self.reminder_message.setPlaceholderText("Enter a custom reminder message")
        reminder_layout.addRow("Custom Message:", self.reminder_message)
        
        reminder_group.setLayout(reminder_layout)
        main_layout.addWidget(reminder_group)
        
        # Create customization group
        customization_group = QGroupBox("Customization")
        customization_layout = QFormLayout()
        
        # Custom GIF selector
        gif_layout = QHBoxLayout()
        self.gif_path = QLineEdit()
        self.gif_path.setText(parent.gif_path)
        self.gif_path.setReadOnly(True)
        
        browse_gif_button = QPushButton("Browse...")
        browse_gif_button.clicked.connect(self.browse_gif)
        gif_layout.addWidget(self.gif_path)
        gif_layout.addWidget(browse_gif_button)
        customization_layout.addRow("Custom GIF:", gif_layout)
        
        # Custom Sound selector
        sound_layout = QHBoxLayout()
        self.sound_path = QLineEdit()
        self.sound_path.setText(parent.sound_path)
        self.sound_path.setReadOnly(True)
        
        browse_sound_button = QPushButton("Browse...")
        browse_sound_button.clicked.connect(self.browse_sound)
        sound_layout.addWidget(self.sound_path)
        sound_layout.addWidget(browse_sound_button)
        customization_layout.addRow("Custom Sound:", sound_layout)
        
        customization_group.setLayout(customization_layout)
        main_layout.addWidget(customization_group)
        
        # Create options group
        options_group = QGroupBox("Options")
        options_layout = QVBoxLayout()
        
        # Start with Windows option
        self.start_with_windows = QCheckBox("Start with Windows")
        self.start_with_windows.setChecked(parent.start_with_windows)
        options_layout.addWidget(self.start_with_windows)
        
        options_group.setLayout(options_layout)
        main_layout.addWidget(options_group)
        
        # Add stats group
        stats_group = QGroupBox("Your Stats")
        stats_layout = QVBoxLayout()
        
        # Daily stats
        daily_stats = QLabel(
            f"<h3>Today's Progress</h3>"
            f"Water count: {parent.stats['daily']['water_count']}<br>"
            f"Songs played: {parent.stats['daily']['songs_played']}<br>"
            f"Last water: {parent.stats['daily']['last_water_time'].toString('hh:mm:ss') if isinstance(parent.stats['daily']['last_water_time'], QTime) else 'Never'}"
        )
        daily_stats.setStyleSheet("""
            QLabel {
                color: #333;
                font-size: 12px;
                padding: 10px;
            }
        """)
        
        # Weekly stats
        weekly_stats = QLabel(
            f"<h3>Weekly Progress</h3>"
            f"Current streak: {parent.stats['weekly']['streak']} days<br>"
            f"Best day: {parent.stats['weekly']['best_day']} drinks<br>"
            f"Average daily: {sum(parent.stats['weekly']['water_count']) / 7:.1f} drinks<br>"
            f"Total songs this week: {sum(parent.stats['weekly']['songs_played'])}"
        )
        weekly_stats.setStyleSheet("""
            QLabel {
                color: #333;
                font-size: 12px;
                padding: 10px;
            }
        """)
        
        # Total stats
        total_stats = QLabel(
            f"<h3>Total Progress</h3>"
            f"Total water count: {parent.stats['total']['water_count']}<br>"
            f"Total songs played: {parent.stats['total']['songs_played']}<br>"
            f"Days used: {parent.stats['total']['days_used']}"
        )
        total_stats.setStyleSheet("""
            QLabel {
                color: #333;
                font-size: 12px;
                padding: 10px;
            }
        """)
        
        # Achievements
        achievements = QLabel(
            f"<h3>Achievements</h3>"
            f"{'🏆' if parent.stats['achievements']['first_sip'] else '🔒'} First Sip<br>"
            f"{'🏆' if parent.stats['achievements']['hydration_hero'] else '🔒'} Hydration Hero<br>"
            f"{'🏆' if parent.stats['achievements']['consistent_companion'] else '🔒'} Consistent Companion<br>"
            f"{'🏆' if parent.stats['achievements']['music_master'] else '🔒'} Music Master"
        )
        achievements.setStyleSheet("""
            QLabel {
                color: #333;
                font-size: 12px;
                padding: 10px;
            }
        """)
        
        stats_layout.addWidget(daily_stats)
        stats_layout.addWidget(weekly_stats)
        stats_layout.addWidget(total_stats)
        stats_layout.addWidget(achievements)
        stats_group.setLayout(stats_layout)
        main_layout.addWidget(stats_group)
        
        # Add stretch to push buttons to bottom
        main_layout.addStretch()
        
        # Add buttons at the bottom
        button_layout = QHBoxLayout()
        
        # Cancel button
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #FFB6C1;
                color: white;
            }
            QPushButton:hover {
                background-color: #FF69B4;
            }
        """)
        
        # Save button
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_settings)
        
        button_layout.addWidget(cancel_button)
        button_layout.addWidget(save_button)
        main_layout.addLayout(button_layout)
        
        self.setLayout(main_layout)
    
    def update_color_button(self):
        self.theme_color_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.theme_color};
                border-radius: 15px;
                border: 2px solid white;
            }}
            QPushButton:hover {{
                border: 2px solid #FF1493;
            }}
        """)
    
    def choose_color(self):
        color = QColorDialog.getColor(QColor(self.theme_color), self)
        if color.isValid():
            self.theme_color = color.name()
            self.update_color_button()
    
    def browse_gif(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select GIF", "", "GIF Files (*.gif)"
        )
        if file_path:
            self.gif_path.setText(file_path)
    
    def browse_sound(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Sound", "", "Sound Files (*.mp3 *.wav)"
        )
        if file_path:
            self.sound_path.setText(file_path)
    
    def save_settings(self):
        self.parent.reminder_interval = self.interval_spinbox.value() * 60000  # Convert to ms
        self.parent.reminder_message = self.reminder_message.text()
        self.parent.gif_path = self.gif_path.text()
        self.parent.sound_path = self.sound_path.text()
        self.parent.start_with_windows = self.start_with_windows.isChecked()
        self.parent.theme_color = self.theme_color
        self.parent.cat_name = self.cat_name.text()
        
        # Update reminder timer
        self.parent.reminder_timer.stop()
        self.parent.reminder_timer.start(self.parent.reminder_interval)
        
        # Update GIF if changed
        if self.parent.current_gif_path != self.parent.gif_path:
            self.parent.load_gif()
        
        # Update sound if changed
        if self.parent.current_sound_path != self.parent.sound_path:
            self.parent.load_sound()
        
        # Update startup registry
        self.parent.update_startup_registry()
        
        # Update theme
        self.parent.apply_theme()
        
        # Save settings to file
        self.parent.save_settings()
        
        # Show confirmation message
        self.parent.show_custom_notification("✨ Settings saved successfully!", duration=2000)
        
        self.accept()

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About")
        self.setFixedSize(350, 200)
        
        # Apply pink theme
        self.setStyleSheet(f"""
            QDialog {{
                background-color: #FFF0F5;
            }}
            QLabel {{
                color: {parent.theme_color};
            }}
        """)
        
        layout = QVBoxLayout()
        
        # About information
        about_text = QLabel(
            f"<h2>Cat Companion</h2>"
            f"<p>Version 1.1</p>"
            f"<p>Created by {parent.creator_name}</p>"
            f"<p>A cute companion to remind you to stay hydrated!</p>"
        )
        about_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        about_text.setWordWrap(True)
        
        ok_button = QPushButton("OK")
        ok_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {parent.theme_color};
                color: white;
                border-radius: 5px;
                padding: 5px 10px;
                border: none;
            }}
            QPushButton:hover {{
                background-color: #FF1493;
            }}
        """)
        ok_button.clicked.connect(self.accept)
        
        layout.addWidget(about_text)
        layout.addWidget(ok_button, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.setLayout(layout)

class AchievementsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Achievements")
        self.setMinimumWidth(400)
        self.setMinimumHeight(500)
        
        # Apply pink theme
        self.setStyleSheet(f"""
            QDialog {{
                background-color: #FFF0F5;
            }}
            QLabel {{
                color: {parent.theme_color};
                font-size: 12px;
                font-weight: bold;
            }}
            QPushButton {{
                background-color: {parent.theme_color};
                color: white;
                border-radius: 8px;
                padding: 8px 16px;
                border: none;
                font-weight: bold;
                min-width: 100px;
            }}
            QPushButton:hover {{
                background-color: #FF1493;
            }}
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Add title
        title_label = QLabel("Your Achievements")
        title_label.setStyleSheet(f"""
            font-size: 18px;
            font-weight: bold;
            color: {parent.theme_color};
            padding-bottom: 10px;
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        # Create achievements list
        achievements = [
            {
                "title": "First Sip",
                "description": "Take your first sip with your cat companion",
                "icon": "🏆" if parent.stats["achievements"]["first_sip"] else "🔒"
            },
            {
                "title": "Hydration Hero",
                "description": "Drink water 8+ times in a day",
                "icon": "🏆" if parent.stats["achievements"]["hydration_hero"] else "🔒"
            },
            {
                "title": "Consistent Companion",
                "description": "Maintain a 7-day streak of drinking water",
                "icon": "🏆" if parent.stats["achievements"]["consistent_companion"] else "🔒"
            },
            {
                "title": "Music Master",
                "description": "Play 50 songs with your cat companion",
                "icon": "🏆" if parent.stats["achievements"]["music_master"] else "🔒"
            }
        ]
        
        # Add each achievement
        for achievement in achievements:
            achievement_widget = QWidget()
            achievement_layout = QHBoxLayout()
            achievement_layout.setSpacing(10)
            
            # Icon
            icon_label = QLabel(achievement["icon"])
            icon_label.setStyleSheet("font-size: 24px;")
            achievement_layout.addWidget(icon_label)
            
            # Text
            text_widget = QWidget()
            text_layout = QVBoxLayout()
            text_layout.setSpacing(5)
            
            title = QLabel(achievement["title"])
            title.setStyleSheet("font-size: 14px; font-weight: bold;")
            
            description = QLabel(achievement["description"])
            description.setStyleSheet("font-size: 12px; color: #666;")
            description.setWordWrap(True)
            
            text_layout.addWidget(title)
            text_layout.addWidget(description)
            text_widget.setLayout(text_layout)
            
            achievement_layout.addWidget(text_widget)
            achievement_widget.setLayout(achievement_layout)
            layout.addWidget(achievement_widget)
        
        # Add close button
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.setLayout(layout)

class CatCompanion(QMainWindow):
    def __init__(self):
        super().__init__()
        # Initialize default settings
        self.reminder_interval = 30 * 60 * 1000  # 30 minutes in milliseconds
        self.reminder_message = "🐱 Time to drink water!"
        self.gif_path = "cat.gif"
        self.current_gif_path = self.gif_path
        self.sound_path = "notification.mp3"
        self.current_sound_path = self.sound_path
        self.purr_sound_path = "purr.mp3"
        self.current_purr_sound_path = self.purr_sound_path
        self.start_with_windows = False
        self.theme_color = "#FF69B4"  # Pink
        self.paused = False
        self.creator_name = "po1sontre"
        self.is_dragging = False
        self.is_resizing = False
        self.resize_handle_size = 10
        self.show_media_controls = True
        self.cat_name = "Kitty"  # Default cat name
        
        # Initialize stats tracking
        self.stats = {
            "daily": {
                "water_count": 0,
                "songs_played": 0,
                "start_time": QTime.currentTime(),
                "last_water_time": None
            },
            "weekly": {
                "water_count": [0] * 7,  # Last 7 days
                "songs_played": [0] * 7,  # Last 7 days
                "streak": 0,
                "best_day": 0
            },
            "achievements": {
                "first_sip": False,
                "hydration_hero": False,
                "consistent_companion": False,
                "music_master": False
            },
            "total": {
                "water_count": 0,
                "songs_played": 0,
                "days_used": 0
            }
        }
        
        # Load stats from file
        self.load_stats()
        
        # Setup daily stats reset timer
        self.daily_reset_timer = QTimer(self)
        self.daily_reset_timer.timeout.connect(self.check_daily_reset)
        self.daily_reset_timer.start(60000)  # Check every minute
        
        # Cute reminder messages
        self.reminder_messages = [
            "🐱 Hey friend! Time for a water break!",
            "😺 Stay hydrated, stay pawsome!",
            "😸 Meow! Water time!",
            "🐈 Your cat friend says: drink water!",
            "😺 Take care of yourself, have some water!",
            "🐱 *purrs* Water break time!",
            "😸 You're doing great! Time for water!",
            "🐈 Friendly reminder: stay hydrated!",
            "😺 Your well-being matters! Drink water!",
            "🐱 Sending positive vibes and water reminders!"
        ]
        
        # Load settings if exist
        self.load_settings()
        
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Create central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Create label for the cat GIF with rounded corners
        self.cat_label = QLabel(self.central_widget)
        self.cat_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.cat_label.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.cat_label.setScaledContents(True)  # Enable scaling
        
        # Set stylesheet for rounded corners
        self.cat_label.setStyleSheet("""
            QLabel {
                border-radius: 15px;
            }
        """)
        
        # Create media controls first
        self.setup_media_controls()
        
        # Load the cat GIF
        self.load_gif()
        
        # Create system tray icon
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("cat.gif"))
        self.tray_icon.setVisible(True)
        
        # Setup media player for sound
        self.media_player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.media_player.setAudioOutput(self.audio_output)
        self.load_sound()
        self.audio_output.setVolume(0.5)
        
        # Setup purr sound player
        self.purr_player = QMediaPlayer()
        self.purr_audio_output = QAudioOutput()
        self.purr_player.setAudioOutput(self.purr_audio_output)
        self.load_purr_sound()
        self.purr_audio_output.setVolume(0.5)
        
        # Create context menu
        self.create_context_menu()
        
        # Setup reminder timer
        self.reminder_timer = QTimer(self)
        self.reminder_timer.timeout.connect(self.show_reminder)
        self.reminder_timer.start(self.reminder_interval)
        
        # Apply theme after all UI elements are created
        self.apply_theme()
        
        # Setup hover animation
        self.hover_animation = None
        self.original_pos = None
        
        # Update startup registry
        self.update_startup_registry()
        
        # Create notification label with improved styling
        self.notification_label = QLabel(self)
        self.notification_label.setStyleSheet(f"""
            QLabel {{
                background-color: rgba(255, 192, 203, 180);
                color: white;
                padding: 12px 24px;
                border-radius: 15px;
                font-size: 14px;
                font-weight: bold;
                font-family: 'Segoe UI', Arial, sans-serif;
            }}
        """)
        self.notification_label.hide()
        
        # Setup click animation
        self.click_particles = []
        self.particle_timer = QTimer(self)
        self.particle_timer.timeout.connect(self.update_particles)
        self.particle_timer.start(16)  # 60 FPS
        
        # Show welcome message
        QTimer.singleShot(1000, self.show_welcome_message)
    
    def load_settings(self):
        try:
            if os.path.exists("settings.json"):
                with open("settings.json", "r") as f:
                    settings = json.load(f)
                    self.reminder_interval = settings.get("reminder_interval", self.reminder_interval)
                    self.reminder_message = settings.get("reminder_message", self.reminder_message)
                    self.gif_path = settings.get("gif_path", self.gif_path)
                    self.current_gif_path = self.gif_path
                    self.sound_path = settings.get("sound_path", self.sound_path)
                    self.current_sound_path = self.sound_path
                    self.purr_sound_path = settings.get("purr_sound_path", self.purr_sound_path)
                    self.current_purr_sound_path = self.purr_sound_path
                    self.start_with_windows = settings.get("start_with_windows", self.start_with_windows)
                    self.theme_color = settings.get("theme_color", self.theme_color)
                    self.creator_name = settings.get("creator_name", self.creator_name)
                    self.show_media_controls = settings.get("show_media_controls", self.show_media_controls)
                    self.cat_name = settings.get("cat_name", self.cat_name)
        except Exception as e:
            print(f"Error loading settings: {e}")
    
    def save_settings(self):
        try:
            settings = {
                "reminder_interval": self.reminder_interval,
                "reminder_message": self.reminder_message,
                "gif_path": self.gif_path,
                "sound_path": self.sound_path,
                "purr_sound_path": self.purr_sound_path,
                "start_with_windows": self.start_with_windows,
                "theme_color": self.theme_color,
                "creator_name": self.creator_name,
                "show_media_controls": self.show_media_controls,
                "cat_name": self.cat_name
            }
            with open("settings.json", "w") as f:
                json.dump(settings, f)
        except Exception as e:
            print(f"Error saving settings: {e}")
    
    def load_gif(self):
        try:
            if os.path.exists(self.gif_path):
                if hasattr(self, 'movie'):
                    self.movie.stop()
                
                self.movie = QMovie(self.gif_path)
                self.cat_label.setMovie(self.movie)
                self.movie.start()
                self.current_gif_path = self.gif_path
                self.update_window_size()
            else:
                # Fallback to default
                if self.gif_path != "cat.gif":
                    self.gif_path = "cat.gif"
                    self.load_gif()
        except Exception as e:
            print(f"Error loading GIF: {e}")
            # Fallback to default
            if self.gif_path != "cat.gif":
                self.gif_path = "cat.gif"
                self.load_gif()
    
    def load_sound(self):
        try:
            if os.path.exists(self.sound_path):
                self.media_player.setSource(QUrl.fromLocalFile(self.sound_path))
                self.current_sound_path = self.sound_path
            else:
                # Fallback to default
                if self.sound_path != "notification.mp3":
                    self.sound_path = "notification.mp3"
                    self.load_sound()
        except Exception as e:
            print(f"Error loading sound: {e}")
            # Fallback to default
            if self.sound_path != "notification.mp3":
                self.sound_path = "notification.mp3"
                self.load_sound()
    
    def load_purr_sound(self):
        try:
            if os.path.exists(self.purr_sound_path):
                self.purr_player.setSource(QUrl.fromLocalFile(self.purr_sound_path))
                self.current_purr_sound_path = self.purr_sound_path
            else:
                print(f"Purr sound file not found: {self.purr_sound_path}")
        except Exception as e:
            print(f"Error loading purr sound: {e}")
    
    def update_window_size(self):
        if hasattr(self, 'movie') and self.movie:
            original_size = self.movie.frameRect().size()
            self.scale_factor = 0.25  # Make the window 25% of the original size
            
            # Calculate initial size
            scaled_width = int(original_size.width() * self.scale_factor)
            scaled_height = int(original_size.height() * self.scale_factor)
            
            # Set base size for the GIF
            self.base_size = QSize(scaled_width, scaled_height)
            
            # Set window size including media controls if shown
            total_height = scaled_height
            if self.show_media_controls:
                total_height += 40  # Height for media controls
            
            # Resize window
            self.resize(scaled_width, total_height)
            
            # Update cat label and media controls
            self.cat_label.setGeometry(0, 0, scaled_width, scaled_height)
            if self.show_media_controls:
                self.update_media_controls_position()
    
    def update_media_controls_position(self):
        if self.show_media_controls:
            # Position media controls directly under the GIF
            self.media_controls.setGeometry(
                0,  # Align with window
                self.base_size.height() + 4,  # Small gap after GIF
                self.width(),  # Full window width
                36  # Just enough height for the buttons
            )
            self.media_controls.show()
        else:
            self.media_controls.hide()
    
    def apply_theme(self):
        # Update context menu style
        self.context_menu.setStyleSheet(f"""
            QMenu {{
                background-color: #FFF0F5;
                border: 1px solid {self.theme_color};
                border-radius: 8px;
                padding: 5px;
            }}
            QMenu::item {{
                padding: 8px 30px 8px 30px;
                color: {self.theme_color};
                border-radius: 4px;
            }}
            QMenu::item:selected {{
                background-color: {self.theme_color};
                color: white;
            }}
        """)
    
    def update_startup_registry(self):
        # For Windows only
        if sys.platform == "win32":
            import winreg
            key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
            app_path = os.path.abspath(sys.argv[0])
            
            try:
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, 
                                  winreg.KEY_WRITE) as registry_key:
                    if self.start_with_windows:
                        winreg.SetValueEx(registry_key, "CatCompanion", 0, 
                                       winreg.REG_SZ, app_path)
                    else:
                        try:
                            winreg.DeleteValue(registry_key, "CatCompanion")
                        except FileNotFoundError:
                            pass
            except Exception as e:
                print(f"Error updating registry: {e}")
    
    def create_context_menu(self):
        self.context_menu = QMenu()
        
        # Add menu actions
        test_reminder_action = QAction("Test Reminder", self)
        test_reminder_action.triggered.connect(self.show_reminder)
        
        # Toggle pause action
        self.pause_action = QAction("Pause Reminders", self)
        self.pause_action.triggered.connect(self.toggle_pause)
        
        # Toggle media controls
        self.toggle_media_action = QAction("Show Media Controls", self)
        self.toggle_media_action.setCheckable(True)
        self.toggle_media_action.setChecked(self.show_media_controls)
        self.toggle_media_action.triggered.connect(self.toggle_media_controls)
        
        # Add achievements action
        achievements_action = QAction("View Achievements", self)
        achievements_action.triggered.connect(self.show_achievements)
        
        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(self.show_settings)
        
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.cleanup_and_exit)
        
        self.context_menu.addAction(test_reminder_action)
        self.context_menu.addAction(self.pause_action)
        self.context_menu.addAction(self.toggle_media_action)
        self.context_menu.addAction(achievements_action)
        self.context_menu.addAction(settings_action)
        self.context_menu.addAction(about_action)
        self.context_menu.addAction(exit_action)
        
        # Apply theme to context menu
        self.apply_theme()
        
        # Also set up tray icon menu
        self.tray_icon.setContextMenu(self.context_menu)
        self.tray_icon.activated.connect(self.tray_activated)
    
    def toggle_pause(self):
        self.paused = not self.paused
        
        if self.paused:
            self.pause_action.setText("Resume Reminders")
            self.reminder_timer.stop()
        else:
            self.pause_action.setText("Pause Reminders")
            self.reminder_timer.start(self.reminder_interval)
    
    def tray_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            # Show/hide the app when clicking the tray icon
            if self.isVisible():
                self.hide()
            else:
                self.show()
    
    def contextMenuEvent(self, event):
        self.context_menu.exec(event.globalPos())
    
    def show_settings(self):
        dialog = SettingsDialog(self)
        dialog.exec()
    
    def show_about(self):
        dialog = AboutDialog(self)
        dialog.exec()
    
    def show_reminder(self):
        # Don't show if paused
        if self.paused:
            return
            
        # Play notification sound
        self.media_player.play()
        
        # Increment water count (assume user drank water)
        self.increment_water_count()
        
        # Show random reminder message with checkmark
        self.show_custom_notification(f"✅ {random.choice(self.reminder_messages)}")
    
    def show_welcome_message(self):
        current_hour = QTime.currentTime().hour()
        if 5 <= current_hour < 12:
            greeting = "Good morning"
        elif 12 <= current_hour < 17:
            greeting = "Good afternoon"
        else:
            greeting = "Good evening"
            
        self.show_custom_notification(
            f"🐱 {greeting}! {self.cat_name} is here to keep you company!",
            duration=4000
        )

    def show_custom_notification(self, message, duration=3000):
        self.notification_label.setText(message)
        self.notification_label.adjustSize()
        
        # Calculate maximum width based on GIF width with padding
        max_width = self.cat_label.width() - 40  # 20px padding on each side
        if self.notification_label.width() > max_width:
            self.notification_label.setWordWrap(True)
            self.notification_label.setFixedWidth(max_width)
            self.notification_label.adjustSize()
        
        # Position notification at the top center with padding
        self.notification_label.move(
            self.cat_label.x() + (self.cat_label.width() - self.notification_label.width()) // 2,
            self.cat_label.y() + 10  # 10px from top
        )
        
        # Show with fade effect
        self.notification_label.setWindowOpacity(0.0)
        self.notification_label.show()
        
        # Create fade in animation
        fade_in = QPropertyAnimation(self.notification_label, b"windowOpacity")
        fade_in.setDuration(500)
        fade_in.setStartValue(0.0)
        fade_in.setEndValue(1.0)
        fade_in.setEasingCurve(QEasingCurve.Type.OutCubic)
        fade_in.start()
        
        # Create fade out animation
        self.fade_animation = QPropertyAnimation(self.notification_label, b"windowOpacity")
        self.fade_animation.setDuration(500)
        self.fade_animation.setEasingCurve(QEasingCurve.Type.InCubic)
        self.fade_animation.finished.connect(lambda: self.notification_label.hide())
        
        # Start fade out after duration
        QTimer.singleShot(duration, self.start_fade_out)

    def start_fade_out(self):
        if self.notification_label.isVisible():
            self.fade_animation.setStartValue(1.0)
            self.fade_animation.setEndValue(0.0)
            self.fade_animation.start()
    
    def cleanup_and_exit(self):
        # Stop all timers
        self.reminder_timer.stop()
        
        # Stop media player
        self.media_player.stop()
        
        # Stop the GIF animation
        self.movie.stop()
        
        # Hide the tray icon
        self.tray_icon.hide()
        
        # Close the window
        self.close()
        
        # Quit the application
        QApplication.quit()
    
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            # Check if clicking the cat
            if self.cat_label.geometry().contains(event.pos()):
                # Play purr sound
                self.purr_player.stop()  # Stop any existing sound
                self.purr_player.play()
                
                self.create_heart_particles(event.pos())
                self.show_custom_notification(
                    random.choice([
                        "😺 *purrs happily*",
                        "🐱 *nuzzles*",
                        "😸 Meow! Thanks for the pets!",
                        "🐈 *happy cat noises*",
                        "😺 You're the best!",
                        "🐱 *rubs against your hand*"
                    ]),
                    duration=2000
                )
            
            # Handle resize and drag
            if (self.width() - self.resize_handle_size <= event.position().x() <= self.width() and
                self.height() - self.resize_handle_size <= event.position().y() <= self.height()):
                self.is_resizing = True
                self.resize_start_pos = event.globalPosition().toPoint()
                self.resize_start_size = self.size()
            else:
                self.is_dragging = True
                self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()
            
    def mouseMoveEvent(self, event):
        if self.is_resizing and event.buttons() == Qt.MouseButton.LeftButton:
            # Calculate new size
            delta = event.globalPosition().toPoint() - self.resize_start_pos
            new_width = max(100, self.resize_start_size.width() + delta.x())
            new_height = max(100, self.resize_start_size.height() + delta.y())
            
            # Maintain aspect ratio
            aspect_ratio = self.resize_start_size.width() / self.resize_start_size.height()
            if new_width / new_height > aspect_ratio:
                new_width = int(new_height * aspect_ratio)
            else:
                new_height = int(new_width / aspect_ratio)
            
            self.resize(new_width, new_height)
            self.update()
        elif self.is_dragging and event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()
            
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.is_dragging = False
            self.is_resizing = False
            # Update the original position after dragging completes
            self.original_pos = self.pos()
            event.accept()
            
    def enterEvent(self, event):
        # Check if cursor is in resize handle area
        if (self.width() - self.resize_handle_size <= event.position().x() <= self.width() and
            self.height() - self.resize_handle_size <= event.position().y() <= self.height()):
            self.setCursor(QCursor(Qt.CursorShape.SizeFDiagCursor))
        else:
            self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
            # Only create hover effect if not dragging
            if not self.is_dragging:
                if not self.hover_animation:
                    self.original_pos = self.pos()
                    self.hover_animation = QPropertyAnimation(self, b"pos")
                    self.hover_animation.setDuration(200)
                    self.hover_animation.setStartValue(self.pos())
                    # Slightly move up when hovered
                    self.hover_animation.setEndValue(QPoint(self.pos().x(), self.pos().y() - 10))
                    self.hover_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
                    self.hover_animation.start()
                    
    def leaveEvent(self, event):
        self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        # Only revert hover effect if not dragging
        if not self.is_dragging and self.original_pos and self.hover_animation:
            self.hover_animation.stop()
            self.hover_animation = QPropertyAnimation(self, b"pos")
            self.hover_animation.setDuration(200)
            self.hover_animation.setStartValue(self.pos())
            self.hover_animation.setEndValue(self.original_pos)
            self.hover_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
            self.hover_animation.start()

    def paintEvent(self, event):
        super().paintEvent(event)
        
        if self.click_particles:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            
            for particle in self.click_particles:
                painter.setOpacity(particle['opacity'])
                
                # Draw heart shape
                path = QPainterPath()
                size = particle['size']
                x, y = particle['pos'].x(), particle['pos'].y()
                
                path.moveTo(x, y + size / 4)
                path.cubicTo(
                    x, y, 
                    x - size / 2, y,
                    x - size / 2, y + size / 4
                )
                path.cubicTo(
                    x - size / 2, y + size / 2,
                    x, y + size * 3/4,
                    x, y + size
                )
                path.cubicTo(
                    x, y + size * 3/4,
                    x + size / 2, y + size / 2,
                    x + size / 2, y + size / 4
                )
                path.cubicTo(
                    x + size / 2, y,
                    x, y,
                    x, y + size / 4
                )
                
                painter.fillPath(path, QBrush(QColor(self.theme_color)))

    def create_heart_particles(self, pos):
        for _ in range(8):  # Create 8 particles
            particle = {
                'pos': QPointF(pos.x(), pos.y()),
                'velocity': QPointF(
                    random.uniform(-2, 2),  # Random horizontal velocity
                    random.uniform(-4, -2)  # Upward velocity
                ),
                'opacity': 1.0,
                'size': random.uniform(15, 25)  # Random size
            }
            self.click_particles.append(particle)

    def update_particles(self):
        if not self.click_particles:
            return
        
        # Update particles
        for particle in self.click_particles[:]:
            # Apply gravity
            particle['velocity'].setY(particle['velocity'].y() + 0.1)
            
            # Update position
            particle['pos'] += particle['velocity']
            
            # Fade out
            particle['opacity'] -= 0.02
            
            if particle['opacity'] <= 0:
                self.click_particles.remove(particle)
        
        # Trigger repaint
        self.update()

    def media_previous(self):
        self.increment_songs_played()
        win32api.keybd_event(0xB1, 0, 0, 0)  # VK_MEDIA_PREV_TRACK
        win32api.keybd_event(0xB1, 0, win32con.KEYEVENTF_KEYUP, 0)

    def media_play_pause(self):
        self.increment_songs_played()
        # Toggle between play and pause icons
        if hasattr(self, 'is_playing') and self.is_playing:
            self.play_pause_button.setIcon(QIcon(QPixmap.fromImage(QImage.fromData(f"""
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M6 19H10V5H6V19Z" fill="{self.theme_color}"/>
                    <path d="M14 19H18V5H14V19Z" fill="{self.theme_color}"/>
                </svg>
            """.encode()))))
        else:
            self.play_pause_button.setIcon(QIcon(QPixmap.fromImage(QImage.fromData(f"""
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M8 5V19L19 12L8 5Z" fill="{self.theme_color}"/>
                </svg>
            """.encode()))))
        self.is_playing = not getattr(self, 'is_playing', False)
        win32api.keybd_event(0xB3, 0, 0, 0)  # VK_MEDIA_PLAY_PAUSE
        win32api.keybd_event(0xB3, 0, win32con.KEYEVENTF_KEYUP, 0)

    def media_next(self):
        self.increment_songs_played()
        win32api.keybd_event(0xB0, 0, 0, 0)  # VK_MEDIA_NEXT_TRACK
        win32api.keybd_event(0xB0, 0, win32con.KEYEVENTF_KEYUP, 0)

    def media_volume_up(self):
        self.increment_songs_played()
        win32api.keybd_event(0xAF, 0, 0, 0)  # VK_VOLUME_UP
        win32api.keybd_event(0xAF, 0, win32con.KEYEVENTF_KEYUP, 0)

    def media_volume_down(self):
        self.increment_songs_played()
        win32api.keybd_event(0xAE, 0, 0, 0)  # VK_VOLUME_DOWN
        win32api.keybd_event(0xAE, 0, win32con.KEYEVENTF_KEYUP, 0)

    def media_mute(self):
        self.increment_songs_played()
        win32api.keybd_event(0xAD, 0, 0, 0)  # VK_VOLUME_MUTE
        win32api.keybd_event(0xAD, 0, win32con.KEYEVENTF_KEYUP, 0)

    def keyPressEvent(self, event):
        # Handle custom keyboard shortcuts
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            if event.key() == Qt.Key.Key_Left:
                self.media_previous()
            elif event.key() == Qt.Key.Key_Right:
                self.media_next()
            elif event.key() == Qt.Key.Key_Space:
                self.media_play_pause()
            elif event.key() == Qt.Key.Key_Up:
                self.media_volume_up()
            elif event.key() == Qt.Key.Key_Down:
                self.media_volume_down()
            elif event.key() == Qt.Key.Key_M:
                self.media_mute()
        super().keyPressEvent(event)

    def toggle_media_controls(self):
        self.show_media_controls = not self.show_media_controls
        self.toggle_media_action.setChecked(self.show_media_controls)
        # Resize window based on media controls visibility
        if self.show_media_controls:
            self.resize(self.base_size.width(), self.base_size.height() + 40)  # 40px for media controls
        else:
            self.resize(self.base_size.width(), self.base_size.height())
        self.update_media_controls_position()
        self.save_settings()

    def setup_media_controls(self):
        # Create media controls widget with minimal styling
        self.media_controls = QWidget(self)
        self.media_controls.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                border: none;
                border-radius: 6px;
                padding: 6px;
            }}
            QPushButton:hover {{
                background-color: rgba(255, 192, 203, 0.3);
            }}
        """)
        
        # Create custom SVG icons with dynamic color
        def create_svg_icon(path_data):
            return f"""
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="{path_data}" fill="{self.theme_color}"/>
                </svg>
            """
        
        prev_icon = create_svg_icon("M6 6h2v12H6V6zm3.5 6l7.5-6v12l-7.5-6z")
        play_icon = create_svg_icon("M8 5v14l11-7z")
        pause_icon = create_svg_icon("M6 19h4V5H6v14zm8-14v14h4V5h-4z")
        next_icon = create_svg_icon("M16 6h2v12h-2V6zM6 6l7.5 6L6 18V6z")
        vol_down_icon = create_svg_icon("M3 9v6h4l5 5V4L7 9H3zm13.5 3c0-1.77-1.02-3.29-2.5-4.03v8.05c1.48-.73 2.5-2.25 2.5-4.02z")
        vol_up_icon = create_svg_icon("M3 9v6h4l5 5V4L7 9H3zm13.5 3c0-1.77-1.02-3.29-2.5-4.03v8.05c1.48-.73 2.5-2.25 2.5-4.02zM14 3.23v2.06c2.89.86 5 3.54 5 6.71s-2.11 5.85-5 6.71v2.06c4.01-.91 7-4.49 7-8.77s-2.99-7.86-7-8.77z")
        mute_icon = create_svg_icon("M3 9v6h4l5 5V4L7 9H3zm7-4.17v2.51l3-3v-2.51l-3 3zm0 15.34l3 3v-2.51l-3-3v2.51zM14 3.23v2.06c2.89.86 5 3.54 5 6.71s-2.11 5.85-5 6.71v2.06c4.01-.91 7-4.49 7-8.77s-2.99-7.86-7-8.77z")
        
        # Create simple buttons
        def create_button(icon):
            button = QPushButton(self.media_controls)
            button.setIcon(QIcon(QPixmap.fromImage(QImage.fromData(icon.encode()))))
            button.setIconSize(QSize(20, 20))
            button.setFixedSize(32, 32)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            return button
        
        # Create all buttons
        self.prev_button = create_button(prev_icon)
        self.prev_button.clicked.connect(self.media_previous)
        
        self.play_pause_button = create_button(play_icon)
        self.play_pause_button.clicked.connect(self.media_play_pause)
        
        self.next_button = create_button(next_icon)
        self.next_button.clicked.connect(self.media_next)
        
        self.vol_down_button = create_button(vol_down_icon)
        self.vol_down_button.clicked.connect(self.media_volume_down)
        
        self.vol_up_button = create_button(vol_up_icon)
        self.vol_up_button.clicked.connect(self.media_volume_up)
        
        self.mute_button = create_button(mute_icon)
        self.mute_button.clicked.connect(self.media_mute)
        
        # Simple horizontal layout
        media_layout = QHBoxLayout(self.media_controls)
        media_layout.setSpacing(4)
        media_layout.setContentsMargins(0, 0, 0, 0)
        media_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Add buttons directly to layout
        media_layout.addWidget(self.prev_button)
        media_layout.addWidget(self.play_pause_button)
        media_layout.addWidget(self.next_button)
        media_layout.addSpacing(20)  # Space between groups
        media_layout.addWidget(self.vol_down_button)
        media_layout.addWidget(self.vol_up_button)
        media_layout.addWidget(self.mute_button)

    def load_stats(self):
        try:
            if os.path.exists("stats.json"):
                with open("stats.json", "r") as f:
                    saved_stats = json.load(f)
                    
                    # Migrate old stats format to new format if needed
                    self.migrate_stats_format(saved_stats)
                    
                    # Update current stats with saved data
                    self.stats.update(saved_stats)
                    
                    # Convert string times back to QTime objects
                    if isinstance(self.stats["daily"]["start_time"], str):
                        self.stats["daily"]["start_time"] = QTime.fromString(self.stats["daily"]["start_time"], "hh:mm:ss")
                    if isinstance(self.stats["daily"]["last_water_time"], str):
                        self.stats["daily"]["last_water_time"] = QTime.fromString(self.stats["daily"]["last_water_time"], "hh:mm:ss")
                    
                    # Check if we need to reset daily stats
                    current_time = QTime.currentTime()
                    if self.stats["daily"]["start_time"]:
                        # Calculate time difference in seconds
                        start_secs = self.stats["daily"]["start_time"].msecsSinceStartOfDay() // 1000
                        current_secs = current_time.msecsSinceStartOfDay() // 1000
                        if current_secs < start_secs:  # New day
                            self.reset_daily_stats()
            else:
                # Initialize stats file if it doesn't exist
                self.initialize_stats()
                self.save_stats()
        except Exception as e:
            print(f"Error loading stats: {e}")
            # Reset stats to default if there's an error
            self.initialize_stats()
            self.save_stats()

    def migrate_stats_format(self, saved_stats):
        """Migrate old stats format to new format"""
        # Ensure daily stats exist
        if "daily" not in saved_stats:
            saved_stats["daily"] = {}
        
        # Migrate water count
        if "water_count" not in saved_stats["daily"]:
            saved_stats["daily"]["water_count"] = 0
        
        # Add songs played if it doesn't exist
        if "songs_played" not in saved_stats["daily"]:
            saved_stats["daily"]["songs_played"] = 0
        
        # Ensure weekly stats exist
        if "weekly" not in saved_stats:
            saved_stats["weekly"] = {}
        
        # Migrate weekly water count
        if "water_count" not in saved_stats["weekly"]:
            saved_stats["weekly"]["water_count"] = [0] * 7
        
        # Add weekly songs played
        if "songs_played" not in saved_stats["weekly"]:
            saved_stats["weekly"]["songs_played"] = [0] * 7
        
        # Ensure total stats exist
        if "total" not in saved_stats:
            saved_stats["total"] = {}
        
        # Migrate total water count
        if "water_count" not in saved_stats["total"]:
            saved_stats["total"]["water_count"] = 0
        
        # Add total songs played
        if "songs_played" not in saved_stats["total"]:
            saved_stats["total"]["songs_played"] = 0
        
        # Ensure achievements exist
        if "achievements" not in saved_stats:
            saved_stats["achievements"] = {
                "first_sip": False,
                "hydration_hero": False,
                "consistent_companion": False,
                "music_master": False
            }
        
        # Remove old stats if they exist
        if "cat_pets" in saved_stats["daily"]:
            del saved_stats["daily"]["cat_pets"]
        if "media_controls_used" in saved_stats["daily"]:
            del saved_stats["daily"]["media_controls_used"]
        if "cat_pets" in saved_stats["total"]:
            del saved_stats["total"]["cat_pets"]
        if "media_controls_used" in saved_stats["total"]:
            del saved_stats["total"]["media_controls_used"]
        if "cat_lover" in saved_stats["achievements"]:
            del saved_stats["achievements"]["cat_lover"]

    def initialize_stats(self):
        """Initialize stats with default values"""
        self.stats = {
            "daily": {
                "water_count": 0,
                "songs_played": 0,
                "start_time": QTime.currentTime(),
                "last_water_time": None
            },
            "weekly": {
                "water_count": [0] * 7,  # Last 7 days
                "songs_played": [0] * 7,  # Last 7 days
                "streak": 0,
                "best_day": 0
            },
            "achievements": {
                "first_sip": False,
                "hydration_hero": False,
                "consistent_companion": False,
                "music_master": False
            },
            "total": {
                "water_count": 0,
                "songs_played": 0,
                "days_used": 0
            }
        }

    def save_stats(self):
        try:
            # Convert QTime to string for JSON serialization
            stats_to_save = self.stats.copy()
            if isinstance(stats_to_save["daily"]["start_time"], QTime):
                stats_to_save["daily"]["start_time"] = stats_to_save["daily"]["start_time"].toString("hh:mm:ss")
            if isinstance(stats_to_save["daily"]["last_water_time"], QTime):
                stats_to_save["daily"]["last_water_time"] = stats_to_save["daily"]["last_water_time"].toString("hh:mm:ss")
            
            with open("stats.json", "w") as f:
                json.dump(stats_to_save, f, indent=4)  # Add indentation for better readability
        except Exception as e:
            print(f"Error saving stats: {e}")

    def check_daily_reset(self):
        current_time = QTime.currentTime()
        if isinstance(self.stats["daily"]["start_time"], QTime):
            # Calculate time difference in seconds
            start_secs = self.stats["daily"]["start_time"].msecsSinceStartOfDay() // 1000
            current_secs = current_time.msecsSinceStartOfDay() // 1000
            if current_secs < start_secs:  # New day
                self.reset_daily_stats()

    def reset_daily_stats(self):
        # Update weekly stats
        self.stats["weekly"]["water_count"].pop(0)  # Remove oldest day
        self.stats["weekly"]["water_count"].append(self.stats["daily"]["water_count"])
        
        self.stats["weekly"]["songs_played"].pop(0)  # Remove oldest day
        self.stats["weekly"]["songs_played"].append(self.stats["daily"]["songs_played"])
        
        # Update streak
        if self.stats["daily"]["water_count"] > 0:
            self.stats["weekly"]["streak"] += 1
        else:
            self.stats["weekly"]["streak"] = 0
            
        # Update best day
        if self.stats["daily"]["water_count"] > self.stats["weekly"]["best_day"]:
            self.stats["weekly"]["best_day"] = self.stats["daily"]["water_count"]
        
        # Reset daily stats
        self.stats["daily"] = {
            "water_count": 0,
            "songs_played": 0,
            "start_time": QTime.currentTime(),
            "last_water_time": None
        }
        
        # Update total days used
        self.stats["total"]["days_used"] += 1
        
        # Save updated stats
        self.save_stats()

    def increment_water_count(self):
        self.stats["daily"]["water_count"] += 1
        self.stats["total"]["water_count"] += 1
        self.stats["daily"]["last_water_time"] = QTime.currentTime()
        
        # Check achievements
        if not self.stats["achievements"]["first_sip"]:
            self.stats["achievements"]["first_sip"] = True
            self.show_achievement("First Sip", "You took your first sip with your cat companion!")
        
        if self.stats["daily"]["water_count"] >= 8:
            if not self.stats["achievements"]["hydration_hero"]:
                self.stats["achievements"]["hydration_hero"] = True
                self.show_achievement("Hydration Hero", "You drank water 8+ times today!")
        
        if self.stats["weekly"]["streak"] >= 7:
            if not self.stats["achievements"]["consistent_companion"]:
                self.stats["achievements"]["consistent_companion"] = True
                self.show_achievement("Consistent Companion", "7-day streak achieved!")
        
        self.save_stats()

    def increment_songs_played(self):
        self.stats["daily"]["songs_played"] += 1
        self.stats["total"]["songs_played"] += 1
        
        if self.stats["total"]["songs_played"] >= 50:
            if not self.stats["achievements"]["music_master"]:
                self.stats["achievements"]["music_master"] = True
                self.show_achievement("Music Master", "You've played 50 songs!")
        
        self.save_stats()

    def show_achievement(self, title, message):
        # Create achievement notification
        achievement_label = QLabel(self)
        achievement_label.setStyleSheet(f"""
            QLabel {{
                background-color: rgba(255, 215, 0, 200);
                color: white;
                padding: 12px 24px;
                border-radius: 15px;
                font-size: 14px;
                font-weight: bold;
                font-family: 'Segoe UI', Arial, sans-serif;
            }}
        """)
        achievement_label.setText(f"🏆 {title}\n{message}")
        achievement_label.adjustSize()
        
        # Calculate maximum width based on GIF width with padding
        max_width = self.cat_label.width() - 40  # 20px padding on each side
        if achievement_label.width() > max_width:
            achievement_label.setWordWrap(True)
            achievement_label.setFixedWidth(max_width)
            achievement_label.adjustSize()
        
        # Position at top center with padding
        achievement_label.move(
            self.cat_label.x() + (self.cat_label.width() - achievement_label.width()) // 2,
            self.cat_label.y() + 10  # 10px from top
        )
        
        # Show with fade effect
        achievement_label.setWindowOpacity(0.0)
        achievement_label.show()
        
        # Create fade in animation
        fade_in = QPropertyAnimation(achievement_label, b"windowOpacity")
        fade_in.setDuration(500)
        fade_in.setStartValue(0.0)
        fade_in.setEndValue(1.0)
        fade_in.setEasingCurve(QEasingCurve.Type.OutCubic)
        fade_in.start()
        
        # Create fade out animation
        fade_out = QPropertyAnimation(achievement_label, b"windowOpacity")
        fade_out.setDuration(500)
        fade_out.setEasingCurve(QEasingCurve.Type.InCubic)
        fade_out.finished.connect(lambda: achievement_label.hide())
        
        # Start fade out after longer duration (5000ms = 5 seconds)
        QTimer.singleShot(5000, lambda: fade_out.start())

    def show_achievements(self):
        dialog = AchievementsDialog(self)
        dialog.exec()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CatCompanion()
    window.show()
    sys.exit(app.exec())