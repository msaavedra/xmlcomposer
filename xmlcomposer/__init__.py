# Copyright (c) 1999, 2012 Michael Saavedra
# This file may be redistributed under the terms of the GNU LPGL v. 3 or later.

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

