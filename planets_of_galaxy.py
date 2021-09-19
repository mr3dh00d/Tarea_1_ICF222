import cocos
import modules.background as background
import modules.game as game

N = 6

if __name__ == "__main__":
    cocos.director.director.init(width=900, height=900, caption="Planets of the Galaxy")
    scene = cocos.scene.Scene()
    bkg = background.BackgroundLayer()
    gm = game.Game()
    scene.add(bkg)
    scene.add(gm)
    cocos.director.director.run(scene)
