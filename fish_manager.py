from random import randint

from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QColor

from fish import Fish

TICK = 40


class FishManager:

    def __init__(self, scene):
        self._fishes = []
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(TICK)

        self._scene = scene

        for i in range(1, 100):
            color = QColor(randint(0,255), randint(0,255), randint(0,255))
            fish = Fish(randint(0, scene.width()), randint(0, scene.height()), color)
            self.add_fish(fish)
            fish.set_theta(randint(0, 360))

    def update(self):
        for fish in self._fishes:
            fish.move()

    def add_fish(self, fish):
        self._fishes.append(fish)
        self._scene.addItem(fish)
