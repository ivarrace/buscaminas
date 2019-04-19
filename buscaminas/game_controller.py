import random


class GameController:
    tablero = []
    num_filas = 0
    num_columnas = 0
    num_minas = 0
    num_seguros = 0
    celdas_reveladas = 0
    gui = None

    def __init__(self, num_filas, num_columnas, num_minas):
        self.num_filas = num_filas
        self.num_columnas = num_columnas
        self.num_minas = num_minas
        print("Tablero: " + str(self.num_filas) + "x" + str(self.num_columnas))
        print("Número de minas: " + str(self.num_minas))

    def set_default_game_data(self):
        self.tablero = []
        self.num_seguros = 0
        self.celdas_reveladas = 0

    def set_gui(self, gui_controller):
        self.gui = gui_controller

    def set_new_game(self):
        self.set_default_game_data()
        self.init_celdas()
        self.init_minas()
        for fila in range(0, self.num_filas):
            for columna in range(0, self.num_columnas):
                celda = self.get_celda(fila, columna)
                button = self.gui.add_celda_tablero(celda, lambda event, c1=celda: self.revelar_celda(c1),
                                                    lambda event, c1=celda: self.asegurar_celda(c1))
                celda.gui = button

    def get_celda(self, fila, columna):
        return self.tablero[fila][columna]

    # Genera una celda nueva en cada elemento del tablero
    def init_celdas(self):
        for i in range(self.num_filas):
            self.tablero.append([])
            for j in range(self.num_columnas):
                self.tablero[i].append(Celda(i, j))

    # Genera minas de forma aleatoria
    def init_minas(self):
        for i in range(self.num_minas):
            # Genera posiciones aleatorias hasta que encuentra una sin mina
            while True:
                fila = random.randrange(0, self.num_filas)
                columna = random.randrange(0, self.num_columnas)
                if not self.tablero[fila][columna].tiene_mina:
                    # Encuentra una posición válida
                    self.tablero[fila][columna].tiene_mina = True
                    # Actualiza las celdas adyacentes
                    for celda in self.obtener_celdas_adyacentes(fila, columna):
                        celda.minas_cercanas += 1
                    # Una vez genera la mina aleatoria, sale del bucle infinito
                    break

    # Busca las celdas adyacentes en de una posición, dentro de los límites del tablero
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
            self.gui.revela_celda_con_mina(celda)
            self.gui.game_over(self)
        else:
            self.celdas_reveladas += 1
            self.gui.revela_celda_sin_mina(celda)
            if celda.minas_cercanas == 0:
                for celda_adyacente in self.obtener_celdas_adyacentes(celda.posicion_x, celda.posicion_y):
                    if not celda_adyacente.descubierta:
                        self.revelar_celda(celda_adyacente)
        if self.celdas_reveladas == (self.num_filas * self.num_columnas) - self.num_minas:
            self.gui.winner(self)

    def asegurar_celda(self, celda):
        if celda.descubierta:
            return
        if celda.asegurada:
            self.num_seguros -= 1
            celda.asegurada = False
            self.gui.bloquear_celda(celda)

        else:
            if self.num_seguros >= self.num_minas:
                return
            self.num_seguros += 1
            celda.asegurada = True
            self.gui.desbloquear_celda(celda)


class Celda:
    posicion_x = 0
    posicion_y = 0
    tiene_mina = False
    minas_cercanas = 0
    gui = None
    descubierta = False
    asegurada = False

    def __init__(self, x, y):
        self.posicion_x = x
        self.posicion_y = y
