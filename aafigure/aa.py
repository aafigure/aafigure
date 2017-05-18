#!python
#
# This file is part of aafigure. https://github.com/aafigure/aafigure
# (C) 2006 Chris Liechti <cliechti@gmx.net>
#
# SPDX-License-Identifier:    BSD-3-Clause
"""\
Simple ASCII output of the rendered image.  Think of it as a low resolution
black and white image.
"""

import sys


class AsciiOutputVisitor:
    """\
    Render a list of shapes as ASCII art.
    Scaled, think of it as a low resolution black and white image.
    """

    def __init__(self, options):
        self.options = options
        self.image = {}
        self.scale = options['scale']

    def visit_image(self, aa_image):
        self.visit_shapes(aa_image.shapes)
        self.options['file_like'].write(self.create_image())

    def visit_shapes(self, shapes):
        for shape in shapes:
            shape_name = shape.__class__.__name__.lower()
            visitor_name = 'visit_{}'.format(shape_name)
            function = getattr(self, visitor_name, None)
            if function is not None:
                function(shape)
            else:
                sys.stderr.write("WARNING: don't know how to handle shape {!r}\n".format(shape))

    def visit_group(self, group):
        self.visit_shapes(group.shapes)

    def visit_point(self, point):
        self.image[point.x * self.scale, point.y * self.scale] = '#'

    def visit_line(self, line):
        x1, x2 = line.start.x * self.scale, line.end.x * self.scale
        y1, y2 = line.start.y * self.scale, line.end.y * self.scale
        if x1 > x2:
            x1, x2 = x2, x1
        if y1 > y2:
            y1, y2 = y2, y1
        dx = x2 - x1
        dy = y2 - y1
        if dx > dy:
            y = y1
            if dx:
                m = float(dy) / dx
            else:
                m = 0
            for x in range(int(x1), int(x2 + 1)):
                self.image[x, int(y)] = '#'
            y += m
        else:
            x = x1
            if dy:
                m = float(dx) / dy
            else:
                m = 0
            for y in range(int(y1), int(y2+1)):
                self.image[int(x), y] = '#'
            x += m

    def visit_rectangle(self, rectangle):
        x1, x2 = rectangle.p1.x * self.scale, rectangle.p2.x * self.scale
        y1, y2 = rectangle.p1.y * self.scale, rectangle.p2.y * self.scale
        if x1 > x2:
            x1, x2 = x2, x1
        if y1 > y2:
            y1, y2 = y2, y1
        for y in range(int(y1), int(y2)):
            for x in range(int(x1), int(x2)):
                self.image[x, y] = '#'

    def visit_label(self, label):
        x, y = int(label.position.x * self.scale), int(label.position.y * self.scale)
        for character in label.text:
            self.image[x, y] = character
            x += 1

    def __str__(self):
        return self.create_image()

    def create_image(self):
        """return a cropped image"""
        # find out size
        min_x = min_y = 1000000
        max_x = max_y = -1000000
        for x, y in self.image:
            min_x = min(min_x, x)
            max_x = max(max_x, x)
            min_y = min(min_y, y)
            max_y = max(max_y, y)
        # render image to lines of text, fill unused fields with a dot
        result = []
        for y in range(min_y, max_y+1):
            line = []
            for x in range(min_x, max_x+1):
                line.append(self.image.get((x, y), '.'))
            result.append(''.join(line))
        return u'{}\n'.format('\n'.join(result))
