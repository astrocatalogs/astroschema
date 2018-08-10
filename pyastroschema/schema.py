"""
"""
import os
import copy
from collections import OrderedDict

from urllib.parse import urlparse

import jsonschema

from pyastroschema import utils, validation

import warnings
warnings.showwarning = utils.warn_with_traceback


class JSONOrderedDict(OrderedDict):

    def __str__(self):
        return utils.json_dump_str(self)

    def dump(self, fname, sort_func=None):
        package = self if sort_func is None else sort_func(self)
        return utils.json_dump_file(package, fname)

    def dumps(self, sort_func=None):
        package = self if sort_func is None else sort_func(self)
        return utils.json_dump_str(package)

    @classmethod
    def load(cls, fname):
        return cls(utils.json_load_file(fname))

    @classmethod
    def loads(cls, jstr):
        return cls(utils.json_load_str(jstr))

    def extend(self, data, **kwargs):
        """Add elements from `schema` not present in self (recursively).
        """
        # data = utils.get_schema_odict(schema)
        # print("schema = ", schema)
        # data = JSONOrderedDict(schema)
        _extend(self, data, **kwargs)
        return


class SchemaDict(JSONOrderedDict):

    def __init__(self, schema={}, path=None):
        """
        Path is used for RefResolver (using relative paths in schema).
        """
        schema, schema_path, schema_name = _get_schema_dict_and_path_str(schema)
        super(SchemaDict, self).__init__(schema)
        if path is None:
            path = schema_path

        if (schema_path is None) or (schema_name is None):
            fname = None
        else:
            fname = os.path.join(schema_path, schema_name + ".json")

        self.finalize()
        self._name = schema_name

        self._validator = None
        self._ref_resolver = None
        self._changed = True
        self._ref_path = path
        self._filename = fname
        path_formatted = 'file://{}/'.format(path) if (path is not None) else None
        self._ref_path_formatted = path_formatted

        # Validate the schema itself
        self.validate()
        return

    def __set__(self, key, val):
        self._changed = True
        return super(SchemaDict).__set__(key, val)

    @classmethod
    def to_SchemaDict(cls, data):
        # If object is already a `SchemaDict`, return it
        if isinstance(data, cls):
            return data

        # Otherwise, create a new `SchemaDict`
        return cls(data)

    @property
    def properties(self):
        return self.get('properties', None)

    def validate(self, data=None):
        # Validate this object (i.e. this schema)
        if data is None:
            validator = jsonschema.validators.validator_for(self)
            validator.check_schema(self)

        # Validate the given data using this object as a schema
        else:
            # Construct and cache a validator
            if (self._validator is None) or (self._changed):
                path = self._ref_path_formatted
                resolver = jsonschema.RefResolver(path, None) if (path is not None) else None
                self._validator = validation.PAS_Validator(self, resolver=resolver)
                self._changed = False

            try:
                self._validator.validate(data)
            except jsonschema.exceptions.RefResolutionError as err:
                myname = self.get('title', None)
                if myname is None:
                    myname = self._name
                if myname is None:
                    myname = str(self)
                msg = "Reference resolution failure with: {}".format(myname)
                raise jsonschema.exceptions.RefResolutionError(msg) from err

        return

    def finalize(self):
        pass

    def extend(self, schema, **kwargs):
        kwargs.setdefault("check_conflict", True)
        # data = utils.get_schema_odict(schema)
        # schema, schema_path = _get_schema_dict_and_path_str(schema)
        data = SchemaDict(schema)
        data_keys = list(data.keys())

        # NOTE: FIX: Temporary warnings for actions outside of currently tested usage
        #     Once this is resolved, remove this (overriding) method
        # ---------------------------------------------------------------------------------
        # Warn if there is no 'properties'
        if "properties" not in data_keys:
            warn = "`SchemaDict.extend()` designed to add 'properties', which is not found!"
            warnings.warn(warn)
        else:
            data_keys.remove("properties")

        if "definitions" in data_keys:
            data_keys.remove("definitions")

        # Warn if there are keys *besides* 'properties'
        if len(data_keys) > 0:
            warn = "`SchemaDict.extend()` designed to *only* add 'properties'; other keys found!"
            warnings.warn(warn)

        super(SchemaDict, self).extend(data, **kwargs)
        return

    def update(self, schema):
        data = SchemaDict(schema)
        super(SchemaDict, self).update(data)
        return


def _extend(aa, bb, copy_type='deep', check_conflict=False):
    """Add the key-values from `bb` into `aa`.
    """

    for key, val in bb.items():
        # If both dicts have the key, make sure deeper levels also match
        if (key in aa):
            # If there is a lower-level dictionary, pass that to `_extend` to continue copying
            if isinstance(aa[key], dict):
                _extend(aa[key], val, check_conflict=check_conflict)
            # If `check_conflicts` make sure leaf values match
            elif check_conflict and (aa[key] != val):
                raise ValueError("Key: '{}' conflict!  '{}' vs '{}'".format(key, aa[key], val))

        # If `aa` does not have the key-value, add them
        else:
            if copy_type == 'deep':
                aa[key] = copy.deepcopy(val)
            elif copy_type == 'shallow':
                aa[key] = copy.copy(val)
            elif copy_type == 'point':
                aa[key] = val
            else:
                raise ValueError("Unrecognized `copy_type` = '{}'!".format(copy_type))

    return aa


def _get_schema_dict_and_path_str(schema):
    if isinstance(schema, dict):
        schema_path = None
        schema_name = schema.get('title', None)
    elif isinstance(schema, str):
        # A string specification can be a path, or name of the schema-file and the standard
        # path will be assumed
        schema, schema_path, schema_name = utils.load_schema_dict(schema)
    else:
        err = "`schema` type '{}' not allowed!".format(type(schema))
        raise ValueError(err)

    return schema, schema_path, schema_name


def main():
    '''
    FNAME = ("/Users/lzkelley/Research/catalogs/astrocats/astrocats/schema/"
             "quantity.json")

    schema = Schema(FNAME)

    print(schema)
    print()
    '''

    _one = {
        'a': 'aaa',
        'b': {
            '1': 111
        },
        'c': 'ccc'
    }

    _two = {
        'b': {
            '1': 123,
            '2': 222,
            '3': {
                'iv': '444'
            }
        },
        'c': 'cde'
    }

    one = copy.deepcopy(_one)
    two = copy.deepcopy(_two)
    _extend(one, two)
    print(utils.json_dump_str(one))
    print("")
    one = copy.deepcopy(_one)
    two = copy.deepcopy(_two)
    _extend(two, one)
    print(utils.json_dump_str(two))

    return
