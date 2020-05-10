from random import randint

from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QColor

from obstacle import Obstacle
from fish import Fish
from utils import random_name

TICK = 40


class FishManager:

    def __init__(self, scene):
        self._fishes = []
        self._obstacles = []
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(TICK)

        self._scene = scene

        for i in range(1, 101):
            color = QColor(randint(0,255), randint(0,255), randint(0,255))
            max_speed = 10
            fish = Fish(randint(0, scene.width()), randint(0, scene.height()), color, max_speed, name=random_name())
            self.add_fish(fish)
            fish.set_theta(randint(0, 360))
            # fish.set_speed(10)

        for i in range(11):
            color = QColor(255, 255, 255)
            obstacle = Obstacle(randint(0, scene.width()), randint(0, scene.height()), color)
            self.add_obstacle(obstacle)

    def update(self):
        # print('--------------------------- pouet')
        for fish in self._fishes:
            neighbours = []
            crowders = []
            for i in self._fishes:
                if i != fish:
                    close, too_close = fish.nearby(i)
                    if close:
                        neighbours.append(i)
                    if too_close:
                        crowders.append(i)
            fish.cohesive(neighbours)
            fish.repulsive(crowders)
            fish.random()
            fish.obstacles(self._obstacles)
            fish.move()

    def add_fish(self, fish):
        self._fishes.append(fish)
        self._scene.addItem(fish)

    def add_obstacle(self, obstacle):
        self._obstacles.append(obstacle)
        self._scene.addItem(obstacle)
