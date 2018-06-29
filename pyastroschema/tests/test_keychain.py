"""Test methods.

Can be run with:
    $ nosetests path/to/test_file.py
    $ nosetests path/to/test_file.py:Test_Class.test_method

"""
# from __future__ import absolute_import, division, print_function, unicode_literals

from nose.tools import assert_true, assert_raises  # , assert_false, assert_equal,

# import pyastroschema as pas
from pyastroschema.source import Keychain


SIMPLEST_SCHEMA = dict(
    kitten=123,
    properties=dict(
        alias=1,
        name={"type": "string"}
    )
)


def test_basics():
    keys = Keychain(SIMPLEST_SCHEMA)
    good_values = ["alias", "name"]
    good_keys = [gv.upper() for gv in good_values]

    print("Checking values")
    assert_true(len(keys.values()) == 2)
    assert_true(all([gv in keys.values() for gv in good_values]))
    #   test the `__contains__` overridden method
    assert_true(all([gv in keys for gv in good_values]))

    print("Checking keys")
    assert_true(len(keys.keys()) == 2)
    assert_true(all([gk in keys.keys() for gk in good_keys]))

    print("Checking attribute access")
    assert_true(keys.ALIAS == "alias")
    assert_true(keys.NAME == "name")
    with assert_raises(AttributeError):
        keys.alias
    with assert_raises(AttributeError):
        keys.name

    return


def test_mutable():
    print("Testing mutable=True")
    for extend in [True, False]:
        keys = Keychain(SIMPLEST_SCHEMA, mutable=True, extendable=extend)
        assert_true(keys.ALIAS == "alias")

        keys.ALIAS = "alias2"
        assert_true(keys.ALIAS == "alias2")
        assert_true(len(keys.keys()) == 2)
        assert_true(len(keys.values()) == 2)

    print("Testing mutable=False")
    for extend in [True, False]:
        keys = Keychain(SIMPLEST_SCHEMA, mutable=False, extendable=extend)
        assert_true(keys.ALIAS == "alias")

        with assert_raises(RuntimeError):
            keys.ALIAS = "alias2"

        assert_true(keys.ALIAS == "alias")
        assert_true(len(keys.keys()) == 2)
        assert_true(len(keys.values()) == 2)

    return


def test_extendable():
    print("Test extendable=True")
    for mutab in [True, False]:
        keys = Keychain(SIMPLEST_SCHEMA, mutable=mutab, extendable=True)

        # should be able to add an arbitrary key
        keys.CHECK_BIG = "check-big"
        keys.check_small = "check-small"
        good_keys = ["CHECK_BIG", "check_small"]
        good_values = ["check-big", "check-small"]

        print("Checking values")
        assert_true(len(keys.values()) == 4)
        assert_true(all([gv in keys.values() for gv in good_values]))

        print("Checking keys")
        assert_true(len(keys.keys()) == 4)
        assert_true(all([gk in keys.keys() for gk in good_keys]))

    print("Test extendable=False")
    for mutab in [True, False]:
        keys = Keychain(SIMPLEST_SCHEMA, mutable=mutab, extendable=False)

        # should be able to add an arbitrary key
        with assert_raises(RuntimeError):
            keys.CHECK_BIG = "check-big"
            keys.check_small = "check-small"

        assert_true(len(keys.values()) == 2)
        assert_true(len(keys.keys()) == 2)

    return


def test_valid_key_val():
    print("test_valid_key_val()")
    simplest = dict(
        properties=dict(
            alias=1
        )
    )

    print("\tChecking baseline")
    keys = Keychain(simplest)
    assert_true(len(keys.keys()) == 1)

    print("\tChecking skip underscores")
    for mutab in [True, False]:
        for extend in [True, False]:

            for bad_key in ["_test", "__test"]:
                badest = dict(
                    properties=dict(
                        alias=1,
                    )
                )
                badest['properties'][bad_key] = bad_key
                keys = Keychain(badest, mutable=mutab, extendable=extend)
                assert_true(len(keys.keys()) == 1)
                assert_true(len(keys.values()) == 1)
                assert_true(bad_key not in keys.values())
                assert_true(bad_key not in keys.keys())
                assert_true(bad_key.upper() not in keys.keys())
                # But it should still have the attribute
                assert_true(hasattr(keys, bad_key.upper()))
                check_val = getattr(keys, bad_key.upper())
                assert_true(check_val == bad_key)

    print("\tChecking skip callables")
    for mutab in [True, False]:

        good = dict(
            properties=dict(
                alias=1,
            )
        )
        good_key = "new"
        good['properties'][good_key] = 123
        keys = Keychain(good, mutable=mutab, extendable=True)
        assert_true(len(keys.keys()) == 2)
        assert_true(len(keys.values()) == 2)
        assert_true(good_key.upper() in keys.keys())
        assert_true(good_key in keys.values())

        bad_key = "new"
        bad_val = lambda xx: xx*2  # noqa
        setattr(keys, bad_key, bad_val)
        assert_true(len(keys.keys()) == 2)
        assert_true(len(keys.values()) == 2)
        assert_true(bad_key not in keys.keys())
        assert_true(bad_val not in keys.values())

        # But it still should have been added to the attributes
        assert_true(hasattr(keys, bad_key))
        assert_true(getattr(keys, bad_key) == bad_val)

    return
