"""Test methods.

Can be run with:
    $ nosetests path/to/test_file.py
    $ nosetests path/to/test_file.py:Test_Class.test_method

"""

from nose.tools import assert_true, assert_raises

import pyastroschema as pas
from pyastroschema import struct, schema, keys


SCHEMA_0 = dict(
    properties=dict(
        name=dict(
            type="string"
        ),
        number=dict(
            type="number"
        )
    ),
    required=["name", "number"]
)


# This has no conflict with `SCHEMA_0`
SCHEMA_1 = dict(
    properties=dict(
        alias=dict(
            type="string"
        )
    )
)


# This conflicts with `SCHEMA_0`
SCHEMA_2 = dict(
    properties=dict(
        number=dict(
            type="string"
        )
    ),
    required=["name"]
)


def test_manual_subclass():
    print("test_struct.test_manual_subclass()")

    # First make sure schema is valid
    schema_dict = schema.SchemaDict(SCHEMA_0)

    # Try to create subclass, explicitly adding required attributes
    class Test_Struct(struct.Struct):
        _SCHEMA = schema_dict
        _KEYCHAIN = keys.Keychain(schema_dict)
        _extendable = True

    # Initialize instance
    test = Test_Struct(name="hello", number=1)
    assert_true(test["name"] == "hello")
    assert_true(test[test.keychain.NAME] == "hello")
    assert_true(test["number"] == 1)
    assert_true(test[test.keychain.NUMBER] == 1)

    with assert_raises(pas.ValidationError):
        Test_Struct(name="hello")

    with assert_raises(pas.ValidationError):
        Test_Struct(number=1)

    with assert_raises(pas.ValidationError):
        Test_Struct(name=1, number=1)

    with assert_raises(pas.ValidationError):
        test = Test_Struct(name="hello", number='1')

    return


def test_decorated_subclass():
    print("test_struct.test_decorated_subclass()")

    # First make sure schema is valid
    schema_dict = schema.SchemaDict(SCHEMA_0)

    # Try to create subclass, explicitly adding required attributes
    @struct.set_struct_schema(schema_dict)
    class Test_Struct(struct.Struct):
        pass

    # Initialize instance
    test = Test_Struct(name="hello", number=1)
    assert_true(test["name"] == "hello")
    assert_true(test[test.keychain.NAME] == "hello")
    assert_true(test["number"] == 1)
    assert_true(test[test.keychain.NUMBER] == 1)

    with assert_raises(pas.ValidationError):
        Test_Struct(name="hello")

    with assert_raises(pas.ValidationError):
        Test_Struct(number=1)

    with assert_raises(pas.ValidationError):
        Test_Struct(name=1, number=1)

    with assert_raises(pas.ValidationError):
        test = Test_Struct(name="hello", number='1')

    return


def test_factory_subclass():
    print("test_struct.test_factory_subclass()")

    # First make sure schema is valid
    schema_dict = schema.SchemaDict(SCHEMA_0)

    # Try to create subclass, explicitly adding required attributes
    Test_Struct = struct.Struct.construct(schema_dict)

    # Initialize instance
    test = Test_Struct(name="hello", number=1)
    assert_true(test["name"] == "hello")
    assert_true(test[test.keychain.NAME] == "hello")
    assert_true(test["number"] == 1)
    assert_true(test[test.keychain.NUMBER] == 1)

    with assert_raises(pas.ValidationError):
        Test_Struct(name="hello")

    with assert_raises(pas.ValidationError):
        Test_Struct(number=1)

    with assert_raises(pas.ValidationError):
        Test_Struct(name=1, number=1)

    with assert_raises(pas.ValidationError):
        test = Test_Struct(name="hello", number='1')

    return


def test_struct_extend():
    print("test_struct.test_struct_extend()")

    # Test basic `SCHEMA_0`, make sure everything works
    # -----------------------------------------------------------
    Test_Struct = struct.Struct.construct(SCHEMA_0)

    #     allows extra property `alias` to be whatever
    Test_Struct(name="hello", number=1, alias=2)
    with assert_raises(pas.ValidationError):
        Test_Struct(name="hello")

    # Extend to specify that `alias` must be a string
    # ----------------------------------------------------------
    Test_Struct = struct.Struct.construct(SCHEMA_0, extensions=[SCHEMA_1])

    # Succeeds to str `alias`
    Test_Struct(name="hello", number=1, alias="2")
    # fails if `alias` is a number
    with assert_raises(pas.ValidationError):
        Test_Struct(name="hello", number=1, alias=2)

    # Extend should fail if it produces a conflict
    # ----------------------------------------------------------
    with assert_raises(ValueError):
        Test_Struct = struct.Struct.construct(SCHEMA_0, extensions=[SCHEMA_2])

    return


def test_struct_update():
    print("test_struct.test_struct_update()")

    # Test basic `SCHEMA_0`, make sure everything works
    # -----------------------------------------------------------
    Test_Struct = struct.Struct.construct(SCHEMA_0)

    # `SCHEMA_0` says both `name` and `number` are required
    Test_Struct(name="hello", number=1)
    with assert_raises(pas.ValidationError):
        Test_Struct(name="hello")

    # Update with `SCHEMA_2`, says that only `name` is required
    # ----------------------------------------------------------
    Test_Struct = struct.Struct.construct(SCHEMA_0, updates=[SCHEMA_2])
    Test_Struct(name="hello")

    return


def test_custom_schema_class():

    schema_0 = dict(
        properties=dict(
            name_test=dict(
                type="string"
            ),
            number_test=dict(
                type="number"
            )
        ),
        required=["name_test", "number_test"]
    )

    # Make sure class works as expected; requires both `name_test` and `number_test`
    Test_Struct = struct.Struct.construct(schema_0)
    Test_Struct(name_test="hello", number_test=1)
    with assert_raises(pas.ValidationError):
        Test_Struct(nametest="hello", numbertest=1)

    # Modify the schema in place to change `name_test` to `nametest`... etc
    class Test_SchemaDict(schema.SchemaDict):

        def finalize(self):
            keys = list(self['properties'].keys())
            print("\nold = \n", self)
            for old in keys:
                new = old.replace('_', '')
                self['properties'][new] = self['properties'][old]
                del self['properties'][old]
                idx = self['required'].index(old)
                self['required'][idx] = new

            print("\nnew = \n", self)
            return

    # Make sure modifications take effect, now require `nametest` and `numbertest`
    Test_Struct = struct.Struct.construct(schema_0, schema_class=Test_SchemaDict)
    Test_Struct(nametest="hello", numbertest=1)
    with assert_raises(pas.ValidationError):
        Test_Struct(name_test="hello", number_test=1)

    return
