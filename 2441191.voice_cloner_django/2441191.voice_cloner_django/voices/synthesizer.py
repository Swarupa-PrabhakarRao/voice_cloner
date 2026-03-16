"""
Voice Synthesizer Module
Handles text-to-speech conversion using pyttsx3
"""
import pyttsx3
import os
from django.conf import settings
from django.core.files import File
import wave
import contextlib


class VoiceSynthesizer:
    """Text-to-speech synthesizer"""
    
    def __init__(self):
        self.engine = pyttsx3.init()
        
    def synthesize(self, text, speed=150, pitch=50, volume=1.0, output_path=None):
        """
        Convert text to speech
        
        Args:
            text: Text to convert
            speed: Speech speed (words per minute)
            pitch: Voice pitch (0-100)
            volume: Volume level (0.0-1.0)
            output_path: Path to save audio file
            
        Returns:
            Path to generated audio file
        """
        # Configure voice settings
        self.engine.setProperty('rate', speed)
        self.engine.setProperty('volume', volume)
        
        # Get available voices
        voices = self.engine.getProperty('voices')
        if voices:
            # Adjust pitch by selecting different voice if available
            voice_index = min(int(pitch / 50), len(voices) - 1)
            self.engine.setProperty('voice', voices[voice_index].id)
        
        # Generate audio file
        if output_path is None:
            output_path = os.path.join(settings.MEDIA_ROOT, 'temp_voice.mp3')
        
        self.engine.save_to_file(text, output_path)
        self.engine.runAndWait()
        
        return output_path
    
    def get_duration(self, audio_file_path):
        """
        Get duration of audio file in seconds
        
        Args:
            audio_file_path: Path to audio file
            
        Returns:
            Duration in seconds
        """
        try:
            with contextlib.closing(wave.open(audio_file_path, 'r')) as f:
                frames = f.getnframes()
                rate = f.getframerate()
                duration = frames / float(rate)
                return round(duration, 2)
        except:
            # If not a WAV file or error, return 0
            return 0.0
    
    def cleanup(self):
        """Clean up engine resources"""
        try:
            self.engine.stop()
        except:
            pass
