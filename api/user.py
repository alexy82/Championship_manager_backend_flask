"""User APIs"""
import json
import logging
from http import HTTPStatus
from flask import request
from flask_restplus import Resource

from api import api_namespace
from api.base import wrap_response
from app.core.manager import user
from app.core.manager.user import get_a_user
from app.core.utils.decorators import authorized, validate_offset_limit
from app.core.utils.request_helper import log_api_request

LOGGER = logging.getLogger('main')


@api_namespace.route('/users')
class UserList(Resource):
    """ User list API """

    @validate_offset_limit
    def get(self, limit, offset):
        """Get user list"""
        try:
            data = user.get_all_users(value=request.args.get('value', ''))
            if data is None:
                return wrap_response('Server Internal Error: ',
                                     HTTPStatus.INTERNAL_SERVER_ERROR)
            response = {
                'total': len(data),
                'items': data[offset: offset + limit],
            }
            return wrap_response(data=response)
        except Exception as e:
            return wrap_response('Server Internal Error: ' + str(e),
                                 HTTPStatus.INTERNAL_SERVER_ERROR)

    @authorized
    def post(self):
        """Create a user"""
        try:
            log_api_request(request)
            data = json.loads(request.data.decode())
            return user.create_user(data=data)
        except Exception as e:
            return wrap_response('Server Internal Error: ' + str(e),
                                 HTTPStatus.INTERNAL_SERVER_ERROR)

    @authorized
    def put(self):
        """Update an user"""
        try:
            log_api_request(request)
            data = json.loads(request.data.decode())
            data['id'] = request.args.get('user_id')
            return user.update_user(data=data)
        except Exception as e:
            return wrap_response('Server Internal Error: ' + str(e),
                                 HTTPStatus.INTERNAL_SERVER_ERROR)

    @authorized
    def delete(self):
        """Delete an user"""
        try:
            log_api_request(request)
            user_id = request.args.get('user_id')
            return user.delete_user(user_id=user_id)
        except Exception as e:
            return wrap_response('Server Internal Error: ' + str(e),
                                 HTTPStatus.INTERNAL_SERVER_ERROR)


@api_namespace.route('/users/<user_id>')
class UserDetail(Resource):
    """ User detail API """

    @authorized
    def get(self, user_id):
        """Get an user"""
        try:
            user_id = int(user_id)
        except Exception as e:
            LOGGER.error(str(e))
            return wrap_response('Bad request', HTTPStatus.BAD_REQUEST)
        try:
            log_api_request(request)
            user = get_a_user(user_id=user_id)
            if user is None:
                return wrap_response('Not found', HTTPStatus.NOT_FOUND)
            return wrap_response(data=user)
        except Exception as e:
            return wrap_response('Server Internal Error: ' + str(e),
                                 HTTPStatus.INTERNAL_SERVER_ERROR)


@api_namespace.route('/users/assignrole')
class UsersAssignRole(Resource):
    """ User assign role API"""

    @authorized
    def get(self):
        """Assign role for user"""
        try:
            log_api_request(request)
            args = request.args
            return user.assign_role(args=args)
        except Exception as e:
            return wrap_response('Server Internal Error: ' + str(e),
                                 HTTPStatus.INTERNAL_SERVER_ERROR)
