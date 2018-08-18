#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import math
from random import choice
from itertools import filterfalse

import pyxel

from .mobs import Obstacle, Ship


class Xagon:
    # App window
    width = 200
    height = 150

    # Hexagon position and size
    center_x = 77
    center_y = 75
    radius = 72
    inner_radius = 5

    # Obstacles
    obstacles = []
    num_obstacles = 4
    rate_obstacles = 100
    _cycle = 0

    # Ship
    ship = None

    # Games parameters
    obstacles_rate = 60
    speed = 5
    level = 0
    level_size = 10
    _waves = 0
    started = False
    loose = False
    score = 0

    # Loose blink
    _blink = 0

    def __init__(self):
        pyxel.init(self.width, self.height, caption="Xagon")

        # Load assets
        assets = os.path.join(os.path.dirname(__file__), 'assets')
        pyxel.image(0).load(0, 0, os.path.join(assets, 'logo.png'))

        # Start the game
        pyxel.run(self.update, self.draw)

    def add_obstacles(self, color=9):
        quadrants = set((0, 1, 2, 3, 4, 5))

        # Add num_obstacles obstacles on different quadrants
        for i in range(0, self.num_obstacles):
            quadrant = choice(list(quadrants))
            quadrants = quadrants - set((quadrant,))
            self.obstacles.append(Obstacle(self, quadrant, 0, color=color))

    def update(self):
        """
            Keyboard events
        """
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        elif pyxel.btnp(pyxel.KEY_R):
            self.restart()

        if not self.loose:
            if pyxel.btn(pyxel.KEY_A):
                self.ship.rotate_r()

            elif pyxel.btn(pyxel.KEY_D):
                self.ship.rotate_l()

    def restart(self):
        """
            Restart the game, set all game parameters to default values
        """
        self.started = True
        self.loose = False
        self.level = 0
        self.score = 0
        self._cycle = 0
        self._waves = 0

        # Initialize obstacles
        self.obstacles = []
        self.add_obstacles()

        # Initialize ship
        self.ship = Ship(self)

    def draw(self):
        """
            Clear the screen and draw again
        """
        pyxel.cls(0)
        self.draw_ui()

        if self.started:
            # If the game is started, a run iteration is done every frame
            self.run()

    def run(self):
        """
            Game iteration routine
        """
        if not self.loose:
            # Increase the score
            self.score = self.score + self.level + 1

            # Move obstacles one bit (the higher the level, the faster)
            for obstacle in self.obstacles:
                obstacle.pos = obstacle.pos + (self.speed + self.level) / 1000

            # removed obstacles the ship has cleared
            self.obstacles[:] = filterfalse(
                    lambda x: x.pos > 1, self.obstacles)

            # Add more obstacles at the end of a cycle
            self._cycle = self._cycle + 1
            if self._cycle > (self.obstacles_rate - (self.level * 5)):
                self._cycle = 0
                self._waves = self._waves + 1
                color = 9

                # Every level_size waves, increase the level
                if self._waves >= self.level_size:
                    self._waves = 0
                    self.level = self.level + 1
                    color = 11

                self.add_obstacles(color)

        # Draw obstacles and ship and check for collisions
        for obstacle in self.obstacles:
            # On collision, loose the game and mark the collided obstacle
            if obstacle.at_border and obstacle.quadrant == self.ship.quadrant:
                obstacle.color = 14
                self.loose = True

            obstacle.draw()

        self.ship.draw()

        # If the player loose, taunt that looser !
        if self.loose:
            self._blink = (self._blink + 1) % 10
            pyxel.rect(
                    self.center_x - 42, self.center_y - 5,
                    self.center_x + 39, self.center_x + 1,
                    7 if self._blink > 5 else 8
            )
            pyxel.text(
                    self.center_x - 40, self.center_y - 3,
                    "T'es mauvais, Jack !",
                    8 if self._blink > 5 else 7
            )

    def draw_ui(self):
        """
            Draw everything but mobs
        """
        # Right rect for score, etc
        pyxel.rect(self.height + 6, 3, self.width - 4, self.height - 4, 1)

        # Logo
        pyxel.blt(self.height + 11, 6, 0, 0, 0, 32, 16)

        # Help text, current level and score
        pyxel.text(self.height + 11, 32, "Press R\nto start", 7)
        pyxel.text(self.height + 11, 64, "Level {}".format(self.level + 1), 7)
        pyxel.text(self.height + 11, 80, "Score :\n{}".format(self.score), 7)

        # Outter hexagon
        self.draw_hexagon(
            self.center_x,
            self.center_y,
            self.radius,
        )

        # Inner hexagon
        self.draw_hexagon(
            self.center_x,
            self.center_y,
            self.inner_radius,
        )

    def draw_hexagon(self, center_x, center_y, radius, color=1):
        """
            Draw an hexagon

            args:
                center_x/y : the hexagon center pos
                radius : the hexagon radius
                color: the hexagon color
        """
        prev_x = center_x + radius
        prev_y = center_y

        i = 2 * math.pi / 6
        # Every 6th of a circle draw a line from that point to the previous
        while i <= 2 * math.pi:
            next_x = center_x + (math.cos(i) * radius)
            next_y = center_y + (math.sin(i) * radius)
            pyxel.line(
                    prev_x,
                    prev_y,
                    center_x + (math.cos(i) * radius),
                    center_y + (math.sin(i) * radius),
                    color
            )
            prev_x = next_x
            prev_y = next_y

            i = i + (2 * math.pi / 6)


if __name__ == "__main__":
    Xagon()
