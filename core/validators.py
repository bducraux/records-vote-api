import django
from django.core.validators import BaseValidator, ValidationError
import jsonschema


class JSONSchemaValidator(BaseValidator):
    def compare(self, value, schema):
        try:
            jsonschema.validate(value, schema)
        except jsonschema.exceptions.ValidationError:
            raise ValidationError(
                '%(value)s failed JSON schema check', params={'value': value}
            )
