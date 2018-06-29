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
    index = load_schema_index()
    index = index[META_KEYS.INDEX]
    if sname not in index.keys():
        err = "Schema name '{}' not found in index!".format(sname)
        raise ValueError(err)

    # Load the meta-data for this particular schema
    schema_meta = index[sname]
    # Get the filename for the schema file
    schema_fname = schema_meta[META_KEYS.FNAME]
    schema_fname = os.path.join(PATHS.ASTROSCHEMA, schema_fname)

    schema = json_load_file(schema_fname)

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
