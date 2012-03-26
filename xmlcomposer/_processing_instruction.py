
from _element import Element
from _namespace import DocumentScope, BASE_SCOPE
from _layout import DEFAULT_LAYOUT, SPARTAN_LAYOUT, MINIMAL_LAYOUT


class ProcessingInstruction(Element):
    """A class for generating XML processing instructions.
    
    It is a subclass of Element (although a processing instruction is of
    course not an Element, they are similar enough to use mostly the same
    code).
    
    Example:
    >>> class Word(ProcessingInstruction): pass
    >>> print Word(document='test.doc')
    <?word document="test.doc"?>
    """
    preformatted = True
    
    def determine_tag_name(self):
        """Get a tag name for the ProcessingInstruction instance.
        
        See the Element class for a full discussion of the goals of this
        method.
        """
        if self.__class__.tag_name:
            return self.__class__.tag_name
        else:
            for base in self.__class__.__bases__:
                if not issubclass(base, Element):
                    # The subclass is using multiple inheritance. Skip.
                    continue
                if base is ProcessingInstruction:
                    return self.__class__.__name__.lower()
                else:
                    return base.__name__.lower()
    
    def open_tag(self, xmlns):
        attribs = self.format_attributes()
        if attribs:
            attribs = ' %s' % attribs
        
        return '<?%s%s' % (self.tag_name, attribs)
    
    def close_tag(self):
        """Return a string representing the closing version of the tag.
        """
        return '?>'
    
    def generate(self, layout=DEFAULT_LAYOUT, scope=BASE_SCOPE, session=None):
        return self._generate_preformatted(layout, scope, session)


class XMLDeclaration(ProcessingInstruction):
    """A line in the document prolog to specify xml version, encoding, etc.
    
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


