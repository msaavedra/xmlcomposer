"""Ancestor class for nearly all objects in the package.

This used internally, and should generally be avoided by users of
the package.
"""

import re

from _layout import SPARTAN_LAYOUT
from _namespace import BASE_SCOPE

class TextBlock(object):
    """A holder for intermingled character data and markup.
    
    The TextBlock does not guarantee that its contents are well-formed.
    It generally should not be used directly. Instead use one of
    its subclasses.
    """
    
    # If preformatted, line break, spaces and tabs will be preserved.
    preformatted = False
    
    # A regular expression for finding unescaped non-entity ampersands.
    _amp_regex = re.compile(r'&(?P<suffix>([^;&\s]{0,32}(?=(&|\s|\Z))))')
    
    def __init__(self, lines):
        """Initialize the instance with an iterable holding lines of XML.
        """
        self._contents = lines
    
    def __str__(self):
        return ''.join(self.generate()).rstrip()
    
    @classmethod
    def escape(cls, text, substitutions=None):
        if substitutions:
            for old, new in substitutions.items():
                text = text.replace(old, new)
        text = cls._amp_regex.sub(cls.__replace_on_match, text)
        text = text.replace('<', '&lt;')
        return text
    
    @classmethod
    def __replace_on_match(self, match):
        return '&amp;'+ match.group('suffix')
    
    @classmethod
    def unescape(cls, text, substitutions=None):
        text = text.replace('&lt;', '<').replace('&amp;', '&')
        if substitutions:
            for old, new in substitutions.items():
                text = text.replace(old, new)
    
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
        if isinstance(callback, CallBack):
            callback = callback.func
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


class PCData(SubstitutableTextBlock):
    """A section of parsed character data.
    
    Like SubstitutableTextBlock, but the arg is a single string. This
    class is seldom needed in practice, because the element classes are
    able to accept XML PCDATA sections as plain strings.
    """
    def __init__(self, text, escape=True):
        if escape:
            text = self.escape(text)
        if '\t' in text or '\n' in text or '   ' in text:
            self.preformatted = True
        super(PCData, self).__init__(text.split('\n'))


class CData(SubstitutableTextBlock):
    """A section of unparsed character data.
    
    Like SubstitutableTextBlock, but the arg is a single string.
    """
    preformatted = True
    def generate(self, layout=SPARTAN_LAYOUT, scope=BASE_SCOPE, session=None):
        yield layout('<![CDATA[')
        for line in super(Cdata, self).generate(layout, session, scope):
            yield line
        yield layout(']]>')


class CallBack(TextBlock):
    """
    """
    def __init__(self, func, return_type=None):
        self.func = func
        if isinstance(return_type, CallBack):
            raise Exception()
        self.return_type = return_type
    
    def generate(self, layout=SPARTAN_LAYOUT, scope=BASE_SCOPE, session=None):
        return self.func(session).generate(layout, scope, session)

