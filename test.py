"""
"""

# import copy
import glob
from collections import OrderedDict

import json
import pyastroschema as pas
import jsonschema


# fname = "entry_1.json"
fname = "entry_2.json"
schema = pas.utils.json_load_file("/Users/lzkelley/Research/catalogs/astroschema/schema/" + fname)

# print(schema)
validator = jsonschema.validators.validator_for(schema)
validator.check_schema(schema)


'''
entry = dict(
    meta=dict(
        name="test12",
        sources=[src_1, src_2]
    ),
    quantities=dict(
        redshift=redz
        # redshift=5.0
    )
)
'''

'''
entry = dict(
    name="test12",
    sources=[src_1, src_2],
    redshift=redz
    # redshift=5.0
)
'''

'''
src_1 = dict(alias=0, arxivid="1605.01054")
src_2 = dict(alias=1, arxivid="1606.12345")
# src_2 = dict(alias=1, hello="goodbye")
redz = dict(value=1.5, source="1")

print("Entry = ", entry)

jsonschema.validate(entry, schema)

print("Done")
'''


path = "/Users/lzkelley/Research/catalogs/astrocats/astrocats/testcat/output/testcat-output/"
files = sorted(glob.glob(path + "*.json"))
for ii, ff in enumerate(files):
    print("\n{:4d}: '{}'".format(ii, ff))
    # entry = pas.utils.json_load_file(ff)
    with open(ff, 'r') as inp:
        entry = json.load(inp, object_pairs_hook=OrderedDict)

    name = list(entry.keys())[0]
    entry = entry[name]
    # entry = json.dumps(entry)
    # print("\t'{}'".format(name))
    # print(entry)
    jsonschema.validate(entry, schema)

print("Done")


'''
SIMPLEST_SCHEMA = dict(
    properties=dict(
        alias=dict(
            names={"test_one": "test_two"},
            type="string",
            unique=True
        ),
        name=dict(
            type="string",
            unique=True
        )
    )
)

t1 = pas.keys.Key("t1", type='string', unique=False)
print("key = ", t1)
print("type = '{}', unique = '{}'".format(t1.type, t1.unique))

t2 = pas.keys.Key("t2")
print("key = ", t2)
print("type = '{}', unique = '{}'".format(t2.type, t2.unique))

print("direct = ", t1, t2)
print("str = ", str(t1), str(t2))
print("repr = ", repr(t1), repr(t2))

print("hash = ", hash(t1), hash(t2))
print("hash(str) = ", hash(str(t1)), hash(str(t2)))

# print("defauilt = '{}'".format(t1.default))
'''



'''
META_SCHEMA = pas.utils.json_load_file(pas.PATHS.META_SCHEMA_FILE)
jsonschema.validate(SIMPLEST_SCHEMA, META_SCHEMA)
'''

# temp = pas.keys.Key('test', type='string', unique=False)

# print("Validate = ", jsonschema.validate(temp, SCHEMA))


#
# for kk, vv in SIMPLEST_SCHEMA['properties'].items():
#     print(kk, vv)
#     temp = pas.keys.Key(kk, **vv)
#     print(temp)
#     break

# keys = pas.source.Source.get_keychain()

# schema = pas.utils.load_schema('source')
# keys = pas.keys.Keychain(schema, mutable=False, extendable=True)

'''
SIMPLEST_SOURCE = dict(
    alias=0,
    name="Paper et al 2017"
)

# source = pas.source.Source(**SIMPLEST_SOURCE)
source = pas.struct.Source(**SIMPLEST_SOURCE)
print(type(source), source)
quant = pas.struct.Quantity(value=1.1232, source="1")
print(type(quant), quant)
'''

# _s1 = {
#     "name":"1999AJ....117..707R",
#     "bibcode":"1999AJ....117..707R",
#     "reference":"Riess et al. (1999)",
#     "alias":"3"
# }
#
# _s2 = {
#     "name":"1999AJ....117..707R",
#     "bibcode":"1999AJ....117..707R",
#     "reference":"Riess et al. (1999)",
#     "alias":"4"
# }
#
# s1 = pas.source.Source(**_s1)
# print(s1)
# s2 = pas.source.Source(**_s2)
# print(s2)
# print(s1 == s2)
# print(s1.is_duplicate_of(s2))
# print(s2.is_duplicate_of(s1))

'''
t1 = {
    "$schema": "http://json-schema.org/schema#",
    "title": "source",
    "description": "An item representing a bibliographic attribution or reference.",
    "version": "0.3",
    "type": "object",
    "properties": {
        "alias": {
            "description": "The unique identifier for this source.",
            "type": ["integer", "string"],
            "unique": False,
            "minimum": 0
        },
    }
}


t2 = {
    "$schema": "http://json-schema.org/schema#",
    "title": "source",
    "description": "An item representing a bibliographic attribution or reference.",
    "version": "0.3",
    "type": "object",
    "properties": {
        "alias": {
            "description": "The unique identifier for this source.",
            "unique": False,
            "minimum": 0
        },
    }
}

import jsonschema

print("t1 good")
jsonschema.validate(t1, SCHEMA)

print("t2 bad")
jsonschema.validate(t2, SCHEMA)
'''
