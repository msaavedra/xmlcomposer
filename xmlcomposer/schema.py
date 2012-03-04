
import os
import sys
import urllib2
from urlparse import urlparse, urlunparse
from operator import attrgetter

from _namespace import Namespace
from _document import EmptyElement, NestedElement, FormattedElement, FlatElement

if os.name == 'posix':
    CACHE = os.path.join(os.environ['HOME'], '.config/xmlcomposer/schema/')
elif sys.platform == 'win32' and os.environ.has_key('APPDATA'):
    CACHE = os.path.join(os.environ['APPDATA'], 'xmlcomposer/cache/schema/')
else:
    # Unknown system (maybe win9x?). Punt.
    CACHE = os.path.join(os.getcwd(), 'xmlcomposer/cache/schema/')
CACHE = os.path.normpath(CACHE)

def load(schema_location, namespace_id, namespace_prefix=''):
    schema = SchemaDocument(schema_location)
    return schema.parse(namespace_id, namespace_prefix)

def export(schema_location, namespace_id, export_path=None):
    namespace = load(schema_location, namespace_id)
    if export_path:
        f = open(export_path, 'w')
    else:
        f = sys.stdout
    try:
        f.write('\nimport xmlcomposer\n\n')
        f.write("__namespace__='%s'\n" % namespace_id)
        
        for element in sorted(namespace, key=attrgetter('__name__')):
            ancestors = ', '.join(
                ['xmlcomposer.' + base.__name__ for base in element.__bases__]
                )
            f.write('\nclass %s(%s): pass\n' % (element.__name__, ancestors))
        f.write('\n')
        f.flush()
    finally:
        if export_path:
            f.close()


class SchemaError(Exception): pass

class SchemaDocument(object):
    
    def __init__(self, location, base=''):
        self.location, self.base = self.normalize_location(location, base)
        self.text = self.open_location()
    
    def parse(self, namespace_id, namespace_prefix=''):
        extension_parser_map = {
            'dtd': DtdParser,
            'xsd': XsdParser,
            }
        extension = os.path.splitext(self.location)[1][1:]
        parse = extension_parser_map[extension]
        namespace = Namespace(namespace_id, prefix=namespace_prefix)
        parse(self, namespace)
        return namespace
    
    def normalize_location(self, location, base):
        protocol, host, path = urlparse(location)[:3]
        if os.path.isabs(path):
            if not (protocol and host):
                protocol = 'file'
                host = 'localhost'
            base = urlunparse(
                (protocol, host, os.path.dirname(path), '', '', '')
                )
        else:
            protocol, host, base_path = urlparse(base)[:3]
            path = os.path.join(base_path, path)
        location = urlunparse((protocol, host, path, '', '', ''))
        return location, base
    
    def open_location(self):
        cache_relative_path = self.location.split('//', 1)[1]
        cache_path = os.path.join(CACHE, cache_relative_path)
        if os.path.isfile(cache_path):
            f = open(cache_path, 'r')
            text = f.read()
            f.close()
        else:
            f = urllib2.urlopen(self.location)
            text = f.read()
            dirname = os.path.dirname(cache_path)
            if not os.path.exists(dirname):
                os.makedirs(dirname)
            f = open(cache_path, 'w')
            f.write(text)
            f.close()
        return text

class DtdParser(object):
    
    def __init__(self, schema_doc, namespace):
        self.entities = {}
        self.elements = {}
        self.opened_urls = []
        for declaration in self.yield_declarations(schema_doc):
            self.process_declaration(declaration, schema_doc)
        self.fill_namespace(namespace)
    
    def yield_declarations(self, schema_doc):
        if schema_doc.location in self.opened_urls:
            text = ''
        else:
            text = schema_doc.text
            self.opened_urls.append(schema_doc.location)
        
        while text:
            parts = text.split('>', 1)
            if len(parts) != 2:
                break
            declaration, text = parts
            if '<!' not in declaration:
                continue
            yield declaration.split('<!')[-1]
    
    def process_declaration(self, declaration, schema_doc):
        if declaration.startswith('ELEMENT'):
            name, contents = declaration.split(None, 2)[1:]
            self.elements[name] = contents
        elif declaration.startswith('ENTITY %'):
            if ' SYSTEM ' in declaration:
                mod_uri = declaration.split(None, 4)[4]
            elif ' PUBLIC ' in declaration:
                mod_uri = declaration.split(None, 4)[4].split('"')[3]
            else:
                name, contents = declaration.split(None, 3)[2:]
                name = self.substitute_entities(name)
                contents = contents.replace('"', '')
                self.entities[name] = contents
                return
            mod_doc = SchemaDocument(mod_uri, schema_doc.base)
            for mod_declaration in self.yield_declarations(mod_doc):
                self.process_declaration(mod_declaration, mod_doc)
    
    def fill_namespace(self, namespace):
        for name, contents in self.elements.items():
            name = self.substitute_entities(name).title()
            contents = self.substitute_entities(contents)
            
            if 'EMPTY' in contents:
                ancestor = EmptyElement
            elif ',' in contents or '#PCDATA' not in contents:
                ancestor = NestedElement
            elif '#PCDATA' in contents and '|' not in contents:
                ancestor = FlatElement
            else:
                ancestor = FormattedElement
            new_class = type(name, (ancestor,), {'__module__': namespace})
            setattr(namespace, name, new_class)
    
    def substitute_entities(self, text):
        while '%' in text:
            entity_name = text.split('%', 1)[1].split(';', 1)[0]
            if self.entities.has_key(entity_name):
                sub = self.entities[entity_name]
                text = text.replace('%%%s;' % entity_name, sub)
        return text


class XsdParser(object): pass

