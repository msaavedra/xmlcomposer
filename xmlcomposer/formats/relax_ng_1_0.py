
import xmlcomposer

__namespace__='http://relaxng.org/ns/structure/1.0'

class AnyName(xmlcomposer.Element):
    tag_name = 'anyName'

class Attribute(xmlcomposer.Element):
    pass

class Choice(xmlcomposer.Element):
    pass

class Data(xmlcomposer.Element):
    pass

class Define(xmlcomposer.Element):
    pass

class Div(xmlcomposer.Element):
    pass

class Element(xmlcomposer.Element):
    pass

class Empty(xmlcomposer.Element):
    pass

class Except(xmlcomposer.Element):
    pass

class ExternalRef(xmlcomposer.Element):
    tag_name = 'externalRef'

class Grammar(xmlcomposer.Element):
    pass

class Group(xmlcomposer.Element):
    pass

class Include(xmlcomposer.Element):
    pass

class Interleave(xmlcomposer.Element):
    pass

class List(xmlcomposer.Element):
    pass

class Mixed(xmlcomposer.Element):
    pass

class Name(xmlcomposer.Element):
    pass

class NotAllowed(xmlcomposer.Element):
    tag_name = 'notAllowed'

class NsName(xmlcomposer.Element):
    tag_name = 'nsName'

class OneOrMore(xmlcomposer.Element):
    tag_name = 'oneOrMore'

class Optional(xmlcomposer.Element):
    pass

class Param(xmlcomposer.Element):
    pass

class ParentRef(xmlcomposer.Element):
    tag_name = 'parentRef'

class Ref(xmlcomposer.Element):
    pass

class Start(xmlcomposer.Element):
    pass

class Text(xmlcomposer.Element):
    pass

class Value(xmlcomposer.Element):
    pass

class ZeroOrMore(xmlcomposer.Element):
    tag_name = 'zeroOrMore'

