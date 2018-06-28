"""
"""

import os

import jsonschema

import pyastroschema as pas
import pyastroschema.utils  # noqa
import pyastroschema.source  # noqa

head = "astroschema test"
print("\n{}\n{}\n".format(head, "="*len(head)))

# Load the schema for a 'source' structure
source_schema = pas.utils.load_schema('source')

print("Loaded schema for 'source'\n")
# Print the schema nicely
print(pas.utils.json_dump_str(source_schema))
print("")
print("---------------------------------------------------\n")

# Construct filenames of test JSON source files
tests = ['a', 'b', 'c', 'd']
test_dir = os.path.join(pas.PATHS.ASTROSCHEMA, 'tests/source/')
fnames = [os.path.join(test_dir, tt + ".json") for tt in tests]

# Go through each test JSON file
for fn in fnames:
    print("Testing file '{}'".format(os.path.basename(fn)))
    # Load the actual contents of the 'source' entry
    src = pas.utils.json_load_file(fn)['entry']
    # Load whether this is a 'valid' entry, i.e. whether it should succeed or fail
    val = pas.utils.json_load_file(fn)['valid']
    print("\n" + pas.utils.json_dump_str(src) + "\n")

    print("--------")
    print("Using `jsonschema` validation:")
    # Try using `jsonschema` to validate the entry against the schema directly
    try:
        jsonschema.validate(src, source_schema)
        success = True
    except Exception as err:
        print("\tError:" + err.message)
        success = False

    print("\tValid: {:5s}  Pass: {}\n".format(str(val), success))

    print("--------")
    print("Using `Source` instance validation:")
    # Construct a `Source` instance and use it's internal validation methods
    #    dont validate on initialization, do it explicitly below
    source = pas.source.Source(validate=False, **src)
    print("\n" + str(source) + "\n")

    try:
        source.validate()
        success = True
    except Exception as err:
        success = False
        print("\tError:" + err.message)

    print("\tValid: {:5s}  Pass: {}\n".format(str(val), success))

    print("---------------------------------------------------")
