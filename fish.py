import math
from random import randint
from typing import List

from PyQt5.QtCore import QPointF, QRectF
from PyQt5.QtGui import QPainterPath, QPolygonF, QPainter
from PyQt5.QtWidgets import QGraphicsItem


class Fish(QGraphicsItem):
    def __init__(self, x, y, speed, color, name):
        super().__init__(None)
        self._x = x
        self._y = y
        self._theta = 0
        self.setPos(self._x, self._y)
        self.setRotation(self._theta)
        self._speed = speed
        self._color = color

        points = [QPointF(10, 0), QPointF(8, -3),QPointF(5, -5),QPointF(-10, 0), QPointF(5, 5), QPointF(8, 3)]
        polygon = QPolygonF(points)
        self._path = QPainterPath()
        self._path.addPolygon(polygon)
        self._path.closeSubpath()

        self._swim_counter = 0
        self._theta_swim = 0

        self._name = name
        self._cohesive_r = 20
        self._repulsive_r = 20

    def paint(self, painter, options, widget=None):
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(self._color)
        painter.drawPath(self._path)
        painter.rotate(-self._theta - self._theta_swim)
        painter.drawText(10, -10, self._name)

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
        distance = math.sqrt((self._x-other._x)**2 +(self._y-other._y)**2)
        return distance < self._cohesive_r, distance < self._repulsive_r

    def cohesive(self, neighbours: List["Fish"]):
        thetas = []
        speeds = []
        for i in neighbours:
            thetas.append(i._theta)
            speeds.append(i._speed)
        self._theta = self._theta * 0.8 + 0.2 * sum(thetas)/len(thetas)
        self._speed = self._speed * 0.8 + 0.2 * sum(speeds)/len(speeds)

    def repulsive(self, crowders: List["Fish"]):
        for i in crowders:
            repulsion = [-(i._x - self._x), -(i._y - self._y)]
            speed_vector = [self._speed*math.cos(self._theta), self._speed*math.sin(self._theta)]
            new_speed_vector = [0.8*speed_vector[0] + 0.2*repulsion[0], 0.8*speed_vector[1] + 0.2*repulsion[1]]
            self._speed = math.hypot(new_speed_vector[0], new_speed_vector[1])
            self._theta = math.atan(new_speed_vector[1]/new_speed_vector[0])

    def random(self):
        self._theta += 0.2 * (randint(0, 100)/50 - 1) * 90
        self._speed += 0.2 * self._speed * ((randint(0, 100)/50) - 1)

    @property
    def theta(self):
        return self._theta

    @property
    def speed(self):
        return self._speed

    @property
    def pos(self):
        return [self._x, self._y]
