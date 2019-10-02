import json
import os
import base64

from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, '.env'), override=True, verbose=True)

DEBUG = (os.environ.get('DEBUG', 'False') == 'True')

LOGGING = {
    'version': 1,
    # 'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s | %(levelname)s | %(process)d | %(thread)d | %(filename)s:%('
                      'lineno)d | %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'simple': {
            'format': '%(levelname)s | %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'daily_http': {
            'level': 'INFO',
            'class': 'app.core.logging_handlers.PythonHTTPHandler',
            'url': 'http-daily-logger/',
            'formatter': 'verbose',
            'host': os.environ.get('LOGGING_DAILY_HTTP_HOST', '0.0.0.0:5000'),
            'method': 'POST',
            'logPath': os.environ.get('LOGGING_DAILY_HTTP_FILE_PATH',
                                      '/var/log/championship/daily.log'),
        },
        'slack_notification': {
            'level': os.environ.get('SLACK_NOTIFICATION_LEVEL', 'ERROR'),
            'class': 'app.core.logging_handlers.LogSlackHandler',
            'formatter': 'simple',
            'webhook': os.environ.get('SLACK_NOTIFICATION_WEBHOOK',
                                      'https://hooks.slack.com/services/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'),
            'sender': os.environ.get('SLACK_NOTIFICATION_SENDER', '[ORDER PROCESSING][Prod]'),
            'channel': os.environ.get('SLACK_NOTIFICATION_CHANNEL', '#order-processing'),
        },
    },
    'loggers': {
        'main': {
            'level': 'INFO',
            'handlers': os.environ.get('LOGGER_MAIN_HANDLERS', 'console').split(','),
            'propagate': True,
        },
    },
}

SCHEMA_DIR = os.path.join(BASE_DIR, 'app', 'schema')

ENV_NAME = os.environ.get('ENV_NAME', 'dev')

DB_HOST = os.getenv('DB_HOST', '127.0.0.1')
DB_PORT = os.getenv('DB_PORT', '3306')
DB_NAME = os.getenv('DB_NAME', 'order_processing')
DB_USER = os.getenv('DB_USER', 'pvis')
DB_PASS = os.getenv('DB_PASS', '111111')
DB_POOL_PRE_PING = os.environ.get('DB_POOL_PRE_PING', 'True') == 'True'
DB_POOL_RECYCLE = int(os.environ.get('DB_POOL_RECYCLE', '3600'))

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(DB_USER, DB_PASS, DB_HOST,
                                                                                      DB_PORT, DB_NAME)
SQLALCHEMY_TRACK_MODIFICATIONS = False

DATABASES = {
    'default': {
        'ENGINE': 'core.db.backends.mysql.MySQLDB',
        'NAME': os.environ.get('DB_NAME', 'order_processing'),
        'USERNAME': os.environ.get('DB_USERNAME', 'pvis'),
        'PASSWORD': os.environ.get('DB_PASSWORD', '111111'),
        'HOST': os.environ.get('DB_HOST', '127.0.0.1'),
        'PORT': os.environ.get('DB_PORT', '3306'),
        'ENGINE_OPTIONS': {
            'pool_pre_ping': os.environ.get('DB_POOL_PRE_PING', 'True') == 'True',
            'pool_recycle': int(os.environ.get('DB_POOL_RECYCLE', '3600')),
        },
    },
}

REDIS = {
    'default': {
        'HOST': os.getenv('REDIS_HOST'),
        'PORT': os.getenv('REDIS_PORT'),
        'DB': os.getenv('REDIS_DB')
    }
}
API_ENDPOINT_ORDER = os.getenv('API_ENDPOINT_ORDER')
API_ENDPOINT_REGION = os.getenv('API_ENDPOINT_REGION')

