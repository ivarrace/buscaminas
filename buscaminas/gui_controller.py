from tkinter import Button, Frame, Tk, messagebox


class GuiController:
    window = None
    frame_tablero = None

    def __init__(self):
        self.window = Tk()
        self.window.title("Buscaminas")
        self.frame_tablero = Frame(self.window)
        self.frame_tablero.grid()

    def launch(self):
        self.window.mainloop()

    def add_celda_tablero(self, celda, left_click_action, right_click_action):
        button = Button(self.frame_tablero, bg=Color.CELDA_DEFAULT, activebackground=Color.CELDA_DEFAULT_OVER)
        button.bind("<Button-1>", left_click_action)
        button.bind("<Button-3>", right_click_action)
        button.config(height=1, width=1)
        button.grid(row=celda.posicion_x, column=celda.posicion_y)
        return button

    def revela_celda_con_mina(self, celda):
        celda.gui.configure(bg=Color.CELDA_MINA, state="disabled", text="X")

    def revela_celda_sin_mina(self, celda):
        celda.gui.configure(bg=Color.CELDA_LIBRE, state="disabled", text=str(celda.minas_cercanas))

    def bloquear_celda(self, celda):
        celda.gui.configure(bg=Color.CELDA_DEFAULT, activebackground=Color.CELDA_DEFAULT_OVER)

    def desbloquear_celda(self, celda):
        celda.gui.configure(bg=Color.CELDA_SEGURA, activebackground=Color.CELDA_SEGURA_OVER)

    def reset_tablero(self):
        self.frame_tablero.grid_forget()
        self.frame_tablero.destroy()
        self.frame_tablero = Frame(self.window)
        self.frame_tablero.grid()

    def game_over(self, game_controller):
        if messagebox.askretrycancel("Game over", "BOOM!"):
            game_controller.set_new_game()
        else:
            quit()

    def winner(self, game_controller):
        if messagebox.askquestion("You win", "¿Jugar de nuevo?"):
            game_controller.set_new_game()
        else:
            quit()


class Color:
    CELDA_DEFAULT = "grey"
    CELDA_DEFAULT_OVER = "darkgrey"
    CELDA_SEGURA = "blue"
    CELDA_SEGURA_OVER = "darkblue"
    CELDA_LIBRE = "green"
    CELDA_MINA = "red"
