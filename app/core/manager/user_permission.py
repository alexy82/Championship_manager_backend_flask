# coding=utf-8
from app.core.models.permission import Permission
from app.core.models.user import User
from app.core.models.user_permission import UserPermission
from app.core.models import db


def delete_all_permission_by_user_id(user_id: int):
    try:
        UserPermission.query.filter_by(user_id=user_id).delete()
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        return False


def create_permissions_with_user_id(user_id: int, permissions_id: list):
    try:
        for permission_id in permissions_id:
            user_permission = UserPermission(user_id=user_id,
                                             permission_id=permission_id)
            db.session.add(user_permission)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        return False


def has_permission(email, permission_key: list, **kwargs):
    try:
        if kwargs.get('user_id', None) is None:
            user_id = 0
        else:
            user_id = kwargs['user_id']
        if user_id is not None:
            obj = UserPermission.query \
                .filter((UserPermission.user_id == user_id) | (User.email == email),
                        Permission.key.in_(permission_key)) \
                .join(User, UserPermission.user_id == User.id) \
                .join(Permission, UserPermission.permission_id == Permission.id) \
                .first()
            return obj is not None
        return False
    except:
        return False
