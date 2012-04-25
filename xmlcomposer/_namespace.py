# Copyright (c) 1999, 2012 Michael Saavedra
# This file may be redistributed under the terms of the GNU LPGL v. 3 or later.

from types import ModuleType

class Namespace(ModuleType):
    """A module-like object representing an XML namespace.
    
    Example:
    >>> xhtml = Namespace(module='xmlcomposer.formats.xhtml_1_strict')
    >>> print xhtml
    <Namespace "http://www.w3.org/1999/xhtml">
    
    Membership can be tested:
    >>> from xmlcomposer.formats import html5
    >>> html = Namespace(module=html5)
    >>> html5.Title in html
    True
    
    One can iterate over the Elements in the namespace:
    >>> from xmlcomposer import Element
    >>> class Author(Element): pass
    >>> class Title(Element): pass
    >>> n = Namespace(elements=(Author, Title))
    >>> print sorted([element.__name__ for element in n])
    ['Author', 'Title']
    """
    def __init__(self, name='', prefix='', module=None, elements=()):
        """Create a new namespace instance
        
        The name arg is the globally unique string (used in an xmlns attribute)
        that identifies the namespace. If not specified, no namespace
        declaration will be made in generated XML.
        
        The prefix arg, if supplied, will cause each element in the namespace
        to be preceded by the supplied string when generated in the format
        "prefix:element".
        
        The module arg allows one to add the contents of a module to the
        namespace. The value may be a module instance, or a string (in which
        case the module is imported automatically). Only subclasses of Element
        are added to the namespace. If the __namespace__ name is defined in
        the module, it will be used to set the name attribute of the new
        Namespace instance.
        
        The elements arg is an alternate method of adding elements to the
        namespace. It should be a sequence of Element subclasses.
        """
        super(Namespace, self).__init__(name)
        super(Namespace, self).__setattr__('__prefix__', prefix)
        del self.__doc__
        
        if module:
            if isinstance(module, str):
                module = __import__(module, fromlist=[module])
            for item in vars(module).itervalues():
                if hasattr(item, 'tag_name'):
                    self.__setattr__(item.__name__, item)
            if hasattr(module, '__namespace__'):
                super(Namespace, self).__setattr__(
                    '__name__', module.__namespace__
                    )
        
        for element in elements:
            setattr(self, element.__name__, element)
    
    def __repr__(self):
        ret_val = '<Namespace'
        if self.__prefix__:
            ret_val += ' "%s"' % self.__prefix__
        if self.__name__:
            ret_val += ' "%s"' % self.__name__
        ret_val += '>'
        return ret_val
    
    def __setattr__(self, name, value):
        setattr(value, 'namespace', self)
        super(Namespace, self).__setattr__(name, value)
    
    def __iter__(self):
        for obj in vars(self).itervalues():
            if isinstance(obj, type) and hasattr(obj, 'tag_name'):
                yield obj
    
    def __contains__(self, element):
        if isinstance(element, str):
            print [e for e in iter(self)]
            return element in (e.__class__.__name__ for e in iter(self))
        return (element in iter(self))
    
    def __eq__(self, other):
        return (self.__name__ == other.__name__)


class Scope(frozenset):
    """The collection of namespaces that are valid in an element's context.
    
    Instances of this class are used solely as arguments to the TextBlock
    generate() method and its kin, where lack of side-effects is a design goal.
    Therefore, Scope instances are designed to be immutable, though a clever
    but unwise programmer may be able to circumvent this.
    """
    def __new__(cls, *args):
        return super(Scope, cls).__new__(cls, args)
    
    def __str__(self):
        return "%s('%s')" % (
            self.__class__.__name__,
            "', '".join([n.__name__ for n in self])
            )
    
    def __repr__(self):
        return str(self)
    
    def merge(self, *args):
        """Return a new scope with additional namespaces
        """ 
        return self.union(args)
    
    def make_document_scope(self):
        return DocumentScope(*self)


class DocumentScope(Scope):
    """An optional specification of the namespaces for an entire document.
    
    Instances of this class are used solely as arguments to the Document
    generate() method and its kin, where lack of side-effects is a design goal.
    Therefore, DocumentScope instances are designed to be immutable, though a
    clever but unwise programmer may be able to circumvent this.
    """
    def merge(self, *args):
        """Return a new scope with additional namespaces.
        
        Note that this creates a regular Scope, not a DocumentScope.
        """
        return Scope(*self.union(args))
    
    def make_regular_scope(self):
        return Scope(*self)
        

# An empty scope to use as a default.
BASE_SCOPE = Scope()

