"""Test methods.

Can be run with:
    $ nosetests path/to/test_file.py
    $ nosetests path/to/test_file.py:Test_Class.test_method

"""
# from __future__ import absolute_import, division, print_function, unicode_literals

import jsonschema

from nose.tools import assert_true, assert_raises, assert_false  # , assert_equal,

import pyastroschema as pas
# from pyastroschema.source import Source


SIMPLEST_SOURCE = dict(
    alias=0,
    name="Paper et al 2017"
)


def test_basics():
    # source_schema = pas.utils.load_schema('source')

    # Should work with alias and name
    source = pas.source.Source(**SIMPLEST_SOURCE)

    keys = source.keychain
    assert_true(source['alias'] == SIMPLEST_SOURCE['alias'])
    assert_true(source['name'] == SIMPLEST_SOURCE['name'])
    assert_true(source[keys.ALIAS] == SIMPLEST_SOURCE['alias'])
    assert_true(source[keys.NAME] == SIMPLEST_SOURCE['name'])

    return


def test_validation():

    # Load parameters during initialization
    # ----------------------------------------------

    # Should fail with no parameters
    with assert_raises(jsonschema.exceptions.ValidationError):
        source = pas.source.Source()

    # Should fail with negative alias
    with assert_raises(jsonschema.exceptions.ValidationError):
        source = pas.source.Source(name='Test', alias=-1)

    # Should fail with negative alias
    with assert_raises(jsonschema.exceptions.ValidationError):
        source = pas.source.Source(alias=0)

    # Load parameters after initialization
    # ----------------------------------------------
    source = pas.source.Source(validate=False)

    # Should fail with no parameters
    with assert_raises(jsonschema.exceptions.ValidationError):
        source.validate()

    for kk, vv in SIMPLEST_SOURCE.items():
        source[kk] = vv

    # Now it should validate okay
    source.validate()
    for kk, vv in SIMPLEST_SOURCE.items():
        assert_true(source[kk] == vv)

    # Should fail with deleted alias
    keys = source.keychain
    del source[keys.ALIAS]
    with assert_raises(jsonschema.exceptions.ValidationError):
        source.validate()

    return


def test_duplicate_comparison():
    print("test_source.py:test_duplicate_comparison()")

    s1 = pas.source.Source(validate=False)
    s2 = pas.source.Source(validate=False)
    assert_false(s1 is s2)
    assert_true(s1.is_duplicate_of(s2))
    assert_true(s2.is_duplicate_of(s1))

    s1 = pas.source.Source(**SIMPLEST_SOURCE)
    s2 = pas.source.Source(**SIMPLEST_SOURCE)
    assert_false(s1 is s2)
    assert_true(s1.is_duplicate_of(s2))
    assert_true(s2.is_duplicate_of(s1))

    s1 = pas.source.Source(**SIMPLEST_SOURCE)
    s2 = pas.source.Source(validate=False)
    assert_false(s1.is_duplicate_of(s2))
    assert_false(s2.is_duplicate_of(s1))
    for kk, vv in SIMPLEST_SOURCE.items():
        s2[kk] = vv

    assert_true(s1.is_duplicate_of(s2))
    assert_true(s2.is_duplicate_of(s1))

    s2['alias'] = 20
    assert_false(s1.is_duplicate_of(s2))
    assert_false(s2.is_duplicate_of(s1))

    s1 = pas.source.Source(**SIMPLEST_SOURCE)
    s2 = pas.source.Source(validate=False)
    s2['alias'] = s1['alias']
    assert_false(s1.is_duplicate_of(s2))
    assert_false(s2.is_duplicate_of(s1))

    return
