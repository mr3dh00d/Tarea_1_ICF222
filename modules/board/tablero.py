import cocos
import modules.board.casilla as casilla
from modules.board.inPlanet import inPlanet
from random import randint

N = 6

class Tablero(cocos.layer.Layer):
    is_event_handler = True
    def __init__(self):
        super().__init__()
        self.casillas =  []
        self.red = []
        self.blue = []
        position = (190, 100)
        r = randint(0,1)
        for i in range(N):
            self.casillas.append([])
            for j in range(N):
                self.casillas[i].append(casilla.Casilla((position[0] + (104*i), position[1] + (104*j))))
                if((i == 2+r and j == 2) or (i == 3-r and j == 3)):
                    self.casillas[i][j].valor = "x"
                    self.casillas[i][j].setDry()
                    self.red.append((i, j))
                elif((i == 3-r and j == 2) or (i == 2+r and j == 3)):
                    self.casillas[i][j].valor = "o"
                    self.casillas[i][j].setWet()
                    self.blue.append((i, j))
                self.add(self.casillas[i][j].sprite)
        self.setLabels()


    def on_mouse_press (self, x, y, buttons, modifiers):
        ip = False
        for i in range(N):
            for j in range(N):
                if(inPlanet(self.casillas[i][j].position, (x,y))):
                    ip = True
                    break
            if(ip):
                break
        if(ip):
            print("estoy en un planeta")

    def setLabels(self):
        self.title = cocos.text.Label('Planets of the Galaxy',
        font_name = 'DPComic',
        font_size = 32,
        position = (450,800),
        anchor_x = 'center', anchor_y = 'center') 
        self.add(self.title)
        self.vs = cocos.text.Label('vs',
        font_name = 'DPComic',
        font_size = 32,
        position = (450,750),
        anchor_x = 'center', anchor_y = 'center') 
        self.add(self.vs)
        self.blue_score = cocos.text.Label(str(len(self.blue)),
        font_name = 'DPComic',
        font_size = 32,
        position = (400,750),
        color = (79, 164, 184, 255),
        anchor_x = 'center', anchor_y = 'center') 
        self.add(self.blue_score)
        self.red_score = cocos.text.Label(str(len(self.blue)),
        font_name = 'DPComic',
        font_size = 32,
        position = (500,750),
        color = (230, 69, 57, 255),
        anchor_x = 'center', anchor_y = 'center') 
        self.add(self.red_score)

    def updateScore(self):
        self.blue_score.element.text = str(len(self.blue))
        self.red_score.element.text = str(len(self.blue))