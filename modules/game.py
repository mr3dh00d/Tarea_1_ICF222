import cocos
import modules.possibility as possibility
import modules.casilla as casilla
import modules.ia as ia
from modules.sleeper import sleeper
from modules.inPlanet import inPlanet
from random import randint

N = 6

class Game(cocos.layer.Layer):
    is_event_handler = True
    def __init__(self):
        super().__init__()
        self.canSelect = True
        self.Turn = 1
        self.casillas =  []
        self.availables = []
        self.red = []
        self.blue = []
        position = (190, 100)
        r = randint(0,1)
        for i in range(N):
            self.casillas.append([])
            for j in range(N):
                self.casillas[i].append(casilla.Casilla((position[0] + (104*i), position[1] + (104*j))))
                if((i, j) == (2+r, 2) or (i, j)== (3-r, 3)):#(i, j) == (2, 3) or (i,j) == (3, 3) or (i,j) == (3, 4):#((i, j) == (4,5) or (i, j) == (5, 4)):
                    self.casillas[i][j].setDry()
                    self.red.append((i, j))
                elif((i, j)== (3-r, 2) or (i, j) == (2+r, 3)):#(i ,j) == (2, 2) or (i, j) == (2, 4):#((i, j) == (4,4) or (i, j) == (5, 5)):
                    self.casillas[i][j].setWet()
                    self.blue.append((i, j))
                self.add(self.casillas[i][j].sprite)
        self.setLabels()
        print("en blue hay: ", self.blue)
        self.checkAvailablesFor(self.blue)

    def checkAvailablesFor(self, objetives):
        self.availables = []
        for objetive in objetives:
            self.checkAdjacency(objetive)

    def checkAdjacency(self, point):
        x, y = point
        for i in range(x-1, x+2):
            for j in range(y-1, y+2):
                if (N > i >= 0 and N > j >= 0) and (i != x or j != y):
                    val = self.casillas[i][j].value
                    # print("del punto:", point, "reviso casilla:", (i, j), "su valor es:", val, end=" ")
                    if(val == self.reverse(self.casillas[x][y].value)):
                        # print("revisare su posiblidad...", end=" ")
                        available = self.checkPossibility(point, (i-x, j-y))
                        if available:
                            # print("es posible en el punto", available, end=" ")
                            if available not in [a.point for a in self.availables]:
                                pos = possibility.Possibility()
                                pos.point = available
                                pos.objetives.append(point)
                                self.availables.append(pos)
                            else:
                                for ava in self.availables:
                                    if ava.point == available:
                                        ava.objetives.append(point)

                    #     else: 
                    #         print("no es posible", end=" ")
                    # print()

    def checkPossibility(self, point, direction):
        x, y = point
        dirx, diry = direction
        count = 1
        posibility = False
        obj = self.reverse(self.casillas[x][y].value)
        while True:
            i, j = x+(dirx*count), y+(diry*count)
            if 0 > i or i > N-1 or 0 > j or j > N-1:
                posibility = False
                break
            cursor = self.casillas[i][j].value
            if cursor == obj:
                posibility = True
                count += 1
                continue
            if posibility and cursor == "-":
                posibility = (i, j)
                break
            else:
                posibility = False
                break
        return posibility
    
    def reverse(self, value):
        if value == "x":
            return "o"
        elif value == "o":
            return "x"
    

    def changeSprite(self, position, option):
        x, y = position
        self.remove(self.casillas[x][y].sprite)
        self.casillas[x][y].setByNumber(option)
        self.add(self.casillas[x][y].sprite)

    def on_mouse_motion (self, x, y, dx, dy):
        if self.canSelect:
            for available in [a.point for a in self.availables]:
                i, j = available
                inP = inPlanet(self.casillas[i][j].position, (x,y))
                if(inP and self.casillas[i][j].state != "available"):
                    self.changeSprite((i, j), 2)
                elif(not inP and self.casillas[i][j].state == "available"):
                    self.changeSprite((i, j), 1)
                
    def on_mouse_press (self, x, y, buttons, modifiers):
        if self.canSelect and self.Turn%2 == 1:
            ip = False
            for available in self.availables:
                i, j = available.point
                if inPlanet(self.casillas[i][j].position, (x, y)):
                    self.Turn+=1
                    self.canSelect = False
                    select = available
                    ip = True
                    break
            if ip:
                for casilla in select.getTilesToChange():
                    self.changeSprite(casilla, 4)
                self.updateScore()
                self.checkAvailablesFor(self.red)
                self.redAction()
    
    def redAction(self):
        for casilla in ia.minimax(self.availables).getTilesToChange():
            self.changeSprite(casilla, 3)
        self.updateScore()
        self.checkAvailablesFor(self.blue)
        self.Turn+=1
        self.canSelect = True
        # for available in self.availables:
        #     print(available.point, available.objetives, available.getTilesToChange())
    # def on_mouse_motion (self, x, y, dx, dy):
        # ip = False
        # for i in range(N):
        #     for j in range(N):
        #         if(inPlanet(self.casillas[i][j].position, (x,y))):
        #             ip = True
        #             break
        #     if(ip):
        #         break
        # if(ip):
        #     print("estoy en el planeta", (i,j))

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
        self.blue = []
        self.red = []
        for x in range(N):
            for y in range(N):
                if self.casillas[x][y].value == "x":
                    self.red.append((x,y))
                if self.casillas[x][y].value == "o":
                    self.blue.append((x,y))
        self.blue_score.element.text = str(len(self.blue))
        self.red_score.element.text = str(len(self.red))