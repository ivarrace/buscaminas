from tkinter import *
from buscaminas import Buscaminas

window = Tk()
window.title("Buscaminas")
bm = Buscaminas(10, 10, 10)
bm.play(window)

window.mainloop()
