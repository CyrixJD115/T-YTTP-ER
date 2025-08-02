from PySide6.QtWidgets import (
    QMainWindow, QStackedWidget, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QLineEdit, QTextEdit, QProgressBar, QComboBox, QCheckBox,
    QFileDialog, QSizePolicy, QScrollArea, QFrame, QGroupBox, QTabWidget,
    QListWidget, QListWidgetItem, QGridLayout, QMessageBox
)
from PySide6.QtCore import Qt, QTimer, QThread, Signal
from PySide6.QtGui import QFont, QColor, QPalette, QTextCursor
from function import Config, TranscriptHandler
import process
import time
import re

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("T(YTTP)ER")
        self.setMinimumSize(800, 600)
        
        # Apply dark theme
        self.set_dark_theme()
        
        # Initialize config and handler
        self.config = Config()
        self.handler = TranscriptHandler(self.config)
        
        # Create stacked widget for screens
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        # Create screens
        self.splash_screen = SplashScreen(self)
        self.menu_screen = MenuScreen(self)
        self.start_screen = StartScreen(self)
        self.processing_screen = ProcessingScreen(self)
        self.settings_screen = SettingsScreen(self)
        self.history_screen = HistoryScreen(self)
        
        # Add to stack
        self.stacked_widget.addWidget(self.splash_screen)
        self.stacked_widget.addWidget(self.menu_screen)
        self.stacked_widget.addWidget(self.start_screen)
        self.stacked_widget.addWidget(self.processing_screen)
        self.stacked_widget.addWidget(self.settings_screen)
        self.stacked_widget.addWidget(self.history_screen)
        
        # Show splash screen first
        self.stacked_widget.setCurrentWidget(self.splash_screen)
        
        # Start splash animation
        self.splash_screen.start_animation()
    
    def set_dark_theme(self):
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(30, 30, 46))       # #1e1e2e
        dark_palette.setColor(QPalette.WindowText, Qt.white)
        dark_palette.setColor(QPalette.Base, QColor(46, 46, 63))         # #2e2e3f
        dark_palette.setColor(QPalette.AlternateBase, QColor(30, 30, 46))
        dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
        dark_palette.setColor(QPalette.ToolTipText, Qt.white)
        dark_palette.setColor(QPalette.Text, Qt.white)
        dark_palette.setColor(QPalette.Button, QColor(59, 59, 94))       # #3b3b5e
        dark_palette.setColor(QPalette.ButtonText, Qt.white)
        dark_palette.setColor(QPalette.BrightText, Qt.red)
        dark_palette.setColor(QPalette.Highlight, QColor(106, 106, 181)) # #6a6ab5
        dark_palette.setColor(QPalette.HighlightedText, Qt.black)
        self.setPalette(dark_palette)
    
    def show_screen(self, screen_name):
        screens = {
            "splash": self.splash_screen,
            "menu": self.menu_screen,
            "start": self.start_screen,
            "processing": self.processing_screen,
            "settings": self.settings_screen,
            "history": self.history_screen
        }
        widget = screens[screen_name]
        if screen_name == "history":
            widget.load_history()  # dynamically reload history.json
        self.stacked_widget.setCurrentWidget(widget)
    
    def start_processing(self, video_url):
        self.show_screen("processing")
        self.processing_screen.start_processing(video_url)
    
    def exit_application(self):
        self.config.clean_temp()
        self.close()

class SplashScreen(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        self.label = QLabel("")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 24pt; color: #e0e0e0;")
        layout.addWidget(self.label)
        
        self.text_to_type = "-- == T(YTTP)ER == --"
        self.char_index = 0
    
    def start_animation(self):
        self.char_index = 0
        self.type_text()
    
    def type_text(self):
        if self.char_index < len(self.text_to_type):
            current_text = self.label.text() + self.text_to_type[self.char_index]
            self.label.setText(current_text)
            self.char_index += 1
            QTimer.singleShot(50, self.type_text)
        else:
            QTimer.singleShot(1000, lambda: self.parent.show_screen("menu"))

class MenuScreen(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        
        # Gradient background
        self.setStyleSheet("""
            background: qlineargradient(x1:0,y1:0,x2:1,y2:1,
                stop:0 #1a1a2e, stop:0.5 #16213e, stop:1 #0f3460);
        """)
        
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setContentsMargins(20,40,20,40)
        self.setLayout(main_layout)
        
        title = QLabel("T(YTTP)ER")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size:42pt; font-weight:bold; color:#e94560;
        """)
        main_layout.addWidget(title)
        
        subtitle = QLabel("YouTube Transcript Processing Tool")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("font-size:14pt; color:#b8b8d1; margin-bottom:30px;")
        main_layout.addWidget(subtitle)
        
        button_container = QWidget()
        button_container.setStyleSheet("""
            background-color:#1f1f3d; border-radius:15px;
            padding:20px; border:1px solid #3a3a5a;
        """)
        button_layout = QVBoxLayout(button_container)
        button_layout.setSpacing(15)
        button_layout.setContentsMargins(20,20,20,20)
        
        buttons = [
            ("Start", lambda: self.parent.show_screen("start")),
            ("History", lambda: self.parent.show_screen("history")),
            ("Settings", lambda: self.parent.show_screen("settings")),
            ("Exit", self.parent.exit_application)
        ]
        for text, action in buttons:
            btn = self.create_menu_button(text)
            btn.clicked.connect(action)
            button_layout.addWidget(btn)
        main_layout.addWidget(button_container, alignment=Qt.AlignCenter)
        main_layout.addStretch()
        
        footer = QLabel("This tool is made by CyrixJD115")
        footer.setAlignment(Qt.AlignCenter)
        footer.setStyleSheet("color:#707090; font-size:10pt; margin-top:30px;")
        main_layout.addWidget(footer)
    
    def create_menu_button(self, text):
        button = QPushButton(text)
        button.setMinimumSize(300,60)
        button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                    stop:0 #4e54c8, stop:1 #8f94fb);
                color:white; font-size:18pt; font-weight:bold;
                border-radius:10px; padding:10px; border:none;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                    stop:0 #6a6fd3, stop:1 #a7abff);
                border:2px solid #e94560;
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                    stop:0 #3d42b2, stop:1 #7b80e8);
            }
        """)
        return button
        
    def get_button_style(self):
        return """
            QPushButton {
                background-color:#3b3b5e; color:white;
                font-size:14pt; padding:15px; border-radius:5px;
            }
            QPushButton:hover {
                background-color:#5a5a8a;
            }
        """

class StartScreen(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)
        
        header = QLabel("Enter YouTube URL:")
        header.setStyleSheet("font-size:14pt; color:white;")
        layout.addWidget(header, alignment=Qt.AlignCenter)
        
        self.url_entry = QLineEdit()
        self.url_entry.setPlaceholderText("https://www.youtube.com/watch?v=...")
        self.url_entry.setStyleSheet("""
            QLineEdit {
                background-color:#2e2e3f; color:white;
                padding:10px; font-size:12pt; border-radius:5px;
                min-width:400px;
            }
        """)
        layout.addWidget(self.url_entry, alignment=Qt.AlignCenter)
        
        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color:#ff7373; font-size:12pt;")
        self.error_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.error_label, alignment=Qt.AlignCenter)
        
        buttons_layout = QHBoxLayout()
        submit_btn = QPushButton("Submit")
        submit_btn.setStyleSheet(self.parent.menu_screen.get_button_style())
        submit_btn.clicked.connect(self.on_submit)
        buttons_layout.addWidget(submit_btn)
        back_btn = QPushButton("Back")
        back_btn.setStyleSheet(self.parent.menu_screen.get_button_style())
        back_btn.clicked.connect(self.back_to_menu)
        buttons_layout.addWidget(back_btn)
        layout.addLayout(buttons_layout)
    
    def on_submit(self):
        url = self.url_entry.text().strip()
        if not url:
            self.error_label.setText("Error: URL cannot be empty.")
            return
        if ("youtube.com" not in url) and ("youtu.be" not in url):
            self.error_label.setText("Error: Invalid YouTube URL format.")
            return
        
        self.error_label.setText("")
        self.parent.start_processing(url)
        self.parent.history_screen.load_history()
        self.url_entry.clear()
    
    def back_to_menu(self):
        self.parent.config.clean_temp()
        self.parent.show_screen("menu")

class ProcessingScreen(QWidget):
    update_progress = Signal(int,int)
    update_text = Signal(str)
    update_status = Signal(str,str)
    processing_complete = Signal()
    
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.cancel_processing = False
        self.video_id = ""
        self.video_title = ""
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        top_layout = QHBoxLayout()
        self.progress_label = QLabel("Processing: 0/0")
        self.progress_label.setStyleSheet("color:white; font-size:12pt;")
        top_layout.addWidget(self.progress_label)
        self.spinner_label = QLabel("")
        self.spinner_label.setStyleSheet("color:white; font-size:16pt;")
        top_layout.addWidget(self.spinner_label, alignment=Qt.AlignRight)
        layout.addLayout(top_layout)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border:2px solid #2e2e3f; border-radius:5px;
                text-align:center; background:#2e2e3f; height:20px;
            }
            QProgressBar::chunk {
                background:#6a6ab5; width:10px;
            }
        """)
        layout.addWidget(self.progress_bar)
        
        self.response_text = QTextEdit()
        self.response_text.setReadOnly(True)
        self.response_text.setStyleSheet("""
            QTextEdit {
                background-color:#2e2e3f; color:#f0f0f0;
                font-family:'Segoe UI'; font-size:11pt;
                border-radius:5px; padding:10px;
            }
        """)
        layout.addWidget(self.response_text)
        
        footer_layout = QHBoxLayout()
        footer_layout.addWidget(QLabel("Filename:"))
        self.filename_entry = QLineEdit()
        self.filename_entry.setStyleSheet("""
            QLineEdit {
                background-color:#2e2e3f; color:white;
                padding:5px; min-width:200px;
            }
        """)
        footer_layout.addWidget(self.filename_entry)
        self.save_btn = QPushButton("Save")
        self.save_btn.setStyleSheet(self.parent.menu_screen.get_button_style())
        self.save_btn.clicked.connect(self.save_output)
        footer_layout.addWidget(self.save_btn)
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setStyleSheet(self.parent.menu_screen.get_button_style())
        self.cancel_btn.clicked.connect(self.cancel)
        footer_layout.addWidget(self.cancel_btn)
        layout.addLayout(footer_layout)
        
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("font-size:12pt;")
        layout.addWidget(self.status_label)
        
        self.update_progress.connect(self.update_progress_display)
        self.update_text.connect(self.update_text_display)
        self.update_status.connect(self.update_status_display)
        self.processing_complete.connect(self.on_processing_complete)
    
    def start_processing(self, video_url):
        self.cancel_processing = False
        self.response_text.clear()
        self.progress_bar.setValue(0)
        self.progress_label.setText("Processing: 0/0")
        self.status_label.setText("")
        self.filename_entry.setText(self.parent.config.settings.get("last_video_id",""))
        
        self.worker = process.ProcessingWorker(self.parent, video_url)
        self.worker.update_progress.connect(self.update_progress.emit)
        self.worker.update_text.connect(self.update_text.emit)
        self.worker.update_status.connect(self.update_status.emit)
        self.worker.finished.connect(self.on_worker_finished)
        self.worker.start()
    
    def update_progress_display(self, current, total):
        self.progress_label.setText(f"Processing: {current}/{total}")
        self.progress_bar.setValue(int((current/total)*100))
        spinner = ["◐","◓","◑","◒"][current % 4]
        self.spinner_label.setText(spinner)
    
    def update_text_display(self, text):
        cursor = self.response_text.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        self.response_text.setTextCursor(cursor)
        self.response_text.ensureCursorVisible()
    
    def update_status_display(self, message, color):
        self.status_label.setText(message)
        self.status_label.setStyleSheet(f"color:{color}; font-size:12pt;")
    
    def on_worker_finished(self):
        self.processing_complete.emit()
    
    def on_processing_complete(self):
        self.status_label.setText("Processing complete. Enter filename and press Save.")
        self.status_label.setStyleSheet("color:#b5e0a8; font-size:12pt;")
        self.filename_entry.setText(self.video_id)
        self.parent.config.settings["inline_output_name"] = self.video_id
        self.parent.config.save_config()
    
    def save_output(self):
        name = self.filename_entry.text().strip()
        self.parent.config.settings["inline_output_name"] = name
        self.parent.config.save_config()
        def status_callback(message, color):
            self.update_status.emit(message, color)
        # FIX: Properly indent the combine_output call inside the method
        process.combine_output(self.parent, self.video_id, self.video_title, status_callback)
        # FIX: Add timer navigation inside the method
        QTimer.singleShot(3000, lambda: self.parent.show_screen("menu"))
    
    def cancel(self):
        self.cancel_processing = True
        self.status_label.setText("Cancelling...")
        self.status_label.setStyleSheet("color:#ff7373; font-size:12pt;")
        QTimer.singleShot(500, self.back_to_menu)
    
    def back_to_menu(self):
        self.parent.config.clean_temp()
        self.parent.show_screen("menu")

class SettingsScreen(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        # GLOBAL STYLE: force all text to white, cross‑platform
        self.setStyleSheet("""
            * {
                color: white;
            }
        """)

        layout = QVBoxLayout()
        self.setLayout(layout)

        title = QLabel("Settings")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24pt;")  # text color inherits white
        layout.addWidget(title)

        # Tab widget
        self.tab_widget = QTabWidget()
        # CUSTOM TAB STYLING: dark backgrounds, white text
        self.tab_widget.setStyleSheet("""
            QTabBar::tab {
                background: #2e2e3f;
                padding: 10px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background: #44475a;
            }
            QTabWidget::pane {
                border: 1px solid #44475a;
                top: -1px;
                background: #2e2e3f;
            }
        """)
        layout.addWidget(self.tab_widget)

        # Create tabs
        self.chunk_tab = self.create_chunk_tab()
        self.processing_tab = self.create_processing_tab()
        self.output_tab = self.create_output_tab()

        self.tab_widget.addTab(self.chunk_tab, "Chunk Settings")
        self.tab_widget.addTab(self.processing_tab, "Processing Settings")
        self.tab_widget.addTab(self.output_tab, "Output Settings")

        # Status label
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("font-size: 12pt;")  # inherits white
        layout.addWidget(self.status_label)

        # Buttons
        buttons_layout = QHBoxLayout()

        save_btn = QPushButton("Save Settings")
        save_btn.setStyleSheet(self.parent.menu_screen.get_button_style() + "color: white;")
        save_btn.clicked.connect(self.save_settings)
        buttons_layout.addWidget(save_btn)

        back_btn = QPushButton("Back to Menu")
        back_btn.setStyleSheet(self.parent.menu_screen.get_button_style() + "color: white;")
        back_btn.clicked.connect(self.back_to_menu)
        buttons_layout.addWidget(back_btn)

        layout.addLayout(buttons_layout)

    def create_chunk_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        tab.setLayout(layout)

        group = QGroupBox("Chunk Settings")
        group_layout = QVBoxLayout()
        group.setLayout(group_layout)
        layout.addWidget(group)

        # Chunk size
        chunk_size_layout = QHBoxLayout()
        chunk_size_layout.addWidget(QLabel("Chunk Size (words):"))
        self.chunk_size_entry = QLineEdit(str(self.parent.config.settings["chunk_size"]))
        self.chunk_size_entry.setStyleSheet("background: #2e2e3f; padding: 5px;")
        chunk_size_layout.addWidget(self.chunk_size_entry)
        group_layout.addLayout(chunk_size_layout)

        # Chunk overlap
        chunk_overlap_layout = QHBoxLayout()
        chunk_overlap_layout.addWidget(QLabel("Chunk Overlap (words):"))
        self.chunk_overlap_entry = QLineEdit(str(self.parent.config.settings["chunk_overlap"]))
        self.chunk_overlap_entry.setStyleSheet("background: #2e2e3f; padding: 5px;")
        chunk_overlap_layout.addWidget(self.chunk_overlap_entry)
        group_layout.addLayout(chunk_overlap_layout)

        # Retry count
        retry_layout = QHBoxLayout()
        retry_layout.addWidget(QLabel("Retry Count:"))
        self.retry_entry = QLineEdit(str(self.parent.config.settings["retry_count"]))
        self.retry_entry.setStyleSheet("background: #2e2e3f; padding: 5px;")
        retry_layout.addWidget(self.retry_entry)
        group_layout.addLayout(retry_layout)

        # Description
        desc = QLabel("Chunk size and overlap are in words. Retry count is for transcript extraction.")
        desc.setStyleSheet("color: #a0a0c0; font-size: 10pt; margin-top: 10px;")
        group_layout.addWidget(desc)

        return tab

    def create_processing_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        tab.setLayout(layout)

        group = QGroupBox("Processing Settings")
        group_layout = QVBoxLayout()
        group.setLayout(group_layout)
        layout.addWidget(group)

        # Ollama model
        model_layout = QHBoxLayout()
        model_layout.addWidget(QLabel("Ollama Model:"))
        self.ollama_model_entry = QLineEdit(self.parent.config.settings["ollama_model"])
        self.ollama_model_entry.setStyleSheet("background: #2e2e3f; padding: 5px;")
        model_layout.addWidget(self.ollama_model_entry)
        group_layout.addLayout(model_layout)

        # Processing prompt
        group_layout.addWidget(QLabel("Processing Prompt:"))
        self.processing_prompt_entry = QTextEdit()
        self.processing_prompt_entry.setPlainText(self.parent.config.settings["processing_prompt"])
        self.processing_prompt_entry.setStyleSheet("background: #2e2e3f; padding: 5px; min-height: 150px;")
        group_layout.addWidget(self.processing_prompt_entry)

        # Description
        desc = QLabel("This prompt will be sent to Ollama with each chunk of text.")
        desc.setStyleSheet("color: #a0a0c0; font-size: 10pt; margin-top: 10px;")
        group_layout.addWidget(desc)

        return tab

    def create_output_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        tab.setLayout(layout)

        group = QGroupBox("Output Settings")
        group_layout = QVBoxLayout()
        group.setLayout(group_layout)
        layout.addWidget(group)

        # Output format
        format_layout = QHBoxLayout()
        format_layout.addWidget(QLabel("Output Format:"))
        self.output_format_combo = QComboBox()
        self.output_format_combo.addItems(["docx", "txt"])
        self.output_format_combo.setCurrentText(self.parent.config.settings["output_format"])
        self.output_format_combo.setStyleSheet("background: #2e2e3f; padding: 5px;")
        format_layout.addWidget(self.output_format_combo)
        group_layout.addLayout(format_layout)

        # Checkboxes
        checkbox_layout = QHBoxLayout()

        self.skip_name_check = QCheckBox("Skip Manual Naming")
        checkbox_layout.addWidget(self.skip_name_check)

        self.include_title_check = QCheckBox("Include Title")
        checkbox_layout.addWidget(self.include_title_check)

        group_layout.addLayout(checkbox_layout)

        # Title settings
        title_size_layout = QHBoxLayout()
        title_size_layout.addWidget(QLabel("Title Font Size:"))
        self.title_size_entry = QLineEdit(str(self.parent.config.settings["title_font_size"]))
        self.title_size_entry.setStyleSheet("background: #2e2e3f; padding: 5px;")
        title_size_layout.addWidget(self.title_size_entry)
        group_layout.addLayout(title_size_layout)

        custom_title_layout = QHBoxLayout()
        custom_title_layout.addWidget(QLabel("Custom Title:"))
        self.custom_title_entry = QLineEdit(self.parent.config.settings["custom_title"])
        self.custom_title_entry.setStyleSheet("background: #2e2e3f; padding: 5px;")
        custom_title_layout.addWidget(self.custom_title_entry)
        group_layout.addLayout(custom_title_layout)

        # Typewriter speed
        speed_layout = QHBoxLayout()
        speed_layout.addWidget(QLabel("Typewriter Speed (ms):"))
        self.speed_entry = QLineEdit(str(self.parent.config.settings["typewriter_speed"]))
        self.speed_entry.setStyleSheet("background: #2e2e3f; padding: 5px;")
        speed_layout.addWidget(self.speed_entry)
        group_layout.addLayout(speed_layout)

        # Description
        desc = QLabel("Leave custom title blank to use filename as title.")
        desc.setStyleSheet("color: #a0a0c0; font-size: 10pt; margin-top: 10px;")
        group_layout.addWidget(desc)

        return tab

    def save_settings(self):
        try:
            self.parent.config.settings["chunk_size"] = int(self.chunk_size_entry.text())
            self.parent.config.settings["chunk_overlap"] = int(self.chunk_overlap_entry.text())
            self.parent.config.settings["retry_count"] = int(self.retry_entry.text())
            self.parent.config.settings["ollama_model"] = self.ollama_model_entry.text().strip()
            self.parent.config.settings["processing_prompt"] = self.processing_prompt_entry.toPlainText().strip()
            self.parent.config.settings["output_format"] = self.output_format_combo.currentText()
            self.parent.config.settings["skip_manual_name"] = self.skip_name_check.isChecked()
            self.parent.config.settings["include_docx_title"] = self.include_title_check.isChecked()
            self.parent.config.settings["title_font_size"] = int(self.title_size_entry.text())
            self.parent.config.settings["custom_title"] = self.custom_title_entry.text().strip()
            self.parent.config.settings["typewriter_speed"] = int(self.speed_entry.text())

            self.parent.config.save_config()
            self.status_label.setText("Settings saved successfully.")
            self.status_label.setStyleSheet("color: #b5e0c8;")
            self.parent.config.clean_temp()
        except ValueError:
            self.status_label.setText("Error: Numeric values must be integers.")
            self.status_label.setStyleSheet("color: #ff7373;")

    def back_to_menu(self):
        self.parent.config.clean_temp()
        self.parent.show_screen("menu")


class HistoryScreen(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        title = QLabel("History")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24pt; color: #e0e0e0;")
        layout.addWidget(title)
        
        # Back button
        back_btn = QPushButton("Back to Menu")
        back_btn.setStyleSheet(self.parent.menu_screen.get_button_style())
        back_btn.clicked.connect(lambda: self.parent.show_screen("menu"))
        layout.addWidget(back_btn, alignment=Qt.AlignLeft)
        
        # History list
        self.history_list = QListWidget()
        self.history_list.setStyleSheet("""
            QListWidget {
                background-color: #2e2e3f;
                color: white;
                border-radius: 5px;
                padding: 10px;
            }
            QListWidget::item {
                padding: 10px;
                border-bottom: 1px solid #3d3d5e;
            }
            QListWidget::item:selected {
                background-color: #5a5a8a;
            }
        """)
        self.history_list.itemDoubleClicked.connect(self.load_history_item)
        layout.addWidget(self.history_list)
        
        # Load history
        self.load_history()
    
    def load_history(self):
        self.history_list.clear()
        history = self.parent.config.load_history()
        
        # Ensure history is a list
        if not isinstance(history, list):
            history = []
            
        for entry in history:
            # Skip if entry is not a dictionary
            if not isinstance(entry, dict):
                continue
                
            title = entry.get('title', '')
            url = entry.get('url', '')
            date = entry.get('date', '')
            item_text = f"{title}\nURL: {url}\nDate: {date}"
            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, url)
            self.history_list.addItem(item)
    
    def load_history_item(self, item):
        url = item.data(Qt.UserRole)
        self.parent.show_screen("start")
        self.parent.start_screen.url_entry.setText(url)
        self.parent.start_screen.on_submit()
