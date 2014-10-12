# Copyright (c) 1999, 2012 Michael Saavedra
# This file may be redistributed under the terms of the GNU LPGL v. 3 or later.

"""Classes for adding arbitrary text to XML documents.
"""

import re
import inspect

from _layout import SPARTAN_LAYOUT
from _namespace import BASE_SCOPE

class TextBlock(object):
    """A holder for intermingled character data and markup.
    
    The TextBlock does not guarantee that its contents are well-formed.
    It generally should not be used directly. Instead use one of
    its subclasses.
    
    A very basic example:
    >>> test = TextBlock(('Hello World!', 'This is a test.'))
    >>> print test
    Hello World!
    This is a test.
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
        """This is a routine to process special characters gracefully.
        
        The only truly reserved characters in XML are the ampersand and
        the less-than sign. These are substituted with the appropriate XML
        entities (&amp; and &lt; respectively).
        
        This routine recognizes XML entities in the text and does not
        substitute for their leading ampersand.
        
        The text argument is a string from which you wish to handle the special
        characters.
        
        The substitutions argument should be a dictionary whose
        key/value pairs hold, respectively, the characters needing to be
        substituted, and their replacement.
        
        Examples:
        
        >>> print TextBlock.escape('Hello & Goodbye')
        Hello &amp; Goodbye
        
        >>> print TextBlock.escape('Hello &amp; Goodbye')
        Hello &amp; Goodbye
        
        >>> print TextBlock.escape('Double quotes "escaped."', {'"': '&quot;'})
        Double quotes &quot;escaped.&quot;
        """
        if substitutions:
            for old, new in substitutions.items():
                text = text.replace(old, new)
        text = cls._amp_regex.sub(cls.__replace_on_match, text)
        text = text.replace('<', '&lt;')
        return text
    
    @classmethod
    def __replace_on_match(cls, match):
        return '&amp;'+ match.group('suffix')
    
    @classmethod
    def unescape(cls, text, substitutions=None):
        """A routine to convert escaped strings to their original form.
        
        By default, the &amp; and &lt; substrings are converted to & and <
        respectively. Additional conversions can be specified by passing
        a dictionary as the substitutions arg.
        """
        text = text.replace('&lt;', '<').replace('&amp;', '&')
        if substitutions:
            for old, new in substitutions.items():
                text = text.replace(old, new)
    
    def render(self, layout=SPARTAN_LAYOUT, scope=BASE_SCOPE, session=None):
        """Return the entire generated block as a string.
        
        The arguments are identical to the generate() method.
        """
        return ''.join(self.generate(layout, scope, session))
    
    def generate(self, layout=SPARTAN_LAYOUT, scope=BASE_SCOPE, session=None):
        """Return a generator that creates a section of XML line-by-line.
        
        This method is the most fundamental part of TextBlock and its
        subclasses. All other built-in output methods use it, and any
        custom-designed output methods should too.
        
        This is a very frequently overridden method because different
        subclasses have different generation strategies. Very often, 
        TextBlock subclass instances are deeply nested within other TextBlock
        subclass instances, and their generate() methods are called
        automatically by their parent instance. Thus, when
        overriding, subclasses MUST accept the same arguments, even
        if some of the args will not be used, or make no sense in that
        class's context. However, different default values can be used
        if appropriate.
        
        Also, generate() is designed to be side-effect free, with the possible
        exception of side-effects added through Callbacks outside the
        control of the TextBlock. This is so that TextBlocks can be created
        once, then used many times in different contexts, in many different
        threads, without being altered. Subclasses are STRONGLY ENCOURAGED to
        maintain the side-effect-free design.
        
        Possible arguments (all of which are optional):
        
        The layout arg should be a Layout instance with settings for handling
        indentation, etc.
        
        The scope arg contains a Scope instance that contains the namespaces
        available in the context of the block's place within a document.
        
        The session arg may contain any data particular to the session
        for which the text is being generated. It is passed to Callbacks
        so they can create appropriate content. This argument is completely
        free-form, programmers can use any type of object they want, as
        long as their Callback functions are capable of using it.
        """
        for line in self._contents:
            yield layout(line)
    
    def on(self, condition):
        """Only generate output if the condition is matched.
        
        If the condition is a boolean expression, it is of course evaluated
        immediately. For some contrived examples:
        
        >>> print TextBlock(['This is a test.']).on(1 + 1 == 2)
        This is a test.
        >>> print TextBlock(['This is a test.']).on(0 == 1)
        <BLANKLINE>
        
        Also, the condition can be any callable object that expects no
        arguments. It will be called at generation-time and the boolean value
        of it's output will be used to determine if output should be generated.
        
        >>> x = True
        >>> test = TextBlock(['This is a test.']).on(lambda: x)
        >>> print test
        This is a test.
        >>> x = False
        >>> print test
        <BLANKLINE>
        
        Note that calling this method multiple times will combine the
        conditions such that all must be True. The conditions will be evaluated
        in the order of most recent first and are short-circuited in the event
        that one of them evaluates to False.
        
        >>> print TextBlock(['This is a test.']).on(True).on(False)
        <BLANKLINE>
        >>> print TextBlock(['This is a test.']).on(False).on(True)
        <BLANKLINE>
        >>> print TextBlock(['This is a test.']).on(True).on(1)
        This is a test.
        
        """
        def skip(*args, **kwargs):
            """Return an empty generator.
            
            This is a conditional replacement for the generate() method.
            """
            return (x for x in ())
        
        if callable(condition):
            layout, scope, session = inspect.getargspec(self.generate).defaults
            current_generate = self.generate
            
            def skip_lazily(self, layout=layout, scope=scope, session=session):
                if condition():
                    return current_generate(layout, scope, session)
                else:
                    return skip()
            
            self.generate = skip_lazily.__get__(self, self.__class__)
            
        elif condition:
            self.generate = self.generate
        else:
            self.generate = skip.__get__(self, self.__class__)
        
        return self


class SubstitutableTextBlock(TextBlock):
    """An text block with support for text substitutions at generation-time.
    
    Like the TextBlock class from which it descends, this has more useful
    subclasses and should generally not be used directly
    """
    def __init__(self, lines):
        super(SubstitutableTextBlock, self).__init__(lines)
        self._substitutions = []
    
    def substitute(self, flag, callback):
        """Set up a substitution which will occur at generation time.
        
        The flag argument indicates a marker string in the contents
        that is substituted with new contents. The callback arg should be a
        Callback instance, though any callable object such as a function or
        method will also work. It must build and return the new content that
        replaces the flag. The callback must accept a single arg containing
        session information, and return a single instance of TextBlock or
        a subclass thereof.
        
        Example:
        >>> def get_name(session):
        ...     return PCData(session['name'])
        >>> 
        >>> c = CallBack(get_name, return_type=PCData)
        >>> e = PCData('Hello %NAME%!').substitute('%NAME%', c)
        >>> print e.render(session={'name': 'Alice'})
        Hello Alice!
        >>> print e.render(session={'name': 'Bob'})
        Hello Bob!
        """
        def yield_substituted_lines(contents, layout, scope, session):
            """A generator-function closure for handling substitutions.
            """
            for line in contents:
                parts = line.split(flag)
                new_line = parts.pop(0)
                for part in parts:
                    substitute = callback(session).generate(
                        layout, scope, session
                        )
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
            contents = substitution(contents, layout, scope, session)
        for line in contents:
            yield layout(line)


class PCData(SubstitutableTextBlock):
    """A section of parsed character data.
    
    Like SubstitutableTextBlock, but the arg may be a single string rather
    than a sequence of strings. This class is seldom needed in practice,
    because the element classes are able to accept XML PCDATA sections as
    plain strings.
    """
    def __init__(self, lines, escape=True):
        if isinstance(lines, str):
            if '\t' in lines or '\n' in lines or '   ' in lines:
                self.preformatted = True
            if escape:
                lines = self.escape(lines)
            lines = [lines]
        else:
            if escape:
                lines = [self.escape(line) for line in lines]
            for line in lines:
                if '\t' in line or '\n' in line or '   ' in line:
                    self.preformatted = True
                    break
        
        super(PCData, self).__init__(lines)


class CData(SubstitutableTextBlock):
    """A section of unparsed character data. Each arg is an individial line.
    
    Example:
    
    >>> c = CData(
    ...     'This is a section of unparsed character data.',
    ...     'Contents must be preformatted by the user.',
    ... )
    >>> print c
    <![CDATA[
    This is a section of unparsed character data.
    Contents must be preformatted by the user.
    ]]>
    """
    preformatted = True
    
    def __init__(self, *lines):
        super(CData, self).__init__(lines)
    
    def generate(self, layout=SPARTAN_LAYOUT, scope=BASE_SCOPE, session=None):
        yield layout('<![CDATA[')
        for line in super(CData, self).generate(layout, session, scope):
            yield line
        yield layout(']]>')


class CallBack(TextBlock):
    """A section whose contents are determined dynamically at generation-time.
    
    See the SubstitutableTextBlock.substitute() method for an example.
    """
    def __init__(self, func, return_type=None):
        """Initialize the callback.
        
        The func arg can be any callable object that accepts a single arg
        that holds session data and returns a TextBlock or any of its
        subclasses.
        
        The return_type arg allows the user to optionally specify the class
        which will be returned by the callback (ie an Element, PCData, etc.).
        This allows a parent element to do a better job of laying out its
        content.
        """
        self.func = func
        if isinstance(return_type, CallBack):
            raise Exception()
        self.return_type = return_type
    
    def __call__(self, session):
        return self.func(session)
    
    def generate(self, layout=SPARTAN_LAYOUT, scope=BASE_SCOPE, session=None):
        return self.func(session).generate(layout, scope, session)


class Comment(TextBlock):
    """An unparsed, non-character-data, explanatory note in an XML document.
    
    Example:
    >>> print Comment('This is an XML comment.')
    <!--This is an XML comment.-->
    """
    def __init__(self, text):
        text = '<!--%s-->' % text
        super(Comment, self).__init__(text.split('\n'))

