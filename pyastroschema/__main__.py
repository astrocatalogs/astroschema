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

    print("Loading schema")
    files = get_schema_filenames()
    schemas = load_schemas(files)

    print("Validating schema")
    validate_schema(schemas)

    print("\tschemas = ", list(schemas.keys()))

    print("Testing schema against sample files")
    # test_schemas(schemas)

    index_fname = PATHS.INDEX_JSON_FILE
    print("Writing summary to index file: '{}'".format(index_fname))
    schemas_index(schemas, files, index_fname)

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
        schemas[title] = _schema

    return schemas


def validate_schema(schemas):
    meta_schema = utils.json_load_file(PATHS.META_SCHEMA_FILE)

    # Validate meta-schema itself
    validator = jsonschema.validators.validator_for(meta_schema)
    validator.check_schema(meta_schema)
    if VERBOSE:
        print("\tmeta-schema validation successful")

    if VERBOSE:
        print("\tValidating astro-schema")
        for title, astroschema in schemas.items():
            print("\t\t'{}'".format(title))
            validator = jsonschema.validators.validator_for(astroschema)
            validator.check_schema(astroschema)
            print("\t\t\tvalidated against json-schema")
            jsonschema.validate(astroschema, meta_schema)
            print("\t\t\tvalidated against astroschema meta-schema")

    return


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


def schemas_index(schemas, file_names, index_fname):
    """
    """

    # Construct index entry for each schema (file)
    # ----------------------------------------------------
    schemas_sub_index = OrderedDict()
    keys = [META_KEYS.DESC, META_KEYS.FNAME, META_KEYS.VERS]
    for (title, astroschema), fname in zip(schemas.items(), file_names):
        # Get filename relative to `PATH_ASTROSCHEMA`
        # common_path = os.path.join(os.path.commonpath([fname, PATHS.ASTROSCHEMA]), '')
        # relpath = fname.split(common_path)[-1]
        schema_file_relpath = utils.get_relative_path(fname, PATHS.ASTROSCHEMA)

        title = astroschema[META_KEYS.TITLE]
        desc = astroschema[META_KEYS.DESC]
        vers = astroschema[META_KEYS.VERS]
        # Get modification time of file
        mtime = os.path.getmtime(fname)
        #     Convert to str via `datetime` instance for nice formatting
        mtime = str(datetime.datetime.fromtimestamp(mtime))

        # Store target parameters to dictionary for this schema
        keys = [META_KEYS.TITLE, META_KEYS.DESC, META_KEYS.FNAME,
                META_KEYS.VERS, META_KEYS.UPDATED]
        vals = [title, desc, schema_file_relpath,
                vers, mtime]
        index_entry_from_schema = OrderedDict()
        for kk, vv in zip(keys, vals):
            index_entry_from_schema[kk] = vv

        schemas_sub_index[title] = index_entry_from_schema

    # Construct top-level dictionary including meta-data
    # --------------------------------------------------------------
    vers = utils.get_astroschema_version()
    index_fname_rel = utils.get_relative_path(index_fname, PATHS.ASTROSCHEMA)
    if VERBOSE:
        print("\tastroschema version: '{}'".format(vers))

    index = OrderedDict()
    index[META_KEYS.TITLE] = "astro-schema index file"
    index[META_KEYS.DESC] = INDEX_DESCRIPTION
    index[META_KEYS.FNAME] = index_fname_rel
    index[META_KEYS.VERS] = vers
    # index[META_KEYS.UPDATED] = str(datetime.datetime.now())
    index[META_KEYS.INDEX] = schemas_sub_index

    # Write to File
    # --------------------------
    fname_base = os.path.basename(index_fname)
    utils.json_dump_file(index, index_fname)
    if VERBOSE:
        size_str = utils.get_file_size_str(index_fname)
        print("\t{}, size: {}".format(fname_base, size_str))

    return index


if __name__ == "__main__":
    main()
