"""Ancestor classes for XML elements.

These are used internally, and should generally be avoided by users of
the package.
"""

from xml.sax.saxutils import escape, unescape

from _text import TextBlock, PCData, PreformattedPCData, CallBack
from _namespace import DocumentScope, BASE_SCOPE
from _layout import DEFAULT_LAYOUT, SPARTAN_LAYOUT, MINIMAL_LAYOUT



class Element(TextBlock):
    """An ancestor class for representing well-formed XML elements.
    
    This provides a means to its subclasses to to add child content, and
    to represent element attributes as if they were items in a dictionary.
    
    Users of this package should rarely need to make instances of this class,
    or even make subclasses directly from it. The only legitimate use
    is to test to see if an object is an element by using the isinstance()
    and issubclass() built-in functions.
    """
    
    # These can, but need not, be replaced in subclasses.
    tag_name = None
    namespace = None
    default_attributes = {}
    
    def __init__(self, *contents, **attributes):
        """Initialize an element instance.
        
        Any contents you wish to put inside this element can be passed as
        positional args. If such args are not descended from TextBlock,
        they will be converted to a strings, then wrapped in a PCData
        instance. This is useful to pass plain strings, or any object where
        you have defined its __str__ method to return something useful.
        
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
        # If inheriting from the Element base class, use the
        # new subclass's name. Otherwise, use the name of the parent class.
        if self.tag_name is None:
            for base in self.__class__.__bases__:
                if not issubclass(base, Element):
                    # The subclass is using multiple inheritance. Skip.
                    continue
                if base is Element:
                    self.tag_name = self.__class__.__name__.lower()
                else:
                    self.tag_name = base.__name__.lower()
                break
        
        self._contents = []
        self._content_types = set()
        
        # Fill our contents. Don't access the list directly, but use our add()
        # method, which validates and processes them.
        self.add(*contents)
    
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
    
    def __call__(self, *contents):
        """An alternate method to add sub-elements.
        
        
        See the __init__ documentation for information on what type of
        contents may be passed here.
        
        Since it returns self, this can be used to make the element
        specification more readable and XML-like, with the attributes listed
        first and sub-elements second. Here is an example (the
        Example class used here being a ContainerElement subclass):
        
        >>> x = Example(id="test")('This is a test.')
        >>> print x
        <example id="test">This is a test.</example>
        """
        self.add(*contents)
        return self
    
    def add(self, *elements):
        """Add any number of objects to the contents of this element.
        
        See the __init__ documentation for 
        """
        for element in elements:
            if not isinstance(element, TextBlock):
                element = PCData(str(element))
            self._contents.append(element)
            self._content_types.add(self.determine_type(element))
    
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
    
    def determine_type(self, element):
        if isinstance(element, Element):
            return 'element'
        elif isinstance(element, PreformattedPCData):
            return 'preformatted'
        elif isinstance(element, PCData):
            return 'pcdata'
        elif isinstance(element, CallBack):
            return self.determine_type(element.return_type)
        else:
            return('indeterminate')
    
    def generate(self, layout=DEFAULT_LAYOUT, scope=BASE_SCOPE, session=None):
        if hasattr(self, 'preformatted'):
            return self._generate_preformatted(layout, scope, session)
        if not self._content_types:
            return self._generate_empty(layout, scope, session)
        elif 'preformatted' in self._content_types:
            return self._generate_preformatted(layout, scope, session)
        elif 'pcdata' in self._content_types \
                and 'indeterminate' not in self._content_types:
            return self._generate_flat(layout, scope, session)
        else:
            return self._generate_nested(layout, scope, session)
    
    def _generate_empty(self, layout, scope, session):
        xmlns = self.determine_scope(scope)[0]
        yield layout('<%s%s%s %s/>' % (
            self.format_prefix(),
            self.tag_name,
            xmlns,
            self.format_attributes(scope)
            ))
    
    def _generate_preformatted(self, layout, scope, session):
        xmlns, inner_scope = self.determine_scope(scope)
        yield layout(self.open_tag(xmlns, scope)).rstrip()
        for element in self._contents:
            if isinstance(element, CallBack):
                element = element.func(session)
            for line in element.generate(SPARTAN_LAYOUT, inner_scope, session):
                yield line.rstrip()
        yield layout(self.close_tag(scope)).lstrip()
    
    def _generate_flat(self, layout, scope, session):
        xmlns, inner_scope = self.determine_scope(scope)
        parts = []
        last = None
        for element in self._contents:
            if isinstance(element, CallBack):
                element = element.func(session)
            part = ''.join(
                element.generate(MINIMAL_LAYOUT, inner_scope, session)
                )
            parts.append(part)
            last = element
        line = '%s%s%s' % (
            self.open_tag(xmlns, scope), ''.join(parts), self.close_tag(scope)
            )
        yield layout(line, wrap=True)
    
    def _generate_nested(self, layout, scope, session):
        xmlns, inner_scope = self.determine_scope(scope)
        yield layout(self.open_tag(xmlns, scope))
        for element in self._contents:
            if isinstance(element, CallBack):
                element = element.func(session)
            for line in element.generate(layout.indent(), inner_scope, session):
                yield line
        yield layout(self.close_tag(scope))

