import math

from PyQt5.QtCore import QPointF, QRectF
from PyQt5.QtGui import QPainterPath, QPolygonF, QPainter
from PyQt5.QtWidgets import QGraphicsItem


class Fish(QGraphicsItem):
    def __init__(self, x, y, color):
        super().__init__(None)
        self._x = x
        self._y = y
        self._theta = 0
        self.setPos(self._x, self._y)
        self.setRotation(self._theta)
        self._speed = 3
        self._color = color

        points = [QPointF(10, 0), QPointF(8, -3),QPointF(5, -5),QPointF(-10, 0), QPointF(5, 5), QPointF(8, 3)]
        polygon = QPolygonF(points)
        self._path = QPainterPath()
        self._path.addPolygon(polygon)
        self._path.closeSubpath()

        self._swim_counter = 0
        self._theta_swim = 0

    def paint(self, painter, options, widget=None):
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(self._color)
        painter.drawPath(self._path)

    def boundingRect(self):
        return QRectF(-10, -10, 20, 20)

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

    @property
    def theta(self):
        return self._theta

    @property
    def speed(self):
        return self._speed

    @property
    def pos(self):
        return [self._x, self._y]