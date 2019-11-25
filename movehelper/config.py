
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
    MOVEHELPER_UPLOAD_PATH = os.path.join(basedir, 'uploads')
    MOVEHELPER_PHOTO_SIZE = {'small': 400,
                         'medium': 800}
    MOVEHELPER_PHOTO_SUFFIX = {
        MOVEHELPER_PHOTO_SIZE['small']: '_s',  # thumbnail
        MOVEHELPER_PHOTO_SIZE['medium']: '_m',  # display
    }

    SECRET_KEY = os.getenv('SECRET_KEY', 'secret string')
    MAX_CONTENT_LENGTH = 3 * 1024 * 1024  # file size exceed to 3 Mb will return a 413 error response.

    BOOTSTRAP_SERVE_LOCAL = True

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    AVATARS_SAVE_PATH = os.path.join(MOVEHELPER_UPLOAD_PATH, 'avatars')
    AVATARS_SIZE_TUPLE = (30, 100, 200)

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'movehelperxxx@gmail.com'
    MAIL_PASSWORD = '741qaz741'
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
    HOSTNAME = '127.0.0.1'
    PORT = '3306'
    DATABASE = 'movehelper'
    USERNAME = 'root'
    PASSWORD = '2erming'
    mydb = 'mysql+mysqlconnector://{}:{}@{}:{}/{}'.format(USERNAME,PASSWORD,HOSTNAME,PORT,DATABASE)
    SQLALCHEMY_DATABASE_URI = mydb
    SQLALCHEMY_TRACK_MODIFICATIONS = False



config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}