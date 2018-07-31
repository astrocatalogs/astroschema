"""Test methods.

Can be run with:
    $ nosetests path/to/test_file.py
    $ nosetests path/to/test_file.py:Test_Class.test_method

"""
# from __future__ import absolute_import, division, print_function, unicode_literals
import copy

import jsonschema

from nose.tools import assert_true, assert_raises, assert_false  # , assert_equal,

# import pyastroschema as pas
from pyastroschema.struct import Quantity


YES_QUANT_0 = dict(
    value=3.14,
    source="0"
)

YES_QUANT_1 = dict(
    value="3.14",
    source=0
)

YES_QUANT_2 = dict(
    value="3.14",
    derived=True,
    description="Some info",
    units_value="km/s",
    units_error="dex",
    error_value="0.1",
    source=0
)

NAW_QUANT_0 = dict(
    value=3.14
)

NAW_QUANT_1 = dict(
    source="0"
)

NAW_QUANT_2 = dict()

NAW_QUANT_3 = dict(
    value="3.14",
    derived=5,      # derived must be boolean
    source=0
)

NAW_QUANT_4 = dict(
    value="3.14",
    kind="",      # kind must have length
    source=0
)

NAW_QUANT_5 = dict(
    value="hello",
    source="0"
)

YES_QUANTS = [YES_QUANT_0, YES_QUANT_1, YES_QUANT_2]
NAW_QUANTS = [NAW_QUANT_0, NAW_QUANT_1, NAW_QUANT_2, NAW_QUANT_3, NAW_QUANT_4, NAW_QUANT_5]


def test_basics():
    # source_schema = pas.utils.load_schema('source')

    # Should work with alias and arxivid

    for qkw in YES_QUANTS:
        print("Trying successful quantity: '{}'".format(qkw))
        quant = Quantity(**qkw)
        print("\t", quant)

    for qkw in NAW_QUANTS:
        print("Trying failure quantity: '{}'".format(qkw))
        with assert_raises(jsonschema.exceptions.ValidationError):
            quant = Quantity(**qkw)
            print("\t", quant)

    quant = Quantity(**YES_QUANT_0)
    keys = quant._keychain
    assert_true(quant['value'] == YES_QUANT_0['value'])
    assert_true(quant['source'] == YES_QUANT_0['source'])

    assert_true(quant[keys.VALUE] == YES_QUANT_0['value'])
    assert_true(quant[keys.SOURCE] == YES_QUANT_0['source'])

    return


'''
def test_duplicate_comparison():
    print("test_source.py:test_duplicate_comparison()")

    s1 = Source(**SIMPLEST_SOURCE)
    s2 = Source(**SIMPLEST_SOURCE)
    print("\nCompare True:")
    print("s1 = '{}'".format(repr(s1)))
    print("s2 = '{}'".format(repr(s2)))
    print('arxivid' in s1, s1['arxivid'])
    print('arxivid' in s2, s2['arxivid'])
    assert_false(s1 is s2)
    assert_true(s1.is_duplicate_of(s2, verbose=True))
    assert_true(s2.is_duplicate_of(s1, verbose=True))

    print("\nCompare False:")
    s1 = Source(**SIMPLEST_SOURCE)
    s2 = Source(validate=False)
    # Initialized with different values, duplicate should be false
    print("s1 = '{}'".format(repr(s1)))
    print("s2 = '{}'".format(repr(s2)))
    assert_false(s1.is_duplicate_of(s2))
    assert_false(s2.is_duplicate_of(s1))
    # Change values to match
    for kk, vv in SIMPLEST_SOURCE.items():
        s2[kk] = vv
    # Matching values should be duplicates
    print("\nCompare True:")
    print("s1 = '{}'".format(repr(s1)))
    print("s2 = '{}'".format(repr(s2)))
    assert_true(s1.is_duplicate_of(s2))
    assert_true(s2.is_duplicate_of(s1))

    # 'alias' is a non-distinguishing parameter, should not affect duplicate test
    s2['alias'] = 20
    assert_true(s1.is_duplicate_of(s2))
    assert_true(s2.is_duplicate_of(s1))

    # 'arxivid' is a distinguishing parameter, should affect duplicate test
    s2['arxivid'] = "1605.00000"
    assert_false(s1.is_duplicate_of(s2))
    assert_false(s2.is_duplicate_of(s1))

    s1 = Source(**SIMPLEST_SOURCE)
    s2 = Source(validate=False)
    s2['alias'] = s1['alias']
    assert_false(s1.is_duplicate_of(s2))
    assert_false(s2.is_duplicate_of(s1))

    return


def test_copy_shallow():

    s1 = Source(validate=False, extendable=True, alias=2, alias_other=[3])
    s1.t1 = [5]
    s2 = copy.copy(s1)

    # Copy and establish baseline, everything should be transferred
    print("s1['alias'] = ", s1['alias'],
          "s1['alias_other'] = ", s1['alias_other'],
          "s1.t1 = ", s1.t1)
    print("s2['alias'] = ", s2['alias'],
          "s2['alias_other'] = ", s2['alias_other'],
          "s2.t1 = ", s2.t1)

    assert_true(s1['alias'] == 2)
    assert_true(s1['alias_other'] == [3])
    assert_true(s1.t1 == [5])
    assert_true(s1['alias'] == s2['alias'])
    assert_true(s1['alias_other'] == s2['alias_other'])
    assert_true(s1.t1 == s2.t1)

    # Modify in original, complex variables should also copy, primitives not
    s1['alias'] = 20
    s1['alias_other'][0] = 30
    s1.t1[0] = 50

    print("s1['alias'] = ", s1['alias'],
          "s1['alias_other'] = ", s1['alias_other'],
          "s1.t1 = ", s1.t1)
    print("s2['alias'] = ", s2['alias'],
          "s2['alias_other'] = ", s2['alias_other'],
          "s2.t1 = ", s2.t1)

    assert_true(s1['alias'] == 20)
    assert_true(s1['alias_other'] == [30])
    assert_true(s1.t1 == [50])
    # This is a primitive and should not transfer
    assert_true(s1['alias'] != s2['alias'])
    # These are complex and should transfer
    assert_true(s1['alias_other'] == s2['alias_other'])
    assert_true(s1.t1 == s2.t1)

    return


def test_copy_deep():

    s1 = Source(validate=False, extendable=True, alias=2, alias_other=[3])
    s1.t1 = [5]
    s2 = copy.deepcopy(s1)

    # Copy and establish baseline, everything should be transferred
    print("s1['alias'] = ", s1['alias'],
          "s1['alias_other'] = ", s1['alias_other'],
          "s1.t1 = ", s1.t1)
    print("s2['alias'] = ", s2['alias'],
          "s2['alias_other'] = ", s2['alias_other'],
          "s2.t1 = ", s2.t1)

    assert_true(s1['alias'] == 2)
    assert_true(s1['alias_other'] == [3])
    assert_true(s1.t1 == [5])
    assert_true(s1['alias'] == s2['alias'])
    assert_true(s1['alias_other'] == s2['alias_other'])
    assert_true(s1.t1 == s2.t1)

    # Modify in original, complex variables should also copy, primitives not
    s1['alias'] = 20
    s1['alias_other'][0] = 30
    s1.t1[0] = 50

    print("s1['alias'] = ", s1['alias'],
          "s1['alias_other'] = ", s1['alias_other'],
          "s1.t1 = ", s1.t1)
    print("s2['alias'] = ", s2['alias'],
          "s2['alias_other'] = ", s2['alias_other'],
          "s2.t1 = ", s2.t1)

    assert_true(s1['alias'] == 20)
    assert_true(s1['alias_other'] == [30])
    assert_true(s1.t1 == [50])

    assert_true(s2['alias'] == 2)
    assert_true(s2['alias_other'] == [3])
    assert_true(s2.t1 == [5])

    return
'''
