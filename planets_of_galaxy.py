import cocos
import modules.board.background as background
import modules.board.tablero as tablero

if __name__ == "__main__":
    cocos.director.director.init(width=900, height=900, caption="Planets of the Galaxy")
    scene = cocos.scene.Scene()
    bkg = background.BackgroundLayer()
    tb = tablero.Tablero()
    scene.add(bkg)
    scene.add(tb)
    cocos.director.director.run(scene)
