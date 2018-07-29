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

- WARNING: some keys don't match up directly, i.e. "FLUX_DENSITY" vs. 'fluxdensity'.  In cases where this has caused errors I've used the version corresponding to json-file values (e.g. 'fluxdensity' is the way its used in json, so I stick with that), and create an extra keychain attribute in the appropriate `astrocats` class (e.g. in `astrocats.catalog.photometry` I add `PHOTOMETRY.FLUX_DENSITY = PHOTOMETRY.FLUXDENSITY` for the time being.

- Instead of `u_` and `e_` attributes, make `quantity` subclasses that require (or have) associated units and/or errors...

- Why are so many `Entry` quantities actually lists without being 'listable'?!

- `source`
    - what are `name` and `reference` for?  Are they needed?

- `quantity`
    - `source` needs a `minLength`

- Handle date-time representations.  Either use custom regex-based parsing or convert everything to json-schema compatible time-specification... or use specialized, new schema

- Need to do some sort of type checking to make sure "string" values representing numbers are convertable to numbers... that or start using numerical values or something.

- Each type of `Struct` should actually be a class-factory that has pre-loaded the target schema to then check against the creation of new instances.  i.e. when calling `Source()`, it should *not* then call the parent `Struct()`, load the schema, etc etc.  Instead it should have the schema already loaded (and validated!) and just create a new instance from there.

- To save memory: have instances share certain class attributes, i.e. all `Source` instances should share the same object for the schema, perhaps for `Keychain` also?

- Name changes:
    - `source` ==> `reference`
        - `alias` ==> `idnum`
        - `reference` ==> `textcite`
    - `is_duplicate_of` ==>  ???   this isn't checking for "duplicate" but for redundancy.
    - `quantity`
        - `source` ==> `source_alias`

- Changes:

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

- `pyastroschema`
    - `tests/`
        - `test_photometry.py` [NEW-FILE]
            - Unittests for the 'photometry' schema and class.
            - Include tests for some of the complex 'dependencies' and requirements in the schema.

    - `__init__.py`
        - `PATHS`
            - `test_dir()` [NEW-METHOD]
                - Return the directory of test json files for specific schema.

- `schema/`
    - `photometry.json`
        - Added dependencies which were coded manually into `astrocats` `Photometry` class, for example requiring frequency, band or energy when flux is included.


### v0.3.0 - 2018-07-28

- `CONVERSION.md` [NEW-FILE]
    - File for documenting conversion procedures from `astrocats` to `astroschema`.
- `README.md`
    - Lots of new 'to-do' items and issues that need to be addressed.

- `schema/`
    - `entry.json` [NEW-FILE]
        - Specifications for a catalog entry (names, sources, quantities, etc).  Based on the `astrocats` `Entry` class.
    - `key.json` [NEW-FILE]
        - Schema specification for individual 'keys' of general astroschema schema.  Used with `meta-schema.json`.
    - `meta-schema.json` <== `meta-schema/astro-schema_draft-0.json`
        - Schema specification that the properties of all other schema match the `key.json` schema.
    - `photometry.json` [NEW-FILE]
        - Schema specifying photometric quantities.  Based on the `astrocats` `Photometry` class.
    - `quantity.json` [NEW-FILE]
        - Schema specifying core 'quantities' which are the data points for entries and composite data values (e.g. `photometry`).
    - `spectrum.json` [NEW-FILE]
        - Schema specifying spectrum quantities.  Based on the `astrocats` `Spectrum` class.
    - `source.json`
        - Use both a 'unique' and 'distinguishing' attributes.  A 'unique' attribute is one that uniquely defines what it is referring to (i.e. if two 'unique' attributes match, then these are referring to the same object).  A 'distinguishing' attribute is one that can be used to compare two instances (based on the `astrocats` concept of 'comparable' values).  If two 'distinguishing' values are different, then the objects are different; if they are the same, the objects *may* be the same.

- `pyastroschema/`
    - `tests/`
        - `test_entry.py` [NEW-FILE]
            - Simplest tests on the new 'entry' schema.
        - `test_key.py`
            - Minor updates for changes to the `Key` class.
        - `test_keychain.py`
            - Minor updates for changes to the `KeyChain` class.
        - `test_quantity.py` [NEW-FILE]
            - Basic testing of new 'quantity' schema.
        - `test_source.py`
            - Minor updates for changes to from `Source` standalone class to `Source(Struct)` subclass.
            
    - `keys.py`
        - `Key`
            - Use `json` validation instead of manual checking (e.g. of requirements).
            - `validate()` [NEW-METHOD]
                - Load a custom validator that not only validates but sets default values.  See `validation.py`.
            - `equals()` [NEW-METHOD]
                - Compare two keys each-other (analogous to astrocats `is_duplicate_of` methods).  Has optional `identical` argument to determine precision of comparison.
    - `schema.py` [NEW-FILE]
        - Beginning of class to represent schema themselves.
        - NOTE: non-operational.
    - `struct.py` <== `source.py`
        - What was previously the `Source` class has been generalized into the `Struct` class which can then be used for any data-structured.
        - `Struct` [NEW-CLASS]
            - Generalized class structure to apply to any catalog-object that is schema-specified.  This is analogous (and largely based on) the `astrocats.catdict.CatDict` class.
            - On initialization, the class uses its corresponding schema to generate a `Keychain` populated with `Key` instances that describe each property of this class.  Validation is performed using jsonschema.
        - `Meta_Struct` [NEW-CLASS]
            - Subclass of `Struct` which is designed to be used for further subclassing to construct particular types of object, e.g. `Source`, `Quantity`, etc.  `Meta_Struct` is used as the method to specify the schema describing/constraining the particular structure.
    - `validation.py` [NEW-FILE]
        - Create a jsonschema validator instance with extended functionality to set default values of parameters.  Currently used to set default `Key` attributes.



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
