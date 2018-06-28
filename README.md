# astroschema

This package defines a set of JSON schema relevant to astronomy and astrophysics research.  The schema are meant to specify the structure of JSON files used to contain astronomical (and associated) data.  The package also contains modules for the use of those schema in `python`, and in the future additional languages.

## Structure

- `schema`: the schema specifications themselves
- `pyastroschema`: the python module for interacting with astroschema
- `astroschema.json`: description of each schema included in this package.


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
