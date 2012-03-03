
import xmlcomposer

__namespace__ = 'http://www.w3.org/1999/xhtml'

class A(xmlcomposer.FlatElement): pass

class Abbr(xmlcomposer.FlatElement): pass

class Acronym(xmlcomposer.FlatElement): pass

class Address(xmlcomposer.FlatElement): pass

class Area(xmlcomposer.EmptyElement): pass

class B(xmlcomposer.FlatElement): pass

class Base(xmlcomposer.EmptyElement): pass

class Bdo(xmlcomposer.FlatElement): pass

class Big(xmlcomposer.FlatElement): pass

class Blockquote(xmlcomposer.FlatElement): pass

class Body(xmlcomposer.NestedElement): pass

class Br(xmlcomposer.EmptyElement): pass

class Button(xmlcomposer.FlatElement): pass

class Caption(xmlcomposer.FlatElement): pass

class Cite(xmlcomposer.FlatElement): pass

class Code(xmlcomposer.FormattedElement): pass

class Col(xmlcomposer.FlatElement): pass

class Colgroup(xmlcomposer.NestedElement): pass

class Dd(xmlcomposer.FlatElement): pass

class Del(xmlcomposer.FlatElement): pass

class Dfn(xmlcomposer.FlatElement): pass

class Div(xmlcomposer.NestedElement): pass

class Dl(xmlcomposer.NestedElement): pass

class Dt(xmlcomposer.FlatElement): pass

class Em(xmlcomposer.FlatElement): pass

class Fieldset(xmlcomposer.NestedElement): pass

class Form(xmlcomposer.NestedElement): pass

class H1(xmlcomposer.FlatElement): pass

class H2(xmlcomposer.FlatElement): pass

class H3(xmlcomposer.FlatElement): pass

class H4(xmlcomposer.FlatElement): pass

class H5(xmlcomposer.FlatElement): pass

class H6(xmlcomposer.FlatElement): pass

class Head(xmlcomposer.NestedElement): pass

class Hr(xmlcomposer.EmptyElement): pass

class Html(xmlcomposer.NestedElement):
    default_attributes = {
        'xml:lang': 'en',
        'lang': 'en'
        }

class I(xmlcomposer.FlatElement): pass

class Img(xmlcomposer.EmptyElement): pass

class Input(xmlcomposer.EmptyElement): pass

class Ins(xmlcomposer.FlatElement): pass

class Kbd(xmlcomposer.FlatElement): pass

class Label(xmlcomposer.NestedElement): pass

class Legend(xmlcomposer.FlatElement): pass

class Li(xmlcomposer.FlatElement): pass

class Link(xmlcomposer.EmptyElement): pass

class Map(xmlcomposer.NestedElement): pass

class Meta(xmlcomposer.EmptyElement): pass

class Noscript(xmlcomposer.NestedElement): pass

class Object(xmlcomposer.NestedElement): pass

class Ol(xmlcomposer.NestedElement): pass

class Optgroup(xmlcomposer.NestedElement): pass

class Option(xmlcomposer.FlatElement): pass

class P(xmlcomposer.FlatElement): pass

class Param(xmlcomposer.EmptyElement): pass

class Pre(xmlcomposer.FormattedElement): pass
    
class Q(xmlcomposer.FlatElement): pass

class Samp(xmlcomposer.FlatElement): pass

class Script(xmlcomposer.FormattedElement): pass

class Select(xmlcomposer.NestedElement): pass

class Small(xmlcomposer.FlatElement): pass

class Span(xmlcomposer.FlatElement): pass

class Strong(xmlcomposer.FlatElement): pass

class Style(xmlcomposer.FormattedElement): pass

class Sub(xmlcomposer.FlatElement): pass

class Sup(xmlcomposer.FlatElement): pass

class Table(xmlcomposer.NestedElement): pass

class Tbody(xmlcomposer.NestedElement): pass

class Td(xmlcomposer.FlatElement): pass

class Textarea(xmlcomposer.FlatElement): pass

class Tfoot(xmlcomposer.NestedElement): pass

class Th(xmlcomposer.FlatElement): pass

class Thead(xmlcomposer.NestedElement): pass

class Title(xmlcomposer.FlatElement): pass

class Tr(xmlcomposer.NestedElement): pass

class Tt(xmlcomposer.FormattedElement): pass

class Ul(xmlcomposer.NestedElement): pass

class Var(xmlcomposer.FlatElement): pass

