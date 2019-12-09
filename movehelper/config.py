
import os
import sys

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# SQLite URI compatible
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

class Operations:
    CONFIRM = 'confirm'
    RESET_PASSWORD = 'reset-password'
    CHANGE_EMAIL = 'change-email'


class BaseConfig:
    MOVEHELPER_ADMIN_EMAIL = 'movehelperxxx@gmail.com'
    MOVEHELPER_TASKS_PER_PAGE = 10
    MOVEHELPER_COMMENT_PER_PAGE = 15
    MOVEHELPER_NOTIFICATION_PER_PAGE = 20
    MOVEHELPER_USER_PER_PAGE = 20
    MOVEHELPER_MANAGE_PHOTO_PER_PAGE = 20
    MOVEHELPER_MANAGE_USER_PER_PAGE = 30
    MOVEHELPER_MANAGE_TAG_PER_PAGE = 50
    MOVEHELPER_MANAGE_COMMENT_PER_PAGE = 30
    MOVEHELPER_SEARCH_RESULT_PER_PAGE = 20
    MOVEHELPER_MAIL_SUBJECT_PREFIX = '[Movehelper]'
    SECRET_KEY = os.getenv('SECRET_KEY', 'secret string')
    MAX_CONTENT_LENGTH = 3 * 1024 * 1024  # file size exceed to 3 Mb will return a 413 error response.

    BOOTSTRAP_SERVE_LOCAL = True

    SQLALCHEMY_TRACK_MODIFICATIONS = False


    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'movehelperxxx@gmail.com'
    MAIL_PASSWORD = 'ydhrxvwtnenccvzp'
    MAIL_DEFAULT_SENDER = ('Movehelper Admin', 'movehelperxxx@gmail.com')

    DROPZONE_ALLOWED_FILE_TYPE = 'image'
    DROPZONE_MAX_FILE_SIZE = 3
    DROPZONE_MAX_FILES = 30
    DROPZONE_ENABLE_CSRF = True

    WHOOSHEE_MIN_STRING_LEN = 1


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = prefix + os.path.join(basedir, 'data-dev.db')


class TestingConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # in-memory database


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', prefix + os.path.join(basedir, 'data.db'))



config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}