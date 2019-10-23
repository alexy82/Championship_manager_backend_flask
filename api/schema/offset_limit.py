from api.schema.base import BaseSchema
from marshmallow import fields, validate


class OffsetLimitSchema(BaseSchema):
    """
    Validate offset limit
    """
    offset = fields.Int(required=False, allow_none=False, validate=validate.Range(min=0), missing=0)
    limit = fields.Int(required=False, allow_none=False, validate=validate.Range(min=1), missing=500)
