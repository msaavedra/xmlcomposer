
import xmlcomposer

__namespace__ = 'http://www.w3.org/1999/xhtml'

class A(xmlcomposer.Element): pass

class Abbr(xmlcomposer.Element): pass

class Acronym(xmlcomposer.Element): pass

class Address(xmlcomposer.Element): pass

class Area(xmlcomposer.Element): pass

class B(xmlcomposer.Element): pass

class Base(xmlcomposer.Element): pass

class Bdo(xmlcomposer.Element): pass

class Big(xmlcomposer.Element): pass

class Blockquote(xmlcomposer.Element): pass

class Body(xmlcomposer.Element): pass

class Br(xmlcomposer.Element): pass

class Button(xmlcomposer.Element): pass

class Caption(xmlcomposer.Element): pass

class Cite(xmlcomposer.Element): pass

class Code(xmlcomposer.Element):
    preformatted = True

class Col(xmlcomposer.Element): pass

class Colgroup(xmlcomposer.Element): pass

class Dd(xmlcomposer.Element): pass

class Del(xmlcomposer.Element): pass

class Dfn(xmlcomposer.Element): pass

class Div(xmlcomposer.Element): pass

class Dl(xmlcomposer.Element): pass

class Dt(xmlcomposer.Element): pass

class Em(xmlcomposer.Element): pass

class Fieldset(xmlcomposer.Element): pass

class Form(xmlcomposer.Element): pass

class H1(xmlcomposer.Element): pass

class H2(xmlcomposer.Element): pass

class H3(xmlcomposer.Element): pass

class H4(xmlcomposer.Element): pass

class H5(xmlcomposer.Element): pass

class H6(xmlcomposer.Element): pass

class Head(xmlcomposer.Element): pass

class Hr(xmlcomposer.Element): pass

class Html(xmlcomposer.Element):
    default_attributes = {
        'xml:lang': 'en',
        'lang': 'en'
        }

class I(xmlcomposer.Element): pass

class Img(xmlcomposer.Element): pass

class Input(xmlcomposer.Element): pass

class Ins(xmlcomposer.Element): pass

class Kbd(xmlcomposer.Element): pass

class Label(xmlcomposer.Element): pass

class Legend(xmlcomposer.Element): pass

class Li(xmlcomposer.Element): pass

class Link(xmlcomposer.Element): pass

class Map(xmlcomposer.Element): pass

class Meta(xmlcomposer.Element): pass

class Noscript(xmlcomposer.Element): pass

class Object(xmlcomposer.Element): pass

class Ol(xmlcomposer.Element): pass

class Optgroup(xmlcomposer.Element): pass

class Option(xmlcomposer.Element): pass

class P(xmlcomposer.Element): pass

class Param(xmlcomposer.Element): pass

class Pre(xmlcomposer.Element):
    preformatted = True
    
class Q(xmlcomposer.Element): pass

class Samp(xmlcomposer.Element): pass

class Script(xmlcomposer.Element):
    preformatted = True

class Select(xmlcomposer.Element): pass

class Small(xmlcomposer.Element): pass

class Span(xmlcomposer.Element): pass

class Strong(xmlcomposer.Element): pass

class Style(xmlcomposer.Element):
    preformatted = True

class Sub(xmlcomposer.Element): pass

class Sup(xmlcomposer.Element): pass

class Table(xmlcomposer.Element): pass

class Tbody(xmlcomposer.Element): pass

class Td(xmlcomposer.Element): pass

class Textarea(xmlcomposer.Element): pass

class Tfoot(xmlcomposer.Element): pass

class Th(xmlcomposer.Element): pass

class Thead(xmlcomposer.Element): pass

class Title(xmlcomposer.Element): pass

class Tr(xmlcomposer.Element): pass

class Tt(xmlcomposer.Element):
    preformatted = True

class Ul(xmlcomposer.Element): pass

class Var(xmlcomposer.Element): pass

