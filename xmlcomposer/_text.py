"""Ancestor class for nearly all objects in the package.

This used internally, and should generally be avoided by users of
the package.
"""

from _layout import SPARTAN_LAYOUT
from _namespace import BASE_SCOPE

class TextBlock(object):
    """A holder for intermingled character data and markup.
    
    The TextBlock does not guarantee that its contents are well-formed.
    It generally should not be used directly. Instead use one of
    its subclasses.
    """
    
    def __init__(self, lines):
        """Initialize the instance with an iterable holding lines of XML.
        """
        self._contents = lines
    
    def __str__(self):
        return ''.join(self.generate())
    
    def render(self, layout=SPARTAN_LAYOUT, scope=BASE_SCOPE, session=None):
        return ''.join(self.generate(layout, scope, session))
    
    def generate(self, layout=SPARTAN_LAYOUT, scope=BASE_SCOPE, session=None):
        """Generate a section of XML.
        
        The args for this method do nothing and are not used; they are here
        purely for compatibility with more feature-rich subclasses.
        
        This yields the contents of the xml block one line at a time.
        When subclassing TextBlock, this method should almost certainly be
        overridden.
        """
        for line in self._contents:
            yield layout(line)


class SubstitutableTextBlock(TextBlock):
    """An text block with support for text substitutions at generation-time.
    
    Like the TextBlock class, this has more useful subclasses and should
    generally not be used directly
    """
    def __init__(self, lines):
        super(SubstitutableTextBlock, self).__init__(lines)
        self._substitutions = []
    
    def substitute(self, flag, callback, layout=SPARTAN_LAYOUT):
        """Set up a substitution which will occur at generation time.
        
        The flag argument indicates a marker string in the contents
        that is substituted with new contents. The callback arg is a function
        or method that can build the new content. It must accept a single arg
        containing session information, and return a single instance of
        TextBlock or a subclass thereof. The layout arg is a Layout object
        that should be used to lay out the output of the callback function.
        """
        def yield_substituted_lines(contents, scope, session):
            """A generator-function closure for handling substitutions.
            """
            for line in contents:
                parts = line.split(flag)
                new_line = parts.pop(0)
                for part in parts:
                    substitute = callback(session).generate(layout, scope, session)
                    new_line += ''.join(substitute).strip()
                    new_line += part
                yield new_line
        
        self._substitutions.append(yield_substituted_lines)
        return self
    
    def generate(self, layout=SPARTAN_LAYOUT, scope=BASE_SCOPE, session=None):
        """Generate a section of XML.
        """
        contents = self._contents
        for substitution in self._substitutions:
            contents = substitution(contents, scope, session)
        for line in contents:
            yield layout(line)

