#!/usr/bin/env python

"""\
ASCII art to image converter.

This is the main module that contains the parser.

See svg.py and aa.py for output modules, that can render the parsed structure.

(C) 2006-2009 Chris Liechti <cliechti@gmx.net>

This is open source software under the BSD license. See LICENSE.txt for more
details.
"""
import codecs
from error import UnsupportedFormatError
from shapes import *
from unicodedata import east_asian_width
import sys

NOMINAL_SIZE = 2

CLASS_LINE = 'line'
CLASS_STRING = 'str'
CLASS_RECTANGLE = 'rect'
CLASS_JOIN = 'join'
CLASS_FIXED = 'fixed'

DEFAULT_OPTIONS = dict(
    background   = '#ffffff',
    foreground   = '#000000',
    line_width   = 2.0,
    scale        = 1.0,
    aspect       = 1.0,
    format       = 'svg',
    debug        = False,
    textual      = False,
    proportional = False,
    encoding     = 'utf-8',
    widechars     = 'F,W',
)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

class AsciiArtImage:
    """This class hold a ASCII art figure and has methods to parse it.
       The resulting list of shapes is also stored here.

       The image is parsed in 2 steps:

       1. horizontal string detection.
       2. generic shape detection.

       Each character that is used in a shape or string is tagged. So that
       further searches don't include it again (e.g. text in a string touching
       a fill), respectively can use it correctly (e.g. join characters when
       two or more lines hit).
    """

    QUOTATION_CHARACTERS = list('"\'`')

    def __init__(self, text, aspect_ratio=1, textual=False, widechars='F,W'):
        """Take a ASCII art figure and store it, prepare for ``recognize``"""
        self.aspect_ratio = float(aspect_ratio)
        self.textual = textual
        # XXX TODO tab expansion
        # detect size of input image, store as list of lines
        self.image = []
        max_x = 0
        y = 0
        # define character widths map
        charwidths = {}
        for key in ['F', 'H', 'W', 'Na', 'A', 'N']:
            if key in widechars.split(','):
                charwidths[key] = 2
            else:
                charwidths[key] = 1
        for line in text.splitlines():
            # extend length by 1 for each wide glyph
            line_len = sum(charwidths[east_asian_width(c)] for c in line)
            max_x = max(max_x, line_len)
            # pad a space for each wide glyph
            padded_line = ''.join(c+' '*(charwidths[east_asian_width(c)]-1) for c in line)
            self.image.append(padded_line)
            y += 1
        self.width = max_x
        self.height = y
        # make sure it's rectangular (extend short lines to max width)
        for y, line in enumerate(self.image):
            if len(line) < max_x:
                self.image[y] = line + ' '*(max_x-len(line))
        # initialize other data structures
        self.classification = [[None]*self.width for y in range(self.height)]
        self.shapes = []
        self.nominal_size = NOMINAL_SIZE

    def __str__(self):
        """Return the original image"""
        return '\n'.join([self.image[y] for y in range(self.height)])

    def get(self, x, y):
        """Get character from image. Gives no error for access out of
           bounds, just returns a space. This simplifies the scanner
           functions.
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.image[y][x]
        else:
            return ' '

    def tag(self, coordinates, classification):
        """Tag coordinates as used, store classification"""
        for x, y in coordinates:
            self.classification[y][x] = classification

    def cls(self, x, y):
        """get tag at coordinate"""
        try:
            return self.classification[y][x]
        except IndexError:
            return 'outside'

    # Coordinate conversion and shifting
    def left(self, x):
        return x*NOMINAL_SIZE*self.aspect_ratio

    def hcenter(self, x):
        return (x + 0.5)*NOMINAL_SIZE*self.aspect_ratio

    def right(self, x):
        return (x + 1)*NOMINAL_SIZE*self.aspect_ratio

    def top(self, y):
        return y*NOMINAL_SIZE

    def vcenter(self, y):
        return (y + 0.5)*NOMINAL_SIZE

    def bottom(self, y):
        return (y + 1)*NOMINAL_SIZE

    def recognize(self):
        """
        Try to convert ASCII art to vector graphics. The result is stored in
        ``self.shapes``.
        """
        # XXX search for symbols
        #~ #search for long strings
        #~ for y in range(self.height):
            #~ for x in range(self.width):
                #~ character = self.image[y][x]
                #~ if self.classification[y][x] is None:
                    #~ if character.isalnum():
                        #~ self.shapes.extend(
                            #~ self._follow_horizontal_string(x, y)
                        #~ )
        # search for quoted texts
        for y in range(self.height):
            for x in range(self.width):
                #if not yet classified, check for a line
                character = self.image[y][x]
                if character in self.QUOTATION_CHARACTERS and self.classification[y][x] is None:
                    self.shapes.extend(
                        self._follow_horizontal_string(x, y, quoted=True))

        # search for standard shapes
        for y in range(self.height):
            for x in range(self.width):
                #if not yet classified, check for a line
                character = self.image[y][x]
                if self.classification[y][x] is None:
                    if character == '-':
                        self.shapes.extend(self._follow_horizontal_line(x, y))
                    elif character == '|':
                        self.shapes.extend(self._follow_vertical_line(x, y))
                    elif character == '_':
                        self.shapes.extend(self._follow_lower_horizontal_line(x, y))
                    elif character == '~':
                        self.shapes.extend(self._follow_upper_horizontal_line(x, y))
                    elif character == '=':
                        self.shapes.extend(self._follow_horizontal_line(x, y, thick=True))
                    elif character in '\\/':
                        self.shapes.extend(self._follow_rounded_edge(x, y))
                    elif character == '+':
                        self.shapes.extend(self._plus_joiner(x, y))
                    elif character in self.FIXED_CHARACTERS:
                        self.shapes.extend(self.get_fixed_character(character)(x, y))
                        self.tag([(x, y)], CLASS_FIXED)
                    elif character in self.FILL_CHARACTERS:
                        if self.textual:
                            if self.get(x, y+1) == character:
                                self.shapes.extend(self._follow_fill(character, x, y))
                        else:
                            if (self.get(x+1, y) == character or self.get(x, y+1) == character):
                                self.shapes.extend(self._follow_fill(character, x, y))

        # search for short strings too
        for y in range(self.height):
            for x in range(self.width):
                character = self.image[y][x]
                if self.classification[y][x] is None:
                    if character != ' ':
                        self.shapes.extend(self._follow_horizontal_string(x, y, accept_anything=True))

    # - - - - - - - - - helper function for some shapes - - - - - - - - -
    # Arrow drawing functions return the (new) starting point of the line and a
    # list of shapes that draw the arrow. The line itself is not included in
    # the list of shapes. The stating point is p1, possibly modified to match
    # the shape of the arrow head.
    #
    # Use complex numbers as 2D vectors as that means easy transformations like
    # scaling, rotation and translation

    # - - - - - - - - - arrows - - - - - - - - -
    def _standard_arrow(self, p1, p2):
        """-->
           return a possibly modified starting point and a list of shapes
        """
        direction_vector = p1 - p2
        direction_vector /= abs(direction_vector)
        return p1, [
            Line(p1, p1-direction_vector*1.5+direction_vector*0.5j),
            Line(p1, p1-direction_vector*1.5+direction_vector*-0.5j)
        ]

    def _reversed_arrow(self, p1, p2):
        """--<"""
        direction_vector = p1 - p2
        direction_vector /= abs(direction_vector)
        return p1-direction_vector*2, [
            Line(p1-direction_vector*2.0, p1+direction_vector*(-0.5+0.5j)),
            Line(p1-direction_vector*2.0, p1+direction_vector*(-0.5-0.5j))
        ]

    def _circle_head(self, p1, p2, radius=0.5):
        """--o"""
        direction_vector = p1 - p2
        direction_vector /= abs(direction_vector)
        return p1-direction_vector, [Circle(p1-direction_vector, radius)]

    def _large_circle_head(self, p1, p2):
        """--O"""
        return self._circle_head(p1, p2, radius=0.9)

    def _rectangular_head(self, p1, p2):
        """--#"""
        direction_vector = p1 - p2
        direction_vector /= abs(direction_vector)
        #~ return p1-direction_vector*1.414, [
            #~ Rectangle(p1-direction_vector-direction_vector*(0.707+0.707j),
                      #~ p1-direction_vector+direction_vector*(0.707+0.707j))
        #~ ]
        return p1-direction_vector*1.707, [
            Line(p1-direction_vector-direction_vector*(0.707+0.707j),
                 p1-direction_vector-direction_vector*(0.707-0.707j)),
            Line(p1-direction_vector+direction_vector*(0.707+0.707j),
                 p1-direction_vector+direction_vector*(0.707-0.707j)),
            Line(p1-direction_vector-direction_vector*(0.707+0.707j),
                 p1-direction_vector+direction_vector*(0.707-0.707j)),
            Line(p1-direction_vector-direction_vector*(0.707-0.707j),
                 p1-direction_vector+direction_vector*(0.707+0.707j)),
        ]

    # the same character can mean a different thing, depending from where the
    # line is coming. this table maps line direction (dx,dy) and the arrow
    # character to a arrow drawing function
    ARROW_TYPES = [
        #chr  dx  dy  arrow type
        ('>',  1,  0, '_standard_arrow'),
        ('<', -1,  0, '_standard_arrow'),
        ('^',  0, -1, '_standard_arrow'),
        ('A',  0, -1, '_standard_arrow'),
        ('V',  0,  1, '_standard_arrow'),
        ('v',  0,  1, '_standard_arrow'),
        ('>', -1,  0, '_reversed_arrow'),
        ('<',  1,  0, '_reversed_arrow'),
        ('^',  0,  1, '_reversed_arrow'),
        ('V',  0, -1, '_reversed_arrow'),
        ('v',  0, -1, '_reversed_arrow'),
        ('o',  1,  0, '_circle_head'),
        ('o', -1,  0, '_circle_head'),
        ('o',  0, -1, '_circle_head'),
        ('o',  0,  1, '_circle_head'),
        ('O',  1,  0, '_large_circle_head'),
        ('O', -1,  0, '_large_circle_head'),
        ('O',  0, -1, '_large_circle_head'),
        ('O',  0,  1, '_large_circle_head'),
        ('#',  1,  0, '_rectangular_head'),
        ('#', -1,  0, '_rectangular_head'),
        ('#',  0, -1, '_rectangular_head'),
        ('#',  0,  1, '_rectangular_head'),
    ]

    ARROW_HEADS = list('<>AVv^oO#')

    def get_arrow(self, character, dx, dy):
        """return arrow drawing function or None"""
        for head, ddx, ddy, function_name in self.ARROW_TYPES:
            if character == head and dx == ddx and dy == ddy:
                return getattr(self, function_name)

    # - - - - - - - - - fills - - - - - - - - -
    # Fill functions return a list of shapes. Each one if covering one cell
    # size.

    def _hatch_left(self, x, y):
        return self._n_hatch_diagonal(x, y, 1, True)

    def _hatch_right(self, x, y):
        return self._n_hatch_diagonal(x, y, 1, False)

    def _cross_hatch(self, x, y):
        return self._n_hatch_diagonal(x, y, 1, True) + \
               self._n_hatch_diagonal(x, y, 1, False)

    def _double_hatch_left(self, x, y):
        return self._n_hatch_diagonal(x, y, 2, True)

    def _double_hatch_right(self, x, y):
        return self._n_hatch_diagonal(x, y, 2, False)

    def _double_cross_hatch(self, x, y):
        return self._n_hatch_diagonal(x, y, 2, True) + \
               self._n_hatch_diagonal(x, y, 2, False)

    def _triple_hatch_left(self, x, y):
        return self._n_hatch_diagonal(x, y, 3, True)

    def _triple_hatch_right(self, x, y):
        return self._n_hatch_diagonal(x, y, 3, False)

    def _triple_cross_hatch(self, x, y):
        return self._n_hatch_diagonal(x, y, 3, True) + \
               self._n_hatch_diagonal(x, y, 3, False)

    def _n_hatch_diagonal(self, x, y, n, left=False):
        """hatch generator function"""
        d = 1/float(n)
        result = []
        if left:
            for i in range(n):
                result.append(Line(
                    Point(self.left(x), self.top(y+d*i)),
                    Point(self.right(x-d*i), self.bottom(y))
                ))
                if n:
                    result.append(Line(
                        Point(self.right(x-d*i), self.top(y)),
                        Point(self.right(x), self.top(y+d*i))
                    ))
        else:
            for i in range(n):
                result.append(Line(Point(self.left(x), self.top(y+d*i)), Point(self.left(x+d*i), self.top(y))))
                if n:
                    result.append(Line(Point(self.left(x+d*i), self.bottom(y)), Point(self.right(x), self.top(y+d*i))))
        return result

    def _hatch_v(self, x, y):
        return self._n_hatch_straight(x, y, 1, True)

    def _hatch_h(self, x, y):
        return self._n_hatch_straight(x, y, 1, False)

    def _hv_hatch(self, x, y):
        return self._n_hatch_straight(x, y, 1, True) + \
               self._n_hatch_straight(x, y, 1, False)

    def _double_hatch_v(self, x, y):
        return self._n_hatch_straight(x, y, 2, True)

    def _double_hatch_h(self, x, y):
        return self._n_hatch_straight(x, y, 2, False)

    def _double_hv_hatch(self, x, y):
        return self._n_hatch_straight(x, y, 2, True) + \
               self._n_hatch_straight(x, y, 2, False)

    def _triple_hatch_v(self, x, y):
        return self._n_hatch_straight(x, y, 3, True)

    def _triple_hatch_h(self, x, y):
        return self._n_hatch_straight(x, y, 3, False)

    def _triple_hv_hatch(self, x, y):
        return self._n_hatch_straight(x, y, 3, True) + \
               self._n_hatch_straight(x, y, 3, False)

    def _n_hatch_straight(self, x, y, n, vertical=False):
        """hatch generator function"""
        d = 1/float(n)
        offset = 1.0/(n+1)
        result = []
        if vertical:
            for i in range(n):
                i = i + offset
                result.append(Line(
                    Point(self.left(x+d*i), self.top(y)),
                    Point(self.left(x+d*i), self.bottom(y))
                ))
                #~ if n:
                    #~ result.append(Line(Point(self.right(x-d*i), self.top(y)), Point(self.right(x), self.top(y+d*i))))
        else:
            for i in range(n):
                i = i + offset
                result.append(Line(
                    Point(self.left(x), self.top(y+d*i)),
                    Point(self.right(x), self.top(y+d*i))
                ))
                #~ if n:
                    #~ result.append(Line(Point(self.left(x+d*i), self.bottom(y)), Point(self.right(x), self.top(y+d*i))))
        return result

    def _fill_trail(self, x, y):
        return [
            Line(
                Point(self.left(x+0.707), self.top(y)),
                Point(self.right(x), self.bottom(y-0.707))
            ),
            Line(
                Point(self.left(x), self.top(y+0.707)),
                Point(self.right(x-0.707), self.bottom(y))
            )
        ]

    def _fill_foreground(self, x, y):
        return [
            Rectangle(
                Point(self.left(x), self.top(y)),
                Point(self.right(x), self.bottom(y))
            )
        ]

    def _fill_background(self, x, y):
        return []

    def _fill_small_circle(self, x, y):
        return [
            Circle(Point(self.left(x+0.5), self.top(y+0.5)), 0.2)
        ]

    def _fill_medium_circle(self, x, y):
        return [
            Circle(Point(self.left(x+0.5), self.top(y+0.5)), 0.4)
        ]

    def _fill_large_circle(self, x, y):
        return [
            Circle(Point(self.left(x+0.5), self.top(y+0.5)), 0.9)
        ]

    def _fill_qmark(self, x, y):
        return [
            Label(Point(self.left(x), self.bottom(y)), '?')
        ]

    def _fill_triangles(self, x, y):
        return [
            Line(Point(self.left(x+0.5), self.top(y+0.2)), Point(self.left(x+0.75), self.top(y+0.807))),
            Line(Point(self.left(x+0.7), self.top(y+0.807)), Point(self.left(x+0.25), self.top(y+0.807))),
            Line(Point(self.left(x+0.25), self.top(y+0.807)), Point(self.left(x+0.5), self.top(y+0.2))),
        ]

    FILL_TYPES = [
        ('A', '_hatch_left'),
        ('B', '_hatch_right'),
        ('C', '_cross_hatch'),
        ('D', '_double_hatch_left'),
        ('E', '_double_hatch_right'),
        ('F', '_double_cross_hatch'),
        ('G', '_triple_hatch_left'),
        ('H', '_triple_hatch_right'),
        ('I', '_triple_cross_hatch'),
        ('J', '_hatch_v'),
        ('K', '_hatch_h'),
        ('L', '_hv_hatch'),
        ('M', '_double_hatch_v'),
        ('N', '_double_hatch_h'),
        ('O', '_double_hv_hatch'),
        ('P', '_triple_hatch_v'),
        ('Q', '_triple_hatch_h'),
        ('R', '_triple_hv_hatch'),
        ('S', '_fill_qmark'),
        ('T', '_fill_trail'),
        ('U', '_fill_small_circle'),
        ('V', '_fill_medium_circle'),
        ('W', '_fill_large_circle'),
        ('X', '_fill_foreground'),
        ('Y', '_fill_triangles'),
        ('Z', '_fill_background'),
    ]

    FILL_CHARACTERS = ''.join([t+t.lower() for (t, f) in FILL_TYPES])

    def get_fill(self, character):
        """return fill function"""
        for head, function_name in self.FILL_TYPES:
            if character == head:
                return getattr(self, function_name)
        raise ValueError('no such fill type')

    # - - - - - - - - - fixed characters and their shapes - - - - - - - - -

    def _open_triangle_left(self, x, y):
        return [
            Line(
                Point(self.left(x), self.vcenter(y)),
                Point(self.right(x), self.top(y))
            ),
            Line(
                Point(self.left(x), self.vcenter(y)),
                Point(self.right(x), self.bottom(y))
            )
        ]
    def _open_triangle_right(self, x, y):
        return [
            Line(
                Point(self.right(x), self.vcenter(y)),
                Point(self.left(x), self.top(y))
            ),
            Line(
                Point(self.right(x), self.vcenter(y)),
                Point(self.left(x), self.bottom(y))
            )
        ]

    def _circle(self, x, y):
        return [
            Circle(Point(self.hcenter(x), self.vcenter(y)), NOMINAL_SIZE/2.0)
        ]


    FIXED_TYPES = [
        ('{', '_open_triangle_left'),
        ('}', '_open_triangle_right'),
        ('*', '_circle'),
    ]
    FIXED_CHARACTERS = ''.join([t for (t, f) in FIXED_TYPES])

    def get_fixed_character(self, character):
        """return fill function"""
        for head, function_name in self.FIXED_TYPES:
            if character == head:
                return getattr(self, function_name)
        raise ValueError('no such character')

    # - - - - - - - - - helper function for shape recognition - - - - - - - - -

    def _follow_vertical_line(self, x, y):
        """find a vertical line with optional arrow heads"""
        # follow line to the bottom
        _, end_y, line_end_style = self._follow_line(x, y, dy=1, line_character='|')
        # follow line to the top
        _, start_y, line_start_style = self._follow_line(x, y, dy=-1, line_character='|')
        # if a '+' follows a line, then the line is stretched to hit the '+' center
        start_y_fix = end_y_fix = 0
        if self.get(x, start_y - 1) == '+':
            start_y_fix = -0.5
        if self.get(x, end_y + 1) == '+':
            end_y_fix = 0.5
        # tag characters as used (not the arrow heads)
        self.tag([(x, y) for y in range(start_y, end_y + 1)], CLASS_LINE)
        # return the new shape object with arrows etc.
        p1 = complex(self.hcenter(x), self.top(start_y + start_y_fix))
        p2 = complex(self.hcenter(x), self.bottom(end_y + end_y_fix))
        shapes = []
        if line_start_style:
            p1, arrow_shapes = line_start_style(p1, p2)
            shapes.extend(arrow_shapes)
        if line_end_style:
            p2, arrow_shapes = line_end_style(p2, p1)
            shapes.extend(arrow_shapes)
        shapes.append(Line(p1, p2))
        return group(shapes)

    def _follow_horizontal_line(self, x, y, thick=False):
        """find a horizontal line with optional arrow heads"""
        if thick:
            line_character = '='
        else:
            line_character = '-'
        # follow line to the right
        end_x, _, line_end_style = self._follow_line(x, y, dx=1, line_character=line_character)
        # follow line to the left
        start_x, _, line_start_style = self._follow_line(x, y, dx=-1, line_character=line_character)
        start_x_fix = end_x_fix = 0
        if self.get(start_x - 1, y) == '+':
            start_x_fix = -0.5
        if self.get(end_x + 1, y) == '+':
            end_x_fix = 0.5
        self.tag([(x, y) for x in range(start_x, end_x+1)], CLASS_LINE)
        # return the new shape object with arrows etc.
        p1 = complex(self.left(start_x + start_x_fix), self.vcenter(y))
        p2 = complex(self.right(end_x + end_x_fix), self.vcenter(y))
        shapes = []
        if line_start_style:
            p1, arrow_shapes = line_start_style(p1, p2)
            shapes.extend(arrow_shapes)
        if line_end_style:
            p2, arrow_shapes = line_end_style(p2, p1)
            shapes.extend(arrow_shapes)
        shapes.append(Line(p1, p2, thick=thick))
        return group(shapes)

    def _follow_lower_horizontal_line(self, x, y):
        """find a horizontal line, the line is aligned to the bottom and a bit
           wider, so that it can be used for shapes like this:
              ___
           __|   |___
        """
        # follow line to the right
        end_x, _, line_end_style = self._follow_line(x, y, dx=1, line_character='_', arrows=False)
        # follow line to the left
        start_x, _, line_start_style = self._follow_line(x, y, dx=-1, line_character='_', arrows=False)
        self.tag([(x, y) for x in range(start_x, end_x+1)], CLASS_LINE)
        # return the new shape object with arrows etc.
        p1 = complex(self.hcenter(start_x-1), self.bottom(y))
        p2 = complex(self.hcenter(end_x+1), self.bottom(y))
        return [Line(p1, p2)]

    def _follow_upper_horizontal_line(self, x, y):
        """find a horizontal line, the line is aligned to the bottom and a bit
           wider, so that it can be used for shapes like this:

             |~~~|
           ~~     ~~~
        """
        # follow line to the right
        end_x, _, line_end_style = self._follow_line(x, y, dx=1, line_character='~', arrows=False)
        # follow line to the left
        start_x, _, line_start_style = self._follow_line(x, y, dx=-1, line_character='~', arrows=False)
        self.tag([(x, y) for x in range(start_x, end_x+1)], CLASS_LINE)
        # return the new shape object with arrows etc.
        p1 = complex(self.hcenter(start_x-1), self.top(y))
        p2 = complex(self.hcenter(end_x+1), self.top(y))
        return [Line(p1, p2)]

    def _follow_line(self, x, y, dx=0, dy=0, line_character=None, arrows=True):
        """helper function for all the line functions"""
        # follow line in the given direction
        while 0 <= x < self.width and 0<= y < self.height and self.get(x+dx, y+dy) == line_character:
            x += dx
            y += dy
        if arrows:
            # check for arrow head
            following_character = self.get(x + dx, y + dy)
            if following_character in self.ARROW_HEADS:
                line_end_style = self.get_arrow(following_character, dx, dy)
                if line_end_style:
                    x += dx
                    y += dy
            else:
                line_end_style = None
        else:
            line_end_style = None
        return x, y, line_end_style

    def _plus_joiner(self, x, y):
        """adjacent '+' signs are connected with a line from center to center
           required for images like these:

              +---+         The box should be closed on all sides
              |   +--->     and the arrow start should touch the box
              +---+
        """
        result = []
        #~ for dx, dy in ((1,0), (-1,0), (0,1), (0,-1)):
        # looking right and down is sufficient as the scan is done from left to
        # right, top to bottom
        for dx, dy in ((1, 0), (0, 1)):
            if self.get(x + dx, y + dy) == '+':
                result.append(Line(
                    Point(self.hcenter(x), self.vcenter(y)),
                    Point(self.hcenter(x + dx), self.vcenter(y + dy))
                ))
        self.tag([(x, y)], CLASS_JOIN)
        return result


    def _follow_fill(self, character, start_x, start_y):
        """fill shapes like the ones below with a pattern. when the character is
           upper case, draw a border too.

            XXX  aaa  BB
           XXX    a
        """
        fill = self.get_fill(character.upper())
        border = character.isupper()
        result = []
        # flood fill algorithm, searching for similar characters
        coordinates = []
        to_scan = [(start_x, start_y)]
        while to_scan:
            x, y = to_scan.pop()
            if self.cls(x, y) is None:
                if self.get(x, y) == character:
                    result.extend(fill(x, y))
                    self.tag([(x, y)], CLASS_RECTANGLE)
                if self.get(x + 1, y) == character:
                    if self.cls(x + 1, y) is None:
                        to_scan.append((x + 1, y))
                elif border:
                    result.append(Line(
                        Point(self.right(x), self.top(y)),
                        Point(self.right(x), self.bottom(y))))
                if self.get(x - 1, y) == character:
                    if self.cls(x - 1, y) is None:
                        to_scan.append((x - 1, y))
                elif border:
                    result.append(Line(
                        Point(self.left(x), self.top(y)),
                        Point(self.left(x), self.bottom(y))))
                if self.get(x, y + 1) == character:
                    if self.cls(x, y + 1) is None:
                        to_scan.append((x, y + 1))
                elif border:
                    result.append(Line(
                        Point(self.left(x), self.bottom(y)),
                        Point(self.right(x), self.bottom(y))))
                if self.get(x, y - 1) == character:
                    if self.cls(x, y - 1) is None:
                        to_scan.append((x, y - 1))
                elif border:
                    result.append(Line(
                        Point(self.left(x), self.top(y)),
                        Point(self.right(x), self.top(y))))
        return group(result)

    def _follow_horizontal_string(self, start_x, y, accept_anything=False, quoted=False):
        """find a string. may contain single spaces, but the detection is
           aborted after more than one space.

              Text one   "Text two"

           accept_anything means that all non space characters are interpreted
           as text.
        """
        # follow line from left to right
        if quoted:
            quotation_character = self.get(start_x, y)
            x = start_x + 1
        else:
            quotation_character = None
            x = start_x
        text = []
        if self.get(x, y) != ' ':
            text.append(self.get(x, y))
            self.tag([(x, y)], CLASS_STRING)
            is_first_space = True
            while 0 <= x + 1 < self.width and self.cls(x + 1, y) is None:
                if not quoted:
                    if self.get(x + 1, y) == ' ' and not is_first_space:
                        break
                    if not accept_anything and not self.get(x + 1, y).isalnum():
                        break
                x += 1
                character = self.get(x, y)
                if character == quotation_character:
                    self.tag([(x, y)], CLASS_STRING)
                    break
                text.append(character)
                if character == ' ':
                    is_first_space = False
                else:
                    is_first_space = True
            if text[-1] == ' ':
                del text[-1]
                x -= 1
            self.tag([(x, y) for x in range(start_x, x + 1)], CLASS_STRING)
            return [Label(
                Point(self.left(start_x), self.bottom(y)),
                ''.join(text)
            )]
        else:
            return []

    def _follow_rounded_edge(self, x, y):
        """check for rounded edges:
            /-    |     -\-    |   and also \    /  etc.
            |    -/      |     \-            -  |
        """
        result = []
        if self.get(x, y) == '/':
            # rounded rectangles
            if (self.get(x + 1, y) == '-' and self.get(x, y + 1) == '|'):
                # upper left corner
                result.append(Arc(
                    Point(self.hcenter(x), self.bottom(y)), 90,
                    Point(self.right(x), self.vcenter(y)),  180
                ))
            if self.get(x - 1, y) == '-' and self.get(x, y - 1) == '|':
                # lower right corner
                result.append(Arc(
                    Point(self.hcenter(x), self.top(y)),  -90,
                    Point(self.left(x), self.vcenter(y)), 0
                ))
            if not result:
                # if used as diagonal line
                p1 = p2 = None
                a1 = a2 = 0
                arc = c1 = c2 = False
                if self.get(x + 1, y - 1) == '|':
                    p1 = Point(self.hcenter(x + 1), self.top(y))
                    a1 = -90
                    arc = c1 = True
                elif self.get(x + 1, y - 1) == '+':
                    p1 = Point(self.hcenter(x + 1), self.vcenter(y - 1))
                    a1 = -135
                elif self.get(x + 1, y - 1) == '-':
                    p1 = Point(self.right(x), self.vcenter(y - 1))
                    a1 = 180
                    arc = c1 = True
                elif self.get(x + 1, y - 1) == '/':
                    p1 = Point(self.right(x), self.top(y))
                    a1 = -135
                    c1 = True
                elif self.get(x + 1, y) == '|':
                    p1 = Point(self.hcenter(x + 1), self.top(y))
                elif self.get(x, y - 1) == '-':
                    p1 = Point(self.right(x), self.vcenter(y - 1))

                if self.get(x - 1, y + 1) == '|':
                    p2 = Point(self.hcenter(x - 1), self.top(y + 1))
                    a2 = 90
                    arc = c2 = True
                elif self.get(x - 1, y + 1) == '+':
                    p2 = Point(self.hcenter(x - 1), self.vcenter(y + 1))
                    a2 = 45
                elif self.get(x - 1, y + 1) == '-':
                    p2 = Point(self.left(x), self.vcenter(y + 1))
                    a2 = 0
                    arc = c2 = True
                elif self.get(x - 1, y + 1) == '/':
                    p2 = Point(self.left(x), self.bottom(y))
                    a2 = 45
                    c2 = True
                elif self.get(x - 1, y) == '|':
                    p2 = Point(self.hcenter(x - 1), self.bottom(y))
                elif self.get(x, y + 1) == '-':
                    p2 = Point(self.left(x), self.vcenter(y + 1))

                if p1 or p2:
                    if not p1:
                        p1 = Point(self.right(x), self.top(y))
                    if not p2:
                        p2 = Point(self.left(x), self.bottom(y))
                    if arc:
                        result.append(Arc(p1, a1, p2, a2, c1, c2))
                    else:
                        result.append(Line(p1, p2))
        else: # '\'
            # rounded rectangles
            if self.get(x-1, y) == '-' and self.get(x, y + 1) == '|':
                # upper right corner
                result.append(Arc(
                    Point(self.hcenter(x), self.bottom(y)), 90,
                    Point(self.left(x), self.vcenter(y)),   0
                ))
            if self.get(x+1, y) == '-' and self.get(x, y - 1) == '|':
                # lower left corner
                result.append(Arc(
                    Point(self.hcenter(x), self.top(y)),   -90,
                    Point(self.right(x), self.vcenter(y)), 180
                ))
            if not result:
                # if used as diagonal line
                p1 = p2 = None
                a1 = a2 = 0
                arc = c1 = c2 = False
                if self.get(x - 1, y - 1) == '|':
                    p1 = Point(self.hcenter(x-1), self.top(y))
                    a1 = -90
                    arc = c1 = True
                elif self.get(x - 1, y - 1) == '+':
                    p1 = Point(self.hcenter(x-1), self.vcenter(y - 1))
                    a1 = -45
                elif self.get(x - 1, y - 1) == '-':
                    p1 = Point(self.left(x), self.vcenter(y-1))
                    a1 = 0
                    arc = c1 = True
                elif self.get(x - 1, y - 1) == '\\':
                    p1 = Point(self.left(x), self.top(y))
                    a1 = -45
                    c1 = True
                elif self.get(x - 1, y) == '|':
                    p1 = Point(self.hcenter(x-1), self.top(y))
                elif self.get(x, y - 1) == '-':
                    p1 = Point(self.left(x), self.hcenter(y - 1))

                if self.get(x + 1, y + 1) == '|':
                    p2 = Point(self.hcenter(x+1), self.top(y + 1))
                    a2 = 90
                    arc = c2 = True
                elif self.get(x + 1, y + 1) == '+':
                    p2 = Point(self.hcenter(x+1), self.vcenter(y + 1))
                    a2 = 135
                elif self.get(x + 1, y + 1) == '-':
                    p2 = Point(self.right(x), self.vcenter(y + 1))
                    a2 = 180
                    arc = c2 = True
                elif self.get(x + 1, y + 1) == '\\':
                    p2 = Point(self.right(x), self.bottom(y))
                    a2 = 135
                    c2 = True
                elif self.get(x + 1, y) == '|':
                    p2 = Point(self.hcenter(x+1), self.bottom(y))
                elif self.get(x, y + 1) == '-':
                    p2 = Point(self.right(x), self.vcenter(y + 1))

                if p1 or p2:
                    if not p1:
                        p1 = Point(self.left(x), self.top(y))
                    if not p2:
                        p2 = Point(self.right(x), self.bottom(y))
                    if arc:
                        result.append(Arc(p1, a1, p2, a2, c1, c2))
                    else:
                        result.append(Line(p1, p2))
        if result:
            self.tag([(x, y)], CLASS_JOIN)
        return group(result)


def process(input, visitor_class, options=None):
    """\
    Parse input and render using the given visitor class.

    :param input: String or file like object with the image as text.

    :param visitor_class: A class object, it will be used to render the
        resulting image.

    :param options: A dictionary containing the settings. When ``None`` is
        given, defaults are used.

    :returns: instantiated ``visitor_class`` and the image has already been
        processed with the visitor.

    :exception: This function can raise an ``UnsupportedFormatError`` exception
        if the specified format is not supported.
    """

    # remember user options (don't want to rename function parameter above)
    user_options = options
    # start with a copy of the defaults
    options = DEFAULT_OPTIONS.copy()
    if user_options is not None:
        # override with settings passed by caller
        options.update(user_options)

    if 'fill' not in options or options['fill'] is None:
        options['fill'] = options['foreground']

    # if input is a file like object, read from it (otherwise it is assumed to
    # be a string)
    if hasattr(input, 'read'):
        input = input.read()

    if options['debug']:
        sys.stderr.write('%r\n' % (input,))

    aaimg = AsciiArtImage(input, options['aspect'], options['textual'], options['widechars'])

    if options['debug']:
        sys.stderr.write('%s\n' % (aaimg,))
    aaimg.recognize()

    visitor = visitor_class(options)
    visitor.visit_image(aaimg)
    return visitor


def render(input, output=None, options=None):
    """
    Render an ASCII art figure to a file or file-like.

    :param input: If ``input`` is a basestring subclass (str or unicode), the
        text contained in ``input`` is rendered. If ``input is a file-like
        object, the text to render is taken using ``input.read()``.

    :param output: If no ``output`` is specified, the resulting rendered image
        is returned as a string. If output is a basestring subclass, a file
        with the name of ``output`` contents is created and the rendered image
        is saved there. If ``output`` is a file-like object, ``output.write()``
        is used to save the rendered image.

    :param options: A dictionary containing the settings. When ``None`` is
        given, defaults are used.

    :returns: This function returns a tuple ``(visitor, output)``, where
        ``visitor`` is visitor instance that rendered the image and ``output``
        is the image as requested by the ``output`` parameter (a ``str`` if it
        was ``None``, or a file-like object otherwise, which you should
        ``close()`` if needed).

    :exception: This function can raise an ``UnsupportedFormatError`` exception
        if the specified format is not supported.
    """

    if options is None:
        options = {}

    close_output = False
    if output is None:
        import StringIO
        options['file_like'] = StringIO.StringIO()
    elif isinstance(output, basestring):
        options['file_like'] = file(output, 'wb')
        close_output = True
    else:
        options['file_like'] = output
    try:
        # late import of visitor classes to not cause any import errors for
        # unsupported backends (this would happen when a library a backend
        # depends on is not installed)
        if options['format'].lower() == 'svg':
            import svg
            visitor_class = svg.SVGOutputVisitor
        elif options['format'].lower() == 'pdf':
            import pdf
            visitor_class = pdf.PDFOutputVisitor
        elif options['format'].lower() == 'ascii':
            import aa
            visitor_class = aa.AsciiOutputVisitor
        else:
            # for all other formats, it may be a bitmap type. let
            # PIL decide if it can write a file of that type.
            import pil
            visitor_class = pil.PILOutputVisitor
        # now render and output the image
        visitor = process(input, visitor_class, options)
    finally:
        if close_output:
            options['file_like'].close()
    return (visitor, options['file_like'])


def main():
    """implement an useful main for use as command line program"""
    import sys
    import optparse
    import os.path

    parser = optparse.OptionParser(
        usage = "%prog [options] [file]",
        version = """\
%prog 0.5

Copyright (C) 2006-2010 aafigure-team

Redistribution and use in source and binary forms, with or without
modification, are permitted under the terms of the BSD License.

THIS SOFTWARE IS PROVIDED BY THE AAFIGURE-TEAM ''AS IS'' AND ANY
EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE AAFIGURE-TEAM BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
""",
    description = "ASCII art to image (SVG, PNG, JPEG, PDF and more) converter."
    )

    parser.add_option("-e", "--encoding",
        dest = "encoding",
        action = "store",
        help = "character encoding of input text",
        default = DEFAULT_OPTIONS['encoding'],
    )

    parser.add_option("-w", "--wide-chars",
        dest = "widechars",
        action = "store",
        help = "unicode properties to be treated as wide glyph (e.g. 'F,W,A')",
        default = DEFAULT_OPTIONS['widechars'],
    )

    parser.add_option("-o", "--output",
        dest = "output",
        metavar = "FILE",
        help = "write output to FILE"
    )

    parser.add_option("-t", "--type",
        dest = "format",
        help = "filetype: png, jpg, svg (by default autodetect from filename)",
        default = None,
    )

    parser.add_option("-D", "--debug",
        dest = "debug",
        action = "store_true",
        help = "enable debug outputs",
        default = DEFAULT_OPTIONS['debug'],
    )

    parser.add_option("-T", "--textual",
        dest = "textual",
        action = "store_true",
        help = "disable horizontal fill detection",
        default = DEFAULT_OPTIONS['textual'],
    )

    parser.add_option("-s", "--scale",
        dest = "scale",
        action = "store",
        type = 'float',
        help = "set scale",
        default = DEFAULT_OPTIONS['scale'],
    )

    parser.add_option("-a", "--aspect",
        dest = "aspect",
        action = "store",
        type = 'float',
        help = "set aspect ratio",
        default = DEFAULT_OPTIONS['aspect'],
    )

    parser.add_option("-l", "--linewidth",
        dest = "line_width",
        action = "store",
        type = 'float',
        help = "set width, svg only",
        default = DEFAULT_OPTIONS['line_width'],
    )

    parser.add_option("--proportional",
        dest = "proportional",
        action = "store_true",
        help = "use proportional font instead of fixed width",
        default = DEFAULT_OPTIONS['proportional'],
    )

    parser.add_option("-f", "--foreground",
        dest = "foreground",
        action = "store",
        help = "foreground color default=%default",
        default = DEFAULT_OPTIONS['foreground'],
    )

    parser.add_option("-x", "--fill",
        dest = "fill",
        action = "store",
        help = "foreground color default=foreground",
        default = None,
    )

    parser.add_option("-b", "--background",
        dest = "background",
        action = "store",
        help = "foreground color default=%default",
        default = DEFAULT_OPTIONS['background'],
    )

    parser.add_option("-O", "--option",
        dest = "_extra_options",
        action = "append",
        help = "pass special options to backends (expert user)",
    )

    (options, args) = parser.parse_args()

    if len(args) > 1:
        parser.error("too many arguments")

    if options.format is None:
        if options.output is None:
            parser.error("Please specify output format with --type")
        else:
            options.format = os.path.splitext(options.output)[1][1:]

    if args:
        _input = file(args[0])
    else:
        _input = sys.stdin
    input = codecs.getreader(options.encoding)(_input)

    if options.output is None:
        output = sys.stdout
    else:
        output = file(options.output, 'wb')

    # explicit copying of parameters to the options dictionary
    options_dict = {}
    for key in ('widechars', 'textual', 'proportional',
                'line_width', 'aspect', 'scale',
                'format', 'debug'):
        options_dict[key] = getattr(options, key)
    # ensure all color parameters start with a '#'
    # this is for the convenience of the user as typing the shell comment
    # character isn't for everyone ;-)
    for color in ('foreground', 'background', 'fill'):
        value = getattr(options, color)
        if value is not None:
            if value[0] != '#':
                options_dict[color] = '#%s' % value
            else:
                options_dict[color] = value
    # copy extra options
    if options._extra_options is not None:
        for keyvalue in options._extra_options:
            try:
                key, value = keyvalue.split('=')
            except ValueError:
                parser.error('--option must be in the format <key>=<value> (not %r)' % (keyvalue,))
            options_dict[key] = value

    if options.debug:
        sys.stderr.write('options=%r\n' % (options_dict,))

    try:
        (visitor, output) = render(input, output, options_dict)
        output.close()
    except UnsupportedFormatError, e:
        print "ERROR: Can't output format '%s': %s" % (options.format, e)


# when module is run, run the command line tool
if __name__ == '__main__':
    main()
