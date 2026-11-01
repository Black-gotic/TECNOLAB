import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'database', 'database.db')
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'svg'}
    DEBUG = True
