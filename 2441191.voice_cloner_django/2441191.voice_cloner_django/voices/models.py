"""
Voice Cloner Django Models
"""
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class VoiceProfile(models.Model):
    """Voice profile for organizing user's voices"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='voice_profiles')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.name} - {self.user.username}"
    
    def get_voice_count(self):
        return self.voices.count()


class Voice(models.Model):
    """Generated voice/speech audio"""
    profile = models.ForeignKey(VoiceProfile, on_delete=models.CASCADE, related_name='voices')
    text = models.TextField(help_text="Text that was converted to speech")
    audio_file = models.FileField(upload_to='voices/%Y/%m/%d/')
    duration = models.FloatField(default=0.0, help_text="Duration in seconds")
    
    # Voice settings
    speed = models.IntegerField(default=150, help_text="Speech speed (words per minute)")
    pitch = models.IntegerField(default=50, help_text="Voice pitch (0-100)")
    volume = models.FloatField(default=1.0, help_text="Volume (0.0-1.0)")
    
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.profile.name} - {self.text[:50]}"
    
    def get_file_size(self):
        """Get file size in MB"""
        if self.audio_file:
            return round(self.audio_file.size / (1024 * 1024), 2)
        return 0
