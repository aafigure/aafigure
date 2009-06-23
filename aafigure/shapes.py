# Common shapes for the aafigure package.
#
# (C) 2009 Chris Liechti <cliechti@gmx.net>
#
# This is open source software under the BSD license. See LICENSE.txt for more
# details.
#
# This intentionally is no doc comment to make it easier to include the module
# in Sphinx ``.. automodule::``

def point(object):
    """return a Point instance.
       - if object is already a Point instance it's returned as is
       - complex numbers are converted to Points
       - a tuple with two elements (x,y)
    """
    if isinstance(object, Point):
        return object
    #~ print type(object), object.__class__
    if type(object) is complex:
        return Point(object.real, object.imag)
    if type(object) is tuple and len(object) == 2:
        return Point(object[0], object[1])
    raise ValueError('can not convert %r to a Point')


def group(list_of_shapes):
    """return a group if the number of shapes is greater than one"""
    if len(list_of_shapes) > 1:
        return [Group(list_of_shapes)]
    else:
        return list_of_shapes


class Point:
    """A single point. This class primary use is to represent coordinates
       for the other shapes.
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return 'Point(%r, %r)' % (self.x, self.y)


class Line:
    """Line with starting and ending point. Both ends can have arrows"""
    def __init__(self, start, end, thick=False):
        self.thick = thick
        self.start = point(start)
        self.end = point(end)

    def __repr__(self):
        return 'Line(%r, %r)' % (self.start, self.end)


class Rectangle:
    """Rectangle with two edge coordinates."""
    def __init__(self, p1, p2):
        self.p1 = point(p1)
        self.p2 = point(p2)
    def __repr__(self):
        return 'Rectangle(%r, %r)' % (self.p1, self.p2)


class Circle:
    """Circle with center coordinates and radius."""
    def __init__(self, center, radius):
        self.center = point(center)
        self.radius = radius

    def __repr__(self):
        return 'Circle(%r, %r)' % (self.center, self.radius)


class Label:
    """A text label at a position"""
    def __init__(self, position, text):
        self.position = position
        self.text = text
    def __repr__(self):
        return 'Label(%r, %r)' % (self.position, self.text)


class Group:
    """A group of shapes"""
    def __init__(self, shapes=None):
        if shapes is None: shapes = []
        self.shapes = shapes
    def __repr__(self):
        return 'Group(%r)' % (self.shapes,)
