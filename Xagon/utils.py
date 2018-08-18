#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math


def quadrant(angle, floor=True):
    """
        Convert an angle to quadrant

        args:
            angle (from 0 to 2*pi)
            ceil (if True return an integer)

        return:
            the quadrant number (from 0 to 5)
    """
    quadrant = (angle / math.pi * 3) % 6

    if floor:
        return math.floor(quadrant)

    return quadrant


def angle(quadrant):
    """
        Convert a quadrant number to angle

        args:
            quadrant (the quadrant number)

        return:
            an angle (from 0 to 2*pi)
    """
    return quadrant * math.pi / 3


def intersect(linea, lineb):
    """
        Return the intersection point of two lines

        args:
            linea (an array of two points)
            lineb (an array of two points)

        return:
            the intersection point of linea and lineb
    """
    xdiff = (linea[0][0] - linea[1][0], lineb[0][0] - lineb[1][0])
    ydiff = (linea[0][1] - linea[1][1], lineb[0][1] - lineb[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    # If linea has a length of 0, that's our intersect point
    if div == 0:
        return linea[0][0], linea[0][1]

    d = (det(*linea), det(*lineb))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div

    return x, y
