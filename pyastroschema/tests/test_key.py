"""Test methods.

Can be run with:
    $ nosetests path/to/test_file.py
    $ nosetests path/to/test_file.py:Test_Class.test_method

"""
# from __future__ import absolute_import, division, print_function, unicode_literals

from nose.tools import assert_true, assert_raises   # , assert_false, assert_equal,

# import pyastroschema as pas
from pyastroschema.keys import Key

import jsonschema  # noqa
# from jsonschema.exceptions import ValidationError


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


def test_basics():
    t1 = Key("t1", type='string', unique=False)
    print("key = ", t1)
    print("type = '{}', unique = '{}', distinguishing = '{}'".format(
        t1.type, t1.unique, t1.distinguishing))
    assert_true(t1 == "t1")
    assert_true(t1.type == "string")
    assert_true(t1.unique == False)

    for kk, vv in SIMPLEST_SCHEMA['properties'].items():
        temp = Key(kk, **vv)
        assert_true(temp == kk)
        assert_true(temp.type == vv['type'])
        assert_true(temp.unique == vv['unique'])

    return


def test_init_errors():

    # NOTE: REMOVED this because defaults are now being set
    '''
    # Missing required attributes should raise an error
    with assert_raises(ValidationError):
        t2 = Key("t2")
        print(t2)
    with assert_raises(ValidationError):
        t2 = Key("t2", type='integer')
        print(t2)
    with assert_raises(ValidationError):
        t2 = Key("t2", unique=True)
        print(t2)
    '''

    # Non-lower-case name should raise error
    with assert_raises(ValueError):
        t2 = Key("HELLO", type='string', unique=True)
        print(t2)

    return


def test_comparisons():

    t1 = Key("t1", type='string', unique=False)
    t2 = Key("t2", type='string', unique=False)
    assert_true(t1 != t2)
    keys = set([t1, t2])
    assert_true(len(keys) == 2)

    t1 = Key("t1", type='string', unique=False)
    t2 = Key("t1", type='string', unique=False)
    assert_true(t1 == t2)
    keys = set([t1, t2])
    print(keys)
    assert_true(len(keys) == 1)

    # Only the string name itself should be used for comparisons
    t1 = Key("t1", type='string', unique=False)
    t2 = Key("t1", type='bool', unique=False)
    assert_true(t1 == t2)
    keys = set([t1, t2])
    print(keys)
    assert_true(len(keys) == 1)

    t1 = Key("t1", type='string', unique=False)
    t2 = Key("t1", type='bool', unique=True)
    assert_true(t1 == t2)
    keys = set([t1, t2])
    print(keys)
    assert_true(len(keys) == 1)
    return
