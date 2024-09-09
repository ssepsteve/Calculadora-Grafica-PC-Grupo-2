import sys
import tkinter.messagebox
sys.path.insert(1,"C:/Users/stves/Documents/GitHub/Proyecto-Programacion-De-Computadores/CALCULADORA GRAFICA/2controller")
import controller_Model as com
import tkinter
from tkinter import ttk

def botonAccederComando(entryUsuario,entryContraseña,ejecutarCalculadora):
    email = str(entryUsuario.get())
    contraseña = str(entryContraseña.get())
    if contraseña == "" or email == "":
        tkinter.messagebox.showerror("Error Registro","Datos Incompletos")
    else:
        if "@" not in email:
            tkinter.messagebox.showerror("Error Registro","Falta un arroba en el email")
        else:
            boolLogin = com.login(email,contraseña)
            if boolLogin: 
                y = ejecutarCalculadora()
            else:
                tkinter.messagebox.showerror("Error Inicio De Sesion","No Se Encuentra El Usuario Y/o Contraseña En La Base De Datos")

def botonCrearCuentaComando(entryUsuario,entryContraseña,ejecutarCalculadora,ventana):
    email = str(entryUsuario.get())
    contraseña = str(entryContraseña.get())
    if contraseña == "" or email == "":
        tkinter.messagebox.showerror("Error Registro","Datos Incompletos")
    else: 
        if "@" not in email:
            tkinter.messagebox.showerror("Error Registro","Falta un arroba en el email")
        else:
            boolLogin = com.register(email,contraseña)
            if boolLogin: 
                y = creacionSeccionAcceso(ventana,ejecutarCalculadora)
            else:
                tkinter.messagebox.showerror("Error Registro","Cuenta Ya Creada y/o Cuenta No Valida")

        


def botonRegistroComando(ventana,ejecutarCalculadora):
    seccionRegistro = ttk.Frame(ventana)
    seccionRegistro.grid(row=0,column=0,sticky="nsew")
    
    seccionRegistro.tkraise()

    seccionRegistro.grid_rowconfigure((0,1,2,3),weight=1,uniform="a")
    seccionRegistro.grid_columnconfigure((0,1),weight=1,uniform="a")

    labelUsuario = ttk.Label(seccionRegistro,text="Email: ")
    labelUsuario.grid(row=0,column=0,sticky="nsew")
    
    entryUsuario = ttk.Entry(seccionRegistro)
    entryUsuario.grid(row=0,column=1,sticky='nsew')

    labelContraseña = ttk.Label(seccionRegistro,text="Contraseña")
    labelContraseña.grid(row=1,column=0,sticky="nsew")

    entryContraseña = ttk.Entry(seccionRegistro,show="*")
    entryContraseña.grid(row=1,column=1,sticky="nsew")

    botonCrearCuenta = ttk.Button(seccionRegistro,text="Crear Cuenta",command=lambda: botonCrearCuentaComando(entryUsuario,entryContraseña,ejecutarCalculadora,ventana))
    botonCrearCuenta.grid(row=2,column=0,columnspan=2,sticky="nsew")

    botonAtras = ttk.Button(seccionRegistro,text="Volver",command=lambda:creacionSeccionAcceso(ventana,ejecutarCalculadora))
    botonAtras.grid(row=3,column=0,sticky="nsew")

def creacionSeccionAcceso(ventana,comandoEjecutarCalculadora):
    ventana.resizable(False,False)
    seccionInicioDeSesion = ttk.Frame(ventana)
    seccionInicioDeSesion.grid(row=0,column=0,sticky="nsew")
    if com.devolverEstadoConexion() == True:        
        '''SECCION INICIO DE SESION'''
        seccionInicioDeSesion.grid_rowconfigure((0,1,2,3),weight=1,uniform="a")
        seccionInicioDeSesion.grid_columnconfigure((0,1),weight=1,uniform="a")
        labelInicioDeSesion = ttk.Label(seccionInicioDeSesion,text="Por favor inicie sesion para acceder a la calculadora")
        labelInicioDeSesion.grid(row=0,column=0,sticky="nsew")

        labelUsuario = ttk.Label(seccionInicioDeSesion,text="Email: ")
        labelUsuario.grid(row=1,column=0,sticky="nsew")
        entryUsuario = ttk.Entry(seccionInicioDeSesion)
        entryUsuario.grid(row=1,column=1,sticky="nsew")

        LabelContraseña = ttk.Label(seccionInicioDeSesion,text="Contraseña")
        LabelContraseña.grid(row=2,column=0,sticky="nsew")
        entryContraseña = ttk.Entry(seccionInicioDeSesion,show="*")
        entryContraseña.grid(row=2,column=1,sticky="nsew")

        botonAcceder = ttk.Button(seccionInicioDeSesion,text="Acceder",command=lambda:botonAccederComando(entryUsuario,entryContraseña,comandoEjecutarCalculadora))
        botonAcceder.grid(row=3,column=0,columnspan=2,sticky="nsew")

        labelRegistro = ttk.Label(seccionInicioDeSesion,text="No Tienes Una Cuenta?")
        labelRegistro.grid(row=4,column=0,columnspan=2,sticky="nsew")

        botonRegistro = ttk.Button(seccionInicioDeSesion,text="Registrarse",command=lambda:botonRegistroComando(ventana,comandoEjecutarCalculadora))
        botonRegistro.grid(row=5,column=0,columnspan=2,sticky="nsew")

    else:
        seccionInicioDeSesion.grid_rowconfigure((0,1),weight=1,uniform="a")
        seccionInicioDeSesion.grid_columnconfigure((0,1),weight=1,uniform="a")
        LabelFalloConexion = ttk.Label(seccionInicioDeSesion,text="No Se Pudo Conectar A La Base De Datos")
        LabelFalloConexion.grid(row=0,column=0,columnspan=2)

        botonAccederABDOffline = ttk.Button(seccionInicioDeSesion,text="Acceder A Calculadora Sin Conexion",command=lambda:comandoEjecutarCalculadora())
        botonAccederABDOffline.grid(row=1,column=0,columnspan=2)

    ventana.mainloop()
