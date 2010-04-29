from Ship import Ship

from math                         import pi, sin, cos
from direct.showbase.ShowBase     import ShowBase
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules          import *
from direct.task                  import Task
from panda3d.core                 import CompassEffect

CAMERA_RADIUS = 30


class SpaceSimulator(ShowBase):
  """World class for capturing everything in the universe
  this defines and contains all the objects"""
  def __init__(self):
    ShowBase.__init__(self)

    self.keyMap = {"left":False, "right":False, "forward":False, "reverse":False, "turn-left":False, "turn-right":False, "lazers":False, "rockets":False}

    self.disableMouse()
    self.enableParticles()

    # Hide the Cursor
    props = WindowProperties()
    props.setCursorHidden(True)
    self.win.requestProperties(props)

    self.angleInt = AngularEulerIntegrator()
    self.physicsMgr.attachAngularIntegrator(self.angleInt)

    Ship.shipNode = self.render.attachNewNode("ShipNode")

    self.player = Ship(self)

    self.loadSkyBox()
    self.drawLines()

    # Set Camera behind the actor
    self.cameraH = 270
    self.cameraP = 18
    self.camera.reparentTo(self.player.actorNP)
    self.camera.setPos(0,-CAMERA_RADIUS,3)

    # Add Simple Shaders and Lights
    #self.render.setShaderAuto()
    #self.render.setAttrib(LightRampAttrib.makeHdr1())
    #ambientLight = AmbientLight("ambientLight")
    #ambientLight.setColor(Vec4(.5,.5,.5,1))
    #self.render.setLight(self.render.attachNewNode(ambientLight))

    #====CONTROLS=============================================================
    self.accept('space',          self.player.enableThruster)
    self.accept('space-up',       self.player.disableThruster)
    self.accept('arrow_up',       self.player.setPitch, [-1])
    self.accept('arrow_up-up',    self.player.setPitch, [0])
    self.accept('arrow_down',     self.player.setPitch, [1])
    self.accept('arrow_down-up',  self.player.setPitch, [0])
    self.accept('arrow_right',    self.player.setTurn,  [-1])
    self.accept('arrow_right-up', self.player.setTurn,  [0])
    self.accept('arrow_left',     self.player.setTurn, [1])
    self.accept('arrow_left-up',  self.player.setTurn, [0])

    #====REGISTER TASKS=======================================================
    self.controlTask = taskMgr.add(self.movement, "controlTask")
    self.controlTask.lastTime = 0

    self.energyTask = taskMgr.add(Ship.updateEnergyTask, "energyTask")
    self.energyTask.lastTime = 0

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

    #===CAMERA CONTROL=========================================================
    if base.mouseWatcherNode.hasMouse():
      md = base.win.getPointer(0)
      x = md.getX()
      y = md.getY()
      deltaX = (md.getX() - 200) / 2
      deltaY = (md.getY() - 200) / 2

      self.cameraH = (self.cameraH + deltaX) % 360
      self.cameraP = ((self.cameraP + deltaY + 90) % 180) - 90

      print self.cameraH
      print self.cameraP
      print ""

      base.win.movePointer(0,200,200)

    #TODO: Fix camera control...
    Hrad = self.cameraH * (pi / 180)
    Prad = self.cameraP * (pi / 180)
    self.camera.setPos( CAMERA_RADIUS * cos(Hrad),
                        CAMERA_RADIUS * sin(Hrad),
                        CAMERA_RADIUS * sin(Prad))

    self.camera.lookAt(self.player.actorNP)

    return Task.cont

  def drawLines(self):
    def printText(name, message, color):
      text = TextNode(name)
      text.setText(message)
      x,y,z = color
      text.setTextColor(x,y,z,1)
      text3d = NodePath(text)
      text3d.reparentTo(render)
      return text3d

    for i in xrange(0,51):
      printText("X", "|", (1,0,0)).setPos(i,0,0)
      printText("Y", "|", (0,1,0)).setPos(0,i,0)
      printText("Z", "-", (0,0,1)).setPos(0,0,i)

    printText("XL", "X", (0,0,0)).setPos(5.5,0,0)
    printText("YL", "Y", (0,0,0)).setPos(0,5.5,0)
    printText("ZL", "Z", (0,0,0)).setPos(0,0,5.5)
    printText("OL", "@", (0,0,0)).setPos(0,0,0)
    print "Displaying DEBUG Lines"

if __name__ == "__main__":
  application = SpaceSimulator()
  application.run()
