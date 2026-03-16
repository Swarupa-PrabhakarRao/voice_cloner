# 🎙️ AI Voice Cloner - Django Web Application

A powerful Django web application for AI-powered voice cloning with text-to-speech synthesis, user authentication, and comprehensive admin management.

## ✨ Features

### User Features
- ✅ **User Registration & Login** - Secure authentication system
- ✅ **Text-to-Speech Synthesis** - Convert text to natural-sounding speech
- ✅ **Voice Customization** - Adjust speed, pitch, and volume
- ✅ **Voice Library** - Save and manage all your generated voices
- ✅ **Audio Playback** - Listen to voices directly in the browser
- ✅ **Download Voices** - Export voices as MP3 files
- ✅ **Voice Profiles** - Organize voices into custom profiles
- ✅ **Search & Filter** - Find voices quickly

### Admin Features
- ✅ **User Management** - View, activate, deactivate, and delete users
- ✅ **Voice Management** - View and delete voices across all users
- ✅ **Usage Statistics** - Monitor total users, voices, and storage
- ✅ **Custom Admin Dashboard** - Enhanced Django admin interface

## 🚀 Installation

### Prerequisites
- Python 3.8+
- pip

### Setup

1. **Navigate to project directory:**
```bash
cd c:\Raghu\2026-colleges\DNR\Projects\anti\voice_cloner_django
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run migrations:**
```bash
python manage.py makemigrations
python manage.py migrate
```

4. **Create superuser (for admin access):**
```bash
python manage.py createsuperuser
```

5. **Run the development server:**
```bash
python manage.py runserver
```

6. **Access the application:**
- Main site: http://127.0.0.1:8000/
- Admin panel: http://127.0.0.1:8000/admin/

## 📖 Usage

### For Users

1. **Register an Account**
   - Go to `/accounts/register/`
   - Fill in username, email, and password
   - Click "Register"

2. **Create a Voice**
   - Click "Create New Voice" from dashboard
   - Enter text to convert
   - Adjust voice settings (speed, pitch, volume)
   - Select a profile
   - Click "Generate Voice"

3. **Manage Voices**
   - View all voices in "My Voices"
   - Play voices directly in browser
   - Download as MP3 files
   - Delete unwanted voices
   - Search and filter by profile

### For Admins

1. **Access Admin Panel**
   - Go to `/admin/`
   - Login with superuser credentials

2. **Manage Users**
   - View all registered users
   - See user statistics (total voices)
   - Activate/deactivate accounts
   - Delete users

3. **Manage Voices**
   - View all voices across users
   - Delete inappropriate content
   - Monitor storage usage
   - Bulk delete voices

## 🏗️ Project Structure

```
voice_cloner_django/
├── manage.py
├── requirements.txt
├── voice_cloner/              # Project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── accounts/                  # User authentication
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   └── urls.py
├── voices/                    # Voice management
│   ├── models.py             # VoiceProfile, Voice models
│   ├── views.py              # CRUD operations
│   ├── forms.py              # Voice creation forms
│   ├── synthesizer.py        # TTS engine
│   ├── admin.py              # Admin configuration
│   └── urls.py
├── templates/
│   ├── base.html             # Base template
│   ├── accounts/             # Auth templates
│   │   ├── register.html
│   │   ├── login.html
│   │   └── profile.html
│   └── voices/               # Voice templates
│       ├── dashboard.html
│       ├── create_voice.html
│       ├── voice_list.html
│       ├── delete_voice.html
│       └── create_profile.html
├── static/                    # Static files (CSS, JS)
└── media/                     # User-generated content
    └── voices/               # Voice audio files
```

## 🎨 Technologies Used

- **Django 4.2** - Web framework
- **pyttsx3** - Text-to-speech engine
- **Bootstrap 5** - Frontend framework
- **SQLite** - Database (development)
- **Crispy Forms** - Form styling

## 🔧 Configuration

### Voice Settings
- **Speed**: 50-300 words per minute (default: 150)
- **Pitch**: 0-100 (default: 50)
- **Volume**: 0.0-1.0 (default: 1.0)

### File Storage
- Audio files are stored in `media/voices/YYYY/MM/DD/`
- Automatic organization by date

## 📊 Database Models

### VoiceProfile
- Links to User
- Contains name and description
- Organizes voices

### Voice
- Links to VoiceProfile
- Stores text and audio file
- Tracks voice settings (speed, pitch, volume)
- Records duration and creation date

## 🔐 Security Features

- CSRF protection enabled
- User authentication required for voice operations
- File upload validation
- Secure password hashing
- Admin-only access to management features

## 🚀 Deployment Considerations

For production deployment:

1. **Update settings.py:**
   - Set `DEBUG = False`
   - Configure `ALLOWED_HOSTS`
   - Use PostgreSQL instead of SQLite
   - Set up proper `SECRET_KEY`

2. **Configure static files:**
   ```bash
   python manage.py collectstatic
   ```

3. **Set up media file serving:**
   - Use cloud storage (AWS S3, Google Cloud Storage)
   - Or configure web server (Nginx, Apache)

4. **Enable HTTPS**

5. **Configure email backend** for password reset

## 📝 License

This project is open source and available for personal and educational use.

---

**Created with ❤️ using Django and pyttsx3**
