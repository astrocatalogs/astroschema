"""Utility functions for `pyastroschema`.
"""

import os
import json

from . import PATH_ASTROSCHEMA_VERSION


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


def _json_dump_kwargs(**kwargs):
    """Load kwargs to be passed to `json.dump` and `json.dumps`.
    """
    kw = dict(indent=2, separators=(',', ':'), ensure_ascii=False)
    for kk, vv in kwargs.items():
        kw[kk] = vv

    return kw


def _get_file_size_str(fil):
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


def _get_astroschema_version():
    """Load the version of the entire `astroschema` package, from the version file.
    """
    # fname = os.path.join(PATH_ASTROSCHEMA, FNAME_VERSION)
    with open(PATH_ASTROSCHEMA_VERSION, 'r') as inp:
        vers = inp.read().strip()
    return vers
