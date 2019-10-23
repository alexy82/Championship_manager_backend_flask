"""Role APIs"""
import json
from http import HTTPStatus
from flask_restplus import Resource
from flask import request

from api import api_namespace
from api.base import wrap_response
from app.core.manager import role
from app.core.utils.decorators import authorized
from app.core.utils.request_helper import log_api_request


@api_namespace.route('/roles')
class RoleList(Resource):
    """ Role list API """

    @authorized
    def get(self):
        """Get List roles"""
        try:
            log_api_request(request)
            args = request.args
            return role.get_role_list(args=args)
        except Exception as e:
            return wrap_response('Server Internal Error: ' + str(e),
                                 HTTPStatus.INTERNAL_SERVER_ERROR)

    @authorized
    def post(self):
        """Add new role"""
        try:
            log_api_request(request)
            data = json.loads(request.data.decode())
            return role.add_role(data=data)
        except Exception as e:
            return wrap_response('Server Internal Error: ' + str(e),
                                 HTTPStatus.INTERNAL_SERVER_ERROR)

    @authorized
    def put(self):
        """Update an existing role"""
        try:
            log_api_request(request)
            data = json.loads(request.data.decode())
            data['id'] = request.args.get('role_id')
            return role.update_role(data=data)
        except Exception as e:
            return wrap_response('Server Internal Error: ' + str(e),
                                 HTTPStatus.INTERNAL_SERVER_ERROR)

    @authorized
    def delete(self):
        """Delete an existing role"""
        try:
            log_api_request(request)
            role_id = request.args.get('role_id')
            return role.delete_role(role_id=role_id)
        except Exception as e:
            return wrap_response('Server Internal Error: ' + str(e),
                                 HTTPStatus.INTERNAL_SERVER_ERROR)


@api_namespace.route('/roles/<role_id>')
class RoleDetail(Resource):
    """ Role detail API """

    @authorized
    def get(self, role_id):
        """Get detail of a role"""
        try:
            log_api_request(request)
            return role.get_role_detail(role_id=role_id)
        except Exception as e:
            return wrap_response('Server Internal Error: ' + str(e),
                                 HTTPStatus.INTERNAL_SERVER_ERROR)
