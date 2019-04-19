from buscaminas.game_controller import GameController
from buscaminas.gui_controller import GuiController

gui = GuiController()
game_controller = GameController(10, 10, 10)
game_controller.set_gui(gui)
game_controller.set_new_game()
gui.launch()
