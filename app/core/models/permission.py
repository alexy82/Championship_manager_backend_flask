# coding=utf-8
from app.core.models import db


class Permission(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "permission"

    id = db.Column(db.INT, primary_key=True, autoincrement=True)
    key = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    module = db.Column(db.String(100), nullable=False)
    desc = db.Column(db.String(500), nullable=False)

    # users = relationship('User', secondary='user_permission')
    # roles = relationship('Role', secondary='role_permission')

    def as_dict(self):
        return {
            'id': self.id,
            'key': self.key,
            'name': self.name,
            'module': self.module,
            'desc': self.desc,
        }

    @classmethod
    def create(cls, key, name, module, desc):
        try:
            permission = Permission(
                key=key,
                name=name,
                module=module,
                desc=desc
            )
            db.session.add(permission)
            db.session.commit()
            return permission
        except:
            return None

    @classmethod
    def update(cls, data):
        try:
            permission = Permission.query.filter_by(id=data.get('id')).update(
                data)
            db.session.commit()
            return permission
        except:
            return None
