"""
Django settings for Docker environment
"""

from .settings import *

# Override database settings for Docker
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'todo_db',
        'USER': 'root',
        'PASSWORD': 'qwerty',
        'HOST': 'db',  # Use the service name as hostname
        'PORT': '5432',
    }
}

# Print debug message to confirm these settings are being used
print("Using Docker database settings with HOST=db")
