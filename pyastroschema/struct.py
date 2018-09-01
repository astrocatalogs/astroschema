"""Eventually this will be generalized from 'source' specifically to any 'struct'.
"""
from collections import OrderedDict
from copy import deepcopy

import json
import numpy as np

from . import keys, schema, utils

VERBOSE = False

EXTENDABLE = True

DUPLICATE_USES_HASH = True


def set_struct_schema(schema_source, extensions=[], updates=[],
                      extendable=None, check_conflict=True, schema_class=schema.SchemaDict):
    if extendable is None:
        extendable = EXTENDABLE

    def wrapper(cls):
        schema_dict = schema_class(schema_source)
        for ext in extensions:
            schema_dict.extend(ext, check_conflict=check_conflict)
        for upd in updates:
            schema_dict.update(upd)
        cls._SCHEMA = schema_dict
        cls._KEYCHAIN = keys.Keychain(schema_dict, mutable=False, extendable=extendable)
        cls._extendable = extendable
        return cls

    return wrapper


class Struct(schema.JSONOrderedDict):

    # _SCHEMA = None
    # _KEYCHAIN = None
    # _extendable = True

    def __init__(self, parent=None, validate=True, **kwargs):
        """Initialize with parameters based on the associated schema.

        Arguments
        ---------

        """
        # NOTE: this is needed for python2 but not python3, not sure why
        super(Struct, self).__init__()

        _schema = getattr(self, "_SCHEMA", None)
        if (_schema is None) or (not isinstance(_schema, schema.SchemaDict)):
            raise ValueError("`_SCHEMA` is a required attribute and must be a `SchemaDict`!")

        _keychain = getattr(self, "_KEYCHAIN", None)
        if (_keychain is None) or (not isinstance(_keychain, keys.Keychain)):
            raise ValueError("`_KEYCHAIN` is a required attribute and must be a `Keychain`!")

        self._parent = parent
        self._hash = None
        self._hash_changed = True

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
        # name = Struct._parse_keyname(name)
        if (not self.extendable) and (name not in self.keychain):
            err = "'{}' not in `keychain`, and not extendable!".format(name)
            raise RuntimeError(err)

        super(Struct, self).__setitem__(name, value)
        # This instance will need to have its hash reconstructed
        self._hash_changed = True
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

    @classmethod
    def construct(cls, schema_source, **kwargs):
        struct_class = set_struct_schema(schema_source, **kwargs)(Struct)
        return struct_class

    @property
    def keychain(self):
        return self._KEYCHAIN

    @property
    def schema(self):
        return self._SCHEMA

    @property
    def hash(self):  # , unique=True, distinguishing=True):
        '''
        hash_name = "_hash"
        if unique:
            hash_name += "_uniq"
        if distinguishing:
            hash_name += "_dist"
        '''
        # print(__file__ + ":hash()")
        # If hash has yet to be constructed, construct one
        if (self._hash is None) or self._hash_changed:
            # print("\tHashing")
            # Store only the values contributing to the hash (i.e. comparable values)
            hash_dict = OrderedDict()
            # Go through keys and store the targeted ones in a sorted order
            for key in sorted(self.keychain.keys()):
                # print("\t\t", key)
                if (key.unique or key.distinguishing) and (key in self):
                    # print("\t\t\tusing: ", self[key])
                    hash_dict[key] = self[key]

            # Construct and store the hash
            try:
                # hash_str = json.dumps(hash_dict, cls=NumpyEncoder)
                hash_str = utils.json_dump_str(hash_dict, pretty=False)
            except:
                print("FAILED TO DUMPS")
                print("hash_dict = ", hash_dict)
                raise

            try:
                self._hash = hash(hash_str)
            except:
                print("FAILED TO HASH")
                print("str = ", hash_str)
                print("nice hash_dict: \n\n", utils.json_dump_str(hash_dict))
                raise

            self._hash_changed = False

        # print("\t", self._hash)
        return self._hash

    @property
    def extendable(self):
        return self._extendable

    def validate(self):
        """Check for consistency between the stored parameters and schema.
        """
        # jsonschema.validate(self, self._schema)
        # self._validator.validate(self)

        # Use the validator in the stored `SchemaDict` instance to validate `self`
        self.schema.validate(self)
        return

    def is_duplicate_of(self, other, hashed=None, ignore_case=True, verbose=None):
        """Compares this instance to another to determine if they are 'duplicates'.

        NOTE: A 'duplicate' means that *certain* types of properties match, not (necessarily) that
              all values are identical.

        The `Key` values are compared between instances to determine 'duplicate' status.
        The `unique` and `distinguishing` properties of each `Key` are used to determine how the
        instances compare to eachother.  If any `unique` element matches, the instances are
        duplicates.  If any `distinguishing` elements are mismatched, the instances are not
        duplicates.  Currently not checking is done to make sure these tests are consistent.

        """
        if verbose is None:
            verbose = VERBOSE

        if hashed is None:
            hashed = DUPLICATE_USES_HASH

        if hashed:
            return (self.hash == other.hash)

        # If these are not the same type, return False
        if type(other) is not type(self):
            if verbose:
                print("type mismatch")
            return False

        DEFAULT_BEHAVIOR = True

        s_keys = self.keychain.keys()
        o_keys = other.keychain.keys()
        keys = set(s_keys + o_keys)
        # NOTE: speed-up comparison by getting 'uniqe'-specific list
        #    perhaps also specific list for `Key`s that are set
        for ky in keys:
            if verbose:
                print("key: '{}'".format(ky))
            # note: this may produce error if a key-chain mismatch occurs... not sure if possible
            s_key = getattr(self.keychain, ky.upper())
            o_key = getattr(other.keychain, ky.upper())
            # Make sure the two versions of this key are identical
            if not s_key.equals(o_key, identical=True):
                if verbose:
                    print("key mismatch!")
                err = "key mismatch occurred! '{}' --- '{}'".format(repr(self), repr(other))
                raise RuntimeError(err)

            # If neither Key is unique or distinguishing, then comparison doesnt matter
            s_uniq = s_key.unique
            o_uniq = o_key.unique
            s_dist = s_key.distinguishing
            o_dist = o_key.distinguishing
            # note: only 2 checks are needed here, as above both versions of key are compared
            if (not s_dist and not o_dist and not s_uniq and not o_uniq):
                if verbose:
                    print("not unique or distinguishing")
                continue

            # key must be unique of distinguishing to matter
            kis = (str(ky) in self) and (s_uniq or s_dist)
            kio = (str(ky) in other) and (o_uniq or o_dist)
            # If only one object has this parameter, not the same
            if kis != kio:
                if verbose:
                    print("instances do not have the same keys")
                return False

            # If neither has parameter
            if not kis:
                if verbose:
                    print("kis: {}, {}".format((ky in self), kis))
                    print("kio: {}, {}".format((ky in other), kio))
                    print("key absent")
                continue

            # Already established that both instances have this key; get the values
            s_val = self[ky]
            o_val = other[ky]
            # established that keys are either unique or distinguishing; thus diff means not dup
            if s_val != o_val:
                if verbose:
                    print("value mismatch")
                return False
            # If the same, and unique, then yes duplicates
            elif (s_uniq or o_uniq):
                if verbose:
                    print("unique value match")
                return True
            # If not unique and values match, indeterminate... continue
            else:
                if verbose:
                    print("non-'unique' matching")
                pass

        if verbose:
            print("No determinant (mis)matches, returning default: '{}'".format(DEFAULT_BEHAVIOR))

        return DEFAULT_BEHAVIOR

    def merge_from(self, other, **kwargs):
        return


@set_struct_schema("source")
class Source(Struct):
    pass


@set_struct_schema("quantity")
class Quantity(Struct):
    pass


@set_struct_schema("photometry")
class Photometry(Struct):
    pass


@set_struct_schema("spectrum")
class Spectrum(Struct):
    pass


@set_struct_schema("entry")
class Entry(Struct):
    pass
