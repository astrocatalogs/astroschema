"""Python module for interaction with astroschema.
"""

__version__ = "0.0.0"

import os

DIR_SCHEMA = "schema"
FNAME_VERSION = "VERSION"

INDEX_JSON_FILENAME = "astroschema_index.json"
INDEX_DESCRIPTION = "Index and summary of schema included in `astroschema`."

PATH_PYASTROSCHEMA = os.path.realpath(os.path.dirname(__file__))
PATH_ASTROSCHEMA = os.path.realpath(os.path.join(PATH_PYASTROSCHEMA, os.path.pardir))

PATH_SCHEMA_DIR = os.path.join(PATH_ASTROSCHEMA, DIR_SCHEMA, "")
PATH_ASTROSCHEMA_VERSION_FILE = os.path.join(PATH_ASTROSCHEMA, FNAME_VERSION)
PATH_INDEX_JSON_FILE = os.path.join(PATH_ASTROSCHEMA, INDEX_JSON_FILENAME)

print("Path: pyastroschema: '{}'".format(PATH_PYASTROSCHEMA))
print("Path:   astroschema: '{}'".format(PATH_ASTROSCHEMA))
print("Path:        schema: '{}'".format(PATH_SCHEMA_DIR))
