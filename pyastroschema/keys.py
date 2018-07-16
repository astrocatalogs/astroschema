"""
"""

import os

# import jsonschema

from . import SCHEMA_KEYS, PATHS
from . import utils, validation


class Key(str):

    __key_schema_fname = os.path.join(PATHS.SCHEMA_DIR, "key.json")
    __key_schema = utils.json_load_file(__key_schema_fname)

    def __new__(cls, name, **kwargs):
        # Enforce lower-case
        if not name.islower():
            raise ValueError("`Key` strings must be lower case!  '{}' invalid".format(name))
        return str.__new__(cls, name)

    def __init__(self, name, **kwargs):
        super(Key, self).__init__()
        for kk, vv in kwargs.items():
            setattr(self, kk, vv)

        # Validate
        self.validate()
        return

    def __repr__(self):
        prop_names = self.schema['properties'].keys()
        prop_list = []
        for pn in prop_names:
            if hasattr(self, pn):
                prop_list.append("{}: '{}'".format(pn, getattr(self, pn)))

        rv = "'{}': ({})".format(str(self), ", ".join(prop_list))
        return rv

    def validate(self):
        """Check for consistency between the stored parameters and schema.
        """
        # Use a custom validator that sets default values
        validator = validation.Validator_Defaults(self.__key_schema)
        validator.validate(self.__dict__)
        # jsonschema.validate(self.__dict__, schema)
        return

    @property
    def schema(self):
        return self.__key_schema


class Keychain(object):
    """Store the named parameters associated with schema properties and entry values.
    """

    _USE_UPPER_CASE = True

    def __init__(self, schema, mutable=False, extendable=True):
        """Initialize this `Keys` object using properties from given schema as keys.

        Arguments
        ---------
        schema : dict,
            A dictionary that is a valid JSON schema specifying the contents of a structure.
        mutable : bool,
            If `True`, then the values associated with stored keys can be changed at runtime.
            This setting does not affect whether new key-value pairs can be added.
        extendable : bool,
            If `True`, then new key-value pairs can be added after initialization.
            This setting does not affect whether existing key-value pairs can be modified.

        """
        props = schema[SCHEMA_KEYS.PROPS]

        # Store all of the property names to this object
        for prop_name, prop_vals in props.items():
            use_name = prop_name.upper() if self._USE_UPPER_CASE else prop_name
            _key = Key(prop_name, **prop_vals)
            setattr(self, use_name, _key)

        # This must be set after changed are made, so that 'False' values will not lead to error
        self._mutable = mutable
        self._extendable = extendable
        return

    def __setattr__(self, name, value):
        """Control mutability and extendability, and store keys when they match requirements.
        """

        # Only control mutability if the `_mutable` variable is set (should happen at end of init)
        if hasattr(self, "_mutable"):
            # If this instance is *not* mutable, but this `name` is already set... raise error
            if not self._mutable and hasattr(self, name):
                raise RuntimeError("This instance is not mutable, cannot modify existing key!")

        # Only control extendability if `_extendable` variable is set (happens at end of init)
        if hasattr(self, "_extendable"):
            # If this instance is *not* extendable, and this `name` is new... raise error
            if not self._extendable and not hasattr(self, name):
                raise RuntimeError("This instance is not extendable, cannot add a new key!")

        # Only store attributes if `_keys` exists
        #    this is needed to prevent recursion when adding `_keys`
        if isinstance(value, Key):
            if not hasattr(self, "_keys"):
                self._keys = []

            # Store valid new attributes to the keys and values lists
            if not hasattr(self, name):
                self._keys.append(value)
            # Update existing attributes
            elif hasattr(self, name):
                idx = self._keys.index(name)
                self._keys[idx] = value

        # Actually store key-value pair as an attribute
        super(Keychain, self).__setattr__(name, value)
        return

    def keys(self):
        return self._keys

    def __contains__(self, key):
        cont = (key in self._keys)
        return cont
