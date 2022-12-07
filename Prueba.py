from tkinter import *
from tkinter import messagebox
import winsound
import threading
import random
import time
import tkinter as tk

#/////////////////////////////////////////////////////////////////VENTANA PRINCIPAL///////////////////////////////////////////////////////////////////////////////
#/////////////////////////////////////////////////////////////////VENTANA PRINCIPAL///////////////////////////////////////////////////////////////////////////////
#/////////////////////////////////////////////////////////////////VENTANA PRINCIPAL///////////////////////////////////////////////////////////////////////////////

#Creacion de la ventana principal
mainwin = tk.Tk()
mainwin.title("Menu")
mainwin.geometry('605x505+100+50')
mainwin.resizable(width=False, height=False)
mainwin.configure(background="black")
#llamada de la foto para utilizar en el canva
imagebackgroundmainwin=PhotoImage(file="fondo.gif")
welcome = tk.Canvas(mainwin, width=605, height=505)
welcome.pack()
#creacion de cada texto en el lienzo(canva)
welcome.create_image(0, 0, image=imagebackgroundmainwin, anchor=NW)
welcome.create_text(300, 20, text="Bienvenido al Simulador", fill="white", font="algerian")
welcome.create_text(100, 50, text="Instrucciones de uso:", fill="white", font="arial")
welcome.create_text(300, 80, text="1- Si desea conocer los datos utilizados anteriormente, seleccione 'datos guardados' y luego 'leer datos'", fill="white")
welcome.create_text(300, 100, text="2- Debe configurar las opciones deseadas para habilitar la animacion", fill="white")
welcome.create_text(300, 120, text="3- Ingrese correctamente como se indican los datos y guardelos", fill="white")
welcome.create_text(300, 140, text="4- Si desea ver los datos guardos, realice el paso 1 y verifique la fecha con la hora de la configuracion", fill="white")
welcome.create_text(300, 160, text="5- Luego de verificar la configuracion, ya puede iniciar la simulacion con esta configuracion", fill="white")

#////////////////////////////////////////////////////////////////CONFIGURACIONES//////////////////////////////////////////////////////////////////////////////////
#////////////////////////////////////////////////////////////////CONFIGURACIONES//////////////////////////////////////////////////////////////////////////////////
#////////////////////////////////////////////////////////////////CONFIGURACIONES//////////////////////////////////////////////////////////////////////////////////

#Funcion para el toplevel de configuraciones
def Configuraciones():
    mainwin.deiconify()
    #Ventana para configurar
    global configurations
    configurations = tk.Toplevel()
    configurations.title("Configuraciones")
    configurations.geometry('380x400+725+150')
    configurations.resizable(width=False, height=False)
    configurations.configure(background="gray")
    #Boton para guardar los datos
    global Save
    Save = tk.Button(configurations, text="Guardar", command=SaveTxT)
    Save.place(x=170, y=340)
    Save.configure(state="normal")
    #Boton para salir de la ventana
    Exit = tk.Button(configurations, text="Salir", command=configurations.destroy)
    Exit.place(x=335, y=365)
    #Label y entry para el tiempo del splash
    timeSplash = tk.Label(configurations, text="Tiempo del splash, por favor ingrese solo el numero\n\n5 segundos\n10 segundos", bg="gray")
    timeSplash.place(x=15, y=25)
    global splash
    splash = tk.IntVar()
    splash.set(0)
    splashEntry = tk.Entry(configurations, textvariable = splash)
    splashEntry.place(x=250, y=65, height=20, width=35)
    #Label y entry para el CB-EW
    CB_EW = tk.Label(configurations, text="Uso del CB-EW, por favor ingrese un valor booleano\n\nTrue = Activado = 1\nFalse = Desactivado = 0", bg="gray")
    CB_EW.place(x=15, y=100)
    global CBEW
    CBEW = tk.BooleanVar()
    CBEW.set(True)
    CBEWEntry = tk.Entry(configurations, textvariable = CBEW)
    CBEWEntry.place(x=250, y=140, height=20, width=35)
    #Label y entry para el parametro de proximidad
    proximited = tk.Label(configurations, text="Parametro de proximidad, por favor ingrese solo el numero\n\n10 metros\n20 metros", bg="gray")
    proximited.place(x=15, y=175)
    global parametro
    parametro = tk.IntVar()
    parametro.set(0)
    parametroEntry = tk.Entry(configurations, textvariable = parametro)
    parametroEntry.place(x=250, y=215, height=20, width=35)
    #Label y radiobotons para el indicador de cambio o frenado
    indicador = tk.Label(configurations, text="Seleccione el indcador", bg="gray")
    indicador.place(x=15, y=250)
    global indicator
    indicator = IntVar()
    indicator.set(2)
    radiobutton1 = tk.Radiobutton(configurations, text="Cambiar de Carril", variable=indicator, value=1)
    radiobutton1.place(x=30, y=290)
    radiobutton2 = tk.Radiobutton(configurations, text="Frenado de emergencia", variable=indicator, value=2)
    radiobutton2.place(x=200, y=290)
    
#Funcion que se encarga de desbloquear los botones faltantes en mainwin, verifica que los datos sean correctos y guarda los datos en un txt para luego leerlos
def SaveTxT():
    Save.configure(state="disabled")
    startanimation.configure(state="normal")
    Splash = splash.get()
    CBEWW = CBEW.get()
    Parametro = parametro.get()
    if Splash == 10 or Splash == 5: #valida los 2 valores del splash
        if CBEWW == True or CBEWW == False: #valida los 2 valores del sensor
            if Parametro == 10 or Parametro == 20: #valida los 2 valores del parametro
                configurationsB.configure(state="disabled")
                date = str(time.strftime("%H:%M:%S")) + "  " + str(time.strftime("%d/%m/%y")) #Formato de 24 horas y fecha
                dataArchivo = open("data.txt", "w")
                dataArchivo.write(date)
                dataArchivo.write("\nLa configuracion usada de esta fecha es: ")
                dataArchivo.write("\n\nTiempo del splash: " + str(Splash) + " segundos")
                dataArchivo.write("\nCB-EW esta: " + str(CBEWW))
                dataArchivo.write("\nEl parametro esta configurado en: " + str(Parametro) + " metros")
                if indicator.get() == 1: #valdia el indicador
                    dataArchivo.write("\nSe realiza cambio de carril")
                else:
                    dataArchivo.write("\nSe realiza freno de emergencia")
                dataArchivo.close()
            else:
                configurations.destroy()
                messagebox.showwarning("Error", "Ingrese correctamente los valores del Parametro")
                return Configuraciones()
        else:
            configurations.destroy()
            messagebox.showwarning("Error", "Ingrese correctamente los valores del CB-EW")
            return Configuraciones()
    else:
        configurations.destroy()
        messagebox.showwarning("Error", "Ingrese correctamente los valores del Splash")
        return Configuraciones()

#/////////////////////////////////////////////////////////////////SPLASH ANIMADO///////////////////////////////////////////////////////////////////////////////////
#/////////////////////////////////////////////////////////////////SPLASH ANIMADO///////////////////////////////////////////////////////////////////////////////////
#/////////////////////////////////////////////////////////////////SPLASH ANIMADO///////////////////////////////////////////////////////////////////////////////////

#funcion para la ventana de animacion antes de iniciar el simulador
def winani():
    mainwin.withdraw()
    #Ventana de animacion
    global animacionW
    animacionW = tk.Toplevel()
    animacionW.title("Ficha Personal")
    animacionW.geometry('440x440+425+50')
    animacionW.resizable(width=False, height=False)
    animacionW.configure(background="gray")
    welcome = tk.Label(animacionW, text="Hola Bienvenido Al Simulador Aguero", font=("Castellar",12))
    welcome.pack(fill=tk.X)
    return IniAni()

#funcion para iniciar los hilos de la animacion
def IniAni():
    global animacion
    animacion = Canvas(animacionW, width=100, height=100, bg="gray")
    animacion.pack(expand=YES, fill=BOTH)
    C1.start()
    C2.start()
    C3.start()
    C4.start()

#time = parametro configurado antes
tiempo = 0   
pos = [25, 50, 75, 100, 125, 150, 175, 200, 225, 250, 275, 300, 325, 350, 375, 400]

#funciones para crear cuadrados de colores aleatorios, funcion reutilizada de tarea anterior
def cuadrado1():
    if tiempo < 2*splash.get():
        random.shuffle(pos)
        animacion.create_rectangle(pos[0], pos[1], pos[2], pos[3], width=2, outline='yellow')
        time.sleep(0.5)
        return cuadrado1()
def cuadrado2():
    if tiempo < 2*splash.get():
        random.shuffle(pos)
        animacion.create_rectangle(pos[0], pos[1], pos[2], pos[3], width=3, outline='red')
        time.sleep(0.5)
        return cuadrado2()
def cuadrado3():
    if tiempo < 2*splash.get():
        random.shuffle(pos)
        animacion.create_rectangle(pos[0], pos[1], pos[2], pos[3], width=3, outline='black')
        time.sleep(0.5)
        return cuadrado3()
def cuadrado4():
    global tiempo
    tiempo += 1
    if tiempo < 2*splash.get():
        random.shuffle(pos)
        animacion.create_rectangle(pos[0], pos[1], pos[2], pos[3], width=2, outline='green')
        time.sleep(0.5)
        return cuadrado4()
    else:
        time.sleep(1)
        animacionW.destroy()
        return StarSimulator()

#Creacion de hilos
C1 = threading.Thread(name="Hilo1", target=cuadrado1)
C2 = threading.Thread(name="Hilo2", target=cuadrado2)
C3 = threading.Thread(name="Hilo3", target=cuadrado3)
C4 = threading.Thread(name="Hilo4", target=cuadrado4)
    
#//////////////////////////////////////////////////////////////////SIMULADOR///////////////////////////////////////////////////////////////////////////////////////    
#//////////////////////////////////////////////////////////////////SIMULADOR///////////////////////////////////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////////////SIMULADOR///////////////////////////////////////////////////////////////////////////////////////

#2 listas, para cargar las imágenes una sola vez y el los carriles 1 y 2
images = [PhotoImage(file="carretera.gif"),
          PhotoImage(file="carrobase.gif"),
          PhotoImage(file="carro.gif")]

carriles = [150, 300]

#Funcion para la ventana del simulador e inicia el splash
def StarSimulator(): 
    mainwin.withdraw()
    #Ventana para el simulador
    global simulator
    simulator = tk.Toplevel()
    simulator.title("Simulador")
    simulator.geometry('450x600+425+050')
    simulator.resizable(width=False, height=False)
    global simulacion
    simulacion = Canvas(simulator, width=450, height=600)
    simulacion.pack()
    simulacion.create_image(225, 300, image=images[0])
    global carro_base
    carro_base = simulacion.create_image(carriles[random.randint(0,1)], 500, image=images[1])
    time.sleep(2)
    if CBEW.get() == True: #valida actividad del sensor
        if indicator.get() == 1: #cambio de carril
            return cambio_carril()
        elif indicator.get() == 2: #frenado de emergencia
            return frenado()
    else:
        return Sin_CBEW() #Simulador sin CBEW

#///////////////////////////////////////////////////////////FRENADO DE EMERGENCIA/////////////////////////////////////////////////////////////////////////////////

#se encarga de crear un carro aleatoriamente en un carril
def frenado():
    if random.randint(1,2) == 2:
        global carro_1
        carro_1 = simulacion.create_image(150, 90, image=images[2])
        return movement_1()
    else:
        global carro_2
        carro_2 = simulacion.create_image(300, 90, image=images[2])
        return movement_2()

#movimiento carro 1 carril izquierdo, valida cuando el carro está cerca y en el mismo carril y redirecciona para deternerlo 
def movement_1():
    simulacion.move(carro_1, 0, 1)
    movimiento1 = simulacion.after(15, movement_1)
    if simulacion.coords(carro_1)[1] >= simulacion.coords(carro_base)[1] - 170 - parametro.get() and simulacion.coords(carro_1)[0] == simulacion.coords(carro_base)[0]:
        winsound.PlaySound("frenado.wav", winsound.SND_FILENAME)
        simulacion.after_cancel(movimiento1)
        return movement_stop_1()
    elif simulacion.coords(carro_1)[1] > 680:
        simulacion.after_cancel(movimiento1)
        simulacion.delete(carro_1)
        return frenado()        
def movement_stop_1():
    simulacion.move(carro_1, 0, -0.5)
    movimiento2 = simulacion.after(15, movement_stop_1)

#movimiento carro 2 carril derecho, valida cuando el carro está cerca y en el mismo carril y redirecciona para deternerlo  
def movement_2():
    simulacion.move(carro_2, 0, 1)
    movimiento2 = simulacion.after(15, movement_2)
    if simulacion.coords(carro_2)[1] >= simulacion.coords(carro_base)[1] - 170 - parametro.get() and simulacion.coords(carro_2)[0] == simulacion.coords(carro_base)[0]:
        winsound.PlaySound("frenado.wav", winsound.SND_FILENAME)
        simulacion.after_cancel(movimiento2)
        return movement_stop_2()
    elif simulacion.coords(carro_2)[1] > 680:
        simulacion.after_cancel(movimiento2)
        simulacion.delete(carro_2)
        return frenado()    
def movement_stop_2():
    simulacion.move(carro_2, 0, -0.5)
    movimiento2 = simulacion.after(15, movement_stop_2)
        
#//////////////////////////////////////////////////////////////////CAMBIO DE CARRIL////////////////////////////////////////////////////////////////////////////////        

#para verificar cuando hay 2 carros o solo 1 en los carriles.
doble = 0

#funcion que se encarga de crear los carros aleatoriametne y redireccionar al movimiento segun el caso
def cambio_carril():
    if random.randint(1,2) == 2:
        global carro_3
        carro_3 = simulacion.create_image(150, 90, image=images[2])
        return movement_3()
    elif random.randint(1,2) == 2:
        global carro_4
        carro_4 = simulacion.create_image(300, 90, image=images[2])
        return movement_4()
    else:
        global doble
        doble = 1
        carro_3 = simulacion.create_image(150, 90, image=images[2])
        carro_4 = simulacion.create_image(300, 90, image=images[2])
        return movement_3(), movement_4()

#movimiento carro 3 carril izquierdo, valida cuando el carro está cerca y en el mismo carril y si vienen 2 carros, redirecciona para cambiar de carril
def movement_3():
    simulacion.move(carro_3, 0, 1)
    global movimiento3
    movimiento3 = simulacion.after(15, movement_3)
    if doble == 1:
        if simulacion.coords(carro_3)[1] >= simulacion.coords(carro_base)[1] - 210 - parametro.get() and simulacion.coords(carro_3)[0] == simulacion.coords(carro_base)[0] and simulacion.coords(carro_4)[1] >= simulacion.coords(carro_base)[1] - 200 - parametro.get():
            return stop()
    elif simulacion.coords(carro_3)[1] >= simulacion.coords(carro_base)[1] - 210 - parametro.get() and simulacion.coords(carro_3)[0] == simulacion.coords(carro_base)[0]:
        return movement_cambio_1()
    elif simulacion.coords(carro_3)[1] > 680:
        simulacion.after_cancel(movimiento3)
        simulacion.delete(carro_3)
        return cambio_carril()
def movement_cambio_1():
    simulacion.move(carro_base, 1, 0)
    movimiento_3 = simulacion.after(15, movement_cambio_1)
    if simulacion.coords(carro_base)[0] == 300.0:
        simulacion.after_cancel(movimiento_3)

#movimiento carro 4 carril derecho, valida cuando el carro está cerca y en el mismo carril y si vienen 2 carros, redirecciona para cambiar de carril
def movement_4():
    simulacion.move(carro_4, 0, 1)
    global movimiento4
    movimiento4 = simulacion.after(15, movement_4)
    if doble == 1:
        if simulacion.coords(carro_4)[1] >= simulacion.coords(carro_base)[1] - 210 - parametro.get() and simulacion.coords(carro_4)[0] == simulacion.coords(carro_base)[0] and simulacion.coords(carro_3)[1] >= simulacion.coords(carro_base)[1] - 200 - parametro.get():
            return stop()
    elif simulacion.coords(carro_4)[1] >= simulacion.coords(carro_base)[1] - 210 - parametro.get() and simulacion.coords(carro_4)[0] == simulacion.coords(carro_base)[0]:
        return movement_cambio_2()
    elif simulacion.coords(carro_4)[1] > 680:
        simulacion.after_cancel(movimiento4)
        simulacion.delete(carro_4)
        return cambio_carril()
def movement_cambio_2():
    simulacion.move(carro_base, -1, 0)
    movimiento_4 = simulacion.after(15, movement_cambio_2)
    if simulacion.coords(carro_base)[0] == 150.0:
        simulacion.after_cancel(movimiento_4)

#funcion que para ambos carros y manda mensaje cuando ya no se puede hacer cambio de carril
def stop():
    winsound.PlaySound("frenado.wav", winsound.SND_FILENAME)
    simulacion.after_cancel(movimiento3)
    simulacion.after_cancel(movimiento4)
    messagebox.showwarning("Peligro de colisión", "No se puede usar cambio de carril, en estas condiciones")
    

#//////////////////////////////////////////////////////////////////Sin CBEW////////////////////////////////////////////////////////////////////////////////////////     

#funcion que se encarga de crear los carros aleatoriametne y redireccionar al movimiento segun el caso
def Sin_CBEW():
    if random.randint(1,2) == 2:
        global carro_5
        carro_5 = simulacion.create_image(150, 90, image=images[2])
        return movement_5()
    else:
        global carro_6
        carro_6 = simulacion.create_image(300, 90, image=images[2])
        return movement_6()

#movimiento carro 5 carril izquierdo, valida cuando ambos carros ya chocaron y reproduce sonido de colision
def movement_5():
    simulacion.move(carro_5, 0, 1.5)
    movimiento5 = simulacion.after(15, movement_5)
    if simulacion.coords(carro_5)[1] >= simulacion.coords(carro_base)[1] - 155 and simulacion.coords(carro_5)[0] == simulacion.coords(carro_base)[0]:
        winsound.PlaySound("choque.wav", winsound.SND_FILENAME)
        simulacion.after_cancel(movimiento5)
    elif simulacion.coords(carro_5)[1] > 680:
        simulacion.after_cancel(movimiento5)
        simulacion.delete(carro_5)
        return Sin_CBEW()
        
#movimiento carro 6 carril derecho, valida cuando ambos carros ya chocaron y reproduce sonido de colision
def movement_6():
    simulacion.move(carro_6, 0, 1.5)
    movimiento6 = simulacion.after(15, movement_6)
    if simulacion.coords(carro_6)[1] >= simulacion.coords(carro_base)[1] - 155 and simulacion.coords(carro_6)[0] == simulacion.coords(carro_base)[0]:
        winsound.PlaySound("choque.wav", winsound.SND_FILENAME)
        simulacion.after_cancel(movimiento6)
    elif simulacion.coords(carro_6)[1] > 680:
        simulacion.after_cancel(movimiento6)
        simulacion.delete(carro_6)
        return Sin_CBEW()

#//////////////////////////////////////////////////////////////////LEER DATOS///////////////////////////////////////////////////////////////////////////////////////    
#//////////////////////////////////////////////////////////////////LEER DATOS///////////////////////////////////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////////////LEER DATOS///////////////////////////////////////////////////////////////////////////////////////

#Funcion data para crear la ventana donde se moestraran los datos y los botones necesarios
def Data():
    mainwin.deiconify()
    #Ventana para datos
    global data
    data = tk.Toplevel()
    data.title("Datos")
    data.geometry('330x220+220+270')
    data.resizable(width=False, height=False)
    data.configure(background="gray")
    #Boton para retornar a la funcion de leer los datos
    Read = tk.Button(data, text="Leer Datos", command=ReadTxT)
    Read.place(x=130, y=10)
    #Boton para salir de la ventana leer los datos
    Exit = tk.Button(data, text="Salir", command=data.destroy)
    Exit.place(x=290, y=190)
#funcion para abrir el archivo de texto y leerlo para mostrarlo en una Label
def ReadTxT():
    dataArchivo = open("data.txt", "r")
    DataLabel = tk.Label(data, text=dataArchivo.read())
    DataLabel.place(x=40, y=60)
    dataArchivo.close()

#/////////////////////////////////////////////////////////////BOTONES//////////////////////////////////////////////////////////////////////////////////////////////
#/////////////////////////////////////////////////////////////BOTONES//////////////////////////////////////////////////////////////////////////////////////////////
#/////////////////////////////////////////////////////////////BOTONES//////////////////////////////////////////////////////////////////////////////////////////////

#Botones ventana princiapal para las funciones deseadas
configurationsB = Button(mainwin, text="Configuraciones", command=Configuraciones)
configurationsB.place(x=70, y=450)

startanimation = Button(mainwin, text="Iniciar Simulacion", command=winani)
startanimation.place(x=250, y=450)
startanimation.configure(state="disabled")

data = Button(mainwin, text="Datos Guardados", command=Data)
data.place(x=430, y=450)


#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

mainwin.mainloop()
