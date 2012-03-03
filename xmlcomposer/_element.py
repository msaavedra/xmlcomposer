"""Ancestor classes for XML elements.

These are used internally, and should generally be avoided by users of
the package.
"""

from xml.sax.saxutils import escape, unescape
from types import FunctionType, MethodType

from _text import TextBlock
from _namespace import DocumentScope

MODULE_NAME = __name__

class Element(object):
    """A very abstract ancestor class for representing well-formed XML elements.
    
    This provides a means to its subclasses to represent element attributes
    as if they were items in a dictionary.
    
    Users of this package should never need to make instances of this class,
    or even make subclasses directly from it. The only legitimate use
    is to test to see if an object is an element by using the isinstance()
    and issubclass() built-in functions.
    """
    
    # These both can, but need not, be replaced in subclasses.
    tag_name = None
    namespace = None
    default_attributes = {}
    
    def __init__(self, **attributes):
        """Initialize an element instance.
        
        You can list any attributes of the element as keyword arguments.
        Note that python reserved words cannot be used as attribute
        names (i.e. a "class" attribute), and it may be undesirable to use a
        name that shadows a builtin function (i.e. the "id" attribute). We 
        therefore follow the PEP 8 standard and use a trailing underscores 
        ("class_" or "id_"). The proper name will be substituted automatically.
        """
        self._attributes = self.default_attributes.copy()
        
        # Don't update() the dictionary directly because we process the
        # attributes using our the __setitem__() method.
        for key, value in attributes.items():
            self[key] = value
        
        # Assign a tag name if it isn't defined explicitly by the class.
        # Try to do what's intuitive for anyone writing subclasses.
        # If inheriting from a base class (anything in this package), use the
        # new subclass's name. Otherwise, use the name of the parent class.
        if self.tag_name is None:
            for base in self.__class__.__bases__:
                if not issubclass(base, Element):
                    # The subclass is using multiple inheritance. Skip.
                    continue
                if base.__module__.startswith('xmlcomposer.'):
                    self.tag_name = self.__class__.__name__.lower()
                else:
                    self.tag_name = base.__name__.lower()
                break
    
    def __setitem__(self, key, value):
        if key.endswith('_'):
            key = key[:-1]
        # We should properly handle values whether they are already escaped
        # or not.
        value = unescape(value, {'&quot;': '"'})
        self._attributes[key] = escape(value, {'"': '&quot;'})
    
    def __getitem__(self, key):
        return unescape(self._attributes[key], {'&quot;': '"'})
    
    def __delitem__(self, key):
        del self._attributes[key]
    
    def has_key(self, key):
        return self._attributes.has_key()
    
    def items(self):
        return self._attributes.items()
    
    def format_attributes(self, scope):
        return ' '.join('%s="%s"' % i for i in self.items())
    
    def determine_scope(self, scope):
        if isinstance(scope, DocumentScope):
            if self.namespace:
                scope = scope.merge(self.namespace)
            else:
                scope = scope.make_regular_scope()
            xmlns = ''.join([self.format_xmlns(ns) for ns in scope])
            return xmlns, scope
        elif self.namespace is None or self.namespace in scope:
            return '', scope
        else:
            xmlns = self.format_xmlns(self.namespace)
            scope = scope.merge(self.namespace)
            return xmlns, scope
    
    def format_prefix(self):
        if self.namespace and self.namespace.__prefix__:
            return self.namespace.__prefix__ + ':'
        else:
            return ''
    
    def format_xmlns(self, namespace):
        attr_name = 'xmlns'
        if namespace.__prefix__:
            attr_name = '%s:%s' % (attr_name, namespace.__prefix__)
        return ' %s="%s"' % (attr_name, namespace.__name__)


class ContainerElement(Element):
    """An abstract ancestor class for representing container XML elements.
    
    This builds off of the Element class by providing a means to include
    the child content found between the opening and closing tags of an
    element.
    
    Users of this package should never need to make instances of this class,
    or even make subclasses directly from it. The only legitimate use
    is to test to see if an object is an element by using the isinstance()
    and issubclass() built-in functions.
    """
    
    def __init__(self, *contents, **attributes):
        """Initialize a container Element.
        
        Any contents you wish to put inside this element can be passed as
        positional args. Optionally, instead of element instances, you can
        pass a function or method (must be a real function or method,
        not just a callable object). It must require no arguments, and return
        a single Element or TextBlock subclass instance. The function will not
        be called until document generation-time, so it can be used to create
        truly dynamic content.
        
        Anything positional args other than element instances or
        functions/methods will be converted to a strings and wrapped
        in a StringBlock classes. This is useful to pass plain strings, or
        any object where you have defined its __str__ method to return
        something useful.
        
        You can specify attributes as keyword elements with the same
        functionality and limitations as in the Element class.
        """
        super(ContainerElement, self).__init__(**attributes)
        self._contents = []
        
        # Fill our contents. Don't access the list directly, but use our add()
        # method, which validates and processes them.
        self.add(*contents)
    
    def __call__(self, *contents):
        """An alternate method to add sub-elements.
        
        
        See the __init__ documentation for information on what type of
        contents may be passed here.
        
        Since it returns self, this can be used to make the element
        specification more readable and XML-like, with the attributes listed
        first and sub-elements second. Here is an example (the
        Example class used here being a ContainerElement subclass):
        
        >>> x = Example(id_="test")('This is a test.')
        >>> x.generate()
        <example id="test">This is a test.</example>
        """
        self.add(*contents)
        return self
    
    def add(self, *elements):
        """Add any number of objects to the contents of this element.
        
        See the __init__ documentation for 
        """
        for element in elements:
            if not (
                    isinstance(element, TextBlock) \
                    or isinstance(element, FunctionType) \
                    or isinstance(element, MethodType)
                    ):
                element = TextBlock(str(element).split('\n'))
            self._contents.append(element)
    
    def open_tag(self, xmlns, scope):
        """Return a string representing the opening version of the tag.
        """
        attribs = self.format_attributes(scope)
        if attribs:
            attribs = ' %s' % attribs
        
        return '<%s%s%s%s>' % (
            self.format_prefix(), self.tag_name, xmlns, attribs
            )
    
    def close_tag(self, scope):
        """Return a string representing the closing version of the tag.
        """
        return '</%s%s>' % (self.format_prefix(), self.tag_name)


