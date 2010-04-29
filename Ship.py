from pandac.PandaModules import *
from direct.task import Task

DEFAULT_ENERGY_GENERATION = 10
DEFAULT_ENERGY_START      = 0
DEFAULT_ENERGY_CAP        = 100

class Ship:
  shipNode = None
  ships = {}

  @staticmethod
  def getShipFromModel(modelNodePath):
    return ships[modelNodePath]

  @staticmethod
  def updateEnergyTask(task):
    dt = task.time - task.lastTime
    task.lastTime = task.time

    for ship in Ship.ships.itervalues():
      ship.updateEnergyByTime(dt)

    return Task.cont

  def __init__(self, modelPath="Models/bullet.egg.pz"):
    self.modelNP = loader.loadModel(modelPath)
    Ship.ships[self.modelNP] = self #For Lookups Later
    self.modelNP.setScale(1)
    self.modelNP.reparentTo(Ship.shipNode)

    self.energy        = DEFAULT_ENERGY_START
    self.energyGenRate = DEFAULT_ENERGY_GENERATION
    self.engineDraw    = 0

  def updateEnergyByTime(self,dt):
    self.energy = min(DEFAULT_ENERGY_CAP, self.energy + (self.energyGenRate * dt))
