"""
Author: Tomas Stary
E-mail: staryto5@fit.cvut.cz
"""


from random import randint

from models import Cannon, BasicEnemy, Position, Missile, DeadEnemy, MovingEnemy


class AbstractGameFactory:
    def __init__(self, model):
        self._model = model

    def createCannon(self):
        raise NotImplementedError

    def createMisile(self):
        raise NotImplementedError

    def createEnemy(self):
        raise NotImplementedError

    def createInfo(self):
        raise NotImplementedError


class GameFactoryArcade(AbstractGameFactory):
    def __init__(self, model):
        super().__init__(model)

    def createCannon(self, x, y):
        return Cannon(x, y, self._model.getAngle(), self._model.getForce(), self._model.getGravity(), self._model.getStrategy(), self)

    def createEnemy(self):
        x = randint(100, 1000)
        y = randint(0, 700)
        return BasicEnemy(x, y)

    def createBird(self, position: Position):
        return Missile(position.x, position.y, self._model.getAngle(), self._model.getForce(), self._model.getGravity(), self._model.getStrategy())

    def createColision(self, position: Position):
        return DeadEnemy(position.x, position.y)


class GameFactoryRealistic(AbstractGameFactory):
    def __init__(self, model):
        super().__init__(model)

    def createCannon(self, x, y):
        return Cannon(x, y, self._model.getAngle(), self._model.getForce(), self._model.getGravity(), self._model.getStrategy(), self)

    def createEnemy(self):
        x = randint(100, 1000)
        y = randint(0, 700)
        return MovingEnemy(x, y)

    def createBird(self, position: Position):
        return Missile(position.x, position.y, self._model.getAngle(), self._model.getForce(), self._model.getGravity(), self._model.getStrategy())

    def createColision(self, position: Position):
        return DeadEnemy(position.x, position.y)