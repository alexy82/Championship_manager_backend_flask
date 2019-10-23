import logging

from http import HTTPStatus

from sqlalchemy import or_

from app.core.models.user import User
from app.core.models.role import Role
from app.core.models.user_role import UserRole
from api.base import wrap_response
from app.core.models import db
from app.core.manager.user_role import delete_all_role_by_user_id, \
    create_roles_with_user_id
from app.core.manager.user_permission import \
    delete_all_permission_by_user_id, create_permissions_with_user_id, has_permission
from app.core.manager.role import get_all_role_by_user_id
from app.core.manager.permission import get_by_ids, get_all_permission_by_user_id
from app.core.utils.constants import InternalErrorCode, TeamStatus, permissions

LOGGER = logging.getLogger('main')


def get_all_users(**kwargs):
    try:
        cond = ()
        value = kwargs.get('value')
        if value is not None:
            cond += (or_(User.username.like('%' + value + '%'), User.fullname.like('%' + value + '%'),
                         User.email.like('%' + value + '%'), User.mobile.like('%' + value + '%')),
                     )
        users = User.query.filter(*cond).all()
        items = []

        for user in users:
            item = user.as_dict()
            item['roles'] = get_all_role_by_user_id(user_id=user.id)
            item['permissions'] = get_all_permission_by_user_id(
                user_id=user.id)
            items.append(item)
        return items
    except Exception as e:
        LOGGER.error(e)
        return None


# TODO: implenent cache
# def get_by_id(id):
#     """Get an user by ID from cache, if data does not exists in cache then get from database"""
#     try:
#         key = 'USER:{id}'.format(id=id)
#         user = cache.get(key)
#         if user is None:
#             user = User.query.filter_by(id=id).first()
#             if user is not None:
#                 cache.set(key, user, timeout=300) # 5 minutes
#     except:
#         user = None
#     return user


def get_a_user(user_id):
    try:
        user = User.query.filter(User.id == user_id).first()
        if user is None:
            LOGGER.error('Get user by user_id: {user_id} not found'.format(user_id=user_id))
            return None
        response = user.as_dict()
        response['roles'] = get_all_role_by_user_id(user_id=user.id)
        response['permissions'] = get_all_permission_by_user_id(
            user_id=user.id)
        return response
    except Exception as e:
        LOGGER.error('Get detail user {user_id} has error: {error}'
                     .format(user_id=user_id, error=str(e)))
        return None


def generate_token(user):
    try:
        # generate the auth token
        auth_token = User.encode_auth_token(user.id)
        response_object = {
            'status': 'success',
            'message': 'Successfully registered.',
            'Authorization': auth_token.decode()
        }
        return response_object, 201
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }
        return response_object, 401


def create_user(data):
    try:
        email = data.get('email')
        username = data.get('username')
        user = User.query.filter(
            (User.email == email) | (User.username == username)).first()
        if user is not None:
            msg = 'email/username already existed'
            return wrap_response(msg, HTTPStatus.CONFLICT)

        new_user = User.create(
            email=data.get('email'),
            username=data.get('email'),
            fullname=data.get('fullname', ''),
            mobile=data.get('mobile', ''),
        )

        id = new_user.id
        inserted = create_roles_with_user_id(user_id=id,
                                             roles_id=data.get('roles', []))
        if not inserted:
            return wrap_response('Server Internal Error',
                                 HTTPStatus.INTERNAL_SERVER_ERROR)

        inserted = create_permissions_with_user_id(user_id=id,
                                                   permissions_id=data.get(
                                                       'permissions', []))
        if not inserted:
            return wrap_response('Server Internal Error',
                                 HTTPStatus.INTERNAL_SERVER_ERROR)

        return wrap_response(data=new_user.as_dict())
    except Exception as e:
        db.session.rollback()
        return wrap_response('Server Internal Error: ' + str(e),
                             HTTPStatus.INTERNAL_SERVER_ERROR)


def update_user(data):
    try:
        id = int(data.get('id'))
    except Exception as e:
        return wrap_response('Bad request', HTTPStatus.BAD_REQUEST)

    try:
        user = User.query.filter((User.email == data.get('email')) | (
                User.username == data.get('username'))).first()
        if user is not None and user.id != id:
            msg = 'email/username already existed'
            LOGGER.error(msg + '| {}'.format(data.get('email')))
            return wrap_response(msg, HTTPStatus.CONFLICT)

        user = User.query.filter_by(id=id).first()
        if user is None:
            LOGGER.error('user id {} NOT EXIST in our system.'.format(id))
            return wrap_response('Bad request', HTTPStatus.BAD_REQUEST)

        data['id'] = id
        res = user.update(data)
        LOGGER.info('update_user result {} | updated data: {}'.format(res, data))
        deleted = delete_all_role_by_user_id(user_id=id)
        if not deleted:
            LOGGER.error('Failed to Delete old roles of user id: {}'.format(id))
            return wrap_response('Server Internal Error',
                                 HTTPStatus.INTERNAL_SERVER_ERROR)
        inserted = create_roles_with_user_id(user_id=id,
                                             roles_id=data.get('roles', []))
        if not inserted:
            LOGGER.error('Failed to RE-INSERT new roles of user id: {}'.format(id))
            return wrap_response('Server Internal Error',
                                 HTTPStatus.INTERNAL_SERVER_ERROR)

        deleted = delete_all_permission_by_user_id(user_id=id)
        if not deleted:
            LOGGER.error('Failed to Delete old permissions of user id: {}'.format(id))
            return wrap_response('Server Internal Error',
                                 HTTPStatus.INTERNAL_SERVER_ERROR)
        perm_ids = data.get('permissions', [])
        inserted = create_permissions_with_user_id(user_id=id,
                                                   permissions_id=perm_ids)
        if not inserted:
            LOGGER.error('Failed to RE-INSERT new permissions of user id: {}'.format(id))
            return wrap_response('Server Internal Error',
                                 HTTPStatus.INTERNAL_SERVER_ERROR)

        perm_lst = get_by_ids(perm_ids)
        can_auto_process = any(permissions['order_process'] == perm['key']
                               for perm in perm_lst) if len(perm_lst) > 0 else False

        # get team which user belongs to

        return wrap_response(data=user.as_dict())
    except Exception as e:
        return wrap_response('Server Internal Error: ' + str(e),
                             HTTPStatus.INTERNAL_SERVER_ERROR)


def assign_role(args):
    try:
        user_id = int(args.get('user_id'))
        role_id = int(args.get('role_id'))
    except Exception as e:
        return wrap_response('Bad request', HTTPStatus.BAD_REQUEST)

    try:
        user = User.query.filter_by(id=user_id).first()
        role = Role.query.filter_by(id=role_id).first()

        if user is None:
            msg = 'User not found'
            return wrap_response(msg, HTTPStatus.NOT_FOUND)

        if role is None:
            msg = 'Role not found'
            return wrap_response(msg, HTTPStatus.NOT_FOUND)

        user_role = UserRole.query.filter_by(user_id=user_id,
                                             role_id=role_id).first()
        if user_role is not None:
            msg = 'User already assigned with the given role. No effect.'
            return wrap_response(msg, HTTPStatus.OK, {})
        else:
            msg = 'Successfully assign'
            UserRole.create(user_id=user_id, role_id=role_id)
            return wrap_response(msg, HTTPStatus.OK, {})
    except Exception as e:
        return wrap_response('Server Internal Error: ' + str(e),
                             HTTPStatus.INTERNAL_SERVER_ERROR)


def get_raw_user_by_id(id: int):
    user = User.query.filter_by(id=id).first()
    return user


def get_by_email(email):
    try:
        user = User.query.filter_by(email=email).first()
    except Exception as e:
        return None
    return user.as_dict() if user is not None else None

