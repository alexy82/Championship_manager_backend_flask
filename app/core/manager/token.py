import ast
import logging

import requests

import configs
from app.core.utils.constants import CacheTimeout
from app.core.utils.redis_helper import redis_helper
from http import HTTPStatus

LOGGER = logging.getLogger('main')
redis = redis_helper.get_connection('default')


def get_info_token(access_token):
    result = redis.get(access_token)
    if result is None:
        result = requests.get(configs.SSO_URL, params={'accessToken': access_token},
                              headers={'Content-Type': 'application/json'})
        if result.status_code == HTTPStatus.OK:
            redis.set(access_token, str(result.json()), ex=CacheTimeout.CLIENT_TOKEN)
            return result.json()
        return None
    return ast.literal_eval(result.decode('utf-8'))


def validate_token(access_token):
    try:
        token = get_info_token(access_token)
        if token is not None:
            return True
        return False
    except Exception as e:
        LOGGER.error(e)
        return False
