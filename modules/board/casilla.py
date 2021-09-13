import cocos
import pyglet

default_path_img = "assets/planets/default.png"
available_path_img = "assets/planets/available.png"
dry_path_img = "assets/planets/dry.png"
wet_path_img = "assets/planets/wet.png"

class Casilla:
    def __init__(self, position):
        self.valor = "-"
        self.position = position
        self.setDefault()
    
    def setDefault(self):
        self.__setSprite(default_path_img)
    def setAvailable(self):
        self.__setSprite(available_path_img)
    def setDry(self):
        self.__setSprite(dry_path_img)
    def setWet(self):
        self.__setSprite(wet_path_img)

    def __setSprite(self, path):
        self.sprite = pyglet.image.ImageGrid(pyglet.image.load(path), 1, 50)
        self.sprite = pyglet.image.Animation.from_image_sequence(self.sprite[0:], 0.2)
        self.sprite = cocos.sprite.Sprite(self.sprite, self.position)