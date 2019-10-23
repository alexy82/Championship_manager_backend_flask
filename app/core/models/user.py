# coding=utf-8
import datetime
import logging

from app.core.models import db
from sqlalchemy.dialects.mysql import BIGINT, TINYINT

LOGGER = logging.getLogger('main')


class User(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "user"

    id = db.Column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    username = db.Column(db.String(100), unique=True)
    fullname = db.Column(db.String(125), nullable=False)
    mobile = db.Column(db.String(32))
    is_active = db.Column(db.Boolean, index=True)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime)
    last_login = db.Column(db.DateTime)

    def __repr__(self):
        return "<User '{}'>".format(self.username)

    def as_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'fullname': self.fullname,
            'mobile': self.mobile,
            'sso_user_id': self.sso_user_id,
            'is_active': self.is_active,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            'last_login': self.last_login.strftime('%Y-%m-%d %H:%M:%S'),
        }

    @classmethod
    def create(cls, email, username, fullname, mobile):
        try:
            user = User(
                email=email,
                username=username,
                fullname=fullname,
                mobile=mobile,
                is_active=True,
                created_at=datetime.datetime.utcnow(),
                updated_at=datetime.datetime.utcnow(),
                last_login=datetime.datetime.utcnow(),
            )
            db.session.add(user)
            db.session.commit()
            return user
        except Exception as e:
            LOGGER.error(
                'Unexpected error occurred when create user. Message: ' + str(
                    e))
            return None

    @classmethod
    def update(cls, data):
        try:
            user_data = {}
            for key in data:
                if hasattr(cls, key):
                    user_data[key] = data[key]
            user_data['updated_at'] = datetime.datetime.utcnow()
            if 'id' not in user_data:
                user = User.query.filter_by(email=user_data.get('email'))
                user.update(user_data)
            else:
                user = User.query.filter_by(id=user_data.get('id'))
                user.update(user_data)
            db.session.commit()
            return user.first()
        except:
            return None

    @classmethod
    def delete(cls, user_id):
        try:
            User.query.filter_by(id=user_id).delete()
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            return False
