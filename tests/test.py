#!/usr/bin/env python2

import sys
import unittest
from doctest import DocTestSuite, NORMALIZE_WHITESPACE
from types import ModuleType, TypeType

import xmlcomposer

suite = unittest.TestSuite()

# Build and add tests from docstrings with doctest.
suite.addTest(DocTestSuite(xmlcomposer, optionflags=NORMALIZE_WHITESPACE))
for obj in vars(xmlcomposer).values():
    if isinstance(obj, ModuleType):
        suite.addTest(DocTestSuite(obj, optionflags=NORMALIZE_WHITESPACE))

# Add the test subpackages. These can also be run individually.
test_names = (
    'test_element',
    'test_text',
    )
suite.addTest(unittest.defaultTestLoader.loadTestsFromNames(test_names))

# Run everything.
unittest.TextTestRunner(verbosity=2).run(suite)

