"""\
Bitmap renderer for the aafigure package, using the Python Imaging Library.

(C) 2006 Chris Liechti <cliechti@gmx.net>

This is open source software under the BSD license. See LICENSE.txt for more
details.
"""

import sys
from error import UnsupportedFormatError
PIL_OK = False
try:
    import Image, ImageDraw
    PIL_OK = True
except ImportError:
    pass
if PIL_OK is False:
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        raise UnsupportedFormatError('please install PIL to get bitmaps output support')
import PILhelper


class PILOutputVisitor:
    """Render a list of shapes as bitmap.
    """

    def __init__(self, options):
        self.options = options
        self.scale = options['scale']*8
        self.debug = options['debug']
        self.line_width = options['line_width']
        self.foreground = options['foreground']
        self.background = options['background']
        self.fillcolor = options['fill']

    def _num(self, number):
        return number * self.scale

    def visit_image(self, aa_image):
        """Process the given ASCIIArtFigure and draw the shapes in
           the bitmap file
        """
        self.aa_image = aa_image        # save for later XXX not optimal to do it here
        self.width = (aa_image.width+1)*aa_image.nominal_size*aa_image.aspect_ratio
        self.height = (aa_image.height+1)*aa_image.nominal_size

        # if font is given explicit, use it instead of proportional flag
        font_size = int(self._num(self.aa_image.nominal_size*1.1))
        if 'font' in self.options:
            self.font = PILhelper.font_by_name(self.options['font'], font_size)
        else:
            self.font = PILhelper.font_by_type(self.options['proportional'], font_size)
        if self.font is None:
            sys.stderr.write("WARNING: font not found, using PIL default font\n")

        self.image = Image.new(
            'RGB',
            (int(self._num(self.width)), int(self._num(self.height))),
            self.background
        )
        self.draw = ImageDraw.Draw(self.image)

        #~ if self.debug:
            #~ #draw a rectangle around entire image
            #~ self._rectangle(
                #~ 0,0,
                #~ aa_image.width, aa_image.height,
                #~ style = 'fill:none;',
            #~ )

        self.visit_shapes(aa_image.shapes)
        del self.draw
        file_type = self.options['format'].lower()
        if file_type == 'jpg': file_type = 'jpeg' # alias
        try:
            if 'file_like' in self.options:
                self.image.save(self.options['file_like'], file_type)
        except KeyError:
            raise UnsupportedFormatError("PIL doesn't support image format %r" %
                    file_type)

    def visit_shapes(self, shapes):
        for shape in shapes:
            shape_name = shape.__class__.__name__.lower()
            visitor_name = 'visit_%s' % shape_name
            if hasattr(self, visitor_name):
                getattr(self, visitor_name)(shape)
            else:
                sys.stderr.write("WARNING: don't know how to handle shape %r\n"
                    % shape)

    def visit_group(self, group):
        self.visit_shapes(group.shapes)

    # - - - - - - drawing helpers - - - - - - -
    def _line(self, x1, y1, x2, y2):
        """Draw a line, coordinates given as four decimal numbers"""
        self.draw.line((self._num(x1), self._num(y1),
                        self._num(x2), self._num(y2)),
                       fill=self.foreground) #self.line_width

    def _rectangle(self, x1, y1, x2, y2):
        """Draw a rectangle, coordinates given as four decimal numbers.
           ``style`` is inserted in the SVG. It could be e.g. "fill:yellow"
        """
        self.draw.rectangle((self._num(x1), self._num(y1),
                             self._num(x2), self._num(y2)),
                            fill=self.fillcolor,
                            outline=self.foreground) #self.line_width

    # - - - - - - visitor function for the different shape types - - - - - - -

    def visit_point(self, point):
        dotsize = 2
        self.draw.ellipse(
            (
                self._num(point.x)-dotsize, self._num(point.y)-dotsize,
                self._num(point.x)+dotsize, self._num(point.y)+dotsize
            ),
            fill=self.foreground
        )

    def visit_line(self, line):
        x1, x2 = line.start.x, line.end.x
        y1, y2 = line.start.y, line.end.y
        self._line(x1, y1, x2, y2)

    def visit_rectangle(self, rectangle):
        self._rectangle(
            rectangle.p1.x, rectangle.p1.y,
            rectangle.p2.x, rectangle.p2.y,
        )


    def visit_circle(self, circle):
        self.draw.ellipse(
            (
                self._num(circle.center.x-circle.radius), self._num(circle.center.y-circle.radius),
                self._num(circle.center.x+circle.radius), self._num(circle.center.y+circle.radius)
            ),
            fill=self.fillcolor,
            outline=self.foreground,
        )

    def visit_label(self, label):
        #  font-weight="bold"
        self.draw.text(
            (self._num(label.position.x), self._num(label.position.y-self.aa_image.nominal_size*1.1)),
            label.text,
            fill=self.foreground,
            font=self.font
        )

    def _bezier(self, p1, c1, c2, p2, level=1):
        # de Casteljau's algorithm
        if self._num(p1.distance(p2)) <= 3:
            self._line(p1.x, p1.y, p2.x, p2.y)
        else:
            cmid = c1.midpoint(c2)
            lp1 = p1
            lc1 = p1.midpoint(c1)
            lc2 = lc1.midpoint(cmid)
            rp2 = p2
            rc2 = p2.midpoint(c2)
            rc1 = rc2.midpoint(cmid)
            lp2 = rc1.midpoint(lc2)
            rp1 = lp2
            self._bezier(lp1, lc1, lc2, lp2, level + 1)
            self._bezier(rp1, rc1, rc2, rp2, level + 1)
        
    def visit_arc(self, arc):
        p1, p2 = arc.start, arc.end
        c1 = arc.start_control_point()
        c2 = arc.end_control_point()
        self._bezier(p1, c1, c2, p2)
