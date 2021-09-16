import cocos
import pyglet

default_path_img = "assets/planets/default.png"
available_path_img = "assets/planets/available.png"
dry_path_img = "assets/planets/dry.png"
wet_path_img = "assets/planets/wet.png"

class Casilla:
    def __init__(self, position):
        self.value = "-"
        self.position = position
        self.state = ""
        self.setDefault()
    
    def setByNumber(self, number):
        if number == 1:
            self.setDefault()
        if number == 2:
            self.setAvailable()
        if number == 3:
            self.setDry()
        if number == 4:
            self.setWet()


    def setDefault(self):
        self.state = "default"
        self.__setSprite(default_path_img)
    def setAvailable(self):
        self.state = "available"
        self.__setSprite(available_path_img)
    def setDry(self):
        self.state = "dry"
        self.__setSprite(dry_path_img)
    def setWet(self):
        self.state = "wet"
        self.__setSprite(wet_path_img)

    def __setSprite(self, path):
        self.sprite = pyglet.image.ImageGrid(pyglet.image.load(path), 1, 50)
        self.sprite = pyglet.image.Animation.from_image_sequence(self.sprite[0:], 0.2)
        self.sprite = cocos.sprite.Sprite(self.sprite, self.position)