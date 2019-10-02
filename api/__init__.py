import os
import configs
from flask_restplus import Namespace

__appname__ = 'api'

api_namespace = Namespace(__appname__)
SCHEMA_DIR = os.path.join(configs.BASE_DIR, __appname__, 'schema')

from api.user import UserList, UserDetail