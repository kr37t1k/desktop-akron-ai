"""
API Handler for AkronNova
Manages communication with TTS, LLM, and voice input systems
"""

import requests
import json
import threading
from typing import Dict, Any, Optional

# Try relative imports first, then absolute imports
try:
    from .config_loader import ConfigLoader
except ImportError:
    from config_loader import ConfigLoader


class APIHandler:
    def __init__(self, config_path: str = "/workspace/AkronNova/config/settings.json"):
        self.config = ConfigLoader(config_path)
        self.tts_url = self.config.get("api_endpoints.tts_server")
        self.llm_url = self.config.get("api_endpoints.llm_server")
        self.voice_input_url = self.config.get("api_endpoints.voice_input")
        
    def call_tts(self, text: str) -> Optional[bytes]:
        """Call TTS system to generate audio from text"""
        try:
            payload = {
                "text": text,
                "voice": "default"  # Adjust based on your STTS system
            }
            response = requests.post(self.tts_url, json=payload, timeout=30)
            if response.status_code == 200:
                return response.content
            else:
                print(f"TTS request failed with status {response.status_code}: {response.text}")
                return None
        except Exception as e:
            print(f"Error calling TTS: {e}")
            return None
            
    def call_llm(self, prompt: str, history: list = None) -> Optional[str]:
        """Call LLM system to generate response"""
        try:
            payload = {
                "prompt": prompt,
                "history": history or [],
                "max_tokens": 200,
                "temperature": 0.7
            }
            response = requests.post(self.llm_url, json=payload, timeout=60)
            if response.status_code == 200:
                result = response.json()
                return result.get("response", result.get("text", "I'm not sure how to respond."))
            else:
                print(f"LLM request failed with status {response.status_code}: {response.text}")
                return "I'm having trouble connecting to my brain right now."
        except Exception as e:
            print(f"Error calling LLM: {e}")
            return "Sorry, I'm experiencing some technical difficulties."
            
    def call_voice_input(self) -> Optional[str]:
        """Call voice input system to capture user speech"""
        try:
            response = requests.get(self.voice_input_url, timeout=10)
            if response.status_code == 200:
                result = response.json()
                return result.get("transcript", "")
            else:
                print(f"Voice input request failed with status {response.status_code}")
                return None
        except Exception as e:
            print(f"Error calling voice input: {e}")
            return None


class AsyncAPIHandler(APIHandler):
    """API Handler with async capabilities"""
    
    def __init__(self, config_path: str = "/workspace/AkronNova/config/settings.json"):
        super().__init__(config_path)
        self.response_callbacks = {}
        
    def call_tts_async(self, text: str, callback=None):
        """Call TTS system asynchronously"""
        def _tts_worker():
            result = self.call_tts(text)
            if callback:
                callback(result)
                
        thread = threading.Thread(target=_tts_worker)
        thread.daemon = True
        thread.start()
        return thread
        
    def call_llm_async(self, prompt: str, history: list = None, callback=None):
        """Call LLM system asynchronously"""
        def _llm_worker():
            result = self.call_llm(prompt, history)
            if callback:
                callback(result)
                
        thread = threading.Thread(target=_llm_worker)
        thread.daemon = True
        thread.start()
        return thread