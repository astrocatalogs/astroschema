"""Python module for interaction with astroschema.
"""

__version__ = "0.4.0"

import os
from jsonschema import ValidationError  # noqa


# Basic hard-coded Parameters
# -------------------------------------

VERBOSE = True

_FNAME_VERSION = "VERSION"
_INDEX_JSON_FILENAME = "astroschema_index.json"
_DIR_SCHEMA = "schema"
_DIR_TESTS = "tests"
_DIR_META_SCHEMA = "meta-schema"
_META_SCHEMA_FILENAME = "meta-schema.json"

INDEX_DESCRIPTION = "Index and summary of schema included in `astroschema`."

# Construct derived parameters
# --------------------------------------


class PATHS:
    PYASTROSCHEMA = os.path.realpath(os.path.dirname(__file__))
    ASTROSCHEMA = os.path.realpath(os.path.join(PYASTROSCHEMA, os.path.pardir))

    SCHEMA_DIR = os.path.join(ASTROSCHEMA, _DIR_SCHEMA, "")
    META_SCHEMA_DIR = os.path.join(SCHEMA_DIR, _DIR_META_SCHEMA, "")
    TESTS_DIR = os.path.join(ASTROSCHEMA, _DIR_TESTS, "")
    ASTROSCHEMA_VERSION_FILE = os.path.join(ASTROSCHEMA, _FNAME_VERSION)
    INDEX_JSON_FILE = os.path.join(ASTROSCHEMA, _INDEX_JSON_FILENAME)

    META_SCHEMA_FILE = os.path.join(SCHEMA_DIR, _META_SCHEMA_FILENAME)

    @classmethod
    def test_dir(cls, name, good=False, bad=False):
        td = os.path.join(cls.TESTS_DIR, name, "")
        if not os.path.exists(td):
            err = "Test directory for '{}' does not exist!  '{}'".format(name, td)
            raise ValueError(err)

        if good and bad:
            raise ValueError("Can only select either `good` or `bad`!")
        elif good:
            td = os.path.join(td, "good", "")
        elif bad:
            td = os.path.join(td, "bad", "")

        return td


class META_KEYS:
    FNAME = "filename"
    TITLE = "title"
    DESC = "description"
    VERS = "version"
    UPDATED = "updated"
    INDEX = "index"
    SCHEMA = "schema"


class SCHEMA_KEYS:
    TITLE = "title"
    DESC = "description"
    PROPS = "properties"
    TYPE = "type"
    REQD = "required"

from . import utils  # noqa
from . import struct  # noqa
from . import schema  # noqa
from . import validation  # noqa
