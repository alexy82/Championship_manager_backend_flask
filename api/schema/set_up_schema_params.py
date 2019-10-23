from api.schema.base import BaseSchema, NotBlank, Timestamp
from marshmallow import fields


def set_up_schema(model):
    config = {
        'str': fields.String(required=False, allow_none=False, validate=NotBlank.not_blank),
        'int': fields.Int(required=False, allow_none=False),
        'float': fields.Float(required=False, allow_none=False),
        'datetime': Timestamp(required=False, allow_none=False)
    }
    declared_fields = {}
    for att in dir(model):
        value = getattr(model, att)
        if hasattr(value, 'type'):
            att_type = value.type.python_type.__name__
            if att_type in config.keys():
                declared_fields.update({att: config[att_type]})

    class ParamsSchema(BaseSchema):
        """
        Validate params for API get list
        """
        pass

    ParamsSchema._declared_fields = declared_fields

    return ParamsSchema()
