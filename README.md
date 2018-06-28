# astroschema

This package defines a set of JSON schema relevant to astronomy and astrophysics research.  The schema are meant to specify the structure of JSON files used to contain astronomical (and associated) data.  The package also contains modules for the use of those schema in `python`, and in the future additional languages.

## Structure

- `schema/`: the schema specifications themselves
- `pyastroschema/`: the python module for interacting with astroschema
- `tests/`: directory containing sample JSON files for testing schema validation
- `astroschema.json`: description of each schema included in this package.


## Definitions and Terminology
- A `struct` is an `astroschema` data structure that has a schema specification.  For example `source` is a particular `astroschema` `struct`, that has a particular `schema` specifying its structure.
- An `entry` is data in the form of a `struct`, i.e. an instance of a `struct` filled with data.


## To-Do

- Name changes:
    - `source` ==> `reference`
        - `alias` ==> `idnum`
        - `reference` ==> `textcite`

- Changes:
    - `source` `alias` should be an integer instead of a string (of an integer).

- Decisions
    - How do we deal with parameters that are used in astrocats, but not generically useful?
        - e.g. in `source` : `alias`, `secondary`, `private`, etc
        - Also internal aspects, e.g. `compare` as a part of any `astrocats.catalog.Key`
    - How should numeric types be handled?  i.e. string vs number
        - Could use either, i.e. `["number", "string"]`
    - Should schema/'structs' be restricted to having one and only one level of properties?

- `astroschema.json` should be dynamically generated

- Add enforced versioning such that for each schema file, if it is changed, ensure that the new version is saved into a special versions directory, and if the file is unchanged, ensure that the version number is not changed.


## Change Log

### Current


### v0.1.0 - 2018-06-28

- Simple schema for 'source' structures created.
- A few test JSON files added in `tests/source` for checking validations.

- `pyastroschema`
    - `Keychain` class to store parameter names ('keys') specified in schema files.
    - `Source` class to store data associated with the `source.json` schema.  Currently specific to the 'source' structure, and will be generalized in the future to arbitrary schema.
    - Validation works for 'source' entries and `Source` instances using the `jsonschema` python package.  This uses the example JSON files in `tests/source`.
