from PyQt5.QtCore import QPointF, QRectF
from PyQt5.QtGui import QPainterPath, QPolygonF, QPainter
from PyQt5.QtWidgets import QGraphicsItem


class Obstacle(QGraphicsItem):
    def __init__(self, x, y, color):
        super().__init__(None)
        self._x = x
        self._y = y
        self._width = 10
        self._height = 10
        self._color = color

        points = [QPointF(x - self._width/2, y - self._height/2), QPointF(x + self._width/2, y - self._height/2),
                  QPointF(x + self._width/2, y + self._height/2), QPointF(x - self._width/2, y + self._height/2)]
        polygon = QPolygonF(points)
        self._path = QPainterPath()
        self._path.addPolygon(polygon)
        self._path.closeSubpath()

    def paint(self, painter, options, widget=None):
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(self._color)
        painter.drawPath(self._path)

    def boundingRect(self):
        return QRectF(self._x, self._y, self._width, self._height)

    @property
    def pos(self):
        return [self._x, self._y]
