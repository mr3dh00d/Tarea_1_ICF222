import cocos
import modules.background as background
import modules.game as game

if __name__ == "__main__":
    cocos.director.director.init(width=900, height=900, caption="Planets of the Galaxy")
    scene = cocos.scene.Scene()
    bkg = background.BackgroundLayer()
    tb = game.Game()
    scene.add(bkg)
    scene.add(tb)
    cocos.director.director.run(scene)
