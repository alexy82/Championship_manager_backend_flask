# coding=utf-8
from app.core.models import db

from sqlalchemy.dialects.mysql import BIGINT


class UserRole(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "user_role"

    user_id = db.Column(BIGINT(unsigned=True), db.ForeignKey('user.id'), nullable=False,
                        primary_key=True)
    role_id = db.Column(db.INT, db.ForeignKey('role.id'), nullable=False,
                        primary_key=True)

    # user = relationship(User, backref=backref('user_role', cascade='all, delete-orphan'))
    # role = relationship(Role, backref=backref('user_role', cascade='all, delete-orphan'))

    def as_dict(self):
        return {
            'user_id': self.user_id,
            'role_id': self.role_id,
        }

    @classmethod
    def create(cls, user_id, role_id):
        try:
            user_role = UserRole(
                user_id=user_id,
                role_id=role_id,
            )
            db.session.add(user_role)
            db.session.commit()
            return user_role
        except:
            return None
