#!/usr/bin/env python2

import time, sys, os
import xmlcomposer
from xmlcomposer import schema
'''
rng = schema.export(
    schema_location='http://www.silmaril.ie/software/rss2.dtd',
    namespace_id='http://backend.userland.com/rss2',
    export_path='./rss2.py'
    )

rss = schema.load(
    schema_location='http://www.silmaril.ie/software/rss2.dtd',
    namespace_id='http://backend.userland.com/rss2',
    #export_path='./rss2.py'
    namespace_prefix='rss'
    )
print dir(rss)
x = xmlcomposer.Namespace(module='xmlcomposer.formats.xhtml_1_strict')
#print dir(x)
sys.exit(0)
'''
#h = schema.load(schema_location='/home/mike/html_5.xsd')
#schema.export(schema_location='/home/mike/html_5.xsd', export_path='./html5.py')
h = xmlcomposer.Namespace(module='xmlcomposer.formats.html5')

def fill_hello(session):
    """A contrived example of a substitution callback."""
    return xmlcomposer.PCData('Hello %s!' % session['USERNAME'].title())

def fill_test(session):
    return h.Em('test')

def random_paragraph(session):
    import random
    num = str(random.randint(1,100))
    return h.P('Here is a random number from 1 to 100: ', num, '.')

paragraph = xmlcomposer.PCData('%REPLACE% This is a %TEST%.', escape=False)
paragraph.substitute('%REPLACE%', fill_hello).substitute('%TEST%', fill_test)

html = h.Html(
    h.Head(
        h.Title('Test')
    ),
    h.Body(
        h.H1('Test'),
        #rss.Author('Michael Saavedra'),
        h.Img(src='test.jpg', alt='Picture'),
        h.Div(class_='main')(
            h.P(paragraph),
            xmlcomposer.CallBack(random_paragraph, xmlcomposer.Element),
            h.P('Here is a paragraph to test wrapping. It is adequately long without really saying anything.'),
            ),
        h.Hr(),
        h.P(id_='addendum')('&copy; 2012 Michael & Dana')
        ),
    )

prolog = xmlcomposer.Prolog(
    #xmlcomposer.XMLDeclaration(),
    xmlcomposer.DocType(
        root_name='html',
        #system_id='http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd',
        #public_id='-//W3C//DTD XHTML 1.0 Strict//EN'
        )
    )
doc = xmlcomposer.Document(root=html, prolog=prolog)
layout = xmlcomposer.Layout(indent_style='  ')
#scope = xmlcomposer.Scope(x, rss)
for line in doc.generate(layout, session=os.environ):
    sys.stdout.write(line)
    sys.stdout.flush()
    #time.sleep(1)
print ''

