import cocos
from modules.board import tile
from modules.game import possibility
from random import randint
from modules.env import ENV

N = ENV["number_of_tiles"]
SPACE = ENV["sprite_size"]+ENV["space_between_tiles"]

class Board:
    def __init__(self, add=None, create_sprites=True) -> None:
        self.tiles =  []
        self.__availables = []
        self.red = []
        self.blue = []
        if create_sprites:
            self.__init_with_sprite(add)


    def __init_with_sprite(self, add: "function(cocos.cocosnode.CocosNode)") -> None:
        position = (190, 100)
        r = randint(0,1)
        for i in range(N):
            self.tiles.append([])
            for j in range(N):
                pos = (i, j)
                tl = tile.Tile()
                tl.position = (position[0] + (SPACE*i), position[1] + (SPACE*j))
                self.tiles[i].append(tl)
                if(pos == (2+r, 2) or pos== (3-r, 3)):
                    self.getTile(pos).setSprite(3)
                    self.red.append(pos)
                elif(pos== (3-r, 2) or pos == (2+r, 3)):
                    self.getTile(pos).setSprite(4)
                    self.blue.append(pos)
                else:
                    self.getTile(pos).setSprite(1)
                add(self.getTile(pos).sprite)

    def getTile(self, position: "tuple[int, int]") -> tile.Tile:
        i, j = position
        return self.tiles[i][j]

    def setTile(self, position: "tuple[int, int]", value: str) -> None:
        self.getTile(position).value = value
        self.updateScore()

    def updateScore(self) -> None:
        self.blue = []
        self.red = []
        for x in range(N):
            for y in range(N):
                position = (x, y)
                if self.getTile(position).value == "x":
                    self.red.append((x,y))
                if self.getTile(position).value == "o":
                    self.blue.append((x,y))

    def availables(self, set=False) -> "list[possibility.Possibility]":
        if type(set) == list:
            self.__availables = set
        return self.__availables