from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3
from pandac.PandaModules import WindowProperties
import math

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
        self.taskMgr.add(self.mouseInput, "mouseInput")
        self.taskMgr.add(self.lookCharacter, "lookCharacter")



        #Positions of character/camera
        self.xpos = 0
        self.ypos = 0

        self.angleH = 0
        self.testAngleH = self.angleH

        self.xInterval = 0.0
        self.yInterval = 0.0

        #Speed at which the character/camera moves
        self.movementInterval = 1
        
        self.lookInterval = 2

        #Dictionary of key states
        self.keys = {"w" : False,
                     "s" : False,
                     "a" : False,
                     "d" : False,
                     "arrow_right" : False,
                     "arrow_left": False}


        
    #Define a procedure to move the camera
    def spinCameraTask(self, task):
        self.camera.setPos(self.xpos, self.ypos, 3)
        self.camera.setHpr(self.angleH, 0, 0)
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



    def setArrowRightToTrue(self):
        self.keys["arrow_right"] = True

    def setArrowRightToFalse(self):
        self.keys["arrow_right"] = False


    def setArrowLeftToTrue(self):
        self.keys["arrow_left"] = True

    def setArrowLeftToFalse(self):
        self.keys["arrow_left"] = False



    def keyInput(self, task):
        self.accept("w", self.setWToTrue)
        self.accept("w-up", self.setWToFalse)

        self.accept("s", self.setSToTrue)
        self.accept("s-up", self.setSToFalse)

        self.accept("a", self.setAToTrue)
        self.accept("a-up", self.setAToFalse)

        self.accept("d", self.setDToTrue)
        self.accept("d-up", self.setDToFalse)

        return Task.cont

    def mouseInput(self, task):
        self.accept("arrow_right", self.setArrowRightToTrue)
        self.accept("arrow_right-up", self.setArrowRightToFalse)

        self.accept("arrow_left", self.setArrowLeftToTrue)
        self.accept("arrow_left-up", self.setArrowLeftToFalse)
        return Task.cont

    def moveCharacter(self, task):
        if self.keys["w"] == True:
            self.testAngleH = self.AngleH + 90
            
                
            self.yInterval = self.movementInterval * math.sin(self.angleH)
            if self.yInterval < 0 and (self.angleH < 90 or self.angleH > 270):
                self.yInterval *= -1

            if self.yInterval > 0 and (self.angleH > 90 and self.angleH < 270):
                self.yInterval *= -1
            
            self.ypos += self.yInterval


            self.xInterval = self.movementInterval * math.cos(self.angleH)
            if self.xInterval > 0 and (self.angleH < 180):
                self.xInterval *= -1

            if self.xInterval < 0 and (self.angleH > 180):
                self.xInterval *= -1
            

            self.xpos += self.xInterval
            
            print(str(self.angleH) + ", " + str(self.yInterval) + ", " + str(self.xInterval))

        if self.keys["s"] == True:
            self.ypos -= self.movementInterval

        if self.keys["a"] == True:
            self.xpos -= self.movementInterval

        if self.keys["d"] == True:
            self.xpos += self.movementInterval
        return Task.cont

    def lookCharacter(self, task):
        if self.keys["arrow_right"] == True:
            self.angleH -= self.lookInterval

            if self.angleH == 0:
                self.angleH = 360

            if self.angleH < 0:
                self.angleH = 360 + self.angleH                
        if self.keys["arrow_left"] == True:
            self.angleH += self.lookInterval

            if self.angleH == 360:
                self.angleH = 0

            if self.angleH > 360:
                self.angleH = 360 - self.angleH
                
        #print str(self.angleH) 
        return Task.cont



app = MyApp()

props = WindowProperties()
props.setTitle("Game")
app.win.requestProperties(props)


app.run()

