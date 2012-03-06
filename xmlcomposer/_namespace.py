
from types import ModuleType

class Namespace(ModuleType):
    """A module-like object representing an XML namespace.
    """
    def __init__(self, name='', prefix='', module=None):
        super(Namespace, self).__init__(name)
        super(Namespace, self).__setattr__('__prefix__', prefix)
        del self.__doc__
        if module:
            if isinstance(module, str):
                module = __import__(module, fromlist=[module])
            for item in vars(module).itervalues():
                if hasattr(item, 'tag_name'):
                    self.__setattr__(item.__name__, item)
            super(Namespace, self).__setattr__(
                '__name__', module.__namespace__
                )
        
        if not self.__name__:
            raise Exception('Name not provided as argument or by module.')
    
    def __repr__(self):
        ret_val = '<Namespace'
        if self.__prefix__:
            ret_val += ' "%s"' % self.__prefix__
        ret_val += ' "%s">' % self.__name__
        return ret_val
    
    def __setattr__(self, name, value):
        setattr(value, 'namespace', self)
        super(Namespace, self).__setattr__(name, value)
    
    def __iter__(self):
        for obj in vars(self).itervalues():
            if isinstance(obj, type) and hasattr(obj, 'tag_name'):
                yield obj
    
    def __contains__(self, element):
        return (element in iter(self))
    
    def __eq__(self, other):
        return (self.__name__ == other.__name__)


class Scope(frozenset):
    """The collection of namespaces that are valid in an element's context.
    """
    def __new__(cls, *args):
        return super(Scope, cls).__new__(cls, args)
    
    def merge(self, *args):
        """Return a new scope merging with additional namespaces
        """ 
        return self.union(args)
    
    def make_document_scope(self):
        return DocumentScope(*tuple(self))

class DocumentScope(Scope):
    
    def merge(self, *args):
        """Return a new scope merging with additional namespaces.
        
        Note that this creates a regular Scope, not a DocumentScope.
        """
        return Scope(*tuple(self.union(args)))
    
    def make_regular_scope(self):
        return Scope(*tuple(self))
        

# An empty scope to use as a default.
BASE_SCOPE = Scope()

