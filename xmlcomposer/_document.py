# Copyright (c) 1999, 2012 Michael Saavedra
# This file may be redistributed under the terms of the GNU LPGL v. 3 or later.

"""A set of classes for easily creating XML documents.
"""

from _text import TextBlock, SubstitutableTextBlock
from _namespace import BASE_SCOPE, DocumentScope
from _layout import DEFAULT_LAYOUT, SPARTAN_LAYOUT, MINIMAL_LAYOUT

class Document(TextBlock):
    """A class used to generate an entire document.
    """
    def __init__(self, *contents):
        """Initialize a Document instance, passing contents to it.
        
        To make a well-formed XML document, it must contain exactly one Element
        instance, though some forms of HTML don't need to have one root element
        that contains all other elements.
        
        Optionally, it can also contain DocType, ProcessingInstruction and
        Comment instances that are not enclosed within the root element.
        
        Example:
        
        >>> import xmlcomposer
        >>> from xmlcomposer.formats.html5 import Html
        >>>
        >>> print Document(
        ...     xmlcomposer.DocType('html'),
        ...     Html('Hello World')
        ... )
        <!DOCTYPE html>
        <html>Hello World</html>
        """
        self.contents = contents
    
    def __str__(self):
        return ''.join(self.generate(DEFAULT_LAYOUT))
    
    def render(self, layout=DEFAULT_LAYOUT, scope=BASE_SCOPE, session=None):
        """Return the generated element as a string.
        
        The arguments are identical to the generate() method.
        """
        return super(Document, self).render(layout, scope, session)
    
    def generate(self, layout=DEFAULT_LAYOUT, scope=BASE_SCOPE, session=None):
        if not isinstance(scope, DocumentScope):
            scope = scope.make_document_scope()
        for item in self.contents:
            for line in item.generate(layout, scope, session):
                yield line


class Template(SubstitutableTextBlock):
    """XML, from a single line to a whole document, loaded from a file.
    
    The contents from the file are not parsed to test for validity or
    well-formedness. You can make substitutions like in the
    SubstitutableTextBlock on which it is based.
    
    Example:
    
    >>> # first we need to create a test template file.
    >>> import os, tempfile
    >>> fd, file_name = tempfile.mkstemp()
    >>> f = os.fdopen(fd, 'w')
    >>> f.write('<p>This is a template test!</p>')
    >>> f.close()
    >>> 
    >>> t = Template(file_name)
    >>> os.remove(file_name)
    >>> print t
    <p>This is a template test!</p>
    """
    def __init__(self, file_name, iterator=False):
        self.file_name = file_name
        if iterator:
            contents = self
        else:
            f = open(file_name, 'r')
            contents = f.readlines()
            f.close()
        super(Template, self).__init__(contents)
    
    def __iter__(self):
        with open(self.file_name, 'r') as f:
            return iter(f)


class DocType(TextBlock):
    """An XML structure to provide schema information to parsers.
    
    The XML spec allows the use of internal DOCTYPE code, but this
    implementation only supports external references.
    
    Example:
    >>> print DocType('example', 'example.dtd')
    <!DOCTYPE example SYSTEM "example.dtd">
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


