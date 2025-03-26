from .settings import *  # noqa 

# Use in-memory SQLite database for testing
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Use console email backend for testing
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'test@example.com'

# Use session storage for messages in tests
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

# Disable password hashers for faster tests
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# Use a faster session engine for tests
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# Disable CSRF protection in tests
CSRF_PROTECT = False
SESSION_COOKIE_SECURE = False

# Disable allauth email verification in tests
EMAIL_VERIFICATION = False
