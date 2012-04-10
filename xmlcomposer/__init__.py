# Copyright (c) 1999, 2012 Michael Saavedra
# This file may be redistributed under the terms of the GNU LPGL v. 3 or later.
"""xmlcomposer is a python package for easily generating XML and HTML.

It has three design goals: first, to provide a useful and uncomplicated API
that aids separation of logic from content; second, to cover as many of the
features of XML as possible while still retaining simplicity; third, to
perform well enough to be used on high traffic web backends.



Here is an example that uses much of the API, including custom-made elements,
an XML declaration, namespaces specified in several different ways, comments,
etc. It was taken more-or-less verbatim from the XHTML1 documentation at
http://www.w3.org/TR/xhtml1/ .

>>> import xmlcomposer
>>> from xmlcomposer import schema
>>> 
>>> # A namespace imported from a DTD on the web.
>>> books = schema.load('http://will-o-wisp.org/books.dtd', 'urn:loc.gov:books')
>>> 
>>> # A custom element with its own namespace for pedagogical purposes.
>>> class Number(xmlcomposer.Element): pass
>>> isbn = xmlcomposer.Namespace(
...     name='urn:ISBN:0-395-36341-6',
...     prefix='isbn',
...     elements=(Number,)
... )
>>> 
>>> # A namespace loaded from a prebuilt module.
>>> x = xmlcomposer.Namespace(
...     name='http://www.w3.org/1999/xhtml',
...     module='xmlcomposer.formats.xhtml_1_strict'
... )
>>> 
>>> doc = xmlcomposer.Document(
...     xmlcomposer.XMLDeclaration(version='1.0', encoding='UTF-8'),
...     xmlcomposer.Comment('Initially, the default namespace is "books"'),
...     books.Book(
...         books.Title('Cheaper by the Dozen'),
...         isbn.Number('1568491379'),
...         books.Notes(
...             xmlcomposer.Comment('XHTML becomes default namespace'),
...             x.P(
...                 'This is also available ',
...                 x.A(href='http://www.w3.org/')('online'),
...                 '.'
...             )
...         )
...     )
... )
>>> print doc.render(scope=xmlcomposer.DocumentScope(books, isbn))
<?xml encoding="UTF-8" version="1.0"?>
<!--Initially, the default namespace is "books"-->
<book xmlns="urn:loc.gov:books" xmlns:isbn="urn:ISBN:0-395-36341-6">
    <title>Cheaper by the Dozen</title>
    <isbn:number>1568491379</isbn:number>
    <notes>
        <!--XHTML becomes default namespace-->
        <p xmlns="http://www.w3.org/1999/xhtml">This is also available
        <a href="http://www.w3.org/">online</a>.</p>
    </notes>
</book>

See the documentation for the individual classes for more information
and examples. Also, check in the utilities directory for more complex
usage of xmlcomposer.
"""

__all__ = (
    'schema',
    'formats',
    '_document',
    '_element',
    '_layout',
    '_namespace',
    '_processing_instruction',
    '_text',
    'Document',
    'Template',
    'Comment',
    'XMLDeclaration',
    'XMLStylesheet',
    'DocType',
    'Element',
    'ProcessingInstruction',
    'Layout',
    'DEFAULT_LAYOUT',
    'SPARTAN_LAYOUT',
    'MINIMAL_LAYOUT',
    'Namespace',
    'Scope',
    'DocumentScope',
    'PCData',
    'CData',
    'CallBack',
    )

# The submodules with a leading underscore are not meant to be imported
# directly by package users. They are there only to improve code clarity
# and ease of development. We import all relevant objects directly into the
# base package namespace

from _document import Document, Template, DocType

from _element import Element

from _layout import Layout, DEFAULT_LAYOUT, SPARTAN_LAYOUT, MINIMAL_LAYOUT

from _namespace import Namespace, Scope, DocumentScope

from _processing_instruction import ProcessingInstruction, \
    XMLDeclaration, XMLStylesheet

from _text import PCData, CData, CallBack, Comment


def _reload():
    """A routine to facilitate reloading all the objects in this package.
    
    This is an ugly hack, and intended to be used only by package developers.
    """
    import _document
    reload(_document)
    global Document, Template, Comment, DocType
    Document = _document.Document
    Template = _document.Template
    
    import _element
    reload(_element)
    global Element
    Element = _element.Element
    
    import _layout
    reload(_layout)
    global Layout, DEFAULT_LAYOUT, SPARTAN_LAYOUT, MINIMAL_LAYOUT
    Layout = _layout.Layout
    DEFAULT_LAYOUT = _layout.DEFAULT_LAYOUT
    SPARTAN_LAYOUT = _layout.SPARTAN_LAYOUT
    MINIMAL_LAYOUT = _layout.MINIMAL_LAYOUT
    
    import _namespace
    reload(_namespace)
    global Namespace, Scope, DocumentScope
    Namespace = _namespace.Namespace
    Scope = _namespace.Scope
    DocumentScope = _namespace.DocumentScope
    
    import _processing_instruction
    reload(_processing_instruction)
    global ProcessingInstruction, XMLDeclaration, XMLStylesheet
    ProcessingInstruction = _processing_instruction.ProcessingInstruction
    XMLDeclaration = _processing_instruction.XMLDeclaration
    XMLStylesheet = _processing_instruction.XMLStylesheet
    
    import _text
    reload(_text)
    global PCData, CData, CallBack, Comment
    PCData = _text.PCData
    CData = _text.PCData
    CallBack = _text.CallBack
    Comment = _text.Comment

