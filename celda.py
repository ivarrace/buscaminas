class Celda:
    posicion_x = 0
    posicion_y = 0
    tiene_mina = False
    minas_cercanas = 0
    button = None
    descubierta = False
    asegurada = False

    def __init__(self, x, y):
        self.posicion_x = x
        self.posicion_y = y
