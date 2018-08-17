"""Python module for interaction with astroschema.
"""
import os

# _par_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
# _PATH_VERSION = os.path.join(_par_dir, "VERSION")
_this_dir = os.path.abspath(os.path.dirname(__file__))
_PATH_VERSION = os.path.join(_this_dir, "VERSION")
with open(_PATH_VERSION, "r") as inn:
    version = inn.read().strip()

__version__ = version
print("\n" + __file__ + " : version : " + version + "\n")

import shutil
from jsonschema import ValidationError  # noqa


# Basic hard-coded Parameters
# -------------------------------------

VERBOSE = True

_FNAME_VERSION = "VERSION"
_INDEX_JSON_FILENAME = "astroschema_index.json"
_DIR_SCHEMA = "schema"
_DIR_TESTS = "tests"
_DIR_TESTS_SCHEMA = "test_schema"
_DIR_META_SCHEMA = "meta-schema"
_META_SCHEMA_FILENAME = "meta-schema.json"

INDEX_DESCRIPTION = "Index and summary of schema included in `astroschema`."

# Construct derived parameters
# --------------------------------------


class PATHS:
    PYASTROSCHEMA = os.path.realpath(os.path.dirname(__file__))
    # ASTROSCHEMA = os.path.realpath(os.path.join(PYASTROSCHEMA, os.path.pardir))

    SCHEMA_DIR = os.path.join(PYASTROSCHEMA, _DIR_SCHEMA, "")
    META_SCHEMA_DIR = os.path.join(SCHEMA_DIR, _DIR_META_SCHEMA, "")
    TESTS_DIR = os.path.join(PYASTROSCHEMA, _DIR_TESTS, "")
    TESTS_SCHEMA_DIR = os.path.join(TESTS_DIR, _DIR_TESTS_SCHEMA, "")
    ASTROSCHEMA_VERSION_FILE = os.path.join(PYASTROSCHEMA, _FNAME_VERSION)
    INDEX_JSON_FILE = os.path.join(PYASTROSCHEMA, _INDEX_JSON_FILENAME)

    META_SCHEMA_FILE = os.path.join(SCHEMA_DIR, _META_SCHEMA_FILENAME)

    @classmethod
    def test_dir(cls, name, good=False, bad=False):
        td = os.path.join(cls.TESTS_SCHEMA_DIR, name, "")
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


def copy_schema_files(target_dir, sname=None, verbose=None):
    """

    Arguments
    ---------
    target_dir : str
        Destination for copied files.  This must be a directory, and it must exist.
    sname : str

    Returns
    -------
    fnames : list of str, or str

    """
    if verbose is None:
        verbose = VERBOSE

    index = utils.load_schema_index()
    index = index[META_KEYS.INDEX]
    schema_names = list(sorted(index.keys()))
    # If a particular schema is targeted then select it, make sure it matches
    if sname is not None:
        if sname not in schema_names:
            raise ValueError("Schema '{}' is not in the index!".format(sname))

        schema_names = [sname]

    # Make sure the target destination looks good
    if not os.path.exists(target_dir):
        raise ValueError("Target directory '{}' does not exist!".format(target_dir))
    elif not os.path.isdir(target_dir):
        raise ValueError("Target directory '{}' is not a directory!".format(target_dir))

    # Iterate over all (targeted) schema files
    fnames = []
    for sch in schema_names:
        # print(sch)
        src = index[sch][META_KEYS.FNAME]
        src = os.path.join(PATHS.PYASTROSCHEMA, src)
        # Make sure source file exists
        if not os.path.exists(src):
            raise RuntimeError("Path for schema '{}' does not exist!  ('{}')".format(sch, src))
        # Construct destination path/filename
        fname_base = os.path.basename(src)
        dst = os.path.join(target_dir, fname_base)

        # Copy file
        shutil.copy(src, dst)
        if not os.path.exists(dst):
            raise RuntimeError("Copy failed '{}'==>'{}'".format(src, dst))
        if verbose:
            print("Copied '{}' to '{}'".format(sch, dst))
        fnames.append(dst)

    # If a single target file was given, return str instead of list
    if sname is not None:
        fnames = fnames[0]

    return fnames


# NOTE: this doesn't work in python2
'''
class MetaEnum(type):
    def __contains__(cls, val):
        return (val in cls.__options)
'''


class META_KEYS(object):  # , metaclass=MetaEnum):
    FNAME = "filename"
    TITLE = "title"
    DESC = "description"
    VERS = "version"
    UPDATED = "updated"
    INDEX = "index"
    SCHEMA = "schema"

    _options = [FNAME, TITLE, DESC, VERS, UPDATED, INDEX, SCHEMA]


class SCHEMA_KEYS(object):  # , metaclass=MetaEnum):
    TITLE = "title"
    DESC = "description"
    PROPS = "properties"
    TYPE = "type"
    REQD = "required"

    _options = [TITLE, DESC, PROPS, TYPE, REQD]


class KEY_FORMATS(object):  # , metaclass=MetaEnum):
    NUMERIC = "numeric"
    ASTROTIME = "astrotime"
    STRING = "string"

    _options = [NUMERIC, ASTROTIME, STRING]



from . import utils  # noqa
from . import struct  # noqa
from . import schema  # noqa
from . import validation  # noqa

from . schema import SchemaDict  # noqa
