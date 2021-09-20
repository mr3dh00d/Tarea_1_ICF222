from random import seed
import cocos
from modules.board import board
from modules.game import ia
from modules.layouts import background, win
from modules.utiles import inPlanet, createLabel
from cocos.actions import *
from cocos.scenes import *

class Game(cocos.layer.Layer):
    is_event_handler = True
    def __init__(self, difficulty: int) -> None:
        super().__init__()
        self.canSelect = True
        self.select = None
        self.finish = False
        self.Turn = 1
        self.board = board.Board(self.add)
        self.ia = ia.IA(difficulty)
        self.setLabels()
        self.ia.checkAvailablesFor(self.board, "o")

    def changeSprite(self, position: "tuple[int, int]", option: int) -> None:
        self.remove(self.board.getTile(position).sprite)
        self.board.getTile(position).setSprite(option)
        self.add(self.board.getTile(position).sprite)

    def on_mouse_motion (self, x, y, dx, dy):
        if self.canSelect:
            for available in self.board.availables():
                inP = inPlanet(self.board.getTile(available.point).position, (x,y))
                if(inP and self.board.getTile(available.point).state != "available"):
                    self.select = available
                    self.changeSprite(available.point, 2)
                elif(not inP and self.board.getTile(available.point).state == "available"):
                    self.select = None
                    self.changeSprite(available.point, 1)

    def turnManager(self):
        if not self.finish:
            if self.Turn%2 == 1:
                if self.ia.checkAvailablesFor(self.board, "x"):
                    self.Turn+=1
                    self.canSelect = False
                    self.viewRed(True)
                elif self.ia.checkAvailablesFor(self.board, "o"):
                    pass
                else:
                    self.finish = True
            else:
                if self.ia.checkAvailablesFor(self.board, "o"):
                    self.Turn+=1
                    self.canSelect = True
                    self.select = None
                elif self.ia.checkAvailablesFor(self.board, "x"):
                    self.redAction()
                else:
                    self.finish = True
            if self.finish:
                self.canSelect = False
                self.viewRed(True)
                
    def on_mouse_press (self, x, y, buttons, modifiers):
        if not self.finish:
            if self.canSelect and self.Turn%2 == 1:
                if len(self.board.availables()) > 0:
                    if self.select:
                        for casilla in self.select.getTilesToChange():
                            self.changeSprite(casilla, 4)
                        self.updateScore()
                        self.turnManager()
                else:
                    self.turnManager()
            else:
                self.viewRed(False)
                self.redAction()
        else:
            w = len(self.board.blue) > len(self.board.red)
            newScene = cocos.scene.Scene()
            newScene.add(background.BackgroundLayer())
            newScene.add(win.WinLayer(w))
            cocos.director.director.replace(FadeTRTransition(newScene, duration=1))

    
    def redAction(self) -> None:
        if len(self.board.availables()) > 0:
            for casilla in self.ia.bestMove(self.board).getTilesToChange():
                self.changeSprite(casilla, 3)
        self.updateScore()
        self.turnManager()

    def setLabels(self) -> None:
        self.title = createLabel('Planets of the Galaxy', (450,800))
        self.add(self.title)
        self.vs = createLabel('vs', (450,750))
        self.add(self.vs)
        self.blue_score = createLabel('', (400,750), (79, 164, 184, 255))
        self.add(self.blue_score)
        self.red_score = createLabel('', (500,750), (230, 69, 57, 255))
        self.add(self.red_score)
        self.view_red = createLabel('', (450, 30), size=20)
        self.add(self.view_red)
        self.updateScore()

    def updateScore(self) -> None:
        self.board.updateScore()
        self.blue_score.element.text = str(len(self.board.blue))
        self.red_score.element.text = str(len(self.board.red))

    def viewRed(self, view: bool) -> None:
        if view:
            if not self.finish:
                self.view_red.element.text = "Click on the screen to see the opponent's play"
            else:
                self.view_red.element.text = "Click on the screen to continue"
        else:
            self.view_red.element.text = ''