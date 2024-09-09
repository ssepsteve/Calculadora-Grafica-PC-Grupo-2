import tkinter.messagebox
import sys
sys.path.insert(1,"C:/Users/stves/Documents/GitHub/Proyecto-Programacion-De-Computadores/CALCULADORA GRAFICA/2controller")
import operaciones
import tkinter

import numpy as np
import matplotlib as mpl
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg , NavigationToolbar2Tk
import matplotlib.figure as mfg


from tkinter import ttk

diccionarioBotones = {}
diccionarioHistorial = {}
diccionarioScrollbar = {}
diccionarioAxGraficas = {}
operacionesPermitidas = ["+","-","/","*"]

listaColores = ["blue","purple","cyan","orange","lime","darkturquoise","steelblue",
                "grey","silver","red","brown","salmon","tomato","orangered","darkorange",
                "burlywood","gold","chartreuse","greenyellow","limegreen","darkgreen", "aquamarine","turquoise",
                "teal","aqua","cyan","deepskyblue","dodgerblue","royalblue","navy","slateblue",
                "blueviolet","indigo","mediumorchid","violet","purple","magenta","crimson","pink"]
listaNomenclatura = ['f(x)', 'g(x)', 'h(x)', 'p(x)', 'q(x)', 'r(x)', 's(x)', 't(x)', 
                     'f1(x)', 'g1(x)', 'h1(x)', 'p1(x)', 'q1(x)', 'r1(x)', 's1(x)', 't1(x)', 
                     'f2(x)', 'g2(x)', 'h2(x)', 'p2(x)', 'q2(x)', 'r2(x)', 's2(x)', 't2(x)', 
                     'f3(x)', 'g3(x)', 'h3(x)', 'p3(x)', 'q3(x)', 'r3(x)', 's3(x)', 't3(x)', 
                     'f4(x)', 'g4(x)', 'h4(x)', 'p4(x)', 'q4(x)', 'r4(x)', 's4(x)', 't4(x)']

'''---------------------LATEX--------------'''

def borrarTodoMensaje(frameH,labelOpWidget,window):
    messagebox = tkinter.messagebox.askquestion("Borrar Graficas","Desea Borrar todas las graficas de la base de datos?")
    if messagebox == "yes":
        operaciones.borrarTodasLasGraficasDeDB()
        global diccionarioScrollbar
        for key in diccionarioHistorial:
            if isinstance(diccionarioHistorial[key],mfg.Figure):
                pass
            elif isinstance(diccionarioHistorial[key],mpl.axes._axes.Axes):
                pass
            elif isinstance(diccionarioHistorial[key],FigureCanvasTkAgg):
                pass
            elif len(key) >17:
                if key[:17] == "ovaloColorFuncion":
                    diccionarioHistorial[key] = 0
                else:
                    diccionarioHistorial[key].destroy()
            else:
                diccionarioHistorial[key].destroy()
        diccionarioScrollbar["scrollBar"].destroy()
        ax.clear()
        botonesHistorial(frameH,labelOpWidget,window)
        ax.grid()
    else:
        tkinter.messagebox.showinfo("Volviendo","Volviendo a la calculadora") 

def graficarLatex():
    if operaciones.latexDisplay[-1] == "^":
        textoLatex = "$"+operaciones.latexDisplay+"ㅤ$"
    else:
        textoLatex = "$"+operaciones.latexDisplay+"$"
    axLatex.clear()
    axLatex.text(0, 0.3, textoLatex, fontsize=50)
    canvasLatex.draw()

def inicializarLatex(labelOpDisplay):
    global axLatex, canvasLatex
    figLatex = mfg.Figure(figsize=(15,1),dpi=20)
    axLatex = figLatex.add_subplot(111)
    canvasLatex = FigureCanvasTkAgg(figLatex, master=labelOpDisplay)
    canvasLatex.get_tk_widget().pack(side="top", expand=True)
    axLatex.get_xaxis().set_visible(False)
    axLatex.get_yaxis().set_visible(False)
    axLatex.set_frame_on(False)

def operacionYDesplegarLatex(funcionOperacion):
    y = funcionOperacion 
    if operaciones.opVar == "ERROR":
        tkinter.messagebox.showwarning("Declarar funcion","Se debe de declarar la funcion en forma y=") 
        operaciones.AC()
    else:
        graficarLatex()

def graficarFunciones(frameGrafica):
    global ax,canvas, fig, toolbar
    fig = mfg.Figure()#
    ax = fig.add_subplot()
    ax.grid()
    canvas = FigureCanvasTkAgg(fig, master=frameGrafica)
    canvas.get_tk_widget().config(width=617,height=318)
    canvas.get_tk_widget().grid(column=0,row=0)
    toolbar = NavigationToolbar2Tk(canvas,frameGrafica,pack_toolbar = False)
    toolbar.update()
    toolbar.grid(column=0,row=1,sticky="W")

def graficarFuncionDeOpVar(color:str,numeroGrafica):
    global canvas, fig
    xlist = np.arange(-1000,1000,0.001)
    dictX = {"x":xlist,"sen":np.sin,"cos":np.cos,"tan":np.tan,"euler":np.e,"pi":np.pi,"log":np.log10,"ln":np.log,"arcsen":np.arcsin,"arctan":np.arctan,"arccos":np.arccos}
    ylist = eval(str(operaciones.strToFunction()),dictX)
    ylist2 = np.abs(np.array(ylist))
    ylist[ ylist2 > 1000] = np.nan
    
    diccionarioAxGraficas[f"axGrafica{numeroGrafica}"] = ax.plot(xlist,ylist,c=color)
    ax.set(xlim=(-10,10),ylim=(-10,10))
    canvas.draw()

def botonesNumeros(frameBotones,ventana):
    global diccionarioBotones
    numero = 7
    for rPosition in range(0,3):
        for cPosition in range(0,3):
            diccionarioBotones[f"Boton{numero}"]=ttk.Button(frameBotones,text=str(numero),command=lambda numero=numero : operacionYDesplegarLatex(operaciones.addNum(str(numero))))
            diccionarioBotones[f"Boton{numero}"].grid(row=rPosition,column=cPosition)
            ventana.bind(f"{numero}",lambda e, numero=numero :operacionYDesplegarLatex(operaciones.addNum(str(numero))))
            numero += 1
        numero -= 6
    diccionarioBotones[f"Boton0"] =ttk.Button(frameBotones,text="0",command=lambda :operacionYDesplegarLatex(operaciones.addNum(str(0))))
    diccionarioBotones[f"Boton0"].grid(row=3,column=1,sticky="nsew")
    ventana.bind(f"0",lambda e:operacionYDesplegarLatex(operaciones.addNum(str(0))))
 
def botonesOperaciones(frameBotones,ventana):
    global diccionarioBotones
    diccionarioBotones[f"BotonPunto"] =ttk.Button(frameBotones,text=".",command=lambda :operacionYDesplegarLatex(operaciones.addOperator(".")))
    diccionarioBotones[f"BotonPunto"].grid(row=3,column=2,sticky="nsew")
    ventana.bind(".",lambda e:operacionYDesplegarLatex(operaciones.addOperator(".")))

    diccionarioBotones[f"BotonAC"] =ttk.Button(frameBotones,text="AC",command=lambda :operacionYDesplegarLatex(operaciones.AC()))
    diccionarioBotones[f"BotonAC"].grid(row=0,column=3,sticky="nsew")

    diccionarioBotones[f"BotonBorrarAtras"] =ttk.Button(frameBotones,text="⌫",command=lambda:operacionYDesplegarLatex(operaciones.erase()))
    diccionarioBotones[f"BotonBorrarAtras"].grid(row=0,column=4,sticky="nsew")
    ventana.bind("<BackSpace>",lambda e:operacionYDesplegarLatex(operaciones.erase()))

    index = 0
    for rPosition in range(1,3):
        for cPosition in range(3,5):
            operacion = operacionesPermitidas[index]
            diccionarioBotones[f"Boton{operacion}"]=ttk.Button(frameBotones,text=operacion,command=lambda operacion=operacion:operacionYDesplegarLatex(operaciones.addOperator(operacion)))
            diccionarioBotones[f"Boton{operacion}"].grid(row=rPosition,column=cPosition,sticky="nsew") 
            ventana.bind(operacion,lambda e, operacion=operacion:operacionYDesplegarLatex(operaciones.addOperator(operacion)))
            index +=1   

    diccionarioBotones[f"BotonEjeX"]=ttk.Button(frameBotones,text="x",command=lambda:operacionYDesplegarLatex(operaciones.addXAxis()))
    diccionarioBotones[f"BotonEjeX"].grid(row=0,column=5,sticky="nsew")
    ventana.bind("x",lambda e:operacionYDesplegarLatex(operaciones.addXAxis()))
    frameParentesis = ttk.Frame(frameBotones)
    frameParentesis.columnconfigure((0,1),weight=1)
    frameParentesis.rowconfigure(0,weight=1)
    frameParentesis.grid(row=2,column=5,sticky="nsew")
    diccionarioBotones[f"BotonParentesisAbierto"]=ttk.Button(frameParentesis,width=5,text="(",command=lambda:operacionYDesplegarLatex(operaciones.parentesisAbierto()))
    diccionarioBotones[f"BotonParentesisAbierto"].grid(row=0,column=0,sticky="nsew")
    diccionarioBotones[f"BotonParentesisCerrado"]=ttk.Button(frameParentesis,width=5,text=")",command=lambda:operacionYDesplegarLatex(operaciones.parentesisCerrado()))
    diccionarioBotones[f"BotonParentesisCerrado"].grid(row=0,column=1,sticky="nsew")

    diccionarioBotones["BotonPotencia"] = ttk.Button(frameBotones,text="^",command= lambda:operacionYDesplegarLatex(operaciones.potencia()))
    diccionarioBotones["BotonPotencia"].grid(row=0,column=6,sticky="nsew")
    diccionarioBotones["BotonLogaritmo"] = ttk.Button(frameBotones,text="log",command= lambda:operacionYDesplegarLatex(operaciones.logaritmos("log")))
    diccionarioBotones["BotonLogaritmo"].grid(row=1,column=6,sticky="nsew")
    diccionarioBotones["BotonPi"] = ttk.Button(frameBotones,text="π",command= lambda:operacionYDesplegarLatex(operaciones.specialVars("pi")))
    diccionarioBotones["BotonPi"].grid(row=2,column=6,sticky="nsew")
    diccionarioBotones["BotonEuler"] = ttk.Button(frameBotones,text="e",command= lambda:operacionYDesplegarLatex(operaciones.specialVars("euler")))
    diccionarioBotones["BotonEuler"].grid(row=3,column=6,sticky="nsew")

    diccionarioBotones["BotonInverso"] = ttk.Button(frameBotones,text="INV",command=lambda:botonInversa())
    diccionarioBotones["BotonInverso"].grid(row=0,column=7,sticky="nsew")
    diccionarioBotones["BotonSeno"] = ttk.Button(frameBotones,text="sen",command= lambda:operacionYDesplegarLatex(operaciones.trigonometrica("sen")))
    diccionarioBotones["BotonSeno"].grid(row=1,column=7,sticky="nsew")
    diccionarioBotones["BotonCoseno"] = ttk.Button(frameBotones,text="cos",command= lambda:operacionYDesplegarLatex(operaciones.trigonometrica("cos")))
    diccionarioBotones["BotonCoseno"].grid(row=2,column=7,sticky="nsew")
    diccionarioBotones["BotonTan"] = ttk.Button(frameBotones,text="tan",command= lambda:operacionYDesplegarLatex(operaciones.trigonometrica("tan")))
    diccionarioBotones["BotonTan"].grid(row=3,column=7,sticky="nsew")

def botonInversa():
    if diccionarioBotones["BotonSeno"].cget("text") == "sen":
        diccionarioBotones["BotonSeno"].configure(text="arcsen",command= lambda:operacionYDesplegarLatex(operaciones.trigonometrica("arcsen")))
        diccionarioBotones["BotonCoseno"].configure(text="arccos",command= lambda:operacionYDesplegarLatex(operaciones.trigonometrica("arccos")))
        diccionarioBotones["BotonTan"].configure(text="arctan",command= lambda:operacionYDesplegarLatex(operaciones.trigonometrica("arctan")))
        diccionarioBotones['BotonLogaritmo'].configure(text="ln",command = lambda:operacionYDesplegarLatex(operaciones.logaritmos("ln")))
    else:
        diccionarioBotones["BotonSeno"].configure(text="sen",command= lambda:operacionYDesplegarLatex(operaciones.trigonometrica("sen")))
        diccionarioBotones["BotonCoseno"].configure(text="cos",command= lambda:operacionYDesplegarLatex(operaciones.trigonometrica("cos")))
        diccionarioBotones["BotonTan"].configure(text="tan",command= lambda:operacionYDesplegarLatex(operaciones.trigonometrica("tan")))
        diccionarioBotones['BotonLogaritmo'].configure(text="log",command = lambda:operacionYDesplegarLatex(operaciones.logaritmos("log")))

def elegirColorGrafica():
    diccionarioBaseDatos = operaciones.devolverBaseDeDatos()
    coloresUsados = []
    cicloCompletadoSinColorPosible = False
    for key in diccionarioBaseDatos:
        if key != "Filler":
            coloresUsados.append(diccionarioBaseDatos[key]["color"])
        else:pass
    for color in listaColores:
        if color in coloresUsados:
            cicloCompletadoSinColorPosible = True
        elif color not in coloresUsados:
            cicloCompletadoSinColorPosible = False
            return color
            
    if cicloCompletadoSinColorPosible:
        print("No hay mas colores disponibles")
        return "gray"
        
def elegirNomenclaturaGrafica():
    diccionarioBaseDatos = operaciones.devolverBaseDeDatos()
    nomenclaturaUsada = []
    cicloCompletadoSinNomenclaturaPosible = False
    for key in diccionarioBaseDatos:
        if key != "Filler":
            nomenclaturaUsada.append(diccionarioBaseDatos[key]["nomenclatura"])
        else:pass
    for nomenclatura in listaNomenclatura:
        if nomenclatura in nomenclaturaUsada:
            cicloCompletadoSinNomenclaturaPosible = True
        elif nomenclatura not in nomenclaturaUsada:
            cicloCompletadoSinNomenclaturaPosible = False
            return nomenclatura
            break
        else:
            pass
    if cicloCompletadoSinNomenclaturaPosible:
        print("No hay mas nomenclaturas disponibles")
        return "F(x)"

def enterButtonCommand(frameH,labelOpWidget,window):
    numeroGraficaActual = operaciones.numeroGrafica
    print(f"el numero de la graficaActual es:{numeroGraficaActual}")
    if numeroGraficaActual !=0:
        operaciones.cambiarDeBaseDatosSoloLaFuncion(numeroGraficaActual,operaciones.opVar,operaciones.latexDisplay)
        
        for key in diccionarioHistorial:
            if isinstance(diccionarioHistorial[key],int):
                pass
            elif isinstance(diccionarioHistorial[key],mfg.Figure):
                pass
            elif isinstance(diccionarioHistorial[key],mpl.axes._axes.Axes):
                pass
            elif isinstance(diccionarioHistorial[key],FigureCanvasTkAgg):
                pass
            else:
                diccionarioHistorial[key].destroy()
        ax.clear()
        ax.grid()
        botonesHistorial(frameH,labelOpWidget,window)
        operaciones.AC()
    else:
        colorGraficaNueva = elegirColorGrafica()
        nomenclaturaGraficaNueva = elegirNomenclaturaGrafica()
        operaciones.mandarABaseDeDatos(colorGraficaNueva,nomenclaturaGraficaNueva)
        botonesHistorial(frameH,labelOpWidget,window)
        operaciones.AC()
        operacionYDesplegarLatex(operaciones.opVar)

def botonAccionGrafica(opVarCambio,parentesisAbiertosCambio,parentesisCerradosCambio,numeroIgualesCambio,numeroGrafica,latexDisplay):
    operaciones.changeValue(parentesisAbiertosCambio,"parentesisAbiertos")
    operaciones.changeValue(parentesisCerradosCambio,"parentesisCerrados")
    operaciones.changeValue(numeroIgualesCambio,"numeroIguales")
    operaciones.changeValue(numeroGrafica,"numeroGrafica")
    operaciones.changeValue(latexDisplay,"latexDisplay")
    operacionYDesplegarLatex(operaciones.changeValue(opVarCambio,"opVar"))

def botonesHistorial(frameH,labelOpWidget,window):
    global alturaLista, alturaLista, canvasScroll, frameBotonesCanvas, alturaFrameCanvas, diccionarioScrollbar
    diccionarioBaseDatos = operaciones.devolverBaseDeDatos()
    numeroGraficas = len(diccionarioBaseDatos)
    alturaItems = 2
    alturaFrameCanvas = 366
    if numeroGraficas != 0:
        alturaLista = numeroGraficas*30
    else:
        alturaLista = 0
    print(f"La altura de la lista es: {alturaLista} y la altura del frameCanvas es {alturaFrameCanvas}")
    canvasScroll = tkinter.Canvas(frameH,width=360,height=conseguirAlturaVentana(window)-30,scrollregion=(0,0,300,alturaLista))
    frameBotonesCanvas = ttk.Frame(window)
    rPosition = 0
    for key in diccionarioBaseDatos:
        if diccionarioBaseDatos[key]==True:
            pass
        else:
            numeroGrafica = int(key[7:])
            colorGrafica = diccionarioBaseDatos[key]["color"]
            nomenclaturaGrafica = diccionarioBaseDatos[key]["nomenclatura"]
            funcionGrafica = diccionarioBaseDatos[key]["funcion"]
            parentesisAbiertosGrafica = diccionarioBaseDatos[key]["parentesisAbiertosUsados"]
            parentesisCerradosGrafica = diccionarioBaseDatos[key]["parentesisCerradosUsados"]
            numeroIgualesGrafica = diccionarioBaseDatos[key]["igualesUsados"]
            latexDisplay = diccionarioBaseDatos[key]["latexDisplay"]
            diccionarioHistorial[f"colorFuncion{numeroGrafica}"] = tkinter.Canvas(frameBotonesCanvas,width=20,height=alturaItems*10)
            diccionarioHistorial[f"colorFuncion{numeroGrafica}"].grid(row=rPosition,column=0,sticky="n")
            diccionarioHistorial[f"ovaloColorFuncion{numeroGrafica}"]= diccionarioHistorial[f"colorFuncion{numeroGrafica}"].create_oval(5,5,20,20,fill=colorGrafica)
            diccionarioHistorial[f"labelNomenclaturaFuncion{numeroGrafica}"] = ttk.Label(frameBotonesCanvas,text=nomenclaturaGrafica,relief="groove")
            diccionarioHistorial[f"labelNomenclaturaFuncion{numeroGrafica}"].grid(row=rPosition,column=1,sticky="n")
            '''-----TEXTO LATEX-----'''
            textoLatex = "$"+latexDisplay+"$"
            diccionarioHistorial[f"contenedorLatexFuncion{numeroGrafica}"] = tkinter.Label(frameBotonesCanvas)
            diccionarioHistorial[f"contenedorLatexFuncion{numeroGrafica}"].grid(row=rPosition,column=2,sticky="n")
            diccionarioHistorial[f"figureFuncion{numeroGrafica}"] = mfg.Figure(figsize=(8,1), dpi=20)
            diccionarioHistorial[f"axFuncion{numeroGrafica}"] = diccionarioHistorial[f"figureFuncion{numeroGrafica}"].add_subplot(111)
            diccionarioHistorial[f"canvasFuncion{numeroGrafica}Latex"] = FigureCanvasTkAgg(diccionarioHistorial[f"figureFuncion{numeroGrafica}"],master=diccionarioHistorial[f"contenedorLatexFuncion{numeroGrafica}"])
            diccionarioHistorial[f"canvasFuncion{numeroGrafica}Latex"].get_tk_widget().grid(row=rPosition,column=2,sticky="n")
            diccionarioHistorial[f"axFuncion{numeroGrafica}"].get_xaxis().set_visible(False)
            diccionarioHistorial[f"axFuncion{numeroGrafica}"].get_yaxis().set_visible(False)
            diccionarioHistorial[f"axFuncion{numeroGrafica}"].set_frame_on(False)
            diccionarioHistorial[f"canvasFuncion{numeroGrafica}Latex"].get_tk_widget().bind("<Button-1>",lambda event,funcionGrafica=funcionGrafica,parentesisAbiertosGrafica = parentesisAbiertosGrafica, parentesisCerradosGrafica=parentesisCerradosGrafica, numeroIgualesGrafica = numeroIgualesGrafica, numeroGrafica= numeroGrafica,latexDisplay = latexDisplay :botonAccionGrafica(funcionGrafica,parentesisAbiertosGrafica,parentesisCerradosGrafica,numeroIgualesGrafica,numeroGrafica,latexDisplay))
            diccionarioHistorial[f"axFuncion{numeroGrafica}"].clear()
            diccionarioHistorial[f"axFuncion{numeroGrafica}"].text(0, 0.3, textoLatex, fontsize=50)  
            diccionarioHistorial[f"canvasFuncion{numeroGrafica}Latex"].draw()
            diccionarioHistorial[f"botonBorrarFuncion{numeroGrafica}"] = ttk.Button(frameBotonesCanvas,text="🗑️",command= lambda numeroGrafica=numeroGrafica: borrarFuncion(numeroGrafica,frameH,labelOpWidget,window))
            diccionarioHistorial[f"botonBorrarFuncion{numeroGrafica}"].grid(row=rPosition, column= 3,sticky="n")
            operaciones.changeValue(funcionGrafica,"opVar")
            graficarFuncionDeOpVar(colorGrafica,numeroGrafica)
            operaciones.AC()
            rPosition +=1
        
    crearOBorrarScrollBar(window)
    
    canvasScroll.create_window((0,0),
                        window=frameBotonesCanvas,
                        anchor="nw",
                        width= 360, 
                        height= alturaLista)    

    canvasScroll.grid(row=0,column=0,sticky="n")

    diccionarioHistorial["BorrarTodasLasGraficas"] = ttk.Button(frameH,text="Borrar Todas Las Graficas",command=lambda frameH=frameH,labelOpWidget=labelOpWidget,window=window:borrarTodoMensaje(frameH,labelOpWidget,window))
    diccionarioHistorial["BorrarTodasLasGraficas"].grid(row=1,column=0,sticky="sew")

def borrarFuncion(numeroGrafica,frameH,labelOp,window):
    global diccionarioScrollbar, canvasScroll
    diccionarioDB = operaciones.devolverBaseDeDatos()
    messagebox = tkinter.messagebox.askquestion("Borrar Funcion",f"Esta seguro que quiere borrar la funcion: {diccionarioDB[f"Grafica{numeroGrafica}"]["nomenclatura"]}?")
    if messagebox == "yes":    
        for key in diccionarioHistorial:
            if  isinstance(diccionarioHistorial[key],int):
                pass
            elif isinstance(diccionarioHistorial[key],mfg.Figure):
                pass
            elif isinstance(diccionarioHistorial[key],mpl.axes._axes.Axes):
                pass
            elif isinstance(diccionarioHistorial[key],FigureCanvasTkAgg):
                pass
            else:
                diccionarioHistorial[key].destroy()
            if len(key) >17:
                if key[:18] == "ovaloColorFuncion":
                    del diccionarioHistorial[key]
                else: pass
        diccionarioScrollbar["scrollBar"].destroy()
        operaciones.borrarDeBaseDeDatos(numeroGrafica)
        ax.clear()
        ax.grid()
        botonesHistorial(frameH,labelOp,window)
        operaciones.AC()
        operacionYDesplegarLatex(operaciones.opVar)
        canvasScroll.update()
    else:
        tkinter.messagebox.showinfo("Volviendo","Volviendo a la calculadora") 
    
def conseguirAlturaVentana(window):
    window.update()
    return window.winfo_height()

def conseguirAnchoVentana(window):
    window.update()
    return window.winfo_width()

def cambiarTamaño(window):
    global toolbar,canvasScroll, diccionarioScrollbar,canvas
    canvas.get_tk_widget().config(height=round((conseguirAlturaVentana(window)*2))/3,width=round((conseguirAnchoVentana(window)*2)/3))
    
def crearOBorrarScrollBar(window):
    if alturaLista > conseguirAlturaVentana(window):
        canvasScroll.bind_all("<MouseWheel>",lambda event: canvasScroll.yview_scroll(-int(event.delta/60),"units"))
        diccionarioScrollbar["scrollBar"] = ttk.Scrollbar(window,orient="vertical",command= canvasScroll.yview)
        diccionarioScrollbar["scrollBar"].grid(row=0,column=2,rowspan=3,sticky="nse")
        canvasScroll.configure(yscrollcommand=diccionarioScrollbar["scrollBar"].set)
    else:
        diccionarioScrollbar["scrollBar"] = ttk.Scrollbar(window,orient="vertical",command= canvasScroll.yview)
        diccionarioScrollbar["scrollBar"].destroy()
        canvasScroll.unbind_all("<MouseWheel>")