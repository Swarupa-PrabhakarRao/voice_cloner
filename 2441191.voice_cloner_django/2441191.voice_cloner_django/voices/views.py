"""
Voice Management Views
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.files.base import ContentFile
from django.http import JsonResponse, FileResponse
from .models import VoiceProfile, Voice
from .forms import VoiceProfileForm, VoiceCreationForm
from .synthesizer import VoiceSynthesizer
import os


@login_required
def dashboard_view(request):
    """User dashboard"""
    profiles = VoiceProfile.objects.filter(user=request.user, is_active=True)
    recent_voices = Voice.objects.filter(profile__user=request.user)[:5]
    
    # Statistics
    total_voices = Voice.objects.filter(profile__user=request.user).count()
    total_profiles = profiles.count()
    
    context = {
        'profiles': profiles,
        'recent_voices': recent_voices,
        'total_voices': total_voices,
        'total_profiles': total_profiles,
    }
    return render(request, 'voices/dashboard.html', context)


@login_required
def create_voice_view(request):
    """Create new voice"""
    profiles = VoiceProfile.objects.filter(user=request.user, is_active=True)
    
    # Create default profile if none exists
    if not profiles.exists():
        VoiceProfile.objects.create(
            user=request.user,
            name="My Voices",
            description="Default voice profile"
        )
        profiles = VoiceProfile.objects.filter(user=request.user, is_active=True)
    
    if request.method == 'POST':
        form = VoiceCreationForm(request.POST)
        profile_id = request.POST.get('profile')
        
        if form.is_valid() and profile_id:
            profile = get_object_or_404(VoiceProfile, id=profile_id, user=request.user)
            
            # Create voice instance
            voice = form.save(commit=False)
            voice.profile = profile
            
            # Generate speech
            try:
                synthesizer = VoiceSynthesizer()
                output_path = synthesizer.synthesize(
                    text=voice.text,
                    speed=voice.speed,
                    pitch=voice.pitch,
                    volume=voice.volume
                )
                
                # Get duration
                voice.duration = synthesizer.get_duration(output_path)
                
                # Save audio file
                with open(output_path, 'rb') as f:
                    voice.audio_file.save(
                        f'voice_{voice.profile.id}_{voice.id}.mp3',
                        ContentFile(f.read()),
                        save=False
                    )
                
                voice.save()
                
                # Cleanup
                synthesizer.cleanup()
                if os.path.exists(output_path):
                    os.remove(output_path)
                
                messages.success(request, 'Voice created successfully!')
                return redirect('voice_list')
                
            except Exception as e:
                messages.error(request, f'Error generating voice: {str(e)}')
    else:
        form = VoiceCreationForm()
    
    context = {
        'form': form,
        'profiles': profiles,
    }
    return render(request, 'voices/create_voice.html', context)


@login_required
def voice_list_view(request):
    """List all user's voices"""
    voices = Voice.objects.filter(profile__user=request.user)
    profiles = VoiceProfile.objects.filter(user=request.user, is_active=True)
    
    # Filter by profile if specified
    profile_id = request.GET.get('profile')
    if profile_id:
        voices = voices.filter(profile_id=profile_id)
    
    # Search
    search_query = request.GET.get('search')
    if search_query:
        voices = voices.filter(text__icontains=search_query)
    
    context = {
        'voices': voices,
        'profiles': profiles,
        'selected_profile': profile_id,
        'search_query': search_query,
    }
    return render(request, 'voices/voice_list.html', context)


@login_required
def delete_voice_view(request, voice_id):
    """Delete a voice"""
    voice = get_object_or_404(Voice, id=voice_id, profile__user=request.user)
    
    if request.method == 'POST':
        # Delete audio file
        if voice.audio_file:
            voice.audio_file.delete()
        voice.delete()
        messages.success(request, 'Voice deleted successfully!')
        return redirect('voice_list')
    
    return render(request, 'voices/delete_voice.html', {'voice': voice})


@login_required
def download_voice_view(request, voice_id):
    """Download voice audio file"""
    voice = get_object_or_404(Voice, id=voice_id, profile__user=request.user)
    
    if voice.audio_file:
        response = FileResponse(voice.audio_file.open('rb'))
        response['Content-Disposition'] = f'attachment; filename="voice_{voice.id}.mp3"'
        return response
    
    messages.error(request, 'Audio file not found!')
    return redirect('voice_list')


@login_required
def profile_list_view(request):
    """List voice profiles"""
    profiles = VoiceProfile.objects.filter(user=request.user)
    return render(request, 'voices/profile_list.html', {'profiles': profiles})


@login_required
def create_profile_view(request):
    """Create voice profile"""
    if request.method == 'POST':
        form = VoiceProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, 'Profile created successfully!')
            return redirect('profile_list')
    else:
        form = VoiceProfileForm()
    
    return render(request, 'voices/create_profile.html', {'form': form})
