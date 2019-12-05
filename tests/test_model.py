import sys, os
sys.path.append(os.path.realpath(os.path.dirname(__file__)+"/.."))

from models import GameModel, Position, AbstractEnemy
from mock import patch, MagicMock


@patch("factory.GameFactoryArcade")
def test_init(arcadeFactory):
    model = GameModel()

    assert model is not None

    model._factory = arcadeFactory
    model.initGame()

    assert model._cannon is not None
    assert arcadeFactory.createEnemy.call_count == 1


@patch("factory.GameFactoryArcade")
def test_spawnEnemy(arcadeFactory):
    model = GameModel()

    assert model is not None

    model._factory = arcadeFactory
    model.spawnEnemy()

    assert arcadeFactory.createEnemy.call_count == 1


def test_scoreUp():
    model = GameModel()

    assert model._base.score == 0

    model.scoreUp()

    assert model._base.score == 1


@patch("factory.GameFactoryArcade")
@patch("models.Missile")
@patch("models.BasicEnemy")
def test_call_collision(arcadeFactory, missile, basicEnemy):
    model = GameModel()
    model._factory = arcadeFactory

    model._birds = [missile]
    model._enemies = [basicEnemy]

    model.tickUpdate()

    assert basicEnemy.colision.call_count == 1



@patch("commands.Command")
def test_command(command):
    model = GameModel()

    model.acceptCommand(command)

    assert len(model._commands) == 1

    model.tickUpdate()

    assert command.execute.call_count == 1

