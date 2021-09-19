import cocos
import modules.board as board
import modules.ia as ia
from modules.utiles import inPlanet
from cocos.actions import *
from planets_of_galaxy import N

class Game(cocos.layer.Layer):
    is_event_handler = True
    def __init__(self):
        super().__init__()
        self.canSelect = True
        self.Turn = 1
        self.board = board.Board(self.add)
        self.ia = ia.IA()
        self.setLabels()
        self.ia.checkAvailablesFor(self.board, "o")

    def changeSprite(self, position, option):
        self.remove(self.board.getCasilla(position).sprite)
        self.board.getCasilla(position).setByNumber(option)
        self.add(self.board.getCasilla(position).sprite)

    def on_mouse_motion (self, x, y, dx, dy):
        if self.canSelect:
            for available in [a.point for a in self.board.availables()]:
                i, j = available
                inP = inPlanet(self.board.getCasilla(available).position, (x,y))
                if(inP and self.board.getCasilla(available).state != "available"):
                    self.changeSprite((i, j), 2)
                elif(not inP and self.board.getCasilla(available).state == "available"):
                    self.changeSprite((i, j), 1)

    def turnManager(self):
        pass
                
    def on_mouse_press (self, x, y, buttons, modifiers):
        if self.canSelect and self.Turn%2 == 1:
            if len(self.board.availables()) > 0:
                ip = False
                for available in self.board.availables():
                    point = available.point
                    if inPlanet(self.board.getCasilla(point).position, (x, y)):
                        select = available
                        ip = True
                        break
                if ip:
                    for casilla in select.getTilesToChange():
                        self.changeSprite(casilla, 4)
                    self.updateScore()
                    if self.ia.checkAvailablesFor(self.board, "x"):
                        self.Turn+=1
                        self.canSelect = False
                        self.redAction()
                    elif self.ia.checkAvailablesFor(self.board, "o"):
                        pass
            else:
                self.updateScore()
                if self.ia.checkAvailablesFor(self.board, "x"):
                    self.Turn+=1
                    self.canSelect = False
                    self.redAction()
                elif self.ia.checkAvailablesFor(self.board, "o"):
                    pass

    
    def redAction(self):
        if len(self.board.availables()) > 0:
            for casilla in self.ia.minimax(self.board.availables()).getTilesToChange():
                self.changeSprite(casilla, 3)
        self.updateScore()
        if self.ia.checkAvailablesFor(self.board, "o"):
            self.Turn+=1
            self.canSelect = True
        elif self.ia.checkAvailablesFor(self.board, "x"):
            self.redAction()

    def setLabels(self):
        self.title = self.createLabel('Planets of the Galaxy', (450,800))
        self.add(self.title)
        self.vs = self.createLabel('vs', (450,750))
        self.add(self.vs)
        self.blue_score = self.createLabel("", (400,750), (79, 164, 184, 255))
        self.add(self.blue_score)
        self.red_score = self.createLabel("", (500,750), (230, 69, 57, 255))
        self.add(self.red_score)
        self.updateScore()

    def createLabel(self, text, position, color=(255, 255, 255, 255)):
        return cocos.text.Label(text,
        font_name = 'DPComic',
        font_size = 32,
        position = position,
        color = color,
        anchor_x = 'center', anchor_y = 'center')

    def updateScore(self):
        self.board.updateScore()
        self.blue_score.element.text = str(len(self.board.blue))
        self.red_score.element.text = str(len(self.board.red))