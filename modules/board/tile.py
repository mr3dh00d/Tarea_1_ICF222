import cocos
import pyglet
from modules.env import ENV

class Tile:
    def __init__(self, position: "tuple [int, int]") -> None:
        self.position = position
        self.setSprite(1)
    
    def setSprite(self, option: int) -> None:
        if option == 1:
            self.state = "default"
            self.value = "-"
            self.__setSprite(ENV["assets_paths"]["default_path_img"])
        if option == 2:
            self.state = "available"
            self.value = "-"
            self.__setSprite(ENV["assets_paths"]["available_path_img"])
        if option == 3:
            self.state = "dry"
            self.value = "x"
            self.__setSprite(ENV["assets_paths"]["dry_path_img"])
        if option == 4:
            self.state = "wet"
            self.value = "o"
            self.__setSprite(ENV["assets_paths"]["wet_path_img"])

    def __setSprite(self, path: str) -> None:
        self.sprite = pyglet.image.ImageGrid(pyglet.image.load(path), 1, 50)
        self.sprite = pyglet.image.Animation.from_image_sequence(self.sprite[0:], 0.2)
        self.sprite = cocos.sprite.Sprite(self.sprite, self.position)