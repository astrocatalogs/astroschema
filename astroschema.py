"""Primary astroschema script for validating schema and producing additional output files.

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

import pyastroschema as pas
from pyastroschema import PATH_ASTROSCHEMA, PATH_SCHEMA

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
    """Load the schema-files filenames: everything in the schema directory.

    returns
    -------
    files : list of str

    """
    schema_file_pattern = os.path.join(PATH_SCHEMA, '*.json')
    if VERBOSE:
        print("\tSearching for files matching '{}'".format(schema_file_pattern))
    files = sorted(glob.glob(schema_file_pattern))
    if VERBOSE:
        print("\t\tFound {} schema".format(len(files)))
    return files


def load_schemas(files):
    """Given a list of schema filenames, load the schema and metadata from each of them.

    Returns
    -------
    schemas : `OrderedDict`

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

    # Construct top-level dictionary including meta-data
    # --------------------------------------------------------------
    vers = pas.utils.get_astroschema_version()
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
    pas.utils.json_dump_file(index, fname)
    if VERBOSE:
        size_str = pas.utils.get_file_size_str(fname)
        print("\t{}, size: {}".format(fname_base, size_str))

    return


if __name__ == "__main__":
    main()
