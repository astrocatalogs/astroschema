"""

To-Do:
- Create a class to contain the keys used in JSON files, e.g. 'filename', 'description', so that
  they aren't always hardcoded in.

"""
import os
import glob
import json
import datetime
from collections import OrderedDict

import jsonschema

PATH_ASTROSCHEMA = os.path.realpath(os.path.dirname(__file__))
DIR_SCHEMA = "schema"
FNAME_VERSION = "VERSION"

VERBOSE = True

INDEX_JSON_FILENAME = "astroschema_index.json"
INDEX_DESCRIPTION = "Index and summary of schema included in `astroschema`."


def main():

    print("Loading schema filenames")
    files = get_schema_filenames()
    print("Validating schema")
    schemas = load_schemas(files)

    index_fname = os.path.join(PATH_ASTROSCHEMA, INDEX_JSON_FILENAME)
    print("Writing summary to index file: '{}'".format(index_fname))
    write_index_json(schemas, index_fname)

    return


def get_schema_filenames():
    """
    """
    schema_file_pattern = os.path.join(PATH_ASTROSCHEMA, DIR_SCHEMA, '*.json')
    if VERBOSE:
        print("\tSearching for files matching '{}'".format(schema_file_pattern))
    files = sorted(glob.glob(schema_file_pattern))
    if VERBOSE:
        print("\t\tFound {} schema".format(len(files)))
    return files


def load_schemas(files):
    """
    """
    schemas = OrderedDict()

    for ii, ff in enumerate(files):
        fname = os.path.basename(ff)
        if VERBOSE:
            print("\t{:2d}: '{}'".format(ii, fname))

        # Load Schema from JSON file
        try:
            with open(ff, 'r') as data:
                _schema = json.load(data)
        except json.decoder.JSONDecodeError:
            print("ERROR: Failed to load file '{}'".format(ff))
            raise

        title = _schema['title']
        desc = _schema['description']
        vers = _schema['version']
        # Get modification time of file
        mtime = os.path.getmtime(ff)
        # Convert to str via `datetime` instance for nice formatting
        mtime = str(datetime.datetime.fromtimestamp(mtime))

        # Load appropriate validator
        validator = jsonschema.validators.validator_for(_schema)

        # Validate schema itself
        validator.check_schema(_schema)

        keys = ['description', 'filename', 'version', 'updated', 'schema']
        vals = [desc, fname, vers, mtime, _schema]
        this_schema = OrderedDict.fromkeys(keys)
        for kk, vv in zip(keys, vals):
            this_schema[kk] = vv

        schemas[title] = this_schema

    return schemas


def write_index_json(schemas, fname):
    """Write a summary of all schema to JSON index file.
    """
    fname_base = os.path.basename(fname)

    # Construct summary/index dictionary
    # ----------------------------------------
    schemas_index = OrderedDict()
    keys = ['description', 'filename', 'version', 'updated']
    for title, entry in schemas.items():
        this = OrderedDict()
        for kk in keys:
            this[kk] = entry[kk]
        schemas_index[title] = this

    vers = _get_astroschema_version()
    if VERBOSE:
        print("\tastroschema version: '{}'".format(vers))

    index = OrderedDict()
    index['description'] = INDEX_DESCRIPTION
    index['filename'] = fname_base
    index['version'] = vers
    index['updated'] = str(datetime.datetime.now())
    index['index'] = schemas_index

    # Save to File
    # ---------------------
    json_dump_file(index, fname)
    if VERBOSE:
        print("\t{}, size: {}".format(fname_base, _get_file_size_str(fname)))

    return


def json_dump_str(odict, **kwargs):
    kw = _json_dump_kwargs(indent=2)
    jsonstring = json.dumps(odict, **kw)
    return jsonstring


def json_dump_file(odict, fname, **kwargs):
    kw = _json_dump_kwargs(**kwargs)
    with open(fname, 'w') as out:
        json.dump(odict, out, **kw)
    return


def _json_dump_kwargs(**kwargs):
    kw = dict(indent=2, separators=(',', ':'), ensure_ascii=False)
    for kk, vv in kwargs.items():
        kw[kk] = vv

    return kw


def _get_file_size_str(fil):
    fsize = os.path.getsize(fil)
    PREC = 1

    abbrevs = (
        (1 << 50, 'PB'),
        (1 << 40, 'TB'),
        (1 << 30, 'GB'),
        (1 << 20, 'MB'),
        (1 << 10, 'KB'),
        (1, 'bytes')
    )

    for factor, suffix in abbrevs:
        if fsize >= factor:
            break

    size_str = '{size:.{prec:}f} {suff}'.format(prec=PREC, size=fsize/factor, suff=suffix)
    return size_str


def _get_astroschema_version():
    """Load the version of the entire `astroschema` package, from the version file.
    """
    fname = os.path.join(PATH_ASTROSCHEMA, FNAME_VERSION)
    with open(fname, 'r') as inp:
        vers = inp.read().strip()
    return vers


if __name__ == "__main__":
    main()
