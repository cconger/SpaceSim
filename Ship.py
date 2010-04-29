from pandac.PandaModules import *
from direct.task import Task

DEFAULT_ENERGY_GENERATION = 10
DEFAULT_ENERGY_START      = 0
DEFAULT_ENERGY_CAP        = 100
DEFAULT_SHIP_WEIGHT       = 1360.77 #3,000 lbs
DEFAULT_THRUSTER_FORCE    = 4000
DEFAULT_TURN_RADIUS       = 45

class Ship:
  shipNode = None
  ships = {}
  shipCount = 0

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

  def __init__(self, world, modelPath="Models/ship.egg"):
    Ship.shipCount += 1

#===LOAD MODEL=================================================================
    self.modelNP = loader.loadModel(modelPath)
    Ship.ships[self.modelNP] = self #For Lookups Later
    self.modelNP.setScale(1)
    self.modelNP.reparentTo(Ship.shipNode)

#===LOAD PHYSICS===============================================================
    self.actorN  = ActorNode("ship%iPhysicsNode" % Ship.shipCount)
    self.actorNP = Ship.shipNode.attachNewNode(self.actorN)
    world.physicsMgr.attachPhysicalNode(self.actorN)
    self.modelNP.reparentTo(self.actorNP)
    self.actorN.getPhysicsObject().setMass(DEFAULT_SHIP_WEIGHT)

    #THRUSTERS=================================================================
    self.thruster = NodePath("thruster%i" % Ship.shipCount)
    self.thruster.reparentTo(self.modelNP)
    self.thruster.setPos(0,-2,0) #Set Behind
     
    self.thrusterFN = ForceNode('ship%iThruster')
    self.thrusterFNP = self.thruster.attachNewNode(self.thrusterFN)
    
    self.thrusterForce = LinearVectorForce(0,DEFAULT_THRUSTER_FORCE,0)
    self.thrusterForce.setMassDependent(1)
    self.thrusterFN.addForce(self.thrusterForce)

    self.pitchForce = AngularVectorForce(0,0,0)
    self.turnForce  = AngularVectorForce(0,0,0)
    self.thrusterFN.addForce(self.pitchForce)
    self.thrusterFN.addForce(self.turnForce)
    self.actorN.getPhysical(0).addAngularForce(self.pitchForce)
    self.actorN.getPhysical(0).addAngularForce(self.turnForce)

#===INIT ENERGY================================================================
    self.energy        = DEFAULT_ENERGY_START
    self.energyGenRate = DEFAULT_ENERGY_GENERATION
    self.engineDraw    = 0

  def enableThruster(self):
    self.actorN.getPhysical(0).addLinearForce(self.thrusterForce)

  def disableThruster(self):
    self.actorN.getPhysical(0).removeLinearForce(self.thrusterForce)

  def setTurn(self, direction):
    self.turnForce.setHpr(direction,0,0)

  def setPitch(self, direction):
    self.pitchForce.setHpr(0,direction,0)

  def updateEnergyByTime(self,dt):
    self.energy = min(DEFAULT_ENERGY_CAP, \
        self.energy +                     \
        (self.energyGenRate * dt) -       \
        (self.engineDraw * dt))
