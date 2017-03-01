
from math import pi, sin, cos

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3

class MyApp(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)

        #Disable mouse controls
        self.disableMouse()

        #Load enviromnment model
        self.scene = self.loader.loadModel("models/environment")

        #Reparent model top renderer
        self.scene.reparentTo(self.render)

        #Apply scale and position transforms on the model
        self.scene.setScale(0.25, 0.25, 0.25)
        self.scene.setPos(-8, 42, 0)

        #Add task spinCameraTask procedure to task manager
        self.taskMgr.add(self.spinCameraTask, "spinCameraTask")
        self.taskMgr.add(self.keyInput, "keyInput")
        self.taskMgr.add(self.moveCharacter, "movecharacter")

        self.pandaActor = Actor("models/panda-model",
                                {"walk": "models/panda-walk4"})
        self.pandaActor.setScale(0.005, 0.005, 0.005)
        self.pandaActor.reparentTo(self.render)
        #Loop its animation
        self.pandaActor.loop("walk")

        #Positions of character/camera
        self.xpos = 0
        self.ypos = 0

        #Speed at which the character/camera moves
        self.movementValue = 0.2

        #Dictionary of key states
        self.keys = {"w" : False, "s" : False, "a" : False, "d" : False}

        #Create the four lerp intervals neede for the panda to
        #walk back and forth
        pandaPosInterval1 = self.pandaActor.posInterval(13,
                                                        Point3(0, -10, 0),
                                                        startPos = Point3(0, 10, 0))
        pandaPosInterval2 = self.pandaActor.posInterval(13,
                                                        Point3(0, 10, 0),
                                                        startPos = Point3(0, -10, 0))
        pandaHprInterval1 = self.pandaActor.hprInterval(3,
                                                        Point3(180, 0, 0),
                                                        startHpr = Point3(0, 0, 0))
        pandaHprInterval2 = self.pandaActor.hprInterval(3,
                                                        Point3(0, 0, 0),
                                                        startHpr = Point3(180, 0, 0))

        #Create and play the sequence that coordinates the intervals
        self.pandaPace = Sequence(pandaPosInterval1,
                                  pandaHprInterval1,
                                  pandaPosInterval2,
                                  pandaHprInterval2,
                                  name="pandaPace")

        self.pandaPace.loop()


        
    #Define a procedure to move the camera
    def spinCameraTask(self, task):
        self.camera.setPos(self.xpos, self.ypos, 3)
        self.camera.setHpr(270, 0, 0)
        return Task.cont

    def setWToTrue(self):
        self.keys["w"] = True

    def setWToFalse(self):
        self.keys["w"] = False



    def setSToTrue(self):
        self.keys["s"] = True

    def setSToFalse(self):
        self.keys["s"] = False



    def setAToTrue(self):
        self.keys["a"] = True

    def setAToFalse(self):
        self.keys["a"] = False



    def setDToTrue(self):
        self.keys["d"] = True

    def setDToFalse(self):
        self.keys["d"] = False


    def keyInput(self, task):
        self.accept("w", self.setWToTrue)
        self.accept("w-up", self.setWToFalse)

        self.accept("s", self.setSToTrue)
        self.accept("s-up", self.setSToFalse)

        self.accept("a", self.setAToTrue)
        self.accept("a-up", self.setAToFalse)

        self.accept("d", self.setDToTrue)
        self.accept("d-up", self.setDToFalse)
        
        print("Getting input...")
        return Task.cont

    def moveCharacter(self, task):
        if self.keys["w"] == True:
            self.xpos += self.movementValue

        if self.keys["s"] == True:
            self.xpos -= self.movementValue

        if self.keys["a"] == True:
            self.ypos += self.movementValue

        if self.keys["d"] == True:
            self.ypos -= self.movementValue
        return Task.cont

app = MyApp()
app.run()

