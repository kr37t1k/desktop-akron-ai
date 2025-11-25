"""
AkronNova - Animated Desktop AI Companion
Main application file
"""

import sys
import os
# Add the current directory to the path to allow imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QDesktopWidget
from PyQt5.QtCore import Qt, QPoint, QTimer
from PyQt5.QtGui import QPixmap, QPainter, QPen, QColor

# Try relative imports first, then absolute imports
try:
    from .api_handler import AsyncAPIHandler
    from .audio_player import AsyncAudioPlayer
    from .config_loader import ConfigLoader
except ImportError:
    from api_handler import AsyncAPIHandler
    from audio_player import AsyncAudioPlayer
    from config_loader import ConfigLoader


class AkronNovaDesktopCharacter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.config = ConfigLoader("/workspace/AkronNova/config/settings.json")
        self.api_handler = AsyncAPIHandler()
        self.audio_player = AsyncAudioPlayer()
        self.conversation_history = []
        
        self.setup_window()
        self.load_character_assets()
        self.setup_interaction_system()
        self.show_character()
        
    def setup_window(self):
        """Setup the desktop overlay window"""
        self.setWindowFlags(
            Qt.FramelessWindowHint | 
            Qt.WindowStaysOnTopHint | 
            Qt.Tool | 
            Qt.X11BypassWindowManagerHint
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowOpacity(1.0)
        
        # Make it click-through except for interaction area
        self.setAttribute(Qt.WA_TransparentForMouseEvents, False)
        
    def load_character_assets(self):
        """Load character images and animations"""
        # Default character image - this will be replaced with your Live2D model later
        self.character_image = QPixmap("/workspace/AkronNova/assets/akronnova_default.png")
        if self.character_image.isNull():
            # Create a placeholder if no image exists
            self.create_placeholder_image()
        
        self.current_image = self.character_image
        self.label = QLabel(self)
        self.label.setPixmap(self.current_image)
        self.label.resize(self.current_image.size())
        
    def create_placeholder_image(self):
        """Create a placeholder image for AkronNova"""
        size = 200
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
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
        
    def mousePressEvent(self, event):
        """Handle mouse press for dragging and interaction"""
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.offset = event.pos()
        elif event.button() == Qt.RightButton:
            # Right click could trigger conversation
            self.start_conversation()
            
    def mouseMoveEvent(self, event):
        """Handle window dragging"""
        if self.dragging:
            self.move(event.globalPos() - self.offset)
            
    def mouseReleaseEvent(self, event):
        """Handle mouse release"""
        self.dragging = False
        
    def show_character(self):
        """Position and show the character on screen"""
        # Position at bottom right of screen
        screen_geometry = QDesktopWidget().screenGeometry()
        x = screen_geometry.width() - self.current_image.width() - 20
        y = screen_geometry.height() - self.current_image.height() - 100
        
        self.setGeometry(x, y, self.current_image.width(), self.current_image.height())
        self.show()
        
    def animate_character(self):
        """Simple animation for idle state"""
        # This would be expanded to include Live2D animations
        pass
        
    def start_conversation(self):
        """Start a conversation with AkronNova"""
        print("Starting conversation with AkronNova...")
        # In a real implementation, this would capture voice input or show a text input
        # For now, we'll simulate a simple conversation
        self.talk_to_user("Hello! I'm AkronNova, your desktop companion. How can I help you today?")
        
    def talk_to_user(self, message):
        """Make AkronNova speak to the user"""
        print(f"AkronNova says: {message}")
        
        # Send message to TTS system using our API handler
        def on_tts_complete(audio_data):
            if audio_data:
                self.audio_player.play_audio_async(audio_data)
            else:
                print("Failed to get audio from TTS system")
        
        self.api_handler.call_tts_async(message, callback=on_tts_complete)
            
    def get_llm_response(self, user_input):
        """Get response from your LLM system"""
        def on_llm_complete(response):
            if response:
                self.conversation_history.append({"user": user_input, "akronnova": response})
                return response
            else:
                return "I'm having trouble connecting to my brain right now."
        
        # For synchronous response, we'll call it directly
        try:
            response = self.api_handler.call_llm(user_input, self.conversation_history)
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
    akronnova = AkronNovaDesktopCharacter()
    
    # Set application properties
    app.setApplicationName("AkronNova")
    app.setApplicationVersion("1.0")
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()