#!/usr/bin/env python2
"""Unit tests for the Layout class.
"""

import unittest

import xmlcomposer

class TestLayoutInternalMethods(unittest.TestCase):
    """Demonstrate that the internal methods work as expected
    """
    def test_indent(self):
        x = xmlcomposer.Layout(indent_style=' ', indent_count=0)
        y = x.indent()
        assert y.indent_count == 1
        assert x('Test') == 'Test\n'
        assert y('Test') == ' Test\n'
    
    def test_line_wrapping(self):
        l = xmlcomposer.Layout('', 0, '\n', 40)
        
        produced = l(
            'This string is longer than 40 characters. Testing wrap.',
            wrap=True
            )
        expected = 'This string is longer than 40\ncharacters. Testing wrap.\n'
        assert produced == expected
        
        produced = l(
            'Layout will not wrap in the middle <em class="test">of a tag</em>.',
            wrap=True
            )
        expected = 'Layout will not wrap in the middle\n<em class="test">of a tag</em>.\n'
        assert produced == expected


    
if __name__ == '__main__':
    unittest.main()

