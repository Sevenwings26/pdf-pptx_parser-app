# config.py
import os
import decouple

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = 'uploads'
MAX_FILE_SIZE = 12 * 1024 * 1024  # 12MB
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'par.db')
ALLOWED_EXTENSIONS = {'pdf', 'pptx'}
SECRET_KEY = decouple.config('SECRET_KEY')

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

