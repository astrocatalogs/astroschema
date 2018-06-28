"""Python module for interaction with astroschema.
"""

__version__ = "0.0.0"

import os

DIR_SCHEMA = "schema"
FNAME_VERSION = "VERSION"

PATH_PYASTROSCHEMA = os.path.realpath(os.path.dirname(__file__))
PATH_ASTROSCHEMA = os.path.realpath(os.path.join(PATH_PYASTROSCHEMA, os.path.pardir))

PATH_SCHEMA = os.path.join(PATH_ASTROSCHEMA, DIR_SCHEMA, "")
PATH_ASTROSCHEMA_VERSION = os.path.join(PATH_ASTROSCHEMA, FNAME_VERSION)

print("Path: pyastroschema: '{}'".format(PATH_PYASTROSCHEMA))
print("Path:   astroschema: '{}'".format(PATH_ASTROSCHEMA))
