"""
AkronNova - Animated Desktop AI Companion
Main application file
"""

import sys
import os
import logging
# Add the current directory to the path to allow imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set environment variables to address DirectComposition issues and GLES3 context errors
os.environ['QTWEBENGINE_DISABLE_DIRECT_COMPOSITION'] = '1'
os.environ['QT_ENABLE_HIGHDPI_SCALING'] = '1'
os.environ['QT_QUICK_BACKEND'] = 'software'
os.environ['QT_OPENGL'] = 'software'
os.environ['QTWEBENGINE_CHROMIUM_FLAGS'] = '--disable-gpu --disable-software-rasterizer --disable-gpu-sandbox --disable-extensions --disable-plugins --disable-images --disable-web-security'
os.environ['QTWEBENGINE_DISABLE_GPU'] = '1'
os.environ['DISABLE_GPU'] = '1'

from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt, QPoint, QTimer
from PyQt6.QtGui import QPixmap, QPainter, QPen, QColor, QGuiApplication, QMouseEvent
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineProfile
from PyQt6.QtCore import QUrl

from api_handler import AsyncAPIHandler
from tts_module import TTSModule
from stt_module import STTModule
from config_loader import ConfigLoader
from live2d_handler import Live2DIntegration, Live2DWebView

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def asset_path(path: str):
    assets_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets')
    return os.path.join(assets_dir, path)

# print(asset_path('live2d_model.zip'), "Exists " if os.path.exists(asset_path('live2d_model.zip')) else "Doesn't exist")

class AkronNovaDesktopCharacter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.config = ConfigLoader("../config/settings.json")
        self.api_handler = AsyncAPIHandler()
        self.conversation_history = []
        
        # Initialize Live2D integration
        self.live2d_integration = Live2DIntegration()

        self.setup_window()
        self.load_character_assets()
        self.setup_interaction_system()
        self.show_character()

        self.tts_module = TTSModule
        self.stt_module = STTModule

        self.init_tts_module()
        self.init_stt_module()

    def setup_window(self):
        """Setup the desktop overlay window"""
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool |
            Qt.WindowType.X11BypassWindowManagerHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowOpacity(1.0)
        
        # Make it click-through except for interaction area
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False)
        
    def load_character_assets(self):
        """Load character assets - now using Live2D web view"""
        # Use Live2D web view instead of static image
        self.live2d_view = Live2DWebView(self)
        
        # Set up the layout to contain the Live2D view
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.live2d_view)
        
        # Set initial size for the Live2D view
        self.live2d_view.setFixedSize(400, 500)
        
        # Keep references to both old and new systems for compatibility
        self.current_widget = self.live2d_view
        
    def create_placeholder_image(self):
        """Create a placeholder image for AkronNova"""
        size = 200
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.GlobalColor.transparent)

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw a simple character representation
        painter.setBrush(QColor(255, 182, 193))  # Light pink
        painter.setPen(QPen(QColor(255, 105, 180), 3))  # Hot pink border
        painter.drawEllipse(50, 20, 100, 100)  # Head

        # Draw simple face
        painter.setBrush(QColor(255, 255, 255))
        painter.drawEllipse(75, 45, 15, 15)  # Left eye
        painter.drawEllipse(110, 45, 15, 15)  # Right eye
        painter.setBrush(QColor(0, 0, 0))
        painter.drawEllipse(80, 50, 5, 5)   # Left eye pupil
        painter.drawEllipse(115, 50, 5, 5)  # Right eye pupil

        painter.setPen(QPen(QColor(255, 105, 180), 2))
        painter.drawArc(90, 70, 20, 10, 0, -180 * 16)  # Smile

        painter.end()
        
        self.character_image = pixmap
        
    def setup_interaction_system(self):
        """Setup interaction with your TTS and LLM systems"""
        # Interaction state
        self.is_listening = False
        
        # Setup mouse event handling
        self.dragging = False
        self.offset = QPoint()
        
        # Animation timer
        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(self.animate_character)
        self.animation_timer.start(100)  # Update every 100ms

    def init_tts_module(self):
        self.tts_module = TTSModule()
    def init_stt_module(self):
        self.stt_module = STTModule()

    def mousePressEvent(self, event):
        """Handle mouse press for dragging and interaction"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = True
            self.offset = event.pos()
        elif event.button() == Qt.MouseButton.RightButton:
            # Right click could trigger conversation
            self.start_conversation()
            
    def mouseMoveEvent(self, event:QMouseEvent):
        """Handle window dragging"""
        if self.dragging:
            new_pos = self.mapToParent(event.pos() - self.offset)
            self.move(new_pos)
            
    def mouseReleaseEvent(self, event):
        """Handle mouse release"""
        self.dragging = False
        
    def show_character(self):
        """Position and show the character on screen"""
        # Position at bottom right of screen
        screen_geometry = QGuiApplication.primaryScreen().geometry()
        x = screen_geometry.width() - 400 - 20  # 400 is the width of the Live2D view
        y = screen_geometry.height() - 500 - 100  # 500 is the height of the Live2D view
        
        self.setGeometry(x, y, 400, 500)
        self.show()
        
    def animate_character(self):
        """Live2D animation for idle state"""
        # This now properly handles Live2D animations through the web view
        # In a real implementation, this would send animation commands to the Live2D model
        pass
        
    def start_conversation(self):
        """Start a conversation with AkronNova"""
        print("Starting conversation with AkronNova...")
        # In a real implementation, this would capture voice input or show a text input
        # For now, we'll simulate a simple conversation with emotion tags
        self.talk_to_user("Hey-y+o I'm Akr+onNov+a, your cute e-g+irl. [joy] How about dreaming about a jooo+oob or cons+uming som+e ice cr+eam??")
        
    def talk_to_user(self, message):
        """Make AkronNova speak to the user"""
        print(f"AkronNova says: {message}")
        
        # Process the message for emotions and update Live2D model
        emotions, clean_message = self.live2d_integration.process_text_for_emotions(message)
        if emotions:
            # Set the first emotion found, or default to neutral (0)
            emotion_index = emotions[0] if emotions else 0
            self.live2d_integration.set_emotion(emotion_index)
            print(f"Applied emotion index: {emotion_index}")
            
            # Update the Live2D model in the web view
            if hasattr(self, 'live2d_view'):
                self.live2d_view.set_emotion(emotion_index)
        
        # Speak the clean message (without emotion tags)
        self.tts_module.synth(text=str(clean_message))
            
    def get_llm_response(self, user_input):
        """Get response from LLM system"""
        try:
            response = self.api_handler.chat(user_input)
            if response:
                self.conversation_history.append({"user": user_input, "akronnova": response})
                return response
            else:
                return "I'm having trouble connecting to my brain right now."
        except Exception as e:
            print(f"LLM error: {e}")
            return "Sorry, I'm experiencing some technical difficulties."
            
    def update_character_state(self, state):
        """Update character's visual state (happy, thinking, talking, etc.)"""
        # This would switch between different Live2D animations/models
        pass


def main():
    app = QApplication(sys.argv)
    pet = AkronNovaDesktopCharacter()
    
    # Set application properties
    app.setApplicationName("AkronNova")
    app.setApplicationVersion("0.2")
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
