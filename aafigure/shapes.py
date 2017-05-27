# Common shapes for the aafigure package.
#
# This file is part of aafigure. https://github.com/aafigure/aafigure
# (C) 2009 Chris Liechti <cliechti@gmx.net>
#
# SPDX-License-Identifier:    BSD-3-Clause
#
# This intentionally is no doc comment to make it easier to include the module
# in Sphinx ``.. automodule::``
import math


def point(obj):
    """\
    return a Point instance.
    - if object is already a Point instance it's returned as is
    - complex numbers are converted to Points
    - a tuple with two elements (x,y)
    """
    if isinstance(obj, Point):
        return obj
    if type(obj) is complex:
        return Point(obj.real, obj.imag)
    if type(obj) is tuple and len(obj) == 2:
        return Point(obj[0], obj[1])
    raise ValueError('can not convert {!r} to a Point'.format(obj))


def group(list_of_shapes):
    """return a group if the number of shapes is greater than one"""
    if len(list_of_shapes) > 1:
        return [Group(list_of_shapes)]
    else:
        return list_of_shapes


class Point:
    """\
    A single point. This class primary use is to represent coordinates
    for the other shapes.
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return 'Point({p.x!r}, {p.y!r})'.format(p=self)

    def distance(self, other):
        return math.sqrt((self.x - other.x) ** 2 +
                         (self.y - other.y) ** 2)

    def midpoint(self, other):
        return Point((self.x + other.x) / 2,
                     (self.y + other.y) / 2)


class Line:
    """Line with starting and ending point. Both ends can have arrows"""
    def __init__(self, start, end, thick=False):
        self.thick = thick
        self.start = point(start)
        self.end = point(end)

    def __repr__(self):
        return 'Line({l.start!r}, {l.end!r})'.format(l=self)


class Rectangle:
    """Rectangle with two edge coordinates."""
    def __init__(self, p1, p2):
        self.p1 = point(p1)
        self.p2 = point(p2)

    def __repr__(self):
        return 'Rectangle({r.p1!r}, {r.p2!r})'.format(r=self)


class Circle:
    """Circle with center coordinates and radius."""
    def __init__(self, center, radius):
        self.center = point(center)
        self.radius = radius

    def __repr__(self):
        return 'Circle({c.center!r}, {c.radius!r})'.format(c=self)


class Label:
    """A text label at a position"""
    def __init__(self, position, text):
        self.position = position
        self.text = text

    def __repr__(self):
        return 'Label({t.position!r}, {t.text!r})'.format(t=self)


class Group:
    """A group of shapes"""
    def __init__(self, shapes=None):
        if shapes is None:
            shapes = []
        self.shapes = shapes

    def __repr__(self):
        return 'Group({!r})'.format(self.shapes)


class Arc:
    """A smooth arc between two points"""
    def __init__(self, start, start_angle, end, end_angle, start_curve=True, end_curve=True):
        self.start = point(start)
        self.end = point(end)
        self.start_angle = start_angle
        self.end_angle = end_angle
        self.start_curve = start_curve
        self.end_curve = end_curve

    def __repr__(self):
        return 'Arc({a.start!r}, {a.start_angle!r}, ' \
               '{a.end!r}, {a.end_angle!r}, {a.start_curve!r}, ' \
               '{a.end_curve!r})'.format(a=self)

    def start_angle_rad(self):
        return self.start_angle * math.pi / 180

    def end_angle_rad(self):
        return self.end_angle * math.pi / 180

    def __tension(self):
        return self.start.distance(self.end) / 3

    # assumptions: x increases going right, y increases going down
    def start_control_point(self):
        if self.start_curve:
            dd = self.__tension()
            angle = self.start_angle_rad()
            return Point(self.start.x + dd * math.cos(angle),
                         self.start.y - dd * math.sin(angle))
        else:
            return self.start

    def end_control_point(self):
        if self.end_curve:
            dd = self.__tension()
            angle = self.end_angle_rad()
            return Point(self.end.x + dd * math.cos(angle),
                         self.end.y - dd * math.sin(angle))
        else:
            return self.end
