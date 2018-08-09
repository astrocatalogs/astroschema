"""Test methods.

Can be run with:
    $ nosetests path/to/test_file.py
    $ nosetests path/to/test_file.py:Test_Class.test_method

"""

# from __future__ import absolute_import, division, print_function, unicode_literals
import os
import glob
import copy

import jsonschema

from nose.tools import assert_true, assert_raises, assert_false  # , assert_equal,

import pyastroschema as pas
from pyastroschema.struct import Spectrum

# Good
# -----------------
YES_0 = dict(
    u_fluxes="jansky",
    u_wavelengths="angstrom",
    data=[["123", "456"], ["987", "654"]],
    source="0"
)

YES_1 = dict(
    u_fluxes="jansky",
    u_wavelengths="angstrom",
    data=[["123", "456"], ["987", "654"]],
    filename="0.json"
)

YES_2 = dict(
    u_fluxes="jansky",
    data=[["123", "456"], ["987", "654"]],
    filename="0.json"
)

# BAD
# ------------------
NAW_0 = dict(
    u_fluxes="jansky",
    data=[["123", "456"], ["987", "654"]],
    source="0"
)

YES = [YES_0, YES_1, YES_2]
NAW = [NAW_0]

spectrum_schema, path = pas.utils.load_schema_dict('spectrum')
RESOLVER = jsonschema.RefResolver('file://{}'.format(path), None)


def validate(obj, schema):
    jsonschema.validate(obj, schema, resolver=RESOLVER)
    return


def test_good():
    print("test_spectrum.test_good()")

    for qkw in YES:
        print("Trying successful schema: '{}'".format(qkw))
        quant = Spectrum(**qkw)
        print("\t", quant)

    return


def test_bad():
    print("test_spectrum.test_bad()")

    for qkw in NAW:
        print("Trying failure schema: '{}'".format(qkw))
        with assert_raises(jsonschema.exceptions.ValidationError):
            quant = Spectrum(**qkw)
            print("\t", quant)

    # Requires 'u_flux'
    test = dict(
        time="213.123123",
        flux=3.14,
        source="0",
    )

    with assert_raises(jsonschema.ValidationError):
        quant = Spectrum(**test)

    return


def test_data_dependencies():

    def check_good(test):
        Spectrum(**test)
        validate(test, spectrum_schema)
        return

    def check_bad(test):
        with assert_raises(jsonschema.exceptions.ValidationError):
            validate(test, spectrum_schema)
        with assert_raises(jsonschema.exceptions.ValidationError):
            Spectrum(**test)
        return

    def run_test(test):
        print("successful test = ", test)
        check_good(test)

        keys = list(test.keys())
        for kk in keys:
            dup = copy.deepcopy(test)
            dup.pop(kk)
            print("removed '{}', should fail...".format(kk))
            check_bad(dup)

        return

    # Each element of this should be required
    t2 = dict(
        u_fluxes="jansky",
        u_wavelengths="angstrom",
        data=[["123", "456"], ["987", "654"]],
        source="0"
    )

    run_test(t2)

    # without 'data' need either (both wavelengths and fluxes) or (filename)
    t1 = copy.deepcopy(t2)
    t1.pop('data')
    check_bad(t1)

    #    try both wavelengths and fluxes
    t1['wavelengths'] = ["1.0", "2.0"]
    check_bad(t1)
    t1['fluxes'] = ["1.0", "2.0"]
    check_good(t1)
    t1.pop('wavelengths')
    check_bad(t1)

    #    try filename
    t1.pop('fluxes')
    check_bad(t1)
    t1['filename'] = 'test.json'
    check_good(t1)

    # With data 'errors' without 'u_errors' is okay, but needed when no 'errors'
    #    good: yes 'data' and no 'u_errors'
    t1 = copy.deepcopy(t2)
    check_good(t1)
    t1['errors'] = ["100", "200"]
    check_good(t1)

    t1 = copy.deepcopy(t2)
    t1.pop('data')
    check_bad(t1)
    t1['wavelengths'] = ["1.0", "2.0"]
    t1['fluxes'] = ["1.0", "2.0"]
    check_good(t1)
    #    bad: no 'data' and no 'u_errors'
    t1['errors'] = ["100", "200"]
    check_bad(t1)
    t1['u_errors'] = "a"
    check_good(t1)

    return


def test():
    pat_good = os.path.join(pas.PATHS.test_dir("spectrum", good=True), "*.json")
    tests_good = sorted(glob.glob(pat_good))
    print("Found {} good tests".format(len(tests_good)))

    for ii, good in enumerate(tests_good):
        print("\t{:3d}: '{}'".format(ii, good))
        gt = pas.utils.json_load_file(good)

        validate(gt, spectrum_schema)

    pat_bad = os.path.join(pas.PATHS.test_dir("spectrum", bad=True), "*.json")
    tests_bad = sorted(glob.glob(pat_bad))
    print("Found {} bad  tests".format(len(tests_bad)))

    for ii, bad in enumerate(tests_bad):
        print("\t{:3d}: '{}'".format(ii, bad))
        bt = pas.utils.json_load_file(bad)

        with assert_raises(jsonschema.exceptions.ValidationError):
            validate(bt, spectrum_schema)

    return
