# astroschema

This package defines a set of JSON schema relevant to astronomy and astrophysics research.  The schema are meant to specify the structure of JSON files used to contain astronomical (and associated) data.  The package also contains modules for the use of those schema in `python`, and in the future additional languages.

## Structure

- `schema/`: the schema specifications themselves
- `pyastroschema/`: the python module for interacting with astroschema
- `validations/`: directory containing sample JSON files for testing schema validation
- `astroschema.json`: description of each schema included in this package.


## Definitions and Terminology
- 


## To-Do

- Name changes:
    - `source` ==> `reference`
        - `alias` ==> `idnum`
        - `reference` ==> `textcite`

- Decisions
    - How do we deal with parameters that are used in astrocats, but not generically useful?
        - e.g. in `source` : `alias`, `secondary`, `private`, etc
        - Also internal aspects, e.g. `compare` as a part of any `astrocats.catalog.Key`
    - How should numeric types be handled?  i.e. string vs number
        - Could use either, i.e. `["number", "string"]`

- `astroschema.json` should be dynamically generated

- Add enforced versioning such that for each schema file, if it is changed, ensure that the new version is saved into a special versions directory, and if the file is unchanged, ensure that the version number is not changed.
