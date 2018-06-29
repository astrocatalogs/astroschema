"""Eventually this will be generalized from 'source' specifically to any 'struct'.
"""

from collections import OrderedDict

import jsonschema

from . import utils
from . import SCHEMA_KEYS


class Keychain(object):
    """Store the named parameters associated with schema properties and entry values.
    """

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
        # `_keys` must be created before keys will be stored internally in `setattr`
        self._keys = []
        self._values = []

        # Store all of the property names to this object
        for prop_name in props.keys():
            setattr(self, prop_name.upper(), prop_name)

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
        if hasattr(self, "_keys") and self._test_key_val(name, value):
            # Store valid new attributes to the keys and values lists
            if not hasattr(self, name):
                self._keys.append(name)
                self._values.append(value)
            # Update existing attributes
            elif hasattr(self, name):
                idx = self._keys.index(name)
                self._values[idx] = value

        # Actually store key-value pair as an attribute
        super(Keychain, self).__setattr__(name, value)
        return

    def __contains__(self, key):
        cont = (key in self.values())
        return cont

    def keys(self):
        return self._keys

    def values(self):
        return self._values

    @staticmethod
    def _test_key_val(key, val):
        """Determine if the given key-value pair is valid.
        """
        if key.startswith('_'):
            return False
        if callable(val):
            return False
        return True


class Source(OrderedDict):

    def __init__(self, *args, extendable=False, validate=True, **kwargs):
        """Initialize with parameters based on the associated schema.

        Arguments
        ---------
        *args : None,
            NOT ALLOWED.  Only keyword-arguments (`kwargs`) can be used.
        extendable : bool,
            If `True`, then new key-value pairs can be added to this dict after initialization.
        validate : bool,
            If `True`, then the internal validation method is called to compare values against the
            associated schema.
        **kwargs : dict,
            Key-value pairs to be stored to this dictionary during initialization.

        """
        if len(args) > 0:
            raise RuntimeError("Only `kwargs` are allowed in initialization, no `args`!")

        # Load the schema for this type of structure
        #    This will eventually be generalized to use an arbitrary schema
        schema = utils.load_schema('source')
        # Create a `Keychain` instance to store the properties described in this schema
        keychain = Keychain(schema, mutable=False, extendable=False)

        self._schema = schema
        self.keychain = keychain
        self._extendable = extendable

        # Store parameters passed during initialization
        for key, val in kwargs.items():
            self[key] = val

        # Compare stored parameters to the schema to perform validation
        if validate:
            self.validate()

        return

    def __setitem__(self, name, value):
        """Control what dictionary elements can be added.

        If `self._extendable` is False, only known parameters (from `self.keychain`) are
        allowed to be stored.

        """
        if (not self._extendable) and (name not in self.keychain):
            err = "'{}' not in `keychain`, and not extendable!".format(name)
            raise RuntimeError(err)

        super(Source, self).__setitem__(name, value)
        return

    def validate(self):
        """Check for consistency between the stored parameters and schema.
        """
        jsonschema.validate(self, self._schema)
        return

    def is_duplicate_of(self, other, ignore_case=True):
        # If these are not the same type, return False
        if type(other) is not type(self):
            return False

        s_keys = self.keychain.keys()
        o_keys = other.keychain.keys()
        if ignore_case:
            s_keys = [sk.lower() for sk in s_keys]
            o_keys = [ok.lower() for ok in o_keys]

        # NOTE: fix-speed
        keys = set(s_keys + o_keys)
        for ky in keys:
            kis = (ky in self)
            kio = (ky in other)
            # If only one object has this parameter, not the same
            if kis != kio:
                return False

            # If neither has parameter
            if not kis:
                continue

            s_val = self[ky]
            o_val = other[ky]
            if type(s_val) != type(o_val):
                return False

            if ignore_case and isinstance(s_val, str):
                s_val = s_val.lower()
                o_val = o_val.lower()

            if s_val != o_val:
                return False

        return True

    def to_json(self):
        jstr = utils.json_dump_str(self)
        return jstr
