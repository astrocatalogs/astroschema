"""
"""

from jsonschema import validators
from jsonschema import Draft4Validator as Validator


def extend_with_default(validator_class):
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


Validator_Defaults = extend_with_default(Validator)

'''
# Example usage:
obj = {}
schema = {'properties': {'foo': {'default': 'bar'}}}
# Note jsonschem.validate(obj, schema, cls=DefaultValidatingDraft6Validator)
# will not work because the metaschema contains `default` directives.
DefaultValidatingDraft6Validator(schema).validate(obj)
assert obj == {'foo': 'bar'}
'''
