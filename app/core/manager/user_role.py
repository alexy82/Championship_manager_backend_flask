# coding=utf-8
import logging

from app.core.models.user_role import UserRole
from app.core.models import db

LOGGER = logging.getLogger('main')


def delete_all_role_by_user_id(user_id: int):
    try:
        UserRole.query.filter_by(user_id=user_id).delete()
        db.session.commit()
        return True
    except Exception as e:
        LOGGER.error('Unexpected error occurred when '
                     'deleting all roles of user. Message: ' + str(e))
        db.session.rollback()
        return False


def create_roles_with_user_id(user_id: int, roles_id: list):
    try:
        for role_id in roles_id:
            user_role = UserRole(user_id=user_id, role_id=role_id)
            db.session.add(user_role)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        return False


def delete_all_user_by_role_id(role_id: int):
    try:
        UserRole.query.filter_by(role_id=role_id).delete()
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        return False
