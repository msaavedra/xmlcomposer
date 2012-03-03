#!/usr/bin/env python2

import time, sys, os
import xmlcomposer
from xmlcomposer import schema

rss = schema.load(
    schema_location='http://www.silmaril.ie/software/rss2.dtd',
    namespace_id='http://backend.userland.com/rss2',
    #export_path='./rss2.py'
    namespace_prefix='rss'
    )

x = xmlcomposer.Namespace(module='xmlcomposer.formats.xhtml_1_strict')

def fill_hello(session):
    """A contrived example of a substitution callback."""
    return xmlcomposer.PCData('Hello %s!' % session['USERNAME'].title())

def fill_test(session):
    return x.Em('test')

def random_paragraph(session):
    import random
    num = str(random.randint(1,100))
    return x.P('Here is a random number from 1 to 100: ', num, '.')

paragraph = xmlcomposer.PCData('<p>%REPLACE% This is a %TEST%.')
paragraph.substitute('%REPLACE%', fill_hello).substitute('%TEST%', fill_test)

html = x.Html(
    x.Head(
        x.Title('Test')
    ),
    x.Body(
        x.H1('Test'),
        rss.Author('Michael Saavedra'),
        x.Img(src='test.jpg', alt='Picture'),
        x.Div(class_='main')(
            paragraph,
            random_paragraph,
            x.P('Here is a paragraph to test wrapping. It is adequately long without really saying anything.'),
            ),
        x.Hr()
        ),
    )

prolog = xmlcomposer.Prolog(
    xmlcomposer.XMLDeclaration(),
    xmlcomposer.DocType(
        root_name='html',
        system_id='http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd',
        public_id='-//W3C//DTD XHTML 1.0 Strict//EN'
        )
    )
doc = xmlcomposer.Document(root=html, prolog=prolog)
layout = xmlcomposer.Layout(indent_style='  ')
scope = xmlcomposer.Scope(x, rss)
for line in doc.generate(layout, scope=scope, session=os.environ):
    sys.stdout.write(line)
    sys.stdout.flush()
    #time.sleep(1)
print ''

