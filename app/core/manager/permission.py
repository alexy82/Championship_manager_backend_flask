from http import HTTPStatus
from app.core.models.permission import Permission
from app.core.models.user_permission import UserPermission
from app.core.models.role_permission import RolePermission
from app.core.manager.role import get_all_role_by_user_id
from api.base import wrap_response


def get_permission_list(args):
    try:
        limit = int(args.get('limit', 100))
        offset = int(args.get('offset', 0))
    except Exception as e:
        return wrap_response('Bad request', HTTPStatus.BAD_REQUEST)

    try:
        data = Permission.query.offset(offset).limit(limit).all()
        response = {
            'total': len(data),
            'items': [],
        }
        for element in data:
            item = element.as_dict()
            response['items'].append(item)
        return wrap_response(data=response)
    except Exception as e:
        return wrap_response('Server Internal Error: ' + str(e),
                             HTTPStatus.INTERNAL_SERVER_ERROR)


def get_permission_detail(permission_id):
    try:
        permission_id = int(permission_id)
    except Exception as e:
        return wrap_response('Bad request', HTTPStatus.BAD_REQUEST)

    try:
        data = Permission.query.filter_by(id=permission_id).first()
        return wrap_response(data=data.as_dict())
    except Exception as e:
        return wrap_response('Server Internal Error: ' + str(e),
                             HTTPStatus.INTERNAL_SERVER_ERROR)


def add_permission(data):
    try:
        key = data.get('key')
        permission = Permission.query.filter_by(key=key).first()
        if permission is not None:
            msg = 'Duplicated permission name'
            return wrap_response(msg, HTTPStatus.CONFLICT)

        new_permission = Permission.create(
            key=data.get('key'),
            name=data.get('name', ''),
            module=data.get('module', ''),
            desc=data.get('desc', ''),
        )
        return wrap_response(data=new_permission.as_dict())
    except Exception as e:
        return wrap_response('Server Internal Error: ' + str(e),
                             HTTPStatus.INTERNAL_SERVER_ERROR)


def update_permission(data):
    try:
        id = int(data.get('id'))
    except Exception as e:
        return wrap_response('Bad request', HTTPStatus.BAD_REQUEST)

    try:
        permission = Permission.query.filter_by(id=id).first()
        if permission is None:
            msg = 'permission not found {id}'.format(id=id)
            return wrap_response(msg, HTTPStatus.NOT_FOUND)

        data['id'] = id
        permission.update(data)
        return wrap_response(data=permission.as_dict())
    except Exception as e:
        return wrap_response('Server Internal Error: ' + str(e),
                             HTTPStatus.INTERNAL_SERVER_ERROR)


def get_all_permission_by_user_id(user_id: int):
    try:
        permissions = Permission.query \
            .join(UserPermission, Permission.id == UserPermission.permission_id) \
            .filter(UserPermission.user_id == user_id) \
            .all()
        result = [permission.as_dict() for permission in permissions]

        roles = get_all_role_by_user_id(user_id=user_id)
        roles_id = [role.get('id') for role in roles]
        permissions_role = Permission.query \
            .join(RolePermission, Permission.id == RolePermission.permission_id) \
            .filter(RolePermission.role_id.in_(roles_id)) \
            .all()
        result.extend([permission.as_dict() for permission in permissions_role])
        result = list({v['id']: v for v in result}.values())
        return result
    except:
        return []


def get_by_ids(ids: list):
    try:
        perms = Permission.query.filter(Permission.id.in_(ids)).all()
        return [perm.as_dict() for perm in perms] if perms is not None else []
    except Exception as e:
        return []


def get_perms_by_user_id(user_id: int):
    try:
        permissions = Permission.query \
            .join(UserPermission, Permission.id == UserPermission.permission_id) \
            .filter(UserPermission.user_id == user_id) \
            .all()
        return [permission.as_dict() for permission in permissions]
    except:
        return []
