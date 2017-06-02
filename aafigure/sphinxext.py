# -*- coding: utf-8 -*-
"""
    sphinxcontrib.aafig
    ~~~~~~~~~~~~~~~~~~~

    Allow embeded ASCII art to be rendered as nice looking images
    using the aafigure reStructuredText extension.

    See the README file for details.

    :author: Leandro Lucarella <llucax@gmail.com>
    :license: BOLA
"""

# original license, copied from LICENSE file:
# # I don't like licenses, because I don't like having to worry about all this
# # legal stuff just for a simple piece of software I don't really mind anyone
# # using. But I also believe that it's important that people share and give back;
# # so I'm placing this work under the following license.
# #
# #
# # BOLA - Buena Onda License Agreement (v1.0)
# # ------------------------------------------
# #
# # This work is provided 'as-is', without any express or implied warranty. In no
# # event will the authors be held liable for any damages arising from the use of
# # this work.
# #
# # To all effects and purposes, this work is to be considered Public Domain.
# #
# #
# # However, if you want to be "buena onda", you should:
# #
# # 1. Not take credit for it, and give proper recognition to the authors.
# # 2. Share your modifications, so everybody benefits from them.
# # 3. Do something nice for the authors.
# # 4. Help someone who needs it.
# # 5. Don't waste. Anything, but specially energy that comes from natural
# #    non-renewable resources.
# # 6. Be tolerant. Everything that's good in nature comes from cooperation.

import posixpath
from os import path
try:
    from hashlib import sha1 as sha
except ImportError:
    from sha import sha

from docutils import nodes
from docutils.parsers.rst.directives import images, nonnegative_int, flag

from sphinx.errors import SphinxError
from sphinx.util import ensuredir, relative_uri

from . import aafigure


DEFAULT_FORMATS = dict(html='svg', latex='pdf', text=None)


def merge_dict(dst, src):
    for (k, v) in src.items():
        if k not in dst:
            dst[k] = v
    return dst


def get_basename(text, options, prefix='aafig'):
    options = options.copy()
    if 'format' in options:
        del options['format']
    hashkey = (text + str(options)).encode('utf-8')
    id = sha(hashkey).hexdigest()
    return '{}-{}'.format(prefix, id)


class AafigError(SphinxError):
    category = 'aafig error'


class AafigDirective(images.Image):
    """
    Directive to insert an ASCII art figure to be rendered by aafigure.
    """
    has_content = True
    required_arguments = 0
    own_option_spec = dict(
        line_width=float,
        background=str,
        foreground=str,
        fill=str,
        aspect=nonnegative_int,
        scale=nonnegative_int,
        textual=flag,
        proportional=flag,
        rounded=flag,
    )
    option_spec = images.Image.option_spec.copy()
    option_spec.update(own_option_spec)

    def run(self):
        aafig_options = dict()
        own_options_keys = self.own_option_spec.keys()
        for (k, v) in list(self.options.items()):
            if k in own_options_keys:
                # convert flags to booleans
                if v is None:
                    v = True
                # convert percentage to float
                if k == 'scale' or k == 'aspect':
                    v = float(v) / 100.0
                aafig_options[k] = v
                del self.options[k]
        self.arguments = ['']
        (image_node,) = images.Image.run(self)
        if isinstance(image_node, nodes.system_message):
            return [image_node]
        text = '\n'.join(self.content)
        image_node.aafig = dict(options=aafig_options, text=text)
        return [image_node]


def render_aafig_images(app, doctree):
    format_map = app.builder.config.aafig_format
    merge_dict(format_map, DEFAULT_FORMATS)
    for img in doctree.traverse(nodes.image):
        if not hasattr(img, 'aafig'):
            continue
        options = img.aafig['options']
        text = img.aafig['text']
        format = app.builder.format
        merge_dict(options, app.builder.config.aafig_default_options)
        if format in format_map:
            options['format'] = format_map[format]
        else:
            app.builder.warn(
                'unsupported builder format "{}", please '
                'add a custom entry in aafig_format config option '
                'for this builder'.format(format))
            img.replace_self(nodes.literal_block(text, text))
            continue
        if options['format'] is None:
            img.replace_self(nodes.literal_block(text, text))
            continue
        try:
            fname, outfn, id, extra = render_aafigure(app, text, options)
        except AafigError as exc:
            app.builder.warn('aafigure error: {}'.format(exc))
            img.replace_self(nodes.literal_block(text, text))
            continue
        img['uri'] = fname
        # FIXME: find some way to avoid this hack in aafigure
        if extra:
            (width, height) = [x.split('"')[1] for x in extra.split()]
            if not img.has_key('width'):
                img['width'] = width
            if not img.has_key('height'):
                img['height'] = height


def render_aafigure(app, text, options):
    """
    Render an ASCII art figure into the requested format output file.
    """
    fname = get_basename(text, options)
    fname = '{}.{}'.format(get_basename(text, options), options['format'])
    if app.builder.format == 'html':
        # HTML
        imgpath = relative_uri(app.builder.env.docname, '_images')
        relfn = posixpath.join(imgpath, fname)
        outfn = path.join(app.builder.outdir, '_images', fname)
    else:
        # Non-HTML
        if app.builder.format != 'latex':
            app.builder.warn(
                'aafig: the builder format {} is not officially '
                'supported, aafigure images could not work. Please report '
                'problems and working builder to avoid this warning in '
                'the future'.format(app.builder.format))
        relfn = fname
        outfn = path.join(app.builder.outdir, fname)
    metadata_fname = '{}.aafig'.format(outfn)

    try:
        if path.isfile(outfn):
            extra = None
            if options['format'].lower() == 'svg':
                f = None
                try:
                    try:
                        f = open(metadata_fname, 'r')
                        extra = f.read()
                    except:
                        raise AafigError()
                finally:
                    if f is not None:
                        f.close()
            return relfn, outfn, id, extra
    except AafigError:
        pass

    ensuredir(path.dirname(outfn))

    try:
        (visitor, output) = aafigure.render(text, outfn, options)
        output.close()
    except aafigure.UnsupportedFormatError as e:
        raise AafigError(str(e))

    extra = None
    if options['format'].lower() == 'svg':
        extra = visitor.get_size_attrs()
        with open(metadata_fname, 'w') as f:
            f.write(extra)

    return relfn, outfn, id, extra


def setup(app):
    app.add_directive('aafig', AafigDirective)
    app.connect('doctree-read', render_aafig_images)
    app.add_config_value('aafig_format', DEFAULT_FORMATS, 'html')
    app.add_config_value('aafig_default_options', dict(), 'html')


# vim: set expandtab shiftwidth=4 softtabstop=4 :
