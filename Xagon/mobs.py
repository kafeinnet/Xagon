#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math

import pyxel

from .utils import quadrant, angle, intersect


class Obstacle(object):
    _at_border = False

    def __init__(self, app, quadrant, pos, height=0.1, color=9):
        self.quadrant = quadrant
        self.pos = pos
        self.height = height
        self.color = color
        self.app = app

    @property
    def at_border(self):
        """
            Return if the obstacle is at the tunnel border
        """
        return self._at_border

    def draw(self):
        """
            Draw the obstacle as an hexagon portion from the current quadrant
            to the next
        """
        tunnel_length = self.app.radius - self.app.inner_radius

        # Inner border
        rpos = pow(self.pos, 4)
        if rpos > 1:
            rpos = 1
        radiusa = rpos * tunnel_length + self.app.inner_radius

        # Outter border
        posb = self.pos + self.height
        rposb = pow(posb, 4)
        if rposb > 1:
            rposb = 1
            self._at_border = True
        radiusb = rposb * tunnel_length + self.app.inner_radius

        # 4 corners position calculation
        i = angle(self.quadrant)
        xaa = self.app.center_x + (math.cos(i) * radiusa)
        yaa = self.app.center_y + (math.sin(i) * radiusa)
        xba = self.app.center_x + (math.cos(i) * radiusb)
        yba = self.app.center_y + (math.sin(i) * radiusb)
        i = angle(self.quadrant + 1)
        xab = self.app.center_x + (math.cos(i) * radiusa)
        yab = self.app.center_y + (math.sin(i) * radiusa)
        xbb = self.app.center_x + (math.cos(i) * radiusb)
        ybb = self.app.center_y + (math.sin(i) * radiusb)

        # Finally draw the obstacle
        pyxel.line(xaa, yaa, xba, yba, self.color)
        pyxel.line(xba, yba, xbb, ybb, self.color)
        pyxel.line(xbb, ybb, xab, yab, self.color)
        pyxel.line(xab, yab, xaa, yaa, self.color)


class Ship(object):
    def __init__(self, app, angle=0, speed=3, color=8):
        self.angle = angle
        self.speed = speed
        self.color = color
        self.app = app

    @property
    def quadrant(self):
        """
            Return the current ship's quadrant
        """
        return quadrant(self.angle)

    def draw(self):
        """
            Draw the ship as a triangle pointing to the center
        """
        # Get quadrant's limit line
        i_angle = quadrant(self.angle, False)
        l_angle = angle(math.floor(i_angle))
        u_angle = angle(math.ceil(i_angle))
        linea = [
            [
                self.app.center_x + math.cos(l_angle) * (self.app.radius - 6),
                self.app.center_y + math.sin(l_angle) * (self.app.radius - 6)
            ], [
                self.app.center_x + math.cos(u_angle) * (self.app.radius - 6),
                self.app.center_y + math.sin(u_angle) * (self.app.radius - 6)
            ]
        ]

        # Get ship direction line (from the center to radius * 2)
        lineb = [
            [
                self.app.center_x,
                self.app.center_y,
            ], [
                self.app.center_x + (
                    math.cos(self.angle) * (self.app.radius * 2)),
                self.app.center_y + (
                    math.sin(self.angle) * (self.app.radius * 2)),
            ]
        ]

        # The ship nose point is the intersection of the quadrant's limit line
        # and the ship direction line
        front_x, front_y = intersect(linea, lineb)

        # Ship's nose angle
        a = math.radians(15)

        # Ship's back points
        backr_x = front_x + (math.cos(self.angle - a) * 10)
        backr_y = front_y + (math.sin(self.angle - a) * 10)
        backl_x = front_x + (math.cos(self.angle + a) * 10)
        backl_y = front_y + (math.sin(self.angle + a) * 10)

        # Finally draw the ship
        pyxel.line(front_x, front_y, backr_x, backr_y, self.color)
        pyxel.line(backr_x, backr_y, backl_x, backl_y, self.color)
        pyxel.line(backl_x, backl_y, front_x, front_y, self.color)

    def rotate_r(self):
        """
            Rotate the ship counterclockwise
        """
        self.angle = self.angle - math.radians(self.speed)

    def rotate_l(self):
        """
            Rotate the ship clockwise
        """
        self.angle = self.angle + math.radians(self.speed)
