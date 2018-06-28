"""Eventually this will be generalized from 'source' specifically to any 'struct'.
"""

from collections import OrderedDict

import jsonschema

from . import utils
from . import SCHEMA_KEYS


class Keychain(object):

    def __init__(self, schema, mutable=False, extendable=True):
        """Initialize this `Keys` object using properties from given schema as keys.
        """
        props = schema[SCHEMA_KEYS.PROPS]
        # `_keys` must be created before keys will be stored internally in `setattr`
        self._keys = []
        self._values = []

        # Store all of the property names to this object
        for prop_name in props.keys():
            setattr(self, prop_name.upper(), prop_name)

        # This must be set after changed are made, so a 'False' value will not lead to error
        self._mutable = mutable
        self._extendable = extendable
        return

    def __setattr__(self, name, value):
        """Control mutability and extendability, and store keys when they match requirements.
        """
        if hasattr(self, "_mutable"):
            # If this instance is *not* mutable, but this `name` is already set... raise error
            if not getattr(self, "_mutable") and hasattr(self, name):
                raise RuntimeError("This instance is not mutable, cannot modify existing key!")

        if hasattr(self, "_extendable"):
            # If this instance is *not* extendable, and this `name` is new... raise error
            if not getattr(self, "_extendable") and hasattr(self, name):
                raise RuntimeError("This instance is not extendable, cannot add a new key!")

        if hasattr(self, "_keys") and self._test_key_val(name, value):
            self._keys.append(name)
            self._values.append(value)

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
        if key.startswith('_'):
            return False
        if callable(val):
            return False
        return True


class Source(OrderedDict):

    def __init__(self, *args, extendable=False, validate=True, **kwargs):
        if len(args) > 0:
            raise RuntimeError("Only `kwargs` are allowed in initialization, no `args`!")

        schema = utils.load_schema('source')
        keychain = Keychain(schema, mutable=False, extendable=extendable)
        self._schema = schema
        self.keychain = keychain
        self._extendable = extendable

        for key, val in kwargs.items():
            self[key] = val

        if validate:
            self.validate()

        return

    def __setitem__(self, name, value):
        if (not self._extendable) and (name not in self.keychain):
            err = "'{}' not in `keychain`, and not extendable!".format(name)
            raise RuntimeError(err)

        super(Source, self).__setitem__(name, value)
        return

    def validate(self):
        jsonschema.validate(self, self._schema)
        return

    def to_json(self):
        jstr = utils.json_dump_str(self)
        return jstr
