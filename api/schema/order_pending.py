from apiv1.schema.base import BaseSchema
from marshmallow import fields, validate


class OrderPendingSchema(BaseSchema):
    offset = fields.Int(required=False, allow_none=False, validate=validate.Range(min=0), missing=0)
    limit = fields.Int(required=False, allow_none=False, validate=validate.Range(min=1), missing=100)
    sso_id = fields.Int(required=False, allow_none=False, validate=validate.Range(min=1))
    region = fields.String(required=False, allow_none=False, validate=validate.Length(min=1))
    order_code = fields.String(required=False, allow_none=False, validate=validate.Length(min=1))
