"""Utility functions for `pyastroschema`.
"""

import os
import json
from collections import OrderedDict

from . import PATHS, META_KEYS


def load_schema_index():
    index = json_load_file(PATHS.INDEX_JSON_FILE)
    return index


def load_schema(sname):
    """

    Returns
    -------
    schema : odict

    """
    if os.path.exists(sname):
        schema = json_load_file(sname)
        return schema

    index = load_schema_index()
    index = index[META_KEYS.INDEX]
    if sname not in index.keys():
        err = "Schema '{}' does not exist as a file, and is not found in the index!".format(sname)
        raise ValueError(err)

    # Load the meta-data for this particular schema
    schema_meta = index[sname]
    # Get the filename for the schema file
    schema_fname = schema_meta[META_KEYS.FNAME]
    schema_fname = os.path.join(PATHS.ASTROSCHEMA, schema_fname)

    schema = json_load_file(schema_fname)
    title = schema['title']
    if title != sname:
        err = "Loaded schema title mismatch!  Target: '{}', Loaded: '{}'".format(sname, title)
        raise ValueError(err)

    return schema


def json_dump_str(odict, **kwargs):
    """Dump the contents of a dictionary to a string using json formatting.
    """
    kw = _json_dump_kwargs(indent=2)
    jsonstring = json.dumps(odict, **kw)
    return jsonstring


def json_dump_file(odict, fname, **kwargs):
    """Dump the contents of a dictionary to a JSON file with the given filename.
    """
    kw = _json_dump_kwargs(**kwargs)
    with open(fname, 'w') as out:
        json.dump(odict, out, **kw)
    return


def json_load_file(fname):
    """Load the contents of a JSON file into an `OrderedDict`.
    """
    try:
        with open(fname, 'r') as inp:
            data = json.load(inp, object_pairs_hook=OrderedDict)
    except:
        print("ERROR: Failed to load file '{}'".format(fname))
        raise

    return data


def json_load_str(jstr):
    """Load the contents of a JSON formatted string into an `OrderedDict`.
    """
    data = json.loads(jstr, object_pairs_hook=OrderedDict)
    return data


def _json_dump_kwargs(**kwargs):
    """Load kwargs to be passed to `json.dump` and `json.dumps`.
    """
    kw = dict(indent=2, separators=(',', ':'), ensure_ascii=False)
    for kk, vv in kwargs.items():
        kw[kk] = vv

    return kw


def get_file_size_str(fil):
    """Given a filename, return the filesize as a string.
    """
    fsize = os.path.getsize(fil)
    # decimal-places precision
    PREC = 1

    abbrevs = (
        (1 << 50, 'PB'),
        (1 << 40, 'TB'),
        (1 << 30, 'GB'),
        (1 << 20, 'MB'),
        (1 << 10, 'KB'),
        (1, 'bytes')
    )

    # Determine the correct abbreviation
    for factor, suffix in abbrevs:
        if fsize >= factor:
            break

    # Construct file size string
    size_str = '{size:.{prec:}f} {suff}'.format(prec=PREC, size=fsize/factor, suff=suffix)
    return size_str


def get_astroschema_version():
    """Load the version of the entire `astroschema` package, from the version file.
    """
    # fname = os.path.join(PATH_ASTROSCHEMA, FNAME_VERSION)
    with open(PATHS.ASTROSCHEMA_VERSION_FILE, 'r') as inp:
        vers = inp.read().strip()
    return vers


def get_relative_path(path, relative_to):
    # Get filename relative to `PATH_ASTROSCHEMA`
    common_path = os.path.join(os.path.commonpath([path, relative_to]), '')
    relpath = path.split(common_path)[-1]
    return relpath


def get_schema_odict(schema):
    """Make sure the given schema is an `odict`.

    If it is a filename (str) load the schema odict.

    """

    # Load the schema for this type of structure
    if isinstance(schema, dict):
        pass
    elif isinstance(schema, str):
        schema = load_schema(schema)
    else:
        err = "Unrecognized `schema` type '{}': '{}'".format(type(schema), schema)
        raise ValueError(err)

    return schema


def get_list_of_schema(schema):
    """Make sure the given schema is a list of `odict`.
    """

    if isinstance(schema, dict):
        schema_list = [schema]
    elif isinstance(schema, str):
        schema_list = [schema]
    elif isinstance(schema, list):
        schema_list = schema
    else:
        err = "`schema` type '{}' not allowed!".format(type(schema))
        raise ValueError(err)

    schema_list = [get_schema_odict(sch) for sch in schema_list]
    return schema_list
