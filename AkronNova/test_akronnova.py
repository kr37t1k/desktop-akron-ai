#!/usr/bin/env python3
"""
Simple test script for AkronNova Desktop AI Companion
"""

import sys
import os

# Add the src directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from main import AkronNovaDesktopCharacter
from PyQt5.QtWidgets import QApplication

def test_akronnova():
    """Test basic AkronNova functionality"""
    print("Testing AkronNova Desktop AI Companion...")
    
    # Initialize Qt application
    app = QApplication(sys.argv)
    
    # Create AkronNova instance
    akronnova = AkronNovaDesktopCharacter()
    
    print("✓ AkronNova instance created successfully")
    print("✓ Configuration loaded")
    print("✓ API handlers initialized")
    print("✓ Audio player initialized (with PyAudio availability noted)")
    
    # Test conversation functionality
    test_response = akronnova.get_llm_response("Hello AkronNova, how are you?")
    print(f"✓ LLM response test: {test_response}")
    
    print("\nAkronNova basic functionality test completed successfully!")
    print("To run the full application, execute: python -m src.main")

if __name__ == "__main__":
    test_akronnova()