
__all__ = (
    'schema',
    'formats',
    '_document',
    '_element',
    '_layout',
    '_namespace',
    '_text',
    'Document',
    'Template',
    'Comment',
    'XMLDeclaration',
    'XMLStylesheet',
    'DocType',
    'Prolog',
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

from _document import Document, Template, Comment, \
    XMLDeclaration, XMLStylesheet, DocType, Prolog

from _element import Element, ProcessingInstruction

from _layout import Layout, DEFAULT_LAYOUT, SPARTAN_LAYOUT, MINIMAL_LAYOUT

from _namespace import Namespace, Scope, DocumentScope

from _text import PCData, CData, CallBack


def _reload():
    """A routine to facilitate reloading all the objects in this package.
    
    This is an ugly hack, and intended to be used only by package developers.
    """
    import _document
    reload(_document)
    global Document, Template, Comment, XMLDeclaration, XMLStylesheet, \
        DocType, Prolog
    Document = _document.Document
    Template = _document.Template
    Comment = _document.Comment
    XMLDeclaration = _document.XMLDeclaration
    XMLStylesheet = _document.XMLStylesheet
    
    import _element
    reload(_element)
    global Element, ProcessingInstruction
    Element = _element.Element
    ProcessingInstruction = _element.ProcessingInstruction
    
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
    
    import _text
    reload(_text)
    global PCData, CData, CallBack
    PCData = _text.PCData
    CData = _text.PCData
    CallBack = _text.CallBack

