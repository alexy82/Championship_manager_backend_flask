"""Base module for API V1"""

from http import HTTPStatus
from flask import jsonify, make_response
from app.core.utils.constants import mapping_internal_codes


class ApiV1BaseException(Exception):
    """Base Exception class"""

    code = HTTPStatus.BAD_REQUEST

    def __init__(self, message='Bad request', status_code=None, payload=None):
        """Init method"""
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.code = status_code
        self.data = payload

    def to_dict(self):
        """Convert Object to dict"""
        rv = dict(error={}, data={})
        rv['error'] = {
            'code': self.code,
            'detail': self.message
        }
        rv['data'] = dict(self.data or ())
        return rv


def wrap_response(message="Success", http_code=200, data=None):
    """ Return general HTTP response
    :param str message: detail info
    :param int http_code:
    :param data: payload data
    :return:
    """
    return make_response(jsonify(
        ApiV1BaseException(message, mapping_internal_codes[http_code],
                           data).to_dict()), http_code)

