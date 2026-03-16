"""
Django Admin Configuration for Voice Cloner
"""
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import VoiceProfile, Voice


@admin.register(VoiceProfile)
class VoiceProfileAdmin(admin.ModelAdmin):
    """Admin for Voice Profiles"""
    list_display = ['name', 'user', 'get_voice_count', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'user__username', 'description']
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = 20
    
    fieldsets = (
        ('Profile Information', {
            'fields': ('user', 'name', 'description')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_voice_count(self, obj):
        return obj.get_voice_count()
    get_voice_count.short_description = 'Voices'


@admin.register(Voice)
class VoiceAdmin(admin.ModelAdmin):
    """Admin for Voices"""
    list_display = ['id', 'profile', 'text_preview', 'duration', 'get_file_size', 'created_at']
    list_filter = ['created_at', 'profile__user']
    search_fields = ['text', 'profile__name', 'profile__user__username']
    readonly_fields = ['created_at', 'duration', 'get_file_size']
    list_per_page = 20
    
    fieldsets = (
        ('Voice Information', {
            'fields': ('profile', 'text')
        }),
        ('Audio Settings', {
            'fields': ('speed', 'pitch', 'volume', 'audio_file')
        }),
        ('Metadata', {
            'fields': ('duration', 'created_at'),
            'classes': ('collapse',)
        }),
    )
    
    def text_preview(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_preview.short_description = 'Text'
    
    def get_file_size(self, obj):
        size = obj.get_file_size()
        return f'{size} MB' if size > 0 else 'N/A'
    get_file_size.short_description = 'File Size'
    
    actions = ['delete_selected_voices']
    
    def delete_selected_voices(self, request, queryset):
        """Delete selected voices and their audio files"""
        count = 0
        for voice in queryset:
            if voice.audio_file:
                voice.audio_file.delete()
            voice.delete()
            count += 1
        self.message_user(request, f'{count} voice(s) deleted successfully.')
    delete_selected_voices.short_description = 'Delete selected voices'


# Customize User Admin
class CustomUserAdmin(BaseUserAdmin):
    """Enhanced User Admin"""
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'get_voice_count']
    
    def get_voice_count(self, obj):
        return Voice.objects.filter(profile__user=obj).count()
    get_voice_count.short_description = 'Total Voices'


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Customize admin site
admin.site.site_header = 'Voice Cloner Admin'
admin.site.site_title = 'Voice Cloner Admin Portal'
admin.site.index_title = 'Welcome to Voice Cloner Administration'
