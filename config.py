# config.py
import os
import decouple
import psycopg2


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = 'uploads'
MAX_FILE_SIZE = 12 * 1024 * 1024  # 12MB
ALLOWED_EXTENSIONS = {'pdf', 'pptx'}

# Database configuration
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'par.db')

# DATABASE_URL = decouple.config('DATABASE_URL')
# SQLALCHEMY_DATABASE_URI = DATABASE_URL.replace('postgres://', 'postgresql://')

SECRET_KEY = decouple.config('SECRET_KEY')
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


REDIS_URL = decouple.config('REDIS_URL', default='redis://localhost:6379/0')

CACHE_REDIS_URL = decouple.config("CACHE_REDIS_URL")

CELERY_BROKER_URL = decouple.config("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = decouple.config("CELERY_RESULT_BACKEND")

CACHE_TYPE = decouple.config("CACHE_TYPE")

