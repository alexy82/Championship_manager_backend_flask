# coding=utf-8
"""
Base Schema for message
"""
import json
import logging
import datetime
import re
from logging import config
from marshmallow import Schema, ValidationError, validate, fields
from marshmallow.fields import DateTime, Boolean, Dict, Str

from configs import LOGGING

logging.config.dictConfig(LOGGING)

_logger = logging.getLogger('main')


class BaseSchema(Schema):
    """
    Base schema for api
    """
    _raw_data = None
    errors = {}
    data = {}

    def load_data(self, dict_or_json):
        """
        Load and validate data
        :param dict_or_json:
        :return:
        """
        if isinstance(dict_or_json, dict):
            self._raw_data = dict_or_json
        else:
            try:
                self._raw_data = json.loads(dict_or_json)
            except:
                self._raw_data = None
        self.parse_message()
        self.validate_data()

    def validate_data(self):
        """
        Validate data
        :return:
        """
        try:
            self.errors = self.validate(data=self._raw_data)
        except Exception as ex:
            _logger.exception(ex)
        if not any(self.errors):
            self.data = self.load(self._raw_data)

    def is_valid(self, raise_error=False):
        """
        Check if data is valid or not
        :return:
        """
        if not any(self.errors):  # validate date, self.errors may not empty if has not been checked
            self.validate_data()
        if any(self.errors) and raise_error:  # check if error and raise
            raise ValidationError(
                '{class_name} | {errors}'.format(class_name=self.__class__.__name__,
                                                 errors=self.errors))
        return not any(self.errors)

    def parse_message(self):
        """
        Parse message
        :return:
        """
        pass


class NotBlank():
    """ String not blank"""
    not_blank = validate.Length(min=1)


def format_from_pattern(value, localtime=False, pattern='%Y-%m-%d %H:%M:%S'):
    result = datetime.datetime.strptime(str(value), pattern)
    return result


def format_by_pattern(value, localtime=False, pattern='%Y-%m-%d %H:%M:%S'):
    # print(type(value), value)
    result = datetime.datetime.strftime(value, pattern)
    return result


class CustomDateTime(DateTime):
    DATEFORMAT_SERIALIZATION_FUNCS = {
        'default': format_by_pattern,
    }

    DATEFORMAT_DESERIALIZATION_FUNCS = {
        'default': format_from_pattern,
    }

    DEFAULT_FORMAT = 'default'

    default_error_messages = {
        'invalid': 'Not a valid datetime.',
        'format': '"{input}" cannot be formatted as a datetime.',
    }

    def __init__(self, format=None, pattern='%Y-%m-%d %H:%M:%S', **kwargs):
        super(CustomDateTime, self).__init__(**kwargs)
        self.dateformat = format
        self.pattern = pattern

    def _add_to_schema(self, field_name, schema):
        super(CustomDateTime, self)._add_to_schema(field_name, schema)
        self.dateformat = self.dateformat or schema.opts.dateformat

    def _serialize(self, value, attr, obj):
        if value is None:
            return None
        self.dateformat = self.dateformat or self.DEFAULT_FORMAT
        format_func = self.DATEFORMAT_SERIALIZATION_FUNCS.get(self.dateformat, None)
        if format_func:
            try:
                return format_func(value, self.localtime, self.pattern)
            except (AttributeError, ValueError):
                self.fail('format', input=value)
        else:
            return value.strftime(self.dateformat)

    def _deserialize(self, value, attr, data):
        if not value:
            raise self.fail('invalid')
        self.dateformat = self.dateformat or self.DEFAULT_FORMAT
        func = self.DATEFORMAT_DESERIALIZATION_FUNCS.get(self.dateformat)
        if func:
            try:
                return func(value, self.localtime, self.pattern)
            except (TypeError, AttributeError, ValueError):
                raise self.fail('invalid')
        elif self.dateformat:
            try:
                return datetime.datetime.strptime(value, self.dateformat)
            except (TypeError, AttributeError, ValueError):
                raise self.fail('invalid')


class Timestamp(fields.Date):
    default_error_messages = {
        'invalid': 'Not a valid timestamp.',
    }

    def _deserialize(self, value, attr, data):
        try:
            value = int(value)
        except:
            return self.fail('invalid')

        if value is None:
            return self.fail('invalid')
        if value < 0:
            raise self.fail('invalid')
        return datetime.date.fromtimestamp(value)


class SkipField(Dict):

    def _deserialize(self, value, attr, data):
        return value


class CustomEmail(Str):
    default_error_messages = {
        'invalid': 'Not a valid email.'
    }

    def __init__(self, allow_blank=False, **kwargs):
        super(CustomEmail, self).__init__(**kwargs)
        self.allow_blank = allow_blank

    def _deserialize(self, value, attr, data):
        if type(value) != str:
            self.fail('invalid')
        if self.allow_blank and value == "":
            return value
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            self.fail('invalid')
        return value


class TemplateField(Str):
    default_error_messages = {
        'invalid': 'value is not match with template'
    }

    def __init__(self, template, allow_blank=False, **kwargs):

        super(TemplateField, self).__init__(**kwargs)
        self.template = template
        self.allow_blank = allow_blank

    def _deserialize(self, value, attr, data):
        if self.allow_blank and value == "":
            return value
        if value not in self.template:
            self.fail('invalid')
        return value


class CustomBoolean(Boolean):
    default_error_messages = {
        'invalid': 'Not a valid boolean.'
    }

    def _serialize(self, value, attr, obj):
        return value

    def _deserialize(self, value, attr, data):
        if type(value) != bool:
            self.fail('invalid')


class ErrorSchema(BaseSchema):
    code = fields.Int(required=True, allow_none=False)
    detail = fields.Str(required=True, allow_none=False, validate=NotBlank.not_blank)


def get_api_schema(schema):
    """ For detail API"""

    class DetailAPISchema(BaseSchema):
        data = fields.Nested(schema)
        error = fields.Nested(ErrorSchema)

    return DetailAPISchema()


def get_data_list_schema(schema):
    """ For list API """

    class DataListSchema(BaseSchema):
        items = fields.List(fields.Nested(schema), required=True, allow_none=False)
        total = fields.Int(required=True, allow_none=False, validate=validate.Range(min=0))
        # @marshmallow.validates_schema(skip_on_field_errors=True)
        # def constraint(self, data):
        #     def check_total(data):
        #         items = data['items']
        #         total = data['total']
        #         if total != len(items):
        #             raise ValidationError('number element of items must equal to total')
        #
        #     check_total(data)

    return DataListSchema()


class ErrorAPISchema(BaseSchema):
    """ For error response"""
    data = SkipField()
    error = fields.Nested(ErrorSchema, required=True, allow_none=False)


class IdSchema(BaseSchema):
    """Validate id auto increase
    """
    id = fields.Int(required=True, allow_none=False, validate=validate.Range(min=1))
