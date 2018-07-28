"""
"""
from collections import OrderedDict

import jsonschema

from pyastroschema import utils


class JSONOrderedDict(OrderedDict):

    def __init__(self, schema):
        # Load the schema for this type of structure
        if isinstance(schema, dict):
            pass
        elif isinstance(schema, str):
            schema = utils.load_schema(schema)
        else:
            err = "Unrecognized `schema` type '{}': '{}'".format(type(schema), schema)
            raise ValueError(err)

        super(Schema, self).__init__(schema)

        # Validate the schema itself
        validator = jsonschema.validators.validator_for(schema)
        validator.check_schema(schema)
        return

    def __str__(self):
        return utils.json_dump_str(self)

    def dump(self, fname):
        return utils.json_dump_file(self, fname)

    @property
    def properties(self):
        return self.get('properties', None)

    @property
    def required(self):
        return self.get('required', None)


def main():
    FNAME = ("/Users/lzkelley/Research/catalogs/astrocats/astrocats/schema/"
             "quantity.json")

    schema = Schema(FNAME)

    print(schema)
    print(
    return
