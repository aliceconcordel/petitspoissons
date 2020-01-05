import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView

from fish_manager import FishManager

WIDTH = 1600
HEIGHT = 800

app = QApplication(sys.argv)
w = QMainWindow()
w.setWindowTitle("Poissons Rouges")
w.setFixedSize(WIDTH, HEIGHT)

scene = QGraphicsScene()
scene.setSceneRect(0, 0, WIDTH, HEIGHT)
view = QGraphicsView(scene)
view.setFixedSize(WIDTH, HEIGHT)
view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
w.setCentralWidget(view)
w.show()

quentin = FishManager(scene)

app.exec()
