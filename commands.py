class Command:
    def __init__(self, model):
        self._model = model

    def execute(self):
        raise NotImplementedError


class CannonUpCommand(Command):
    def execute(self):
        self._model.cannonUp()


class CannonDownCommand(Command):
    def execute(self):
        self._model.cannonDown()


class ShootCommand(Command):
    def execute(self):
        self._model.shoot()


class ShootCommand(Command):
    def execute(self):
        self._model.shoot()


class AngleUpCommand(Command):
    def execute(self):
        self._model.angleUp(2)


class AngleDownCommand(Command):
    def execute(self):
        self._model.angleDown(2)


class ForceUpCommand(Command):
    def execute(self):
        self._model.forceUp(1)


class ForceDownCommand(Command):
    def execute(self):
        self._model.forceDown(1)


class ChangeStrategyCommand(Command):
    def execute(self):
        self._model.changeStrategy()


class SpawnEnemyCommand(Command):
    def execute(self):
        self._model.spawnEnemy()