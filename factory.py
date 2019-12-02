from random import randint

from models import Cannon, BasicEnemy, Position, Missile


class AbstractGameFactory:
    def __init__(self, state):
        self._state = state

    def createCannon(self):
        raise NotImplementedError

    def createMisile(self):
        raise NotImplementedError

    def createEnemy(self):
        raise NotImplementedError

    def createInfo(self):
        raise NotImplementedError


class GameFactoryArcade(AbstractGameFactory):
    def __init__(self, state):
        super().__init__(state)

    def createCannon(self, x, y):
        return Cannon(x, y, self._state.angle, self._state.force)

    def createEnemy(self):
        x = randint(100, 1000)
        y = randint(0, 700)
        return BasicEnemy(x, y)

    def createBird(self, position: Position):
        return Missile(position.x, position.y)