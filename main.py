from Ship import Ship

from math                     import pi, sin, cos
from direct.showbase.ShowBase import ShowBase
from direct.task              import Task
from panda3d.core             import CompassEffect

class SpaceSimulator(ShowBase):
  """World class for capturing everything in the universe
  this defines and contains all the objects"""
  def __init__(self):
    ShowBase.__init__(self)

    self.keyMap = {"left":False, "right":False, "forward":False, "reverse":False, "turn-left":False, "turn-right":False, "lazers":False, "rockets":False}

    self.disableMouse()

    Ship.shipNode = self.render.attachNewNode("ShipNode")

    self.player = Ship()

    self.loadSkyBox()

    self.camera.reparentTo(self.player.modelNP)
    self.camera.setPos(0,-14,1)

#====CONTROLS==================================================================
    self.accept('w',           self.setKey,      ["forward",True])
    self.accept('w-up',        self.setKey,      ["forward",False])
    self.accept('a',           self.setKey,      ["left",True])
    self.accept('a-up',        self.setKey,      ["left",False])
    self.accept('s',           self.setKey,      ["reverse",True])
    self.accept('s-up',        self.setKey,      ["reverse",False])
    self.accept('d',           self.setKey,      ["right",True])
    self.accept('d-up',        self.setKey,      ["right",False])
    self.accept('q',           self.setKey,      ["turn-left",True])
    self.accept('q-up',        self.setKey,      ["turn-left",False])
    self.accept('e',           self.setKey,      ["turn-right",True])
    self.accept('e-up',        self.setKey,      ["turn-right",False])
    self.accept('space',       self.setKey,      ["lazers",True])
    self.accept('right-shift', self.setKey,      ["rocket", True])

#====REGISTER TASKS============================================================
    self.controlTask = taskMgr.add(self.movement, "controlTask")
    self.controlTask.lastTime = 0

    self.energyTask = taskMgr.add(Ship.updateEnergyTask, "energyTask")
    self.energyTask.lastTime = 0

  def setKey(self, key, value):
    """For modifying currently held keys"""
    self.keyMap[key] = value

  def loadSkyBox(self):
    """Loads and centers the skybox."""
    self.skybox = self.loader.loadModel("Models/skybox.egg")
    self.skybox.setScale(1000.0,1000.0,1000.0)
    self.skybox.setPos(0,0,0)
    self.skybox.reparentTo(self.player.modelNP)

    self.skybox.setEffect(CompassEffect.make(self.render, CompassEffect.PRot))

  def movement(self, task):
    """Task body for handling controls on the main player"""
    elapsed = task.time - task.lastTime
    task.lastTime = task.time

    return Task.cont

application = SpaceSimulator()
application.run()
