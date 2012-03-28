# Copyright (c) 1999, 2012 Michael Saavedra
# This file may be redistributed under the terms of the GNU LPGL v. 3 or later.

"""Tools for laying out an XML document.

This includes handling indentation, line endings and text wrapping.
The module has a Layout class that lets you make custom layouts. It also
contains three pre-built layouts that cover most use cases:

DEFAULT_LAYOUT: This indents one tab character for each level of nesting,
uses a newline character at the end of each line, and wraps text at the
80th column. This is the best option to use to make a document human-readable.

SPARTAN_LAYOUT: This does not do any indenting or text-wrapping. However, it
places a newline at the end of each line. This is still human-readable with
some effort, and results in a smaller document.

MINIMAL_LAYOUT: This option does not add any unneeded characters, creating
the smallest possible document. It is very difficult for humans to read.

Note that Layout settings are not absolute; element classes use them at
the discretion of their programmers. They are, for instance, ignored completely
by preformatted elements.
"""

from operator import itemgetter

class Layout(tuple):
    """Settings and routines for managing the layout of generated XML.
    
    Instances of this class are used solely as arguments to the TextBlock
    generate() method and its kin, where lack of side-effects is a design goal.
    Therefore, Layout instances are designed to be immutable, though a clever
    but unwise programmer may be able to circumvent this.
    """
    __slots__ = () # save space used by __dict__.
    
    indent_style = property(itemgetter(0))
    indent_count = property(itemgetter(1))
    line_ending = property(itemgetter(2))
    line_wrap = property(itemgetter(3))
    indentation = property(itemgetter(4))
    default_wrap = property(itemgetter(5))
    min_wrap = property(itemgetter(6))
    
    def __new__(cls, indent_style='\t', indent_count=0,
             line_ending='\n', line_wrap=80):
        indentation = indent_style * indent_count
        default_wrap = max(40, line_wrap - len(indentation))
        min_wrap = default_wrap / 2
        return tuple.__new__(cls, (
            indent_style,
            indent_count,
            line_ending,
            line_wrap,
            indentation,
            default_wrap,
            min_wrap
            ))
    
    def __str__(self):
        return '<Layout (%s, %s, %s, %s)>' % (
            repr(self.indent_style),
            self.indent_count,
            repr(self.line_ending),
            self.line_wrap
            )
    
    def __repr__(self):
        return '"%s"' % str(self)
    
    def __setattr__(self, key, value):
        raise AttributeError('Cannot set attributes of Layout object.')
    
    def indent(self):
        if self.indent_style == '':
            return self
        else:
            return Layout(self.indent_style, self.indent_count + 1,
                self.line_ending, self.line_wrap)
    
    def __call__(self, line, wrap=False):
        if line.strip == '':
            return line_ending
        elif wrap == False or self.line_wrap == 0 or self.line_ending == '':
            return '%s%s%s' % (self.indentation, line, self.line_ending)
        else:
            parts = []
            while len(line) > self.default_wrap:
                index = self.default_wrap
                part = line[:index]
                while not (part.count('<') == part.count('>') \
                        and part.endswith(' ')):
                    if self.min_wrap < index <= self.default_wrap:
                        index -= 1
                    elif index == self.min_wrap:
                        index = self.default_wrap + 1
                    else:
                        index += 1
                    part = line[:index]
                    if part == line:
                        break
                line = line[index:]
                part = self.indentation + part.strip()
                parts.append(part)
            if line:
                parts.append(self.indentation + line)
            return self.line_ending.join(parts) + self.line_ending

# Standard XML formatting for easy human reading.
DEFAULT_LAYOUT = Layout()
# More compact formatting with no indentation.
SPARTAN_LAYOUT = Layout('', 0, '\n', 0)
# Smallest possible output.
MINIMAL_LAYOUT = Layout('', 0, '', 0)

