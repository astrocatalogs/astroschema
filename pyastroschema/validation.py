"""
"""

import six

from jsonschema import FormatChecker
# from jsonschema.exceptions import ValidationError
from jsonschema import validators
from jsonschema import Draft4Validator as Validator

import pyastroschema as pas


def _extend_with_default(validator_class):
    """Take a given validator and add behavior to set default values if they are given.

    See: http://python-jsonschema.readthedocs.io/en/latest/faq/

    """
    validate_properties = validator_class.VALIDATORS["properties"]

    def set_defaults(validator, properties, instance, schema):
        for property, subschema in properties.items():
            if "default" in subschema:
                instance.setdefault(property, subschema["default"])

        for error in validate_properties(validator, properties, instance, schema):
            yield error

    return validators.extend(validator_class, {"properties": set_defaults})


_PAS_Validator = _extend_with_default(Validator)

# Create a new format checker instance.
format_checker = FormatChecker()


# Register a new format checker that checks for numerical values of the proper format
#     NOTE: list of valid numeric values is *not* accepted, must be specified in schema
@format_checker.checks(pas.KEY_FORMATS.NUMERIC)
def contains_numeric_value(value):
    if isinstance(value, list):
        return False

    if isinstance(value, six.string_types) and ' ' in value:
        return False

    try:
        float(value)
    except ValueError:
        return False

    return True


# Register a new format checker that checks for numerical values of the proper format
#     NOTE: list of valid numeric values is *not* accepted, must be specified in schema
@format_checker.checks(pas.KEY_FORMATS.ASTROTIME)
def is_astrotime_compatible(value):
    if isinstance(value, list):
        return False

    if (not contains_numeric_value(value)) and (('-' not in value) and ('/' not in value)):
        return False

    return True


# Register a new format checker that checks for string values
'''
@format_checker.checks(pas.STRING)
def is_string_format(value):
    if isinstance(value, six.string_types):
        return False

    return True
'''

# Create a new instance of your custom validator. Add a custom type.
def PAS_Validator(schema, **kwargs):
    pas_valid = _PAS_Validator(schema, format_checker=format_checker, **kwargs)
    return pas_valid


'''
# Example usage:
obj = {}
schema = {'properties': {'foo': {'default': 'bar'}}}
# Note jsonschem.validate(obj, schema, cls=DefaultValidatingDraft6Validator)
# will not work because the metaschema contains `default` directives.
DefaultValidatingDraft6Validator(schema).validate(obj)
assert obj == {'foo': 'bar'}
'''

'''
# Define custom validators. Each must take exactly 4 arguments as below.
def is_positive(validator, value, instance, schema):
    if not isinstance(instance, Number):
        yield ValidationError("%r is not a number" % (instance))

    if value and instance <= 0:
        yield ValidationError("%r is not positive integer" % (instance))
    elif not value and instance > 0:
        yield ValidationError("%r is not negative integer nor zero" % (instance))

# Add your custom validators among existing ones.
all_validators = dict(Draft4Validator.VALIDATORS)
all_validators["is_positive"] = is_positive

# Create a new validator class. It will use your new validators and the schema
# defined above.
MyValidator = validators.create(
    meta_schema=Draft4Validator.META_SCHEMA,
    validators=all_validators
)
'''
