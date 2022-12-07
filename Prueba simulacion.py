from tkinter import *
import tkinter as tk
import time

simulator = tk.Tk()
simulator.title("Simulador")
simulator.geometry('450x600+425+50')
simulator.resizable(width=False, height=False)
simulacion = Canvas(simulator, width=450, height=600)
simulacion.pack()
images = [PhotoImage(file="carretera.gif"),
          PhotoImage(file="carrobase.gif"),
          PhotoImage(file="carro.gif")]
simulacion.create_image(225,300, image=images[0])
carro_base = simulacion.create_image(150, 500, image=images[1])

def carro1():
    global carro_1
    carro_1 = simulacion.create_image(150, 90, image=images[2])

def movement():
    simulacion.move(carro_1, 0, 1)
    movimiento1 = simulacion.after(15, movement)
    coordenadas_carro_1 = simulacion.coords(carro_1)
    print(coordenadas_carro_1[1])
    if coordenadas_carro_1[1] >= 310:
        simulacion.after_cancel(movimiento1)
        return movement_stop()
def movement_stop():
    simulacion.move(carro_1, 0, -0.5)
    movimiento2 = simulacion.after(15, movement_stop)
        
        
button = tk.Button(simulator, text="carro1", command=carro1)
button.place(x=20, y=50)
button = tk.Button(simulator, text="avanzar", command=movement)
button.place(x=20, y=100)

simulator.mainloop()

#time.sleep(1)
#simulacion.move(carro_base, 0, -100)
  

