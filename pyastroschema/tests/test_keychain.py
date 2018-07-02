"""Test methods.

Can be run with:
    $ nosetests path/to/test_file.py
    $ nosetests path/to/test_file.py:Test_Class.test_method

"""
# from __future__ import absolute_import, division, print_function, unicode_literals

from nose.tools import assert_true, assert_raises  # , assert_false, assert_equal,

# import pyastroschema as pas
from pyastroschema.keys import Keychain, Key


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
    keys = Keychain(SIMPLEST_SCHEMA)
    good_keys = SIMPLEST_SCHEMA['properties'].keys()

    print("Checking keys")
    assert_true(len(keys.keys()) == len(good_keys))
    assert_true(all([gk in keys.keys() for gk in good_keys]))

    print("Checking attribute access")
    for kk, vv in SIMPLEST_SCHEMA['properties'].items():
        # Get each key
        temp = getattr(keys, kk)
        # The key should be a string (subclass) equal to its name
        assert_true(temp == kk)
        for k2, v2 in vv.items():
            # The attributes of the key should match the dictionary values
            assert_true(getattr(temp, k2) == v2)

    return


def test_mutable():
    print("Testing mutable=True")
    for extend in [True, False]:
        keys = Keychain(SIMPLEST_SCHEMA, mutable=True, extendable=extend)
        assert_true(keys.alias == "alias")

        # Added general attribute should not count as a `Key`
        keys.alias = "alias2"
        assert_true(keys.alias == "alias2")
        assert_true(len(keys.keys()) == 2)

    print("Testing mutable=False")
    for extend in [True, False]:
        keys = Keychain(SIMPLEST_SCHEMA, mutable=False, extendable=extend)
        assert_true(keys.alias == "alias")

        with assert_raises(RuntimeError):
            keys.alias = "alias2"

        assert_true(keys.alias == "alias")
        assert_true(len(keys.keys()) == 2)

    return


def test_extendable():

    print("Testing adding random attribute")

    print("\tTest extendable=True")
    for mutab in [True, False]:
        keys = Keychain(SIMPLEST_SCHEMA, mutable=mutab, extendable=True)
        good_keys = SIMPLEST_SCHEMA['properties'].keys()

        # should be able to add an arbitrary attribute
        keys.test = "test"
        print("\tChecking keys")
        # Should not be counted as a `Key` proper
        assert_true(len(keys.keys()) == 2)
        assert_true(all([gk in keys.keys() for gk in good_keys]))

    print("\tTest extendable=False")
    for mutab in [True, False]:
        keys = Keychain(SIMPLEST_SCHEMA, mutable=mutab, extendable=False)

        # should be able to add an arbitrary key
        with assert_raises(RuntimeError):
            keys.test = "test"

        assert_true(len(keys.keys()) == 2)

    # -------------------
    print("Testing adding new `Key`")

    print("\tTest extendable=True")
    for mutab in [True, False]:
        keys = Keychain(SIMPLEST_SCHEMA, mutable=mutab, extendable=True)
        good_keys = SIMPLEST_SCHEMA['properties'].keys()

        keys.test = Key("test", type='string', distinguishing=False)
        good_keys = list(good_keys) + ['test']
        print("\tChecking keys")
        # Should not be counted as a `Key` proper
        assert_true(len(keys.keys()) == len(good_keys))
        assert_true(all([gk in keys.keys() for gk in good_keys]))

    print("\tTest extendable=False")
    for mutab in [True, False]:
        keys = Keychain(SIMPLEST_SCHEMA, mutable=mutab, extendable=False)

        # should be able to add an arbitrary key
        with assert_raises(RuntimeError):
            keys.test = Key("test", type='string', distinguishing=False)

        assert_true(len(keys.keys()) == 2)

    return
