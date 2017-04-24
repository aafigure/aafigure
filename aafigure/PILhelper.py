#!python
#
# This file is part of aafigure. https://github.com/aafigure/aafigure
# (C) 2010 Chris Liechti <cliechti@gmx.net>, Oliver Joos <oliver.joos@hispeed.ch>
#
# SPDX-License-Identifier:    BSD-3-Clause
"""\
Helper objects for bitmap renderer of the aafigure package.
"""

import os
from PIL import ImageFont


# - - - - - - font helpers - - - - - - -

def _find_file(name, top_dir):
    """\
    Find a file by its name in a directory or sub-directories (recursively).
    Return absolute path of the file or None if not found.
    """
    for (dirpath, dirnames, filenames) in os.walk(top_dir):
        if name in filenames:
            return os.path.join(dirpath, name)
    return None


def font_by_name(name, size):
    """\
    Get a PIL ImageFont instance by font name and size. If name is not an
    absolute pathname, it is searched in the default font locations of the
    underlying OS. If not found, None is returned.
    """
    font = None
    try:
        font = ImageFont.truetype(name, size)
    except IOError:
        # PIL upto 1.1.7b1 only tries absolute paths for win32
        if os.name == 'posix':
            font_path = _find_file(name, '/usr/share/fonts')
            if font_path:
                try:
                    font = ImageFont.truetype(font_path, size)
                except IOError:
                    pass
    return font


def font_by_type(proportional, size):
    """\
    Get a PIL ImageFont instance by font type and size. If <proportional> is
    not True, a mono-spaced font is returned. If no suitable font is found,
    None is returned.
    """
    if proportional:
        font = font_by_name('LiberationSans-Regular.ttf', size)
        if font is None:
            font = font_by_name('Arial.ttf', size)
    else:
        font = font_by_name('LiberationMono-Regular.ttf', size)
        if font is None:
            font = font_by_name('Courier_New.ttf', size)
    return font
