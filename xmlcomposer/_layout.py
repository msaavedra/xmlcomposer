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

class Layout(tuple):
    """Settings and routines for managing XML document layout.
    
    Note that instances are designed to be immutable, though a clever but
    unwise programmer can circumvent this.
    """
    def __new__(cls, indent_style='\t', indent_count=0,
             line_ending='\n', line_wrap=80):
        indentation = indent_style * indent_count
        default_wrap = max(48, line_wrap - len(indentation))
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
        raise AttributeError('Cannot add attributes to Layout.')
    
    @property
    def indent_style(self):
        return self[0]
    
    @property
    def indent_count(self):
        return self[1]
    
    @property
    def line_ending(self):
        return self[2]
    
    @property
    def line_wrap(self):
        return self[3]
    
    @property
    def indentation(self):
        return self[4]
    
    @property
    def default_wrap(self):
        return self[5]
    
    @property
    def min_wrap(self):
        return self[6]
    
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
            return self.indentation + line + self.line_ending
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

