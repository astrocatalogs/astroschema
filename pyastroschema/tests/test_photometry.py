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

from nose.tools import assert_true, assert_raises, assert_false

import pyastroschema as pas
from pyastroschema.struct import Photometry

# Good
# -----------------
YES_0 = dict(
    time="12312412.23",
    magnitude=3.14,
    source="0"
)

# BAD
# ------------------
NAW_0 = dict(
    flux=3.14,
    source="0"
)

NAW_1 = dict(
    time="2018-01-01",
    source="0"
)

NAW_2 = dict(
    time="2018-01-01",
    flux=3.14
)

YES = [YES_0]
NAW = [NAW_0, NAW_1, NAW_2]

photometry_schema, path = pas.utils.load_schema_dict('photometry')
RESOLVER = jsonschema.RefResolver('file://{}'.format(path), None)


def test_good():
    print("test_photometry.test_good()")

    for qkw in YES:
        print("Trying successful schema: '{}'".format(qkw))
        quant = Photometry(**qkw)
        print("\t", quant)

    return


def test_bad():
    print("test_photometry.test_bad()")

    for qkw in NAW:
        print("Trying failure schema: '{}'".format(qkw))
        with assert_raises(jsonschema.exceptions.ValidationError):
            quant = Photometry(**qkw)
            print("\t", quant)

    # `u_flux` is required
    test = dict(
        time="2018-01-01",
        flux=3.14,
        source="0",
        hello="goodbye"
    )

    with assert_raises(jsonschema.ValidationError):
        quant = Photometry(**test)

    return


def test_flux_dependencies():

    def run_test(test):
        print("successful test = ", test)
        Photometry(**test)
        jsonschema.validate(test, photometry_schema, resolver=RESOLVER)

        keys = list(test.keys())
        for kk in keys:
            dup = copy.deepcopy(test)
            dup.pop(kk)
            print("removed '{}', should fail...".format(kk))
            with assert_raises(jsonschema.exceptions.ValidationError):
                jsonschema.validate(dup, photometry_schema, resolver=RESOLVER)
            with assert_raises(jsonschema.exceptions.ValidationError):
                Photometry(**dup)

        return

    # Each element of this should be required
    t1 = dict(
        time="45481.00",
        flux="232.324234",
        frequency="123",
        u_frequency="GHz",
        u_flux="erg/s",
        source="1"
    )

    # Each element of this should be required
    t2 = dict(
        time="45481.00",
        fluxdensity="232.324234",
        frequency="123",
        u_frequency="GHz",
        u_fluxdensity="erg/s",
        source="1"
    )

    run_test(t1)
    run_test(t2)

    # `u_frequency` should *not* be required without 'flux' or 'fluxdensity'
    test = dict(
        time="45481.00",
        magnitude="232.324234",
        frequency="123",
        source="1"
    )

    Photometry(**test)
    jsonschema.validate(test, photometry_schema, resolver=RESOLVER)

    # 'frequency' should also not be required at all with 'magnitude'
    test.pop('frequency')

    Photometry(**test)
    jsonschema.validate(test, photometry_schema, resolver=RESOLVER)

    return


def test():
    pat_good = os.path.join(pas.PATHS.test_dir("photometry", good=True), "*.json")
    tests_good = sorted(glob.glob(pat_good))
    print("Found {} good tests".format(len(tests_good)))

    for ii, good in enumerate(tests_good):
        print("\t{:3d}: '{}'".format(ii, good))
        gt = pas.utils.json_load_file(good)

        jsonschema.validate(gt, photometry_schema, resolver=RESOLVER)

    pat_bad = os.path.join(pas.PATHS.test_dir("photometry", bad=True), "*.json")
    tests_bad = sorted(glob.glob(pat_bad))
    print("Found {} bad  tests".format(len(tests_bad)))

    for ii, bad in enumerate(tests_bad):
        print("\t{:3d}: '{}'".format(ii, bad))
        bt = pas.utils.json_load_file(bad)

        with assert_raises(jsonschema.exceptions.ValidationError):
            jsonschema.validate(bt, photometry_schema, resolver=RESOLVER)

    return
