import cocos
import pyglet
from random import randint

class BackgroundLayer(cocos.layer.Layer):
    def __init__(self):
        super().__init__()
        self.spr = cocos.sprite.Sprite('assets/background.png')
        self.spr.position = 450, 450
        self.add(self.spr)
        ls = pyglet.image.ImageGrid(pyglet.image.load('assets/little-star.png'),1,5)
        ls_anim = pyglet.image.Animation.from_image_sequence(ls[0:], 0.1)
        postions_stars = []
        for n in range(randint(70, 80)):
            while True:
                position = randint(8, 892), randint(8, 892)
                if position not in postions_stars:
                    postions_stars.append(position)
                    break
        for p in postions_stars:
            spr_ls = cocos.sprite.Sprite(ls_anim, p)
            spr_ls.scale = (0.27)
            self.add(spr_ls)
