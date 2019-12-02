from random import randint

from models import Cannon, BasicEnemy, Position, Missile, DeadEnemy


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

    def createCannon(self, x, y, angle, force, gravity, strategy):
        return Cannon(x, y, angle, force, gravity, strategy, self)

    def createEnemy(self):
        x = randint(100, 1000)
        y = randint(0, 700)
        return BasicEnemy(x, y)

    def createBird(self, position: Position, angle, force, gravity, strategy):
        return Missile(position.x, position.y, force, angle, gravity, strategy)

    def createColision(self, position: Position):
        return DeadEnemy(position.x, position.y)