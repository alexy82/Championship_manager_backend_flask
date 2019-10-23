# coding=utf-8
from app.core.models import db

from sqlalchemy.dialects.mysql import BIGINT


class UserPermission(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "user_permission"

    user_id = db.Column(BIGINT(unsigned=True), db.ForeignKey('user.id'), nullable=False,
                        primary_key=True)
    permission_id = db.Column(db.INT, db.ForeignKey('permission.id'),
                              nullable=False, primary_key=True)

    # user = relationship(User, backref=backref('user_permission', cascade='all, delete-orphan'))
    # permission = relationship(Permission, backref=backref('user_permission', cascade='all, delete-orphan'))

    def as_dict(self):
        return {
            'user_id': self.user_id,
            'permission_id': self.permission_id,
        }

    @classmethod
    def create(cls, user_id, permission_id):
        try:
            user_permission = UserPermission(
                user_id=user_id,
                permission_id=permission_id,
            )
            db.session.add(user_permission)
            db.session.commit()
            return user_permission
        except:
            return None
