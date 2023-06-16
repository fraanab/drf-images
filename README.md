# Tasks Django Web App

## Table of Contents
- [SetUp](#setup)
- [Introduction](#introduction)
 
## SetUp
Virtual environment
```
python -m venv venv
```
or install virtualenv and
```
virtualenv env
```

You can use pip to install the requirements.txt packages
```
pip install requirements.txt -r
```

In settings.py, you need a SECRET_KEY, you can get one with Django's
```
from django.core.management.utils import get_random_secret_key
```

You can delete "db.sqlite3" if you want to make a new one, to then make migrations
```
python manage.py makemigrations
python manage.py migrate
```

or connect your postgres/mysql here
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',   # change this "django.db.backends.postgresql"
        'NAME': BASE_DIR / 'db.sqlite3',          # change
        
#        "USER": "",
#        "PASSWORD": "",
#        "HOST": "",
#        "PORT": "",
    }
}
```

Create a superuser
```
python manage.py createsuperuser
```

In settings.py you can replace cloudinary for media files with your service of choice
```
# installed apps
    'cloudinary',
    'cloudinary_storage',
#    ...
CLOUDINARY_STORAGE = {
  "CLOUD_NAME": os.getenv('CN'),
  "API_KEY": os.getenv('AK'),
  "API_SECRET": os.getenv('AS'),
  "secure":True
}
CLOUDINARY_STORAGE = {
  "CLOUD_NAME": os.getenv('CN'),
  "API_KEY": os.getenv('AK'),
  "API_SECRET": os.getenv('AS'),
  "secure":True
}

MEDIA_URL = '/media/'
STORAGES = {
    "default": {
        "BACKEND": 
            # "django.core.files.storage.FileSystemStorage",
            "cloudinary_storage.storage.MediaCloudinaryStorage",
  },
    "staticfiles": {
        "BACKEND":
            "django.contrib.staticfiles.storage.StaticFilesStorage",
            # "whitenoise.storage.CompressedManifestStaticFilesStorage",
  }
}
```

send_mail configuration
```
EMAIL_HOST = 'smtp-mail.outlook.com'
EMAIL_PORT = '587'
EMAIL_HOST_USER = os.getenv('HOSTEMAIL')      #  credentials
EMAIL_HOST_PASSWORD = os.getenv('HOSTPASS')   #  credentials
EMAIL_USE_TLS = True
# EMAIL_USE_SSL = True
```

## Introduction
- Classic to do app, this time making use of the django rest framework, to create api endpoints for the CRUD features. Basic relationships between Task, Memberships and Team models, using foreign keys.
- Django session authentication.
