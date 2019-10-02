from http import HTTPStatus
from app.core.models.role import Role
from app.core.models.user_role import UserRole
from app.core.models.role_permission import RolePermission
from app.core.models.permission import Permission
from api.base import wrap_response
from app.core.models import db
from app.core.manager.role_permission import \
    create_permissions_with_role_id, delete_all_permission_by_role_id
from app.core.manager.user_role import delete_all_user_by_role_id


def get_role_list(args):
    try:
        limit = int(args.get('limit', 100))
        offset = int(args.get('offset', 0))
        if limit < 0 or offset < 0:
            return wrap_response('Bad request', HTTPStatus.BAD_REQUEST)
    except Exception as e:
        return wrap_response('Bad request', HTTPStatus.BAD_REQUEST)

    try:
        roles = Role.query.offset(offset).limit(limit).all()
        response = {
            'total': len(roles),
            'items': [],
        }
        for role in roles:
            item = role.as_dict()
            permissions = Permission.query \
                .join(RolePermission,
                      Permission.id == RolePermission.permission_id) \
                .filter(RolePermission.role_id == role.id)
            item['permissions'] = [permission.as_dict() for permission in
                                   permissions]
            response['items'].append(item)
        return wrap_response(data=response)
    except Exception as e:
        return wrap_response('Server Internal Error: ' + str(e),
                             HTTPStatus.INTERNAL_SERVER_ERROR)


def get_role_detail(role_id):
    try:
        role_id = int(role_id)
    except Exception as e:
        return wrap_response('Bad request', HTTPStatus.BAD_REQUEST)

    try:
        role = Role.query.filter_by(id=role_id).first()
        if role is None:
            msg = 'Role id not found'
            return wrap_response(msg, HTTPStatus.NOT_FOUND)

        response = role.as_dict()
        permissions = Permission.query \
            .join(RolePermission, Permission.id == RolePermission.permission_id) \
            .filter(RolePermission.role_id == role.id)
        response['permissions'] = [permission.as_dict() for permission in
                                   permissions]
        return wrap_response(data=response)
    except Exception as e:
        return wrap_response('Server Internal Error: ' + str(e),
                             HTTPStatus.INTERNAL_SERVER_ERROR)


def add_role(data):
    try:
        new_role = Role.create(
            name=data.get('name'),
            desc=data.get('desc'),
        )

        id = new_role.id
        inserted = create_permissions_with_role_id(role_id=id,
                                                   permissions_id=data.get(
                                                       'permissions', []))
        if not inserted:
            return wrap_response('Server Internal Error',
                                 HTTPStatus.INTERNAL_SERVER_ERROR)

        return wrap_response(data=new_role.as_dict())
    except Exception as e:
        db.session.rollback()
        return wrap_response('Server Internal Error: ' + str(e),
                             HTTPStatus.INTERNAL_SERVER_ERROR)


def update_role(data):
    try:
        id = int(data.get('id'))
    except Exception as e:
        return wrap_response('Bad request', HTTPStatus.BAD_REQUEST)

    try:
        role = Role.query.filter_by(id=id).first()
        if role is None:
            msg = 'Role id not found'
            return wrap_response(msg, HTTPStatus.BAD_REQUEST)

        role.update(data)
        deleted = delete_all_permission_by_role_id(role_id=id)
        if not deleted:
            return wrap_response('Server Internal Error',
                                 HTTPStatus.INTERNAL_SERVER_ERROR)
        inserted = create_permissions_with_role_id(role_id=id,
                                                   permissions_id=data.get(
                                                       'permissions', []))
        if not inserted:
            return wrap_response('Server Internal Error',
                                 HTTPStatus.INTERNAL_SERVER_ERROR)

        return wrap_response(data=role.as_dict())
    except Exception as e:
        return wrap_response('Server Internal Error: ' + str(e),
                             HTTPStatus.INTERNAL_SERVER_ERROR)


def delete_role(role_id):
    try:
        role_id = int(role_id)
    except Exception as e:
        return wrap_response('Bad request', HTTPStatus.BAD_REQUEST)

    try:
        delete_permission = delete_all_permission_by_role_id(role_id=role_id)
        if not delete_permission:
            return wrap_response('Server Internal Error',
                                 HTTPStatus.INTERNAL_SERVER_ERROR)
        delete_user = delete_all_user_by_role_id(role_id=role_id)
        if not delete_user:
            return wrap_response('Server Internal Error',
                                 HTTPStatus.INTERNAL_SERVER_ERROR)

        Role.delete(role_id=role_id)
        return wrap_response()
    except Exception as e:
        return wrap_response('Server Internal Error: ' + str(e),
                             HTTPStatus.INTERNAL_SERVER_ERROR)


def get_all_role_by_user_id(user_id):
    try:
        roles = Role.query \
            .join(UserRole, Role.id == UserRole.role_id) \
            .filter(UserRole.user_id == user_id) \
            .all()
        return [role.as_dict() for role in roles]
    except Exception as e:
        return []
