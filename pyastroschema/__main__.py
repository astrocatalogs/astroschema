"""Primary astroschema script for validating schema and producing additional output files.

To-Do:

"""
import os
import glob
import datetime
from collections import OrderedDict

import jsonschema

from . import (PATHS, INDEX_DESCRIPTION, VERBOSE, META_KEYS)
from . import utils


def main():

    print("Loading schema filenames")
    files = get_schema_filenames()
    print("Validating schema")
    schemas = load_schemas(files)

    print("Validating test files")
    test_schemas(schemas)

    index_fname = PATHS.INDEX_JSON_FILE
    print("Writing summary to index file: '{}'".format(index_fname))
    write_index_json(schemas, index_fname)

    return


def get_schema_filenames():
    """Load the schema-files filenames: everything in the schema directory.

    returns
    -------
    files : list of str

    """
    schema_file_pattern = os.path.join(PATHS.SCHEMA_DIR, '*.json')
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

    for ii, fname in enumerate(files):
        fname_base = os.path.basename(fname)
        if VERBOSE:
            print("\t{:2d}: '{}'".format(ii, fname_base))

        # Load schema from file
        _schema = utils.json_load_file(fname)

        title = _schema[META_KEYS.TITLE]
        desc = _schema[META_KEYS.DESC]
        vers = _schema[META_KEYS.VERS]
        # Get modification time of file
        mtime = os.path.getmtime(fname)
        # Convert to str via `datetime` instance for nice formatting
        mtime = str(datetime.datetime.fromtimestamp(mtime))

        # Load appropriate validator
        validator = jsonschema.validators.validator_for(_schema)

        # Validate schema itself
        validator.check_schema(_schema)

        # Get filename relative to `PATH_ASTROSCHEMA`
        common_path = os.path.join(os.path.commonpath([fname, PATHS.ASTROSCHEMA]), '')
        relpath = fname.split(common_path)[-1]

        keys = [META_KEYS.TITLE, META_KEYS.DESC, META_KEYS.FNAME, META_KEYS.VERS,
                META_KEYS.UPDATED, META_KEYS.SCHEMA]
        vals = [title, desc, relpath, vers,
                mtime, _schema]
        this_schema = OrderedDict.fromkeys(keys)
        for kk, vv in zip(keys, vals):
            this_schema[kk] = vv

        schemas[title] = this_schema

    return schemas


def test_schemas(schemas):
    for schema_meta in schemas.values():
        name = schema_meta[META_KEYS.TITLE]
        schem = schema_meta[META_KEYS.SCHEMA]
        test_path = os.path.join(PATHS.TESTS_DIR, name, '')
        test_file_pattern = os.path.join(test_path, '*.json')
        test_files = sorted(glob.glob(test_file_pattern))

        if VERBOSE:
            print("\t{}: '{}' with {} files".format(name, test_path, len(test_files)))

        for fname in test_files:
            entry_meta = utils.json_load_file(fname)
            valid = entry_meta['valid']
            entry = entry_meta['entry']
            rel_fname = os.path.join(name, os.path.basename(fname))

            try:
                jsonschema.validate(entry, schem)
                success = True
            except Exception:
                success = False
                if valid:
                    raise
            else:
                if not valid:
                    err = "This test should have failed!"
                    raise jsonschema.exceptions.ValidationError(err)
            finally:
                print("\t\ttest '{}'  valid: {:5s}  passed: {:5s}".format(
                    rel_fname, str(valid), str(success)))

    return


def write_index_json(schemas, fname):
    """Write a summary of all schema to JSON index file.
    """
    fname_base = os.path.basename(fname)

    # Construct summary/index dictionary
    # ----------------------------------------
    schemas_index = OrderedDict()
    keys = [META_KEYS.DESC, META_KEYS.FNAME, META_KEYS.VERS]
    for title, entry in schemas.items():
        this = OrderedDict()
        for kk in keys:
            this[kk] = entry[kk]
        schemas_index[title] = this

    # Construct top-level dictionary including meta-data
    # --------------------------------------------------------------
    vers = utils.get_astroschema_version()
    if VERBOSE:
        print("\tastroschema version: '{}'".format(vers))

    index = OrderedDict()
    index[META_KEYS.DESC] = INDEX_DESCRIPTION
    index[META_KEYS.FNAME] = fname_base
    index[META_KEYS.VERS] = vers
    # index[META_KEYS.UPDATED] = str(datetime.datetime.now())
    index[META_KEYS.INDEX] = schemas_index

    # Save to File
    # ---------------------
    utils.json_dump_file(index, fname)
    if VERBOSE:
        size_str = utils.get_file_size_str(fname)
        print("\t{}, size: {}".format(fname_base, size_str))

    return


if __name__ == "__main__":
    main()
