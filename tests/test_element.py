#!/usr/bin/env python2
"""Unit tests for the Element class.

Much of this class is tested using doctest instead of traditional unit testing.
This mostly covers internal methods, edge cases, bug regression preventatives,
etc.
"""

import unittest

import xmlcomposer

class TestElementInternalMethods(unittest.TestCase):
    """Demonstrate that the internal methods work as expected
    """
    def test_format_attributes(self):
        e = xmlcomposer.Element(id_='format_attributes', class_='element_test')
        expected = 'class="element_test" id="format_attributes"'
        assert e.format_attributes() == expected
    
    def test_format_prefix(self):
        assert xmlcomposer.Element().format_prefix() == ''
        r = xmlcomposer.Namespace(module='xmlcomposer.formats.rss2', prefix='r')
        assert r.Author().format_prefix() == 'r:'
    
    def test_format_xmlns(self):
        e = xmlcomposer.Element()
        
        n = xmlcomposer.Namespace()
        assert e.format_xmlns(n) == ''
        
        n = xmlcomposer.Namespace(name='test')
        assert e.format_xmlns(n) == ' xmlns="test"'
        
        n = xmlcomposer.Namespace(name='test', prefix='t')
        assert e.format_xmlns(n) == ' xmlns:t="test"'
    
    def test_open_tag(self):
        class Example(xmlcomposer.Element): pass
        n = xmlcomposer.Namespace(name='test', prefix='r')
        n.Example = Example
        e = Example(id='test')
        xmlns = ''
        assert e.open_tag(xmlns) == '<r:example id="test">'
    
    def test_close_tag(self):
        class Example(xmlcomposer.Element): pass
        n = xmlcomposer.Namespace(prefix='r')
        n.Example = Example
        e = Example(id='test')
        assert e.close_tag() == '</r:example>'
    
    def test_determine_content_type(self):
        x = xmlcomposer.Namespace(module='xmlcomposer.formats.xhtml_1_strict')
        e = xmlcomposer.Element()
        assert e.determine_content_type(x.Pre()) == 'preformatted'
        assert e.determine_content_type(x.H1()) == 'element'
        assert e.determine_content_type(xmlcomposer.PCData('')) == 'pcdata'
        
        callback = xmlcomposer.CallBack(func=dir, return_type=x.Pre)
        assert e.determine_content_type(callback) == 'preformatted'
        
        callback = xmlcomposer.CallBack(func=dir, return_type=x.H1)
        assert e.determine_content_type(callback) == 'element'
        
        assert e.determine_content_type('') == 'indeterminate'
    
if __name__ == '__main__':
    unittest.main()

