"""Test methods.

Can be run with:
    $ nosetests path/to/test_file.py
    $ nosetests path/to/test_file.py:Test_Class.test_method

"""
# from __future__ import absolute_import, division, print_function, unicode_literals
# import copy
import warnings
import json
import os
# import jsonschema

from nose.tools import assert_true, assert_raises, assert_false  # , assert_equal,

import pyastroschema as pas
from pyastroschema.schema import SchemaDict


SIMPLEST_SCHEMA = dict(
    kitten=123,
    properties=dict(
        alias=dict(
            names={"type": "string"},
            type="string",
            unique=True
        ),
        name=dict(
            type="string",
            unique=True
        )
    )
)


def test_create_from_dict():
    schema = SchemaDict(SIMPLEST_SCHEMA)
    props = schema.properties
    assert_true('alias' in props)
    assert_true('name' in props)
    assert_false('hello' in props)

    return


def test_create_from_str():
    schema = SchemaDict.loads(json.dumps(SIMPLEST_SCHEMA))
    props = schema.properties
    assert_true('alias' in props)
    assert_true('name' in props)
    assert_false('hello' in props)

    with assert_raises(ValueError):
        SchemaDict("Hello")

    with assert_raises(ValueError):
        SchemaDict(123)

    SchemaDict({})
    SchemaDict()

    return


def test_create_from_file():
    schema_path = os.path.join(pas.PATHS.SCHEMA_DIR, 'source.json')
    schema = SchemaDict(schema_path)
    props = schema.properties
    assert_true('alias' in props)
    assert_true('arxivid' in props)
    assert_false('hello' in props)

    schema = SchemaDict.load(schema_path)
    props = schema.properties
    assert_true('alias' in props)
    assert_true('arxivid' in props)
    assert_false('hello' in props)

    return


def test_create_from_multiple():
    SCHEMA_1 = dict(
        kitten_one=123,
        properties=dict(
            alias=dict(
                names={"type": "string"},
                type="string",
                unique=True
            )
        )
    )

    SCHEMA_2 = dict(
        kitten_two=987,
        properties=dict(
            name=dict(
                type="string",
                unique=True
            )
        )
    )

    print("\n1+2 = ")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        # schema = SchemaDict([SCHEMA_1, SCHEMA_2])
        schema = SchemaDict(SCHEMA_1)
        schema.extend(SCHEMA_2)

    print(schema)
    props = schema.properties
    assert_true('alias' in props)
    assert_true('name' in props)
    assert_false('hello' in props)

    SCHEMA_3 = dict(
        properties=dict(
            name=dict(
                type="string",
                unique=True
            )
        )
    )

    print("\n2+3 = ")
    # schema = SchemaDict([SCHEMA_2, SCHEMA_3])
    schema = SchemaDict(SCHEMA_2)
    schema.extend(SCHEMA_3)
    print(schema)

    SCHEMA_3['properties']['name']['type'] = 'number'
    with assert_raises(ValueError):
        # schema = SchemaDict([SCHEMA_2, SCHEMA_3])
        schema = SchemaDict(SCHEMA_2)
        schema.extend(SCHEMA_3)

    return
