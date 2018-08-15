# Notes 

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

## Packaging

- Run tests in current environment with `$ nosetests --with-coverage --cover-package=pyastroschema`
- Generate `requirements.txt` from `requirements.in` by running `$ pip-compile` in the package directory (containing `setup.py`).
- To run tests in environments, use `$ tox`
    - NOTE: if dependencies change, need to rebuild `tox` environments using `$ tox --recreate`
