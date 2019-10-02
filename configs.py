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

SSO_URL = os.getenv('SSO_URL')
AMQP_CONFIG = {
    'default': {
        'HOST': os.environ.get('AMQP_DEFAULT_HOST', 'localhost'),
        'PORT': os.environ.get('AMQP_DEFAULT_PORT', 5672),
        'VHOST': os.environ.get('AMQP_DEFAULT_VHOST', 'localhost'),
        'USER': os.environ.get('AMQP_DEFAULT_USERNAME', 'rabbitmq'),
        'PASSWORD': os.environ.get('AMQP_DEFAULT_PASSWORD', 'rabbitmq'),
        'HEARTBEAT': os.environ.get('AMQP_DEFAULT_HEARTBEAT', 1800),
        'LOOPBACK_QUEUE': os.environ.get('AMQP_LOOPBACK_QUEUE', True),
        'EXCHANGE': os.environ.get('AMQP_DEFAULT_EXCHANGE', 'teko.op'),
        'EXCHANGE_TYPE': os.environ.get('AMQP_DEFAULT_EXCHANGE_TYPE', 'topic'),
        'QUEUE': os.environ.get('AMQP_DEFAULT_QUEUE', 'teko.om.ops_status')
    },
}

DEFAULT_AMQP_URL = os.environ.get(
    'DEFAULT_AMQP_URL',
    'amqp://{user}:{password}@{host}:{port}/{vhost}'.format(
            user=os.environ.get('AMQP_DEFAULT_USERNAME', 'rabbitmq'),
            password=os.environ.get('AMQP_DEFAULT_PASSWORD', 'rabbitmq'),
            host=os.environ.get('AMQP_DEFAULT_HOST', 'localhost'),
            port=os.environ.get('AMQP_DEFAULT_PORT', 5672),
            vhost=os.environ.get('AMQP_DEFAULT_VHOST', 'localhost'),
))

MAX_RETRY_PROCESSING_TIMES = int(os.getenv('MAX_RETRY_PROCESSING_TIMES', 3))

FIREBASE_DB_URL = os.getenv('FIREBASE_DB_URL')

NORTHERN_GROUP = os.getenv('NORTHERN_GROUP', 'northern')
SOUTHERN_GROUP = os.getenv('SOUTHERN_GROUP', 'southern')
CENTRAL_GROUP = os.getenv('CENTRAL_GROUP', 'central')

REDIS_ORDER_LINE_PROCESSING_KEY = os.getenv('REDIS_ORDER_LINE_PROCESSING_KEY', 'order_line_processing')
REDIS_ORDER_PROCESSING_OF_USER_KEY = os.getenv('REDIS_ORDER_PROCESSING_OF_USER_KEY')
REDIS_REGIONS_KEY = os.getenv('REDIS_REGIONS_KEY', 'regions')
API_ENDPOINT_ORDER = os.getenv('API_ENDPOINT_ORDER')
API_ENDPOINT_REGION = os.getenv('API_ENDPOINT_REGION')

OM_ACCESS_TOKEN = os.getenv('OM_ACCESS_TOKEN')
OPS_ORDER_CHANNEL_PROCESS = json.loads(os.getenv('OPS_ORDER_CHANNEL_PROCESS', '[2, 4, 5, 6]'))  # means we only process orders from channel Online (2) & AGENT (4) & VNShop (5)
USER_STATUS_ONLINE = 'online'
USER_STATUS_IDLE = 'idle'
USER_STATUS_OFFLINE = 'offline'


# Pass firebase account as base64 encoded to reduce effort encode, decode and load env varibale
FIREBASE_SERVICE_ACCOUNT_B64 = os.getenv('FIREBASE_SERVICE_ACCOUNT', '')
FIREBASE_SERVICE_ACCOUNT = json.loads(base64.b64decode(FIREBASE_SERVICE_ACCOUNT_B64)) if FIREBASE_SERVICE_ACCOUNT_B64 != '' else {
    "type": os.getenv('FIREBASE_SERVICE_ACC_TYPE'),
    "project_id": os.getenv('FIREBASE_PROJECT_ID'),
    "private_key_id": os.getenv('FIREBASE_PRIVATE_KEY_ID'),
    "private_key": os.getenv('FIREBASE_PRIVATE_KEY').replace('\\n', '\n'),
    "client_email": os.getenv('FIREBASE_CLIENT_EMAIL'),
    "client_id": os.getenv('FIREBASE_CLIENT_ID'),
    "auth_uri": os.getenv('FIREBASE_AUTH_URI'),
    "token_uri": os.getenv('FIREBASE_TOKEN_URI'),
    "auth_provider_x509_cert_url": os.getenv('FIREBASE_AUTH_PROVIDER_x509_CERT_URL'),
    "client_x509_cert_url": os.getenv('FIREBASE_CLIENT_x509_CERT_URL')
}

ORDER_QUANTITY_IN_CHARGE_PER_ASSIGNEE = os.getenv('ORDER_QUANTITY_IN_CHARGE_PER_ASSIGNEE', 10)
TOTAL_ORDER_ITEMS = os.getenv('TOTAL_ORDER_ITEMS', 'no_of_order_items')
TEAM_ALLOCATION_PATH = os.getenv('TEAM_ALLOCATION_PATH', '/order-processing/team_allocate')
ORDER_ALLOCATION_PATH = os.getenv('ORDER_ALLOCATION_TREE_PATH', '/order-processing/order_allocate')
REVIEW_NATION_DEBT_USERS = json.loads(os.getenv('REVIEW_NATION_DEBT_USERS', '["dung.cc@teko.vn"]'))
API_SALEMAN_AGENT = os.getenv('API_SALEMAN_AGENT', 'https://offlinesales.teko.vn/api/v2.1/users/all/')
SALEMAN_TOKEN = os.getenv('SALEMAN_TOKEN', 'NWU2YmM5MzIwMjI1NGQ1NzljNDlkYWVmYTQzOWNlMGU6')
SALESMEN_FIREBASE = os.getenv('SALESMEN_FIREBASE', '/users')
