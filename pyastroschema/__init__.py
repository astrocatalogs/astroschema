"""Python module for interaction with astroschema.
"""

__version__ = "0.0.0"

import os

# Basic hard-coded Parameters
# -------------------------------------

VERBOSE = True

_DIR_SCHEMA = "schema"
_FNAME_VERSION = "VERSION"
_INDEX_JSON_FILENAME = "astroschema_index.json"

INDEX_DESCRIPTION = "Index and summary of schema included in `astroschema`."

# Construct derived parameters
# --------------------------------------


class PATHS:
    PYASTROSCHEMA = os.path.realpath(os.path.dirname(__file__))
    ASTROSCHEMA = os.path.realpath(os.path.join(PYASTROSCHEMA, os.path.pardir))

    SCHEMA_DIR = os.path.join(ASTROSCHEMA, _DIR_SCHEMA, "")
    ASTROSCHEMA_VERSION_FILE = os.path.join(ASTROSCHEMA, _FNAME_VERSION)
    INDEX_JSON_FILE = os.path.join(ASTROSCHEMA, _INDEX_JSON_FILENAME)


print("Path: pyastroschema: '{}'".format(PATHS.PYASTROSCHEMA))
print("Path:   astroschema: '{}'".format(PATHS.ASTROSCHEMA))
print("Path:        schema: '{}'".format(PATHS.SCHEMA_DIR))


class META_KEYS:
    FNAME = "filename"
    TITLE = "title"
    DESC = "description"
    VERS = "version"
    UPDATED = "updated"
    INDEX = "index"
    SCHEMA = "schema"
