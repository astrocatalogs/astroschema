# astroschema

This package defines a set of JSON schema relevant to astronomy and astrophysics research.  The schema are meant to specify the structure of JSON files used to contain astronomical (and associated) data.  The package also contains modules for the use of those schema in `python`, and in the future additional languages.

## Structure

- `schema/`: the schema specifications themselves
    - `metaschema/`: the metaschema specifying the structure of each astro-schema
- `pyastroschema/`: the python module for interacting with astroschema
- `tests/`: directory containing sample JSON files for testing schema validation
- `astroschema.json`: description of each schema included in this package.


## Definitions and Terminology
- A `struct` is an `astroschema` data structure that has a schema specification.  For example `source` is a particular `astroschema` `struct`, that has a particular `schema` specifying its structure.
- An `entry` is data in the form of a `struct`, i.e. an instance of a `struct` filled with data.

- `unique` vs. `distinguishing`
    - A `unique` attribute is one that uniquely identifies what it is referencing, one-to-one.  If two things have different `unique` attributes they are different.  If they have the same `unique` attributes, they are the same.
        - e.g. `bibcode` is `unique`, these `Source`s are the same:
            - `{"name": "Open Supernova Catalog", "bibcode": "2017ApJ...835...64G", "alias": 0}`
            - `{"name": "Guillochon+2017", "bibcode": "2017ApJ...835...64G", "alias": 1}`
    - A `distinguishing` attribute is one that characterizes what it is referencing, not one-to-one.  If two things have different `distinguishing` attributes, they are not necessarily different.  If they have the same `distinguishing` attributes, they are not necessarily the same.
        - e.g. `bibcode` is `unique`, these `Source`s are the same:
            - `{"name": "Open Supernova Catalog", "bibcode": "2017ApJ...835...64G", "alias": 0}`
            - `{"name": "Guillochon+2017", "bibcode": "2017ApJ...835...64G", "alias": 1}`

## To-Do / Questions

- `source` : what are `name` and `reference` for?  Are they needed?

- Name changes:
    - `source` ==> `reference`
        - `alias` ==> `idnum`
        - `reference` ==> `textcite`
    - `is_duplicate_of` ==>  ???   this isn't checking for "duplicate" but for redundancy.

- Changes:
    - `source` `alias` should be an integer instead of a string (of an integer).

- Decisions
    - Upper-case vs lower-case key attribute names in `Keychain`
    - How do we deal with parameters that are used in astrocats, but not generically useful?
        - e.g. in `source` : `alias`, `secondary`, `private`, etc
        - Also internal aspects, e.g. `compare` as a part of any `astrocats.catalog.Key`
    - How should numeric types be handled?  i.e. string vs number
        - Could use either, i.e. `["number", "string"]`
    - Should schema/'structs' be restricted to having one and only one level of properties?
    - How should the package be structured?
        - Should `pyastroschema` be a completely separate package that downloads and/or caches the astroschema specifications?
        - Should `pyastroschema` (and future other language-specific packages) stay inside `pyastroschema`?
            - In that case, should each language package be downloaded/installed on demand, or just all bundled together?

- `astroschema.json` should be dynamically generated

- Add enforced versioning such that for each schema file, if it is changed, ensure that the new version is saved into a special versions directory, and if the file is unchanged, ensure that the version number is not changed.

- Add travis and coveralls integration.

- Add python2 compatibility.


## Change Log


### Current


### v0.2.0 - 2018-07-04

- `schema/`
    - `meta-schema/`
        - `astro-schema_draft-0.json` [NEW-FILE]
            - First version of a astro-schema specific meta-schema for validating all astro-schema schema.  Currently this takes the standard json-schema and extends it slightly: required the 'type' and 'unique' attributes for each 'property'.
    - `source.json`
        - Schema specification for `Source` objects.
        - Currently: v0.4

- `pyastroschema/`
    - `tests/`
        - `test_keychain.py`
            - Unittests for the `Keychain` class.
        - `test_source.py`
            - Basic tests for basic functionality of `Source` class.
            - Tests for both copy and deepcopy behavior.

    - `__main__.py`
        - `main()`
            - This is the primary interface routine.
            - Loads the astro-schema metaschema and validates it against the standard json-schema.
            - Loads all astro-schema and validates them against both the meta-schema and the standard json-schema.
            - Produces an 'index' output file listing the current included schema, and their version and modification information.
    - `keys.py`
        - Moved `Keychain` from `source.py` to here.
        - Added new `Key` class to hold each property key.

    - `source.py`
        - Removed `Keychain` class (see `keys.py`).
        - `Source`
            - Added overriding of `__copy__` and `__deepcopy__` methods.
            - `is_duplicate_of()` [new-function]
                - Duplicated behavior of related method in astrocats class.
    - `utils.py`
        - `json_load_str()` [new-function]
            - Load dictionary from json-formatted string.
        - `get_relative_path()` [new-function]
            - Convert from a full path to a path relative to a given reference path.

### v0.1.0 - 2018-06-28

- Simple schema for 'source' structures created.
- A few test JSON files added in `tests/source` for checking validations.

- `pyastroschema/`
    - `Keychain` class to store parameter names ('keys') specified in schema files.
    - `Source` class to store data associated with the `source.json` schema.  Currently specific to the 'source' structure, and will be generalized in the future to arbitrary schema.
    - Validation works for 'source' entries and `Source` instances using the `jsonschema` python package.  This uses the example JSON files in `tests/source`.
