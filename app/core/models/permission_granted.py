# coding=utf-8
from app.core.models import db


class Permission(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "permission"

    user_role_id = db.Column(db.INT, primary_key=True)
    permission_id = db.Column(db.INT, primary_key=True)

    def as_dict(self):
        return {
            'user_role_id': self.user_role_id,
            'permission_id': self.permission_id
        }
