"""Eventually this will be generalized from 'source' specifically to any 'struct'.
"""
from copy import deepcopy
from collections import OrderedDict

import jsonschema

from . import utils
from . import keys

VERBOSE = False


class Struct(OrderedDict):

    def __init__(self, schema, *args,
                 parent=None, extendable=False, validate=True,
                 **kwargs):
        """Initialize with parameters based on the associated schema.

        Arguments
        ---------
        schema : str or dict,
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
            err = "Only `kwargs` are allowed in initialization, no additional `args`!"
            raise RuntimeError(err)

        # Load the schema for this type of structure
        #    This will eventually be generalized to use an arbitrary schema
        if isinstance(schema, dict):
            pass
        elif isinstance(schema, str):
            schema = utils.load_schema(schema)
        else:
            err = "Unrecognized `schema` type '{}': '{}'".format(type(schema), schema)
            raise ValueError(err)

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
        # name = Struct._parse_keyname(name)
        if (not self._extendable) and (name not in self._keychain):
            err = "'{}' not in `keychain`, and not extendable!".format(name)
            raise RuntimeError(err)

        super(Struct, self).__setitem__(name, value)
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

    '''
    def __contains__(self, key):
        """Compare the given `str` with the `str` representation of each internal `Key`.
        """
        cont = (key in [str(kk) for kk in self._keys])
        return cont
    '''

    def _get_keychain_inst(self):
        return self._keychain

    def validate(self):
        """Check for consistency between the stored parameters and schema.
        """
        jsonschema.validate(self, self._schema)
        return

    def is_duplicate_of(self, other, ignore_case=True, verbose=None):
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

        # If these are not the same type, return False
        if type(other) is not type(self):
            if verbose:
                print("type mismatch")
            return False

        DEFAULT_BEHAVIOR = True

        s_keys = self._keychain.keys()
        o_keys = other._keychain.keys()
        keys = set(s_keys + o_keys)
        # NOTE: speed-up comparison by getting 'uniqe'-specific list
        #    perhaps also specific list for `Key`s that are set
        for ky in keys:
            if verbose:
                print("key: '{}'".format(ky))
            # note: this may produce error if a key-chain mismatch occurs... not sure if possible
            s_key = getattr(self._keychain, ky.upper())
            o_key = getattr(other._keychain, ky.upper())
            # Make sure the two versions of this key are identical
            # if s_key != o_key:
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

    def to_json(self):
        jstr = utils.json_dump_str(self)
        return jstr

    @classmethod
    def get_keychain(cls):
        schema = utils.load_schema(cls._SCHEMA_NAME)
        # Create a `Keychain` instance to store the properties described in this schema
        keychain = keys.Keychain(schema, mutable=False, extendable=False)
        return keychain


class Meta_Struct(Struct):

    _SCHEMA_NAME = None

    def __new__(cls, *args, **kwargs):
        struct = super(Meta_Struct, cls).__new__(cls)
        return struct

    def __init__(self, *args, **kwargs):
        super(Meta_Struct, self).__init__(self._SCHEMA_NAME, *args, **kwargs)
        return


class Source(Meta_Struct):

    _SCHEMA_NAME = "source"


class Quantity(Meta_Struct):

    _SCHEMA_NAME = "quantity"
