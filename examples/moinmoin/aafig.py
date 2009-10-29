#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-
"""
    MoinMoin - aafigure

    This parser is used to visualize aafigure images in the MoinMoin wiki.

    Usage in wiki pages:

    {{{#!aafig scale=1.5 foreground=#ff1010
    DD o--->
    }}}

    @copyright: 2009 by Chris Liechti <cliechti@gmx.net>
    @license: Simplified BSD License

    Install: put this file into /data/plugin/parser
"""
import aafigure
from MoinMoin.action import cache

def sanitizte_color(value):
    """clean string for color codes. the sting is inserted directly in the SVG
       and it must be ensured that the user can not insert arbitrary code"""
    if len(value) == 7 and value[0] == '#':
        return "#%06x" % int(value[1:], 16)
    raise ValueError('invalid color')

Dependencies = ["page"]

class Parser:
    """aafigure parser"""
    extensions = '*.aafigure'

    def __init__(self, raw, request, **kw):
        self.pagename = request.page.page_name
        self.raw = raw
        self.request = request
        self.formatter = request.formatter
        self.args = kw.get('format_args', '')

    def render(self, formatter):
        """text to image conversion"""
        key = 'aafigure_%s' % (cache.key(self.request, itemname=self.pagename, content="%s%s" % (self.raw, self.args)),)
        if not cache.exists(self.request, key) or not cache.exists(self.request, key+'_size'):
            # not in cache, regenerate image
            options = dict(format='svg')
            for arg in self.args.split():
                try:
                    k, v = arg.split('=', 1)
                except ValueError:  # when splitting fails
                    k = arg
                    v = None
                if k == 'aspect':
                    options['aspect'] = float(v)
                elif k == 'scale':
                    options['scale'] = float(v)
                elif k == 'textual':
                    options['textual'] = True
                elif k == 'proportional':
                    options['proportional'] = True
                elif k == 'linewidth':
                    options['linewidth'] = float(v)
                elif k == 'foreground':
                    options['foreground'] = sanitizte_color(v)
                elif k == 'fill':
                    options['fill'] = sanitizte_color(v)
                # no 'background' as SVG backend ignores that
                # no generic options
                # XXX unknown options are ignored with no message

            visitor, output = aafigure.render(self.raw, None, options)
            cache.put(self.request, key, output.getvalue(), content_type="image/svg+xml")
            # need to store the size attributes too
            cache.put(self.request, key+'_size', visitor.get_size_attrs(), content_type="text/plain")

        # get the information from the cache
        #~ return formatter.image(src=cache.url(self.request, key), alt=xxx)
        # XXX this currently only works for HTML, obviously...
        return formatter.rawHTML('<object type="image/svg+xml" data="%s" %s></object>' % (
            cache.url(self.request, key),
            cache._get_datafile(self.request, key+'_size').read() # XXX no way to directly read cache?
        ))

    def format(self, formatter):
        """parser output"""
        self.request.write(self.formatter.div(1, css_class="aafigure"))
        self.request.write(self.render(formatter))
        self.request.write(self.formatter.div(0))


