![](logo_big.png)

# Xagon

A [pyxel](https://github.com/kitao/pyxel) based game.

![](screenshot.png)

# Help

You control a ship at ludicrous speed in an hexagonal tunnel.

Use Q and D keys to slide on the tunnel border and clear all the obstacle.

# Install

<pre>
$ python setup.py build
# python setup.py install
</pre>

# Known issues

On Archlinux with DWGL 3.2.x the game must be started as root or the max user inotify watches must be increased (see [glfw#833](https://github.com/glfw/glfw/issues/833)).

<pre>
# sysctl -w fs.inotify.max_user_watches=16384
</pre>
