"""Eventually this will be generalized from 'source' specifically to any 'struct'.
"""
from copy import deepcopy
from collections import OrderedDict

import jsonschema

from . import utils
from . import keys


class Source(OrderedDict):

    SCHEMA_NAME = 'source'

    def __init__(self, *args, parent=None, extendable=False, validate=True, **kwargs):
        """Initialize with parameters based on the associated schema.

        Arguments
        ---------
        *args : None,
            NOT ALLOWED.  Only keyword-arguments (`kwargs`) can be used.
        parent : obj,
            Parent entry/structure or `None`.
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
        schema = utils.load_schema(self.SCHEMA_NAME)
        # Create a `Keychain` instance to store the properties described in this schema
        keychain = keys.Keychain(schema, mutable=False, extendable=False)

        self._schema = schema
        self._keychain = keychain
        self._extendable = extendable
        # NOTE: Reconsider having parent... is it still needed?
        self._parent = parent
        self.get_keychain = self._get_keychain_inst

        # Store parameters passed during initialization
        # NOTE: this is fine for `source`, but perhaps this should be a deepcopy for other objects?
        for kk, vv in kwargs.items():
            self[kk] = vv

        # Compare stored parameters to the schema to perform validation
        if validate:
            self.validate()

        return

    def __setitem__(self, name, value):
        """Control what dictionary elements can be added.

        If `self._extendable` is False, only known parameters (from `self._keychain`) are
        allowed to be stored.

        """
        if (not self._extendable) and (name not in self._keychain):
            err = "'{}' not in `keychain`, and not extendable!".format(name)
            raise RuntimeError(err)

        super(Source, self).__setitem__(name, value)
        return

    def __copy__(self):
        """

        Based on answer here: https://stackoverflow.com/a/15774013/230468
        """
        cls = self.__class__
        result = cls.__new__(cls)
        # Copy attributes
        result.__dict__.update(self.__dict__)
        # Copy dictionary entries
        result.update(self)
        return result

    def __deepcopy__(self, memo):
        """

        Based on answer here: https://stackoverflow.com/a/15774013/230468
        """
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        # Copy attributes
        for kk, vv in self.__dict__.items():
            setattr(result, kk, deepcopy(vv, memo))
        # Copy dictionary entries
        for kk, vv in self.items():
            result[kk] = deepcopy(vv, memo)

        return result

    def _get_keychain_inst(self):
        return self._keychain

    def validate(self):
        """Check for consistency between the stored parameters and schema.
        """
        jsonschema.validate(self, self._schema)
        return

    def is_duplicate_of(self, other, ignore_case=True):
        # If these are not the same type, return False
        if type(other) is not type(self):
            return False

        s_keys = self._keychain.keys()
        o_keys = other._keychain.keys()
        keys = set(s_keys + o_keys)
        # NOTE: speed-up comparison by getting 'uniqe'-specific list
        #    perhaps also specific list for `Key`s that are set
        for ky in keys:
            s_dist = getattr(self._keychain, ky.upper()).unique
            o_dist = getattr(other._keychain, ky.upper()).unique
            # If neither Key is unique, then comparison doesnt matter
            if (not s_dist and not o_dist):
                continue

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

            # If any `unique` attribute is the same, then they are duplicates
            if s_val == o_val:
                return True
            # if any is different, they are not duplicates
            # else:
            #     return False

        return False

    def to_json(self):
        jstr = utils.json_dump_str(self)
        return jstr

    @classmethod
    def get_keychain(cls):
        schema = utils.load_schema(cls.SCHEMA_NAME)
        # Create a `Keychain` instance to store the properties described in this schema
        keychain = keys.Keychain(schema, mutable=False, extendable=False)
        return keychain
