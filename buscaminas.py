from tkinter import Button
from tkinter import Frame
from tkinter import messagebox
from celda import Celda
import random


class Buscaminas:
    COLOR_CELDA_DEFAULT = "grey"
    COLOR_CELDA_DEFAULT_OVER = "darkgrey"
    COLOR_CELDA_SEGURA = "blue"
    COLOR_CELDA_SEGURA_OVER = "darkblue"
    COLOR_CELDA_LIBRE = "green"
    COLOR_CELDA_MINA = "red"

    tablero = []
    num_filas = 10
    num_columnas = 10
    num_minas = 10
    num_seguros = 0
    celdas_reveladas = 0
    root_window = None
    frame = None

    def __init__(self, num_filas, num_columnas, num_minas):
        self.num_filas = num_filas
        self.num_columnas = num_columnas
        self.num_minas = num_minas
        print("Tablero: " + str(self.num_filas) + "x" + str(self.num_columnas))
        print("Número de minas: " + str(self.num_minas))

    def play(self, window):
        self.root_window = window
        self.frame = Frame(self.root_window)
        self.frame.grid()
        self.tablero = []
        self.num_seguros = 0
        self.celdas_reveladas = 0
        
        self.init_celdas()
        self.init_minas()
        for r in range(0, self.num_filas):
            for c in range(0, self.num_columnas):
                celda = self.get_celda(r, c)
                entry = Button(self.frame, bg=self.COLOR_CELDA_DEFAULT, activebackground=self.COLOR_CELDA_DEFAULT_OVER)
                entry.bind("<Button-1>", lambda event, c1=celda: self.revelar_celda(c1))
                entry.bind("<Button-3>", lambda event, c1=celda: self.asegurar_celda(c1))
                entry.config(height=1, width=1)
                entry.grid(row=r, column=c)
                celda.button = entry

    def init_minas(self):
        for i in range(self.num_minas):
            while True:
                fila = random.randrange(0, self.num_filas)
                columna = random.randrange(0, self.num_columnas)
                if not self.tablero[fila][columna].tiene_mina:
                    self.tablero[fila][columna].tiene_mina = True
                    self.actualizar_celdas_adyacentes(fila, columna)
                    break

    def init_celdas(self):
        for i in range(self.num_filas):
            self.tablero.append([])
            for j in range(self.num_columnas):
                self.tablero[i].append(Celda(i, j))

    def get_celda(self, fila, columna):
        return self.tablero[fila][columna]

    def actualizar_celdas_adyacentes(self, fila, columna):
        for celda in self.obtener_celdas_adyacentes(fila, columna):
            celda.minas_cercanas += 1

    def obtener_celdas_adyacentes(self, fila, columna):
        celdas_adyacentes = []
        for i in [fila - 1, fila, fila + 1]:
            if 0 <= i < self.num_filas:
                for j in [columna - 1, columna, columna + 1]:
                    if 0 <= j < self.num_columnas:
                        celdas_adyacentes.append(self.get_celda(i, j))
        return celdas_adyacentes

    def revelar_celda(self, celda):
        if celda.asegurada:
            return
        celda.descubierta = True
        if celda.tiene_mina:
            celda.button.configure(bg=self.COLOR_CELDA_MINA, state="disabled", text="X")
            self.game_over()
        else:
            self.celdas_reveladas += 1
            celda.button.configure(bg=self.COLOR_CELDA_LIBRE, state="disabled", text=str(celda.minas_cercanas))
            if celda.minas_cercanas == 0:
                for celda_adyacente in self.obtener_celdas_adyacentes(celda.posicion_x, celda.posicion_y):
                    if not celda_adyacente.descubierta:
                        self.revelar_celda(celda_adyacente)
        if self.celdas_reveladas == (self.num_filas * self.num_columnas) - self.num_minas:
            if messagebox.askquestion("You win", "¿Jugar de nuevo?"):
                self.reload_game()
            else:
                self.exit_game()

    def asegurar_celda(self, celda):
        if celda.descubierta:
            return
        if celda.asegurada:
            self.num_seguros -= 1
            celda.asegurada = False
            celda.button.configure(bg=self.COLOR_CELDA_DEFAULT, activebackground=self.COLOR_CELDA_DEFAULT_OVER)
        else:
            if self.num_seguros >= self.num_minas:
                return
            self.num_seguros += 1
            celda.asegurada = True
            celda.button.configure(bg=self.COLOR_CELDA_SEGURA, activebackground=self.COLOR_CELDA_SEGURA_OVER)

    def game_over(self):
        if messagebox.askretrycancel("Game over", "BOOM!"):
            self.reload_game()
        else:
            self.exit_game()

    def reload_game(self):
        self.frame.grid_forget()
        self.frame.destroy()
        self.play(self.root_window)

    def exit_game(self):
        quit()
