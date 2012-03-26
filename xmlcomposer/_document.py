# Copyright (c) 1999, 2012 Michael Saavedra
# This file may be redistributed under the terms of the GNU LPGL v. 3 or later.

"""A set of classes for easily creating XML documents.
"""

from types import FunctionType, MethodType

from _text import TextBlock, SubstitutableTextBlock
from _namespace import BASE_SCOPE, DocumentScope
from _layout import DEFAULT_LAYOUT, SPARTAN_LAYOUT, MINIMAL_LAYOUT
from _element import Element, ProcessingInstruction

class Document(TextBlock):
    """A class used to generate an entire document.
    
    It contains the root element, and optionally a prolog.
    """
    def __init__(self, root, prolog=None):
        root.is_root = True
        self.root = root
        if prolog:
            self.prolog = prolog
        else:
            self.prolog = Prolog()
    
    def __str__(self):
        return ''.join(self.generate(DEFAULT_LAYOUT))
    
    def generate(self, layout=DEFAULT_LAYOUT, scope=BASE_SCOPE, session=None):
        if not isinstance(scope, DocumentScope):
            scope = scope.make_document_scope()
        for line in self.prolog.generate(layout, scope, session):
            yield line
        for line in self.root.generate(layout, scope, session):
            yield line


class Prolog(TextBlock):
    """A TextBlock-compatible holder for all XML lines before the root element.
    """
    def __init__(self, *contents):
        self.contents = contents
    
    def generate(self, layout=SPARTAN_LAYOUT, scope=BASE_SCOPE, session=None):
        for item in self.contents:
            for line in item.generate(layout, scope, session):
                yield line


class Template(SubstitutableTextBlock):
    """XML, from a single line to a whole document, loaded from a file.
    
    The contents from the file are not parsed to test for validity or
    well-formedness. You can make substitutions like in the
    SubstitutableTextBlock on which it is based.
    """
    def __init__(self, file_name, iterator=False):
        self.file_name = file_name
        if iterator:
            contents = self
        else:
            f = (file_name, 'r')
            contents = f.readlines()
            f.close()
        super(Template, self).__init__(self, contents)
    
    def __iter__(self):
        with open(self.file_name, 'r') as f:
            return iter(f)


class Comment(TextBlock):
    """An unparsed comment section in an XML document.
    
    Example:
    >>> print Comment('This is an XML comment.')
    <!--This is an XML comment.-->
    """
    def __init__(self, text):
        text = '<!--%s-->' % text
        super(Comment, self).__init__(text.split('\n'))


class XMLDeclaration(ProcessingInstruction):
    """A line in the prolog to specify xml version, encoding, etc.
    
    Note: the XML declaration is technically not a processing instruction,
    but the difference is not relevant for this use and the format is close
    enough to treat it as one here.
    """
    default_attributes = {'version': '1.0', 'encoding': 'UTF-8'}
    tag_name = 'xml'
    
    def __init__(self, **attributes):
        super(XMLDeclaration, self).__init__(**attributes)


class XMLStylesheet(ProcessingInstruction):
    tag_name = 'xml-stylesheet'
    
    def __init__(self, **attributes):
        super(XMLDeclaration, self).__init__(**attributes)


class DocType(TextBlock):
    """A line in the prolog to provide schema information to parsers.
    
    The XML spec allows the use of internal DOCTYPE code, but this
    implementation only supports external references.
    """
    def __init__(self, root_name, system_id='', public_id=''):
        if system_id and public_id:
            self.line = '<!DOCTYPE %s PUBLIC "%s" "%s">' % (
                root_name, public_id, system_id
                )
        elif system_id:
            self.line = '<!DOCTYPE %s SYSTEM "%s">' % (root_name, system_id)
        else:
            self.line = '<!DOCTYPE %s>' % root_name
    
    def generate(self, layout=SPARTAN_LAYOUT, scope=BASE_SCOPE, session=None):
        yield layout(self.line)


