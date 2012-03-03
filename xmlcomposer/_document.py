#!/usr/bin/env python

"""A set of classes for easily creating XML documents.

"""

from types import FunctionType, MethodType

from _text import TextBlock, SubstitutableTextBlock
from _element import Element, ContainerElement
from _namespace import BASE_SCOPE, DocumentScope
from _layout import DEFAULT_LAYOUT, SPARTAN_LAYOUT, MINIMAL_LAYOUT

class Document(TextBlock):
    
    def __init__(self, root, prolog=None):
        root.is_root = True
        self.root = root
        if prolog:
            self.prolog = prolog
        else:
            prolog = Prolog()
    
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
    
    def __init__(self, *contents):
        self.contents = contents
    
    def generate(self, layout=SPARTAN_LAYOUT, scope=BASE_SCOPE, session=None):
        for item in self.contents:
            for line in item.generate(layout, scope, session):
                yield line


class Template(SubstitutableTextBlock):
    """XML, from a single line to a whole document, loaded from a file.
    """
    def __init__(self, file_name):
        f = open(file_name, 'r')
        lines = f.readlines()
        f.close()
        super(Template, self).__init__(self, lines)


class PCData(SubstitutableTextBlock):
    """A section of parsed character data.
    
    Like SubstitutableTextBlock, but the arg is a single string.
    """
    def __init__(self, text, escape=False):
        if escape:
            text = escape(text)
        super(PCData, self).__init__(text.split('\n'))


class CData(SubstitutableTextBlock):
    
    def generate(self, layout=SPARTAN_LAYOUT, scope=BASE_SCOPE, session=None):
        yield layout('<![CDATA[')
        for line in super(Cdata, self).generate(layout, session, scope):
            yield line
        yield layout(']]>')


class Comment(TextBlock):
    
    def __init__(self, text):
        text = '<!-- %s -->' % text
        super(Comment, self).__init__(text.split('\n'))


class XMLDeclaration(TextBlock):
    
    def __init__(self, **attributes):
        attributes = {'version': '1.0', 'encoding': 'UTF-8'}
        attributes.update(attributes)
        self.line =  '<?xml %s ?>' % \
            ' '.join('%s="%s"' % i for i in attributes.items())
    
    def generate(self, layout=SPARTAN_LAYOUT, scope=BASE_SCOPE, session=None):
        yield layout(self.line)


class DocType(TextBlock):
    
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


# Either finish this or decide not to support it.
class ProcessingInstruction(TextBlock): pass


class EmptyElement(Element, TextBlock):
    """Specifies an element which has no contents and thus no closing tag.
    
    This could be used to make a <br /> or <hr /> tag, for instance. When
    making subclasses, never specify the ' /' in the tag_name. This is
    added automatically.
    """
    def generate(self, layout=DEFAULT_LAYOUT, scope=BASE_SCOPE, session=None):
        xmlns = self.determine_scope(scope)[0]
        yield layout('<%s%s%s %s/>' % (
            self.format_prefix(),
            self.tag_name,
            xmlns,
            self.format_attributes(scope)
            ))


class NestedElement(ContainerElement, TextBlock):
    """This renders an element with contents that are nested on multiple lines.
    
    The opening and closing tags are separated from the contents by 
    new lines. This is useful for many block-level XHTML elements such as <div>.
    """
    def generate(self, layout=DEFAULT_LAYOUT, scope=BASE_SCOPE, session=None):
        xmlns, inner_scope = self.determine_scope(scope)
        yield layout(self.open_tag(xmlns, scope))
        for element in self._contents:
            if type(element) in (FunctionType, MethodType):
                element = element(session)
            for line in element.generate(layout.indent(), inner_scope, session):
                yield line
        yield layout(self.close_tag(scope))


class FormattedElement(ContainerElement, TextBlock):
    """This element's contents are explicitly formatted by the author.
    
    This is useful for elements such as <pre>, <code>, etc. in XHTML.
    """
    def generate(self, layout=DEFAULT_LAYOUT, scope=BASE_SCOPE, session=None):
        xmlns, inner_scope = self.determine_scope(scope)
        yield layout(self.open_tag(xmlns, scope))
        for element in self._contents:
            if type(element) in (FunctionType, MethodType):
                element = element(session)
            for line in element.generate(SPARTAN_LAYOUT, inner_scope, session):
                yield line
        yield layout(self.close_tag(scope))


class FlatElement(ContainerElement, TextBlock):
    """This renders an element whose contents are flat rather than nested.
    
    The opening and closing tags appear inline with the contents. This is
    necessary to maintain proper layout for some tags, such as <td>, and is
    stylistically important for others, such as <span>.
    """
    def generate(self, layout=DEFAULT_LAYOUT, scope=BASE_SCOPE, session=None):
        xmlns, inner_scope = self.determine_scope(scope)
        parts = []
        last = None
        for element in self._contents:
            if type(element) in (FunctionType, MethodType):
                element = element(session)
            part = ''.join(
                element.generate(MINIMAL_LAYOUT, inner_scope, session)
                )
            parts.append(part)
            last = element
        line = '%s%s%s' % (
            self.open_tag(xmlns, scope), ''.join(parts), self.close_tag(scope)
            )
        yield layout(line, wrap=True)


