"""Test methods.

Can be run with:
    $ nosetests path/to/test_file.py
    $ nosetests path/to/test_file.py:Test_Class.test_method

"""
# import copy

import jsonschema

from nose.tools import assert_true

# import pyastroschema as pas
from pyastroschema.struct import Entry


S1 = dict(
    alias=0,
    arxivid="1605.01054"
)

S2 = dict(
    alias=1,
    arxivid="1801.01234"
)

E1 = dict(
    name="test-entry",
    sources=[S1, S2]
)


def test_basics():
    # source_schema = pas.utils.load_schema_dict('source')

    # Should work with alias and arxivid
    ent = Entry(**E1)

    keys = ent.keychain
    assert_true(ent['name'] == E1['name'])
    print('name' in ent)
    print(keys.NAME in ent)

    assert_true(ent[keys.NAME] == E1['name'])

    return
