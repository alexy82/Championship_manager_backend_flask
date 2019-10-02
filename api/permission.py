"""API Permissions"""
import json
from http import HTTPStatus
from flask_restplus import Resource
from flask import request

from api import api_namespace
from app.core.manager import permission
from api.base import wrap_response
from app.core.utils.decorators import authorized
from app.core.utils.request_helper import log_api_request


@api_namespace.route('/permission')
class PermissionList(Resource):
    """ Permission list API """

    @authorized
    def get(self):
        """Get list permissions"""
        try:
            log_api_request(request)
            args = request.args
            return permission.get_permission_list(args=args)
        except Exception as e:
            return wrap_response('Server Internal Error: ' + str(e),
                                 HTTPStatus.INTERNAL_SERVER_ERROR)


    @authorized
    def post(self):
        """Create a permission"""
        try:
            data = json.loads(request.data.decode())
            return permission.add_permission(data=data)
        except Exception as e:
            return wrap_response('Server Internal Error: ' + str(e),
                                 HTTPStatus.INTERNAL_SERVER_ERROR)

    @authorized
    def put(self):
        """Update permission"""
        try:
            data = json.loads(request.data.decode())
            return permission.update_permission(data=data)
        except Exception as e:
            return wrap_response('Server Internal Error: ' + str(e),
                                 HTTPStatus.INTERNAL_SERVER_ERROR)


@api_namespace.route('/permission/<permission_id>')
class PermissionDetail(Resource):
    """ Permission detail API """

    @authorized
    def get(self, permission_id):
        """Get Permission detail"""
        try:
            log_api_request(request)
            return permission.get_permission_detail(
                permission_id=permission_id)
        except Exception as e:
            return wrap_response('Server Internal Error: ' + str(e),
                                 HTTPStatus.INTERNAL_SERVER_ERROR)
