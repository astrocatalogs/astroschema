"""Test methods.

Can be run with:
    $ nosetests path/to/test_file.py
    $ nosetests path/to/test_file.py:Test_Class.test_method

"""
# from __future__ import absolute_import, division, print_function, unicode_literals

from nose.tools import assert_true, assert_raises   # , assert_false, assert_equal,

# import pyastroschema as pas
from pyastroschema.keys import Key


SIMPLEST_SCHEMA = dict(
    kitten=123,
    properties=dict(
        alias=dict(
            names={"type": "string"},
            type="string",
            distinguishing=True
        ),
        name=dict(
            type="string",
            distinguishing=True
        )
    )
)


def test_basics():
    t1 = Key("t1", type='string', distinguishing=False)
    print(t1)
    assert_true(t1 == "t1")
    assert_true(t1.type == "string")
    assert_true(t1.distinguishing == False)

    for kk, vv in SIMPLEST_SCHEMA['properties'].items():
        temp = Key(kk, **vv)
        assert_true(temp == kk)
        assert_true(temp.type == vv['type'])
        assert_true(temp.distinguishing == vv['distinguishing'])

    return


def test_init_errors():

    # Missing required attributes should raise an error
    with assert_raises(ValueError):
        t2 = Key("t2")
        print(t2)
    with assert_raises(ValueError):
        t2 = Key("t2", type='integer')
        print(t2)
    with assert_raises(ValueError):
        t2 = Key("t2", distinguishing=True)
        print(t2)

    # Non-lower-case name should raise error
    with assert_raises(ValueError):
        t2 = Key("HELLO", type='string', distinguishing=True)
        print(t2)

    return


def test_comparisons():

    t1 = Key("t1", type='string', distinguishing=False)
    t2 = Key("t2", type='string', distinguishing=False)
    assert_true(t1 != t2)
    keys = set([t1, t2])
    assert_true(len(keys) == 2)

    t1 = Key("t1", type='string', distinguishing=False)
    t2 = Key("t1", type='string', distinguishing=False)
    assert_true(t1 == t2)
    keys = set([t1, t2])
    print(keys)
    assert_true(len(keys) == 1)

    # Only the string name itself should be used for comparisons
    t1 = Key("t1", type='string', distinguishing=False)
    t2 = Key("t1", type='bool', distinguishing=False)
    assert_true(t1 == t2)
    keys = set([t1, t2])
    print(keys)
    assert_true(len(keys) == 1)

    t1 = Key("t1", type='string', distinguishing=False)
    t2 = Key("t1", type='bool', distinguishing=True)
    assert_true(t1 == t2)
    keys = set([t1, t2])
    print(keys)
    assert_true(len(keys) == 1)
    return
