import os
import secrets

_local_secret_path = os.path.join(os.path.dirname(__file__), 'database', '.secret_key')
_secret_key = os.environ.get('SECRET_KEY')
if not _secret_key:
    os.makedirs(os.path.dirname(_local_secret_path), exist_ok=True)
    try:
        with open(_local_secret_path, 'r', encoding='utf-8') as secret_file:
            _secret_key = secret_file.read().strip()
    except FileNotFoundError:
        _secret_key = secrets.token_hex(32)
        with open(_local_secret_path, 'w', encoding='utf-8') as secret_file:
            secret_file.write(_secret_key)

class Config:
    SECRET_KEY = _secret_key
    DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'database', 'database.db')
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'svg'}
    DEBUG = False
