#!/usr/bin/env python3
"""
Validation script for AkronNova Desktop AI Companion
Checks that all modules can be imported and basic functionality works without GUI
"""

import sys
import os

# Add the src directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def validate_modules():
    """Validate that all modules can be imported"""
    print("Validating AkronNova modules...")
    
    # Test imports
    try:
        from main import AkronNovaDesktopCharacter
        print("✓ Main module imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import main module: {e}")
        return False
        
    try:
        from api_handler import APIHandler, AsyncAPIHandler
        print("✓ API handler module imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import API handler module: {e}")
        return False
        
    try:
        from audio_player import AudioPlayer, AsyncAudioPlayer
        print("✓ Audio player module imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import audio player module: {e}")
        return False
        
    try:
        from config_loader import ConfigLoader
        print("✓ Config loader module imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import config loader module: {e}")
        return False
    
    return True

def validate_config():
    """Validate configuration loading"""
    print("\nValidating configuration...")
    
    try:
        from config_loader import ConfigLoader
        config = ConfigLoader("/workspace/AkronNova/config/settings.json")
        
        # Test accessing some config values
        app_name = config.get("app_name")
        if app_name:
            print(f"✓ Configuration loaded successfully: {app_name}")
        else:
            print("✗ Failed to access configuration values")
            return False
            
        # Test API endpoints
        tts_url = config.get("api_endpoints.tts_server")
        llm_url = config.get("api_endpoints.llm_server")
        if tts_url and llm_url:
            print(f"✓ API endpoints configured: TTS at {tts_url}, LLM at {llm_url}")
        else:
            print("✗ Missing API endpoint configuration")
            return False
            
        return True
    except Exception as e:
        print(f"✗ Configuration validation failed: {e}")
        return False

def validate_api_handler():
    """Validate API handler functionality"""
    print("\nValidating API handler...")
    
    try:
        from api_handler import APIHandler
        api_handler = APIHandler()
        
        # Test that it can access config
        if hasattr(api_handler, 'tts_url') and hasattr(api_handler, 'llm_url'):
            print("✓ API handler initialized successfully")
        else:
            print("✗ API handler missing required attributes")
            return False
            
        return True
    except Exception as e:
        print(f"✗ API handler validation failed: {e}")
        return False

def main():
    """Main validation function"""
    print("AkronNova Desktop AI Companion - Setup Validation")
    print("=" * 55)
    
    # Validate modules
    modules_ok = validate_modules()
    
    # Validate configuration
    config_ok = validate_config()
    
    # Validate API handler
    api_ok = validate_api_handler()
    
    print("\n" + "=" * 55)
    if modules_ok and config_ok and api_ok:
        print("✓ All validations passed! AkronNova is ready.")
        print("\nTo run AkronNova:")
        print("1. Make sure your TTS and LLM servers are running")
        print("2. Update config/settings.json with your API endpoints")
        print("3. Run: python -m src.main")
        print("\nFor more information, see README.md")
        return True
    else:
        print("✗ Some validations failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)