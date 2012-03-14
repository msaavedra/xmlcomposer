"""An ancestor class for XML elements.
"""

from xml.sax.saxutils import escape, unescape

from _text import TextBlock, PCData, CallBack
from _namespace import DocumentScope, BASE_SCOPE
from _layout import DEFAULT_LAYOUT, SPARTAN_LAYOUT, MINIMAL_LAYOUT


class Element(TextBlock):
    """An ancestor class for representing well-formed XML elements.
    
    This provides a means to add child content, and to represent element
    attributes as if they were items in a dictionary.
    
    The Element class is designed to be subclassed; users of this package
    should rarely need to make instances of this class. One common legitimate
    use is to test to see if an object is an element by using the isinstance()
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
        
        Here is the most basic example:
        
        >>> import xmlcomposer
        >>> e = Element('This is a test.', id='most_basic')
        >>> e.tag_name = 'example'
        >>> print e
        <example id="most_basic">This is a test.</example>
        
        This is not the most convenient usage, though. More typical usage
        is like this:
        
        >>> class Example(xmlcomposer.Element): pass
        >>> class Section(xmlcomposer.Element): pass
        >>> e = Example(id='typical_usage')(
        ...     Section('This is the first section in the example.'),
        ...     Section('This is a second.')
        ... )
        >>> print e
        <example id="typical_usage">
        	<section>This is the first section in the example.</section>
        	<section>This is a second.</section>
        </example>
        
        The Element class tries to do the most convenient thing when
        automatically setting tag_name in subclasses. If you are inheriting
        directly from Element, it will set the tag_name to a lowercase version
        of the subclass name. All grandchild, great-grandchild, and further
        descendent classes will keep the child tag_name. If this is not what
        you want, you can always set tag_name explicitly.
        
        You can also explicitly set default_attributes.
        
        >>> class Example(xmlcomposer.Element)
        >>> class Section(xmlcomposer.Element): pass
        >>> class MarkedSection(Section):
        ...     default_attributes = {'class': 'marked'}
        >>> class FinalSection(Section):
        ...     tag_name = 'finalSection' # needed for camelCase
        >>> e = Example(id='typical_usage')(
        ...     Section('This is the first section in the example.'),
        ...     MarkedSection('This section is marked by default'),
        ...     FinalSection('This is the last section.')
        ... )
        >>> print e
        <example id="typical_usage">
        	<section>This is the first section in the example.</section>
        	<section class="marked">This section is marked by default</section>
        	<finalSection>This is the last section.</finalSection>
        </example>
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
                if base in (Element, ProcessingInstruction) :
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
        """Add an attribute to the element.
        """
        if key.endswith('_'):
            key = key[:-1]
        self._attributes[key] = self.escape(value, {'"': '&quot;'})
    
    def __getitem__(self, key):
        """Get the value of an attribute.
        """
        return self.unescape(self._attributes[key], {'&quot;': '"'})
    
    def __delitem__(self, key):
        """Delete an attribute.
        """
        del self._attributes[key]
    
    def __call__(self, *contents):
        """An alternate method to add sub-elements.
        
        See the __init__() documentation for information on what type of
        contents are acceptable in Element instances.
        
        Since this method returns self, this can be used to make the element
        specification more readable and XML-like, with the attributes listed
        first and sub-elements second. Here is an example (the
        Example class used here being a ContainerElement subclass):
        
        >>> x = Example(id="test")('This is a test.')
        >>> print x
        <example id="test">This is a test.</example>
        """
        self.add(*contents)
        return self
    
    def add(self, *contents):
        """Add any number of objects to the contents of this element.
        
        See the __init__() documentation for information on what type of
        contents are acceptable in Element instances.
        """
        for item in contents:
            if not isinstance(item, TextBlock):
                item = PCData(str(item))
            self._contents.append(item)
            self._content_types.add(self.determine_content_type(item))
    
    def has_key(self, key):
        """Returns True if the attribute has been set, False otherwise.
        """
        return self._attributes.has_key()
    
    def items(self):
        """Return key, value pairs representing all the element's attributes.
        """
        return self._attributes.items()
    
    def format_attributes(self, scope):
        """An internal method to build attributes in proper XML format.
        """
        return ' '.join('%s="%s"' % i for i in self.items())
    
    def determine_scope(self, scope):
        """An internal method to figure out the namespace scoping context.
        
        This determines if the current element's namespace is within
        the scope. If not, it returns an xmlns value that needs to be
        specified for the element. If so, an empty string is returned.
        
        It also figures out what the scope will be for this element's
        children, and returns that as well.
        """
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
        """An internal method to get the prefix, if any, to use when generating.
        """
        if self.namespace and self.namespace.__prefix__:
            return self.namespace.__prefix__ + ':'
        else:
            return ''
    
    def format_xmlns(self, namespace):
        """An internal method to get a specially-handled xmlns attribute.
        """
        if not namespace.__name__:
            return ''
        attr_name = 'xmlns'
        if namespace.__prefix__:
            attr_name = '%s:%s' % (attr_name, namespace.__prefix__)
        return ' %s="%s"' % (attr_name, namespace.__name__)
    
    def open_tag(self, xmlns, scope):
        """An internal method to get the opening version of the tag.
        """
        attribs = self.format_attributes(scope)
        if attribs:
            attribs = ' %s' % attribs
        
        return '<%s%s%s%s>' % (
            self.format_prefix(), self.tag_name, xmlns, attribs
            )
    
    def close_tag(self, scope):
        """An internal method to get the closing version of the tag.
        """
        return '</%s%s>' % (self.format_prefix(), self.tag_name)
    
    def determine_content_type(self, item):
        """An internal method to get a description of an arbitrary item.
        """
        if item.preformatted:
            return 'preformatted'
        elif isinstance(item, Element):
            return 'element'
        elif isinstance(item, PCData):
            return 'pcdata'
        elif isinstance(item, CallBack):
            return self.determine_content_type(item.return_type)
        else:
            return('indeterminate')
    
    def generate(self, layout=DEFAULT_LAYOUT, scope=BASE_SCOPE, session=None):
        """Return a generator that produces XML line-by-line for the element.
        """
        if not self._content_types:
            return self._generate_empty(layout, scope, session)
        elif self.preformatted or 'preformatted' in self._content_types:
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


class ProcessingInstruction(Element):
    """
    """
    preformatted = True
    
    def open_tag(self, xmlns, scope):
        attribs = self.format_attributes(scope)
        if attribs:
            attribs = ' %s' % attribs
        
        return '<?%s%s' % (self.tag_name, attribs)
    
    def close_tag(self, scope):
        """Return a string representing the closing version of the tag.
        """
        return '?>'

