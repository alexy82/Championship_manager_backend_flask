import datetime
import logging
from sqlalchemy.dialects.mysql import BIGINT

from app.core.models import db
from app.core.utils.helpers import obj_to_dict

LOGGER = logging.getLogger('main')


class ActivityLog(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "activity_log"

    id = db.Column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    object_id = db.Column(db.String(100), nullable=False)
    module = db.Column(db.String(80), nullable=False)
    action = db.Column(db.String(150), nullable=False)
    data = db.Column(db.Text, nullable=False)
    actor = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

    @classmethod
    def create(cls, obj_id, name, action, data, actor):
        try:
            log_inst = ActivityLog(
                object_id=obj_id,
                module=name,
                action=action,
                data=data,
                actor=actor,  # email
                created_at=datetime.datetime.utcnow()
            )
            return log_inst
        except Exception as e:
            LOGGER.error(
                'Unexpected error occurred when create activity log. Message: ' + str(
                    e))
            return None

    @classmethod
    def get_by_objectid_action(cls, obj_id, action):
        try:
            res = ActivityLog.query.filter_by(object_id=obj_id,
                                              action=action).order_by(
                ActivityLog.id.desc()).first()
            if res is not None:
                return obj_to_dict(res)
        except Exception as e:
            LOGGER.error(
                '{exc_type}: {exc_msg}'.format(exc_type=type(e).__name__,
                                               exc_msg=str(e)))
            return None
