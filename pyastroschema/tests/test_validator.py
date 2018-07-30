"""Test methods.

Can be run with:
    $ nosetests path/to/test_file.py
    $ nosetests path/to/test_file.py:Test_Class.test_method

"""
# from __future__ import absolute_import, division, print_function, unicode_literals

from nose.tools import assert_true, assert_raises   # , assert_false, assert_equal,

# import pyastroschema as pas
from pyastroschema.validation import PAS_Validator

import jsonschema  # noqa
from jsonschema.exceptions import ValidationError


schema_numeric = {
    "type": ["number", "string"],
    "format": "numeric"
}

schema_numeric_list = {
    "type": "array",
    "items": {
        "type": ["number", "string"],
        "format": "numeric"
    }
}

schema_numeric_listable = {
    "anyOf": [schema_numeric, schema_numeric_list]
}


def test_numeric():
    validator = jsonschema.validators.validator_for(schema_numeric)
    validator.check_schema(schema_numeric)

    pas_valid = PAS_Validator(schema_numeric)

    pas_valid.validate(2.234)
    pas_valid.validate("2.234")
    pas_valid.validate("2.23e4")
    pas_valid.validate("-2.23e4")
    pas_valid.validate("89")
    pas_valid.validate("-89")

    with assert_raises(ValidationError):
        pas_valid.validate(" 2.234")

    with assert_raises(ValidationError):
        pas_valid.validate("2.234 ")

    with assert_raises(ValidationError):
        pas_valid.validate("2p234")

    with assert_raises(ValidationError):
        pas_valid.validate("h")

    with assert_raises(ValidationError):
        pas_valid.validate(["2.234", "12"])

    with assert_raises(ValidationError):
        pas_valid.validate([2.234e2, 12])

    return


def test_numeric_list():
    validator = jsonschema.validators.validator_for(schema_numeric_list)
    validator.check_schema(schema_numeric_list)

    pas_valid = PAS_Validator(schema_numeric_list)

    pas_valid.validate([2.234, 12.32])
    pas_valid.validate(["2.234", "-9e12"])
    pas_valid.validate([23.23e2, "-9e12"])

    with assert_raises(ValidationError):
        pas_valid.validate([12, " 2.234"])

    with assert_raises(ValidationError):
        pas_valid.validate([12, "2.234", "hello"])

    with assert_raises(ValidationError):
        pas_valid.validate("2.234")

    with assert_raises(ValidationError):
        pas_valid.validate(12)

    return


def test_numeric_listable():
    validator = jsonschema.validators.validator_for(schema_numeric_listable)
    validator.check_schema(schema_numeric_listable)

    pas_valid = PAS_Validator(schema_numeric_listable)

    pas_valid.validate(2.234)
    pas_valid.validate("2.234")
    pas_valid.validate("2.23e4")
    pas_valid.validate("-2.23e4")
    pas_valid.validate("89")
    pas_valid.validate("-89")

    with assert_raises(ValidationError):
        pas_valid.validate(" 2.234")

    with assert_raises(ValidationError):
        pas_valid.validate("2.234 ")

    with assert_raises(ValidationError):
        pas_valid.validate("2p234")

    with assert_raises(ValidationError):
        pas_valid.validate("h")

    pas_valid.validate([2.234, 12.32])
    pas_valid.validate(["2.234", "-9e12"])
    pas_valid.validate([23.23e2, "-9e12"])

    with assert_raises(ValidationError):
        pas_valid.validate([12, " 2.234"])

    with assert_raises(ValidationError):
        pas_valid.validate([12, "2.234", "hello"])

    return
