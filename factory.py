from models import Cannon


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
        return BasicEnemy(self, x, y)