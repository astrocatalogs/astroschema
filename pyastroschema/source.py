"""
"""

from collections import OrderedDict

from . import SCHEMA_KEYS


class Keys:

    def __init__(self, schema):
        props = schema[SCHEMA_KEYS.PROPS]
        for prop_name in props.keys():
            setattr(self, prop_name.upper(), prop_name)



    def keys(self):
        def _test_key(key):
            if key.startswith('_'):
                return False
            if callable(getattr(self, key)):
                return False
            return True

        keys = [kk for kk in dir(self) if _test_key(kk)]
        return keys


class Source(OrderedDict):
    """
    """

    _KEYS = KeyCollection

    _ALLOW_UNKNOWN_KEYS = True

    _REQ_KEY_SETS = []

    def __init__(self, parent, key=None, **kwargs):
        """Initialize `CatDict`."""
        super(CatDict, self).__init__()
        # Store the parent object (an `Entry` subclass) to which this instance
        # will belong.  e.g. a `Supernova` entry.
        self._parent = parent
        self._key = key
        self._log = parent.catalog.log

        # Store any individual keys which are required
        self._req_keys = []
        for rks in self._REQ_KEY_SETS:
            # If this set is only 1 long, that key is individually required
            if len(rks) == 1:
                self._req_keys.append(rks[0])

        # Iterate over all `_KEYS` parameters, load each if given note that the
        # stored 'values' are the `Key` objects, referred to here with the name
        # 'key'.
        vals = self._KEYS.vals()
        for key in kwargs.copy():
            # If we allow unknown keys, or key is in list of known keys,
            # process and store it.
            kiv = key in vals
            if self._ALLOW_UNKNOWN_KEYS or kiv:
                # Load associated Key object if it exists, otherwise construct
                # a default Key object.
                if kiv:
                    key_obj = vals[vals.index(key)]
                else:
                    self._log.info('[{}] `{}` not in list of keys for `{}`, '
                                   'adding anyway as allow unknown keys is '
                                   '`{}`.'.format(parent[
                                       parent._KEYS.NAME], key,
                                       type(self).__name__,
                                       self._ALLOW_UNKNOWN_KEYS))
                    key_obj = Key(key)

                # Handle Special Cases
                # --------------------
                # Only keep booleans and strings if they evaluate true.
                if ((key_obj.type == KEY_TYPES.BOOL or
                     key_obj.type == KEY_TYPES.STRING) and not kwargs[key]):
                    del kwargs[key]
                    continue

                # Make sure value is compatible with the 'Key' specification.
                check_fail = False
                if not key_obj.check(kwargs[key]):
                    check_fail = True
                    self._log.info("Value for '{}' is invalid "
                                   "'{}':'{}'".format(key_obj.pretty(), key,
                                                      kwargs[key]))
                    # Have the parent log a warning if this is a required key
                    if key in self._req_keys:
                        raise CatDictError(
                            "Value for required key '{}' is invalid "
                            "'{}:{}'".format(key_obj.pretty(), key,
                                             kwargs[key]),
                            warn=True)

                # Check and store values
                # ----------------------
                # Remove key-value pair from `kwargs` dictionary.
                value = kwargs.pop(key)
                value = self._clean_value_for_key(key_obj, value)
                # only store values that are not empty
                if value and not check_fail:
                    self[key] = value

        # If we require all parameters to be a key in `PHOTOMETRY`, then all
        # elements should have been removed from `kwargs`.
        if not self._ALLOW_UNKNOWN_KEYS and len(kwargs):
            raise CatDictError(
                "All permitted keys stored, remaining: '{}'".format(kwargs))

        # Make sure that currently stored values are valid
        self._check()

        return

    def is_duplicate_of(self, other):
        # If these are not the same type, return False
        if type(other) is not type(self):
            return False

        # Go over all expected parameters and check equality of each
        for key in self._KEYS.compare_vals():
            kis = key in self
            kio = key in other
            # If only one object has this parameter, not the same
            if kis != kio:
                return False
            # If self doesnt have this parameter (and thus neither does), skip
            if not kis:
                continue

            # Now, both objects have the same parameter, compare them
            if self[key] != other[key]:
                return False

        return True

    def _clean_value_for_key(self, key, value):
        """

        FIX: should this be in `key`??  like 'check()'??
        """
        if key.type is None:
            return value

        # Store whether given value started as a list or not
        single = True
        # Make everything a list for conversions below
        if isinstance(value, list):
            # But if lists arent allowed, and this is, raise error
            if not key.listable:
                raise CatDictError("`value` '{}' for '{}' shouldnt be a list.".
                                   format(value, key.pretty()))

            single = False

        # Store booleans as booleans, make sure each element of list is bool
        if key.type == KEY_TYPES.BOOL:
            if not all(isinstance(val, bool) for val in listify(value)):
                raise CatDictError("`value` '{}' for '{}' should be boolean".
                                   format(value, key.pretty()))
        # Strings and numeric types should be stored as strings
        elif key.type in [KEY_TYPES.STRING, KEY_TYPES.NUMERIC, KEY_TYPES.TIME]:
            # Clean leading/trailing whitespace
            if single:
                value = value.strip() if isinstance(
                    value, (str, basestring)) else str(value)
            else:
                value = [
                    val.strip() if isinstance(
                        val, (str, basestring)) else str(val)
                    for val in value
                ]
                # Only keep values that are not empty
                value = list(filter(None, value))

        return value


class SOURCE(KeyCollection):
    """`KeyCollection` for the `Source` class.

    Attributes
    ----------
    NAME : STRING
    BIBCODE : STRING
    URL : STRING
    ACKNOWLEDGMENT : STRING
    REFERENCE : STRING
    ALIAS : NUMERIC
        Numerical alias (shorthand) for this entry.  Saved as a string (or
        list of strings), despite being stored as an integer.
    SECONDARY : BOOL
        Whether the given source is one which collected data from another,
        'Primary'-source, from which it actually originated

    """

    # Strings
    NAME = Key('name', KEY_TYPES.STRING)
    BIBCODE = Key('bibcode', KEY_TYPES.STRING)
    ARXIVID = Key('arxivid', KEY_TYPES.STRING)
    DOI = Key('doi', KEY_TYPES.STRING)
    URL = Key('url', KEY_TYPES.STRING, compare=False)
    ACKNOWLEDGMENT = Key('acknowledgment', KEY_TYPES.STRING, compare=False)
    REFERENCE = Key('reference', KEY_TYPES.STRING, compare=False)
    # Numbers
    ALIAS = Key('alias', KEY_TYPES.NUMERIC, compare=False)
    # Booleans
    SECONDARY = Key('secondary', KEY_TYPES.BOOL, compare=False)
    PRIVATE = Key('private', KEY_TYPES.BOOL, compare=False)


class Source(CatDict):
    """Representation for the source/attribution of a data element."""

    _KEYS = SOURCE

    def __init__(self, parent, **kwargs):
        """Initialize `Source`."""
        self._REQ_KEY_SETS = [
            [SOURCE.ALIAS],
            [SOURCE.BIBCODE, SOURCE.ARXIVID, SOURCE.DOI, SOURCE.URL,
             SOURCE.NAME]
        ]
        super(Source, self).__init__(parent, **kwargs)
        return

    def is_duplicate_of(self, other):
        """Check if this Source is a duplicate of another.

        Unlike the function in the super class, this method will return True
        if *either* name or bibcode is the same.
        """
        # If these are not the same type, return False
        if type(other) is not type(self):
            return False

        # Go over all expected parameters and check equality of each
        for key in self._KEYS.compare_vals():
            # If only one object has this parameter, not the same
            # This is commented out for sources because two sources are
            # considered the same if they share a name *or* a bibcode
            # if (key in self) != (key in other):
            #     continue
            # If self doesnt have this parameter (and thus neither does), skip
            if key not in self or key not in other:
                continue

            # Now, both objects have the same parameter, compare them
            if self[key] == other[key]:
                return True

        return False
