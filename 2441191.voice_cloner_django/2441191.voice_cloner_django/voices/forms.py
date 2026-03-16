"""
Voice Management Forms
"""
from django import forms
from .models import VoiceProfile, Voice


class VoiceProfileForm(forms.ModelForm):
    """Form for creating/editing voice profiles"""
    class Meta:
        model = VoiceProfile
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Profile name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Description (optional)',
                'rows': 3
            }),
        }


class VoiceCreationForm(forms.ModelForm):
    """Form for creating voices"""
    class Meta:
        model = Voice
        fields = ['text', 'speed', 'pitch', 'volume']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter text to convert to speech...',
                'rows': 5
            }),
            'speed': forms.NumberInput(attrs={
                'class': 'form-range',
                'min': 50,
                'max': 300,
                'value': 150
            }),
            'pitch': forms.NumberInput(attrs={
                'class': 'form-range',
                'min': 0,
                'max': 100,
                'value': 50
            }),
            'volume': forms.NumberInput(attrs={
                'class': 'form-range',
                'min': 0,
                'max': 1,
                'step': 0.1,
                'value': 1.0
            }),
        }
