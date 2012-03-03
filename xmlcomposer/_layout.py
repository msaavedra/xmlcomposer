
class Layout(object):
    """Settings and routines for managing XML document layout.
    """
    def __init__(self, indent_style='\t', indent_count=0,
             line_ending='\n', line_wrap=80):
        self.indent_style = indent_style
        self.indent_count = indent_count
        self.line_ending = line_ending
        self.line_wrap = line_wrap
        
        self.indentation = indent_style * indent_count
        self.default_wrap = max(48, line_wrap - len(self.indentation)) + 1
        self.min_wrap = self.default_wrap / 2
    
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

#Standard XML formatting for easy human reading.
DEFAULT_LAYOUT = Layout()
#More compact formatting with no indentation.
SPARTAN_LAYOUT = Layout('', 0, '\n', 0)
# Smallest possible output.
MINIMAL_LAYOUT = Layout('', 0, '', 0)

