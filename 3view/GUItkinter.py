import tkinter
from tkinter import Tk,ttk

import GUIBotones
import GUIinicioSesion

ventana = Tk()
ventana.title("Calculadora Grafica")
ventana.grid_columnconfigure((0),uniform="a",weight=1)
ventana.grid_rowconfigure((0),uniform="a",weight=1)

def ejecutarCalculadora():
    global ventana
    ventana.resizable(True,True)
    seccionCalculadora = ttk.Frame(ventana)
    seccionCalculadora.grid(row=0,column=0,sticky="nsew")
    seccionCalculadora.grid_columnconfigure(0,weight=2)
    seccionCalculadora.grid_columnconfigure(1,weight=1)
    seccionCalculadora.grid_rowconfigure((0,2),weight=2)
    seccionCalculadora.grid_rowconfigure(1,weight=1)

    

    frameGrafica = ttk.Frame(seccionCalculadora)
    frameGrafica.grid(row=0,column=0,sticky="nsew")
    GUIBotones.graficarFunciones(frameGrafica)

    frameOperacion = ttk.Frame(seccionCalculadora)
    frameOperacion.grid(row=1,column=0)
    labelOperacion = tkinter.Label(frameOperacion)
    labelOperacion.grid(row=0,column=0)
    GUIBotones.inicializarLatex(labelOperacion)
    GUIBotones.graficarLatex()
    frameBotones = ttk.Frame(seccionCalculadora)
    frameBotones.grid(row=2,column=0,sticky="nsew")
    frameBotones.grid_columnconfigure((0,1,2,3,4,5,6,7),weight=1)
    frameBotones.grid_rowconfigure((0,1,2,3),weight=1)
    GUIBotones.botonesNumeros(frameBotones,seccionCalculadora)
    GUIBotones.botonesOperaciones(frameBotones,seccionCalculadora)


    botonEnter = ttk.Button(frameBotones,text="Enter",command=lambda:GUIBotones.enterButtonCommand(frameHistorial,labelOperacion,seccionCalculadora))
    botonEnter.grid(row=3,column=5,sticky="nsew")

    frameHistorial = ttk.Frame(seccionCalculadora)
    frameHistorial.grid(row=0,column=1,rowspan=3)
    frameHistorial.grid_rowconfigure((0,1),weight=1)
    GUIBotones.botonesHistorial(frameHistorial,labelOperacion,seccionCalculadora)
    seccionCalculadora.update()

    seccionCalculadora.bind("<Return>",lambda e: GUIBotones.enterButtonCommand(frameHistorial,labelOperacion,seccionCalculadora))
    seccionCalculadora.bind("<Configure>",lambda e:GUIBotones.cambiarTamaño(seccionCalculadora))

    seccionCalculadora.tkraise()

def run():
    ventana.grid_columnconfigure(0,weight=1,uniform="a")
    ventana.grid_rowconfigure(0,weight=1,uniform="a")
    GUIinicioSesion.creacionSeccionAcceso(ventana,ejecutarCalculadora)

if __name__ == "__main__":
    run()

