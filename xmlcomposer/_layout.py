
class Layout(tuple):
    """Settings and routines for managing XML document layout.
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
            # this section is ugly and inefficient, but effective.
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

