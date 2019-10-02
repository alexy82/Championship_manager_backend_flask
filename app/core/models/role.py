# coding=utf-8
import datetime

from app.core.models import db


class Role(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "role"

    id = db.Column(db.INT, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150), nullable=False)
    desc = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime)

    # users = relationship('User', secondary='user_role')
    # permissions = relationship('Permission', secondary='role_permission')

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'desc': self.desc,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
        }

    @classmethod
    def create(cls, name, desc):
        try:
            role = Role(
                name=name,
                desc=desc,
                created_at=datetime.datetime.utcnow(),
                updated_at=datetime.datetime.utcnow(),
            )
            db.session.add(role)
            db.session.commit()
            return role
        except:
            return None

    @classmethod
    def update(cls, data):
        try:
            role_data = {}
            for key in data:
                if hasattr(cls, key):
                    role_data[key] = data[key]
            role_data['updated_at'] = datetime.datetime.now()
            role = Role.query.filter_by(id=role_data.get('id')).update(
                role_data)
            db.session.commit()
            return role
        except:
            return None

    @classmethod
    def delete(cls, role_id):
        try:
            Role.query.filter_by(id=role_id).delete()
            db.session.commit()
            return True
        except:
            db.session.rollback()
            return False
