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

- Replace `add_*` methods in `Entry` with a single `Add` method that figures it out.
- Add a universal `Key` attribute that says what type of schema it should be validated against, and also what type of `class` (e.g. in Astrocats) should be used to load/save it.
- Separate particular catalogs (e.g. blackhole) from the overall `astrocats` package.
    - Make a copy of all schema in output of particular package.
    - Reorganize the whole `astrocats` structure... especially for importing / (sub)commands... so convoluted right now.

- Currently `Quantity/value` is any-type (at least to accomodate aliases, perhaps other uses?), but should this be changed to numeric?

- Add some sort of `numeric` tag, and add checking of number-convertibility to a custom validator

- Revise 'time' type/format checking...  Dont forget edge cases of months-only and BC.

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

- *To use relative file paths, have to set a `RefResolver` in the python `jsonschema` package to the appropriate directory.  Also need to set the `id` of each schema file to be that files name so that internal references still work!*

## Change Log



### Current

- Modified numerous schema to remove `astrocats` specific properties: [`photometry`, `quantity`, `source`, `spectrum`].

- `pyastroschema/`
    - [1] Using the `defs.json` file now, and relative paths in schema references, requires validators to use `jsonschema.RefResolver` objects with the base path.  To do this, when creating `struct.SchemaDict` instances, the schema specification should be the absolute file-path.  The method `utils.load_schema_dict` now returns the path to the schema also.  The methods `utils.get_schema_odict` and `utils.get_list_of_schema` have been deprecated (commented out for now), to simplify what types of arguments are acceptable.
    
    - `__init__.py`
        - `copy_schema_files()` [NEW-FUNCTION]
            - Copy all, or a single, schema file to the given target directory.
    - `schema.py`
        - `JSONOrderedDict`
            - Add hooks to sort before `dump` and `dumps` commands by passing sorting function.
        - `SchemaDict`
            - No longer accepts a list of schema as argument.  Schema must be combined using either `extend` or `update` methods.
            - Simplified initialization to limit acceptable arguments (see [1]).
            - Store the schema path and a constructed `jsonschema.RefResolver` when possible (see [1]).
            - `extend()`
                - Set the `check_conflict` parameter to True by default.
            - `update()` [NEW-FUNCTION]
                - Added wrapper around `JSONOrderedDict.update()` to first convert argument to `SchemaDict`.
    - `utils.py`
        - `warn_with_traceback()` [NEW-FUNCTION]
            - Modify the `warnings` module to provide tracebacks
        - `get_schema_odict()` [REMOVED]
            - See [1]
        - `get_list_of_schema()` [REMOVED]
            - See [1]
        - `index_entry_for_schema()` [NEW-FUNCTION]
            - Retrieve the index entry (dict) for the target schema.
        - `path_for_schema_file()` [NEW-FUNCTION]
            - Retrieve the full-path for the target schema.
    - `validation.py`
        - `PAS_Validator()`
            - Pass `kwargs` along so that a `resolver` can be added to the validator.

- `schema/`
    - Restructure schema to reference new `defs.json` file.  Added `'id'` attributes with each files name so that both relative and internal references will work; this is likely a bug in the python `jsonschema` package.
    - `entry.json`
        - Removed astrocats specific fields.
    - `defs.json` [NEW-FILE]
        - New file specifically for schema definitions, references from other schema files.


### v0.5.0 - 2018-08-02

- Add new 'format' schema specifications including 'numeric' and 'astrotime'.
- New `SchemaDict` class that stores schema specifications in `Struct` classes.  Provides internal validation method.
    - NOTE: `SchemaDict` has *not* been integrated into the `Key` class yet, but it is stored to each `Keychain`.
- `Struct` subclasses have been upgraded to use protected class-attributes (i.e. shared) to store schema information.  A wrapper (`struct.set_struct_schema()`) and class factor method (`struct.Struct.construct()`) have been added to provide a customization API for derived classes.

- `pyastroschema/`
    - `tests/`
        - `test_schemadict.py` [NEW-FILE]
            - Basic construction unittests for the new `SchemaDict` class.
        - `test_struct.py` [NEW-FILE]
            - Basic tests for `Struct` class, specifically making sure that subclass works as expected, and with new `SchemaDict` class.
        - `test_validation.py` [NEW-FILE]
            - Tests for new `PAS_Validator()` method (and customized class).

    - `keys.py`
        - `Key`
            - Changed `Key` instances to be immutable.  Once they are created their attributes cannot be changed.
            - `__repr__()`
                - Cache the result of `repr` on initialization to save time.  Depends on `Key` being immutable.
            - `equals()`
                - BUG: in comparison, built-in methods could be compared which would fail, e.g. `format` method of str.
    - `schema.py`
        - `JSONOrderedDict` [NEW-CLASS]
            - This wrapper around an `OrderedDict` class to add some json methods (e.g. loading/saving to/from strings)
            - `extend()` [NEW-FUNCTION]
                - Function that will add the elements from a second `dict` into the first, without overwriting existing parameters (like `update()` does).
        - `SchemaDict` [NEW-CLASS]
            - Subclass of `JSONOrderedDict` designed to contain schema.  Adds validation methods.  Can be initialized from numerous schema, in which case `extend()` is used to combine them.
    - `struct.py`
        - All of the derived structures (subclasses of `Struct`) now use the decorator instead of subclassing with `Meta_Struct`.
        - `Struct`
            - Added `keychain`, `schema` and `extendable` as protected `property` values.
            - Changed to inherits from `schema.JSONOrderedDict` to get the nice json-based import/export methods.
            - `construct()` [NEW-METHOD]
                - Factory method which uses `struct.set_struct_schema` to create a custom sub-class of `Struct` for later instantiation.
            - `get_keychain()` [REMOVED]
                - Deprecated in favor of `keychain` `property`.
            - `to_json()` [REMOVED]
                - Deprecated in favor of inherited `JSONOrderedDict` methods.
            - `validate()`
                - BUG: custom validator wasnt being used.  Now calls internal `SchemaDict` for validation.
        - `Meta_Struct` [REMOVED]
            - Deprecated in favor of new subclassing procedures.
    - `validation.py`
        - `PAS_Validator()` <== `Default_Validator()`
            - New customized validator that not only sets defaults (as before) but also checks the `"numeric"` 'format' specifier.
            - Tests added for behavior.

- `schema/`
    - `quantity.json`
        - BUG, FIX: Changed `value` from being numeric to being any-type.  This is to accommodate 'alias' values in `astrocats`... not sure if this should remain or be changed.
        - BUG, FIX: Changed `source` from being numeric to being any-type.  This is to accommodate strings like `"1,3,4"` currently used in astrocats.  This should be fixed in the future.



### v0.4.0 - 2018-07-30

- FIX: Numerous aspects of the structure schema changed (e.g. variable names, new parameters) for consistency with `astrocats`.  This is temporary.  These should all be restored back / removed later.

- `pyastroschema`
    - `tests/`
        - `test_photometry.py` [NEW-FILE]
            - Unittests for the 'photometry' schema and class.
            - Include tests for some of the complex 'dependencies' and requirements in the schema.
        - `test_spectrum.py` [NEW-FILE]
            - Unittests for the 'spectrum' schema and class.
            - Include tests for some of the complex dependencies and requirements in the schema.

    - `__init__.py`
        - `PATHS`
            - `test_dir()` [NEW-METHOD]
                - Return the directory of test json files for specific schema.
    - `keys.py`
        - `Keychain`
            - `get_key_by_name()` [NEW-METHOD]
                - Based on related method in astrocats.
                - Get the key in this keychain based no its name.
    - `struct.py`
        - `Struct`
            - `get_keychain()`
                - Allow `mutable` and `extendable` arguments to be passed through this method.
        - `Photometry` [NEW-CLASS]
            - New subclass of `Struct` with associated `photometry.json` schema.
        - `Spectrum` [NEW-CLASS]
            - New subclass of `Struct` with associated `spectrum.json` schema.
        - `Entry` [NEW-CLASS]
            - New subclass of `Struct` with associated `entry.json` schema.
    - `utils.py`
        - `get_schema_odict()` [NEW-FUNCTION
            - Function that will return an `OrderedDict` given a filename, indexed schema-name, or odict.
        - `get_list_of_schema()` [NEW-FUNCTION]
            - Returns a list of odict schema given one or more specified by filename, str, or odict.

- `schema/`
    - `photometry.json`
        - Added dependencies which were coded manually into `astrocats` `Photometry` class, for example requiring frequency, band or energy when flux is included.
    - `entry.json`
        - FIX: temporary addition of '...PREF_KINDS' parameters for `astrocats` consistency.
    - `key.json`
        - FIX: temporary changes for `astrocats` compatibility.
    - `spectrum.json`
        - BUG: fixed some incorrect requirements logic.
        - Added more complex requirements/dependencies logic that was hardcoded into `astrocats` `Spectrum` class.


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
