"""
Audio player for AkronNova
Handles playing audio responses from TTS system
"""

import io
import threading
from typing import Optional
import wave

try:
    import pyaudio
    PYAUDIO_AVAILABLE = True
except ImportError:
    PYAUDIO_AVAILABLE = False
    print("PyAudio not available. Audio playback will be disabled.")


class AudioPlayer:
    def __init__(self):
        self.pyaudio_instance = None
        self.stream = None
        self.is_playing = False
        
        if PYAUDIO_AVAILABLE:
            self.pyaudio_instance = pyaudio.PyAudio()
        
    def play_audio(self, audio_data: bytes):
        """Play audio data from TTS system"""
        if not PYAUDIO_AVAILABLE:
            print("Cannot play audio: PyAudio not available")
            return False
            
        if self.is_playing:
            print("Audio is already playing")
            return False
            
        try:
            self.is_playing = True
            
            # Create a wave file from audio data
            wf = wave.open(io.BytesIO(audio_data), 'rb')
            
            # Open stream
            self.stream = self.pyaudio_instance.open(
                format=self.pyaudio_instance.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True
            )
            
            # Play audio
            chunk_size = 1024
            data = wf.readframes(chunk_size)
            
            while data and self.is_playing:
                self.stream.write(data)
                data = wf.readframes(chunk_size)
                
            # Stop and close stream
            self.stream.stop_stream()
            self.stream.close()
            wf.close()
            
            self.is_playing = False
            return True
            
        except Exception as e:
            print(f"Error playing audio: {e}")
            self.is_playing = False
            return False
            
    def stop_audio(self):
        """Stop currently playing audio"""
        self.is_playing = False
        if self.stream and not self.stream.is_stopped():
            self.stream.stop_stream()
            self.stream.close()
            
    def __del__(self):
        """Cleanup on destruction"""
        if hasattr(self, 'stream') and self.stream:
            try:
                if not self.stream.is_stopped():
                    self.stream.stop_stream()
                self.stream.close()
            except:
                pass
                
        if hasattr(self, 'pyaudio_instance') and self.pyaudio_instance:
            self.pyaudio_instance.terminate()


class AsyncAudioPlayer(AudioPlayer):
    """Audio player with async capabilities"""
    
    def __init__(self):
        super().__init__()
        self.playback_thread = None
        
    def play_audio_async(self, audio_data: bytes, on_complete=None):
        """Play audio asynchronously"""
        def _play_worker():
            success = self.play_audio(audio_data)
            if on_complete:
                on_complete(success)
                
        self.playback_thread = threading.Thread(target=_play_worker)
        self.playback_thread.daemon = True
        self.playback_thread.start()
        return self.playback_thread