# coding=utf-8
from app.core.models.role_permission import RolePermission
from app.core.models import db


def delete_all_permission_by_role_id(role_id: int):
    try:
        RolePermission.query.filter_by(role_id=role_id).delete()
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        return False


def create_permissions_with_role_id(role_id: int, permissions_id: list):
    try:
        for permission_id in permissions_id:
            role_permission = RolePermission(role_id=role_id,
                                             permission_id=permission_id)
            db.session.add(role_permission)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        return False
