# coding=utf-8
from app.core.models import db


class RolePermission(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "role_permission"

    role_id = db.Column(db.INT, db.ForeignKey('role.id'), nullable=False,
                        primary_key=True)
    permission_id = db.Column(db.INT, db.ForeignKey('permission.id'),
                              nullable=False, primary_key=True)

    # role = relationship(Role, backref=backref('role_permission', cascade='all, delete-orphan'))
    # permission = relationship(Permission, backref=backref('role_permission', cascade='all, delete-orphan'))

    def as_dict(self):
        return {
            'role_id': self.role_id,
            'permission_id': self.permission_id,
        }

    @classmethod
    def create(cls, role_id, permission_id):
        try:
            role_permission = RolePermission(
                role_id=role_id,
                permission_id=permission_id,
            )
            db.session.add(role_permission)
            db.session.commit()
            return role_permission
        except:
            return None
