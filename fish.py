import math
from random import randint
from typing import List

from PyQt5.QtCore import QPointF, QRectF
from PyQt5.QtGui import QPainterPath, QPolygonF, QPainter
from PyQt5.QtWidgets import QGraphicsItem


class Fish(QGraphicsItem):
    def __init__(self, x, y, color, max_speed, name):
        super().__init__(None)
        self._x = x
        self._y = y
        self._theta = 0
        self.setPos(self._x, self._y)
        self.setRotation(self._theta)
        self._color = color
        self._speed = randint(1, 100)/100 * max_speed

        points = [QPointF(10, 0), QPointF(8, -3), QPointF(5, -5), QPointF(-10, 0), QPointF(5, 5), QPointF(8, 3)]
        polygon = QPolygonF(points)
        self._path = QPainterPath()
        self._path.addPolygon(polygon)
        self._path.closeSubpath()

        self._swim_counter = 0
        self._theta_swim = 0

        self._name = name

        # SETTINGS ======================================================================================#
        self._max_speed = max_speed
        self._cohesive_rad = 50
        self._repulsive_rad = 3
        self._cohesion_factor = 0.3
        self._repulsion_factor = 0.3
        self._random_factor = 0.2

    def paint(self, painter, options, widget=None):
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(self._color)
        painter.drawPath(self._path)
        painter.rotate(-self._theta - self._theta_swim)
        # painter.drawText(10, -10, self._name)

    def boundingRect(self):
        # return QRectF(-10, -10, 20, 20)
        return QRectF(-100, -100, 200, 200)

    def move(self):
        self.swim()
        self._x += self._speed*math.cos(self._theta*math.pi/180.0)
        self._y += self._speed*math.sin(self._theta*math.pi/180.0)
        self.setPos(self._x, self._y)
        self.setRotation(self._theta + self._theta_swim)

    def swim(self):
        swim_increment = 2*math.pi/10.0

        max_degree = 15
        self._theta_swim = math.cos(self._swim_counter)*max_degree
        self._swim_counter += swim_increment

    def set_speed(self, speed):
        self._speed = speed

    def set_theta(self, theta):
        self._theta = theta

    def nearby(self, other: "Fish"):
        distance = math.hypot((self._x-other._x), (self._y-other._y))
        return distance < self._cohesive_rad, distance < self._repulsive_rad

    def cohesive(self, neighbours: List["Fish"]):
        thetas = []
        speeds = []
        for i in neighbours:
            thetas.append(i._theta)
            speeds.append(i._speed)
        factor = self._cohesion_factor
        if len(thetas) != 0:
            self._theta = self._theta * (1-factor) + factor * sum(thetas)/len(thetas)
            self._speed = self._speed * (1-factor) + factor * sum(speeds)/len(speeds)

    def repulsive(self, crowders: List["Fish"]):
        for i in crowders:
            speed_vector = [self._speed*math.cos(self._theta), self._speed*math.sin(self._theta)]
            repulsion = [-(i._x - self._x), -(i._y - self._y)]
            factor = self._repulsion_factor
            new_speed_vector = \
                [(1-factor)*speed_vector[0] + factor*repulsion[0], (1-factor)*speed_vector[1] + factor*repulsion[1]]
            self._speed = math.hypot(new_speed_vector[0], new_speed_vector[1])
            self._theta = math.atan(new_speed_vector[1]/new_speed_vector[0]) * 180/math.pi

    def random(self):
        factor = self._random_factor
        self._theta += factor * (randint(0, 100)/50 - 1) * 90
        self._speed += factor * self._speed * ((randint(0, 100)/50) - 1)
        if self._speed > self._max_speed:
            self._speed = self._max_speed

    @property
    def theta(self):
        return self._theta

    @property
    def speed(self):
        return self._speed

    @property
    def pos(self):
        return [self._x, self._y]
