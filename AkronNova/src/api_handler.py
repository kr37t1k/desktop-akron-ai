"""
API Handler for AkronNova
Manages communication with TTS, LLM, and voice input systems
"""
import queue
import requests
import json
import threading
import time
from typing import Dict, Any, Optional
from config_loader import ConfigLoader


class APIHandler:
    def __init__(self, config_path: str = "../config/settings.json"):
        self.config = ConfigLoader(config_path)
        self.conversation_history = []
        self.stt_working = False
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

    def _make_request(self, payload):
        """Internal method to make the actual request"""
        try:
            start_time = time.time()

            response = requests.post(
                self.llm_url,
                headers={
                    "Content-Type": "application/json",
                    "Connection": "close",  # Close connection after request
                    "User-Agent": "VoiceAssistant/1.0"
                },
                json=payload,
                timeout=120,
                allow_redirects=False
            )

            self.last_response_time = time.time()

            print(f"Task done for {time.time()-start_time} seconds")
            return response
        except Exception as e:
            raise e
    def chat(self, user_message):
        """
        Chat method with threading to prevent blocking
        """
        # Add user message to conversation history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })

        # Prepare the request payload
        payload = {
            "model": "local-model",  # This can be adjusted based on your model
            "messages": self.conversation_history,
            "temperature": 0.7,
            "max_tokens": 300,
            "stream": False
        }

        # Make the request in a separate thread to prevent blocking
        response_queue = queue.Queue()

        def make_request():
            try:
                # Use connection state to make request
                response = self._make_request(payload)

                if response.status_code == 200:
                    try:
                        result = response.json()
                        ai_response = result['choices'][0]['message']['content']

                        # Add AI response to conversation history
                        self.conversation_history.append({
                            "role": "assistant",
                            "content": ai_response
                        })

                        response_queue.put(('success', ai_response))
                    except (KeyError, IndexError, json.JSONDecodeError) as e:
                        print(f"Error parsing AI response: {e}")
                        print(f"Raw response: {response.text[:500]}...")  # First 500 chars
                        response_queue.put(('error', "Sorry, I received an invalid response from the AI server."))
                else:
                    print(f"Error from local AI server: {response.status_code} - {response.text}")
                    response_queue.put(('error', "Sorry, I couldn't get a response from the local AI server."))
            except requests.exceptions.ConnectionError:
                response_queue.put(
                    ('error', "Error: Cannot connect to local AI server. Please make sure it's running on your phone."))
            except requests.exceptions.Timeout:
                response_queue.put(('error', "Error: Local AI server request timed out."))
            except requests.exceptions.RequestException as e:
                print(f"Request error: {e}")
                response_queue.put(('error', f"Error making request to local AI: {str(e)}"))
            except Exception as e:
                print(f"Error in local chat: {e}")
                response_queue.put(('error', "Sorry, there was an error communicating with the local AI."))

        # Start the request in a separate thread
        thread = threading.Thread(target=make_request)
        thread.daemon = True
        thread.start()
        print(self.conversation_history[-1])

        # Return immediately with a placeholder or wait for response based on implementation needs
        # For voice assistant, we might want to wait for the response
        try:
            result_type, result = response_queue.get(timeout=120)
            if result_type == 'success':
                return result
            else:
                return result
        except queue.Empty:
            return "Request timed out waiting for AI response."


class AsyncAPIHandler(APIHandler):
    """API Handler with async capabilities"""
    
    def __init__(self, config_path: str = "../config/settings.json"):
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
        
    def call_llm_async(self, prompt: str, callback=None):
        """Call LLM system asynchronously"""
        def _llm_worker():
            result = self.chat(prompt)
            if callback:
                callback(result)
                
        thread = threading.Thread(target=_llm_worker)
        thread.daemon = True
        thread.start()
        return thread