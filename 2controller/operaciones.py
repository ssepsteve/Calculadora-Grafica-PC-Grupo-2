'''
PONER UN ENLACE CON OTRO ARCHIVO DE CONTROLLER QUE A SU VEZ SE CONECTA CON VIEW EN DONDE SE CAMBIARA LAS VARIABLES DE ABAJO POR LAS VARIABLES
DE LA BASE DE DATOS
'''
import numpy as np
import controller_Model as com




#VARIABLES
opVar = "y=" #VARIABLE EN LA CUAL SE REALIZA LAS OPERACIONES
latexDisplay = r"y="
parentesisAbiertosUsados = 0
parentesisCerradosUsados = 0
numeroIguales = 1
numeroGrafica = 0
listOperators = ["+","-","/","*","="]
diccionarioOpLatex = {"+":"+","-":"-","/":r"\div ","*":r"\cdot "}
digits = ["1","2","3","4","5","6","6","7","8","9","0","x","r","i"]

def changeValue(replacement,type:str):
    global opVar,parentesisAbiertosUsados,parentesisCerradosUsados,numeroIguales,numeroGrafica,latexDisplay
    if type == "parentesisAbiertos":
        parentesisAbiertosUsados = replacement
    elif type == "opVar":
        opVar = replacement
    elif type == "parentesisCerrados":
        parentesisCerradosUsados = replacement
    elif type == "numeroIguales":
        numeroIguales = replacement
    elif type == "numeroGrafica":
        numeroGrafica = replacement
    elif type == "latexDisplay":
        latexDisplay = replacement
    else:
        print(f"{type} no hace referencia a alguna variable que se pueda cambiar")

def addNum(num:str):
    global opVar,latexDisplay,numeroIguales
    if numeroIguales !=0: 
        if opVar[-1] == "x" or opVar[-1] == ")":
            opVar += f"*{num}"
            latexDisplay += fr"{diccionarioOpLatex["*"]}{num}"
        elif (opVar[-1] in listOperators) or (opVar[-1] in digits) or (opVar[-1]=="(") or (opVar[-1]=="."):
            opVar += num
            latexDisplay += num
        else:
            pass
    else:
        opVar = "ERROR"
    return opVar

def addOperator(operator:str): 
    global opVar,latexDisplay
    if operator in listOperators[:4]:
        if opVar[-1] in digits or opVar[-1] == ")":
            opVar += operator
            latexDisplay += fr"{diccionarioOpLatex[operator]}"
        if opVar[-2:] == "**":
            opVar = opVar[:-2]+operator
            latexDisplay =  latexDisplay[:-1]+diccionarioOpLatex[operator]
        elif operator == "-" and (opVar[-1]=="=" or opVar[-1]=="("):
            opVar += "-"
            latexDisplay += "-"
        elif opVar[-1] == ".":
            opVar+=f"0{operator}"
            latexDisplay+=f"0{diccionarioOpLatex[operator]}"
        elif opVar[-1] in listOperators[:4]:
            latexDisplay = fr"{latexDisplay[:-len(diccionarioOpLatex[opVar[-1]])]+diccionarioOpLatex[operator]}"
            opVar = opVar[:-1]+operator
        else:
            pass
    elif operator == ".":
        if opVar[-1] in digits or opVar[-1] == ")":
            opVar += "."
            latexDisplay += "."
        elif opVar[-1] ==")":
            opVar += "*0."
            latexDisplay += f"{diccionarioOpLatex['*']}0."
        elif opVar[-1] == "(":
            opVar += "0."
            latexDisplay += "0."
        else:
            pass
    else:
        pass
    return opVar

def parentesisAbierto():
    global opVar,parentesisAbiertosUsados,parentesisCerradosUsados,latexDisplay
    if numeroIguales != 0: 
        if  opVar[-1] in listOperators or opVar[-1] =="(": 
            opVar += "("
            latexDisplay += "("
            parentesisAbiertosUsados += 1
        elif (opVar[-1] in digits or opVar[-1] == ")"): 
            opVar += "*("
            latexDisplay += r"\cdot ("
            parentesisAbiertosUsados += 1
        else:
            pass
    else:
        opVar = "ERROR"
    return opVar

def parentesisCerrado():
    global opVar,parentesisAbiertosUsados,parentesisCerradosUsados,latexDisplay
    if len(opVar)>1:
        if parentesisAbiertosUsados == parentesisCerradosUsados and parentesisAbiertosUsados !=0:
            pass
        elif parentesisAbiertosUsados > parentesisCerradosUsados and (opVar[-1] in digits or opVar[-1] == ")"):
            opVar += ")"
            latexDisplay += ")"
            parentesisCerradosUsados +=1
        elif parentesisAbiertosUsados > parentesisCerradosUsados and (opVar[-1] in listOperators[:2]):
            opVar += "0)"
            latexDisplay += "0)"
            parentesisCerradosUsados +=1
        elif parentesisAbiertosUsados > parentesisCerradosUsados and (opVar[-1] in listOperators[2:4]): 
            opVar += "1)"
            latexDisplay += "1)"
            parentesisCerradosUsados +=1
        else:
            print(f"Puede que haya algun error ya que numero de parentesis abiertos es:{parentesisAbiertosUsados} y el numero de parentesis cerrados es:{parentesisCerradosUsados}")
    else:
        pass
    
    return opVar     

def erase():
    global opVar,parentesisAbiertosUsados,parentesisCerradosUsados,numeroIguales,latexDisplay
    if len(opVar) == 1:
        print(f"Prueba: opVar:{opVar}, len(opVar):{len(opVar)}")
        opVar = "0"
        latexDisplay = "0" 
    elif opVar[-1] == "i": 
        opVar = opVar[:-2]
        latexDisplay = latexDisplay[:-3]
    elif opVar[-1] == "r": 
        opVar = opVar[:-5]
        latexDisplay = latexDisplay[:-1]
    elif opVar[-1] == ".":
        opVar = opVar[:-1]
        latexDisplay = latexDisplay[:-1]
    elif opVar[-1] == "(":
        if len(opVar)>3 and (opVar[-3:] == "ln("):
            opVar = opVar[:-3]
            latexDisplay = latexDisplay[:-4] #\ln(
            parentesisAbiertosUsados -= 1
        elif len(opVar)>4 and opVar[-4:] == "log(":
            opVar = opVar[:-4]
            latexDisplay = latexDisplay[:-5]
            parentesisAbiertosUsados -= 1
        elif len(opVar)>7 and opVar[-7:] in ["arccos(","arcsen(","arctan("]:
            opVar = opVar[:-7]
            latexDisplay = latexDisplay[:-9]
            parentesisAbiertosUsados -= 1
        elif len(opVar)>4 and (opVar[-4:] in ["sen(","cos(","tan("]):
            opVar = opVar[:-4]
            latexDisplay = latexDisplay[:-4]
            parentesisAbiertosUsados -= 1
        else:
            opVar = opVar[:-1]
            latexDisplay = latexDisplay[:-1]
            parentesisAbiertosUsados -=1
    elif opVar[-1] == ")":
        opVar = opVar[:-1]
        latexDisplay = latexDisplay[:-1]
        parentesisCerradosUsados -=1
    elif opVar[-1] == "=":
        pass
    elif opVar[-1] == "*":
        if  opVar[-2:]=="**":
            opVar = opVar[:-2]
            latexDisplay = latexDisplay[:-1]
        else:
            opVar = opVar[:-1]
            latexDisplay = latexDisplay[:-len(diccionarioOpLatex["*"])]
    elif opVar[-1] == "/":
        opVar = opVar[:-1]
        latexDisplay = latexDisplay[:-len(diccionarioOpLatex["/"])]
    elif opVar[-1] in digits[:12] or opVar[-1] in listOperators[:2]:
        opVar = opVar[:-1]
        latexDisplay = latexDisplay[:-1]
    return opVar

def AC():
    global opVar,parentesisAbiertosUsados,parentesisCerradosUsados,numeroIguales,numeroGrafica,latexDisplay
    opVar = "y="
    latexDisplay = r"y="
    parentesisAbiertosUsados = 0
    parentesisCerradosUsados = 0
    numeroIguales = 1
    numeroGrafica = 0
    return opVar

def addYAxis():
    global opVar,latexDisplay
    if opVar == "0":
        opVar = "y" 
        latexDisplay = "y"
    else:
        pass
    return opVar

def addXAxis():
    global opVar,latexDisplay
    if numeroIguales  != 0:
        if opVar == "0" and len(opVar)==1: 
            opVar = "x"
            latexDisplay = "x"
        elif opVar[-1] == "0" and len(opVar)!=1: 
            opVar += "*x"
            latexDisplay += r"\cdot x"
        elif opVar[-1] in digits and opVar[-1] != "x":
            opVar += "*x"
            latexDisplay += r"\cdot x"
        elif opVar[-1] == ")" and len(opVar)!=1:
            opVar += "*x"
            latexDisplay += r"\cdot x"
        else:
            opVar += "x"
            latexDisplay += "x"
    else:
        opVar = "ERROR"
    return opVar

def equal():
    global opVar,numeroIguales,latexDisplay
    if opVar == "0":
        pass
    elif opVar[-1] in listOperators:
        pass
    elif opVar[-1] == "y":
        opVar += "="
        latexDisplay += "="
        numeroIguales +=1
    else:
        pass
    return opVar

def strToFunction():
    global opVar
    opVarSinY = opVar
    for i in opVar:
        if i == "y":
            opVarSinY = opVarSinY.replace("y","")
        elif i == "=":
            opVarSinY = opVarSinY.replace("=","")
        else:
            pass
    if "x" not in opVarSinY:
        opVarSinY += "+0*x"
    else: pass
    
    return opVarSinY

def mandarABaseDeDatos(color:str,nomenclatura:str): 
    global opVar,parentesisAbiertosUsados,parentesisCerradosUsados,numeroIguales,latexDisplay
    definidaEn1000_y_1000=True
    strAfuncion = strToFunction()
    try: 
        if "x" in opVar:
            a = eval(strAfuncion,{"x":1000,"sen":np.sin,"cos":np.cos,"tan":np.tan,"arcsen":np.arcsin,"arctan":np.arctan,"arccos":np.arccos,"log":np.log10,"ln":np.log,"pi":np.pi,"euler":np.e})
        else:
            opVar = str(eval(opVar[2:],{"sen":np.sin,"cos":np.cos,"tan":np.tan,"arcsen":np.arcsin,"arctan":np.arctan,"arccos":np.arccos,"log":np.log10,"ln":np.log,"pi":np.pi,"euler":np.e}))
            opVar = f"y={opVar}"
            latexDisplay = opVar
    except SyntaxError:
        diferenciaParentesis = parentesisAbiertosUsados - parentesisCerradosUsados
        for i in range(0,diferenciaParentesis):
            parentesisCerrado()
            strAfuncion += ")"
    except ZeroDivisionError: 
        definidaEn1000_y_1000 = False
    else:
        definidaEn1000_y_1000 = True

    try: 
        if "x" in opVar:
            a = eval(str(strAfuncion),{"x":-1000,"sen":np.sin,"cos":np.cos,"tan":np.tan,"arcsen":np.arcsin,"arctan":np.arctan,"arccos":np.arccos,"log":np.log10,"ln":np.log,"pi":np.pi,"euler":np.euler_gamma})
        else:
            opVar = str(eval(opVar[2:],{"sen":np.sin,"cos":np.cos,"tan":np.tan,"arcsen":np.arcsin,"arctan":np.arctan,"arccos":np.arccos,"log":np.log10,"ln":np.log,"pi":np.pi,"euler":np.e}))
            opVar = "y="+opVar
            latexDisplay = opVar
            opVar += "+0*x"
            
    except ZeroDivisionError:
        definidaEn1000_y_1000 = False
    else:
        definidaEn1000_y_1000 = True

    if definidaEn1000_y_1000:
        igualesUsados = numeroIguales
        funcion = opVar
        numeroGrafica = com.devolverNumeroUltimaGrafica() + 1
        print(f"El numero de la grafica que se creara es: {numeroGrafica}")
        com.añadirUnaNuevaGrafica(funcion,color,parentesisAbiertosUsados,parentesisCerradosUsados,igualesUsados,numeroGrafica,nomenclatura,latexDisplay)

def cambiarDeBaseDatosSoloLaFuncion(numeroGrafica,funcion,latexDisplay):
    com.cambiarGrafica(numeroGrafica,funcion,latexDisplay)

def devolverNumeroUltimaGrafica():
    return com.devolverNumeroUltimaGrafica()

def devolverEstadoBaseDeDatos():
    return com.devolverEstadoConexion()

def borrarDeBaseDeDatos(numeroGrafica):
    com.borrarGrafica(numeroGrafica)

def devolverBaseDeDatos():
    return com.devolverTodoElDiccionario()

def borrarTodasLasGraficasDeDB():
    com.borrarTodasLasGraficas()

def potencia():
    global opVar, latexDisplay
    if len(opVar)>1:
        if opVar[-1] in digits or opVar[-1] == ")":
            opVar += "**"
            latexDisplay += "^"
        elif opVar[-1] in listOperators[:4]:
            latexDisplay = latexDisplay[:-len(diccionarioOpLatex[opVar[-1]])]+"^"
            opVar = opVar[-1]+"**"
        elif  opVar[-1]=="(":
            opVar +="0**"
            latexDisplay +="0^"
        else:
            pass
    else:
        pass

def logaritmos(tipoLogaritmo:str):
    global opVar,latexDisplay, parentesisAbiertosUsados
    if tipoLogaritmo in ["log","ln"]:
        if len(opVar)>1:
            if opVar[-1] in digits or opVar[-1]==")":
                opVar += f"*{tipoLogaritmo}("
                latexDisplay += fr"\cdot \{tipoLogaritmo}("
                parentesisAbiertosUsados += 1
            elif opVar[-1] in listOperators or opVar[-1] == "(":
                opVar += f"{tipoLogaritmo}("
                latexDisplay += fr"\{tipoLogaritmo}("
                parentesisAbiertosUsados += 1
            else:
                pass
    else:
        print(f"el logaritmo llamado: {tipoLogaritmo} no es reconocido")

#TRIGONOMETRICAS

def trigonometrica(funcionTrigonometrica:str):
    global opVar,latexDisplay,parentesisAbiertosUsados
    if funcionTrigonometrica in ["sen","cos","tan","arcsen","arccos","arctan"]:
        if funcionTrigonometrica[:3] != "arc":
            if len(opVar)>1 and (opVar[-1] in digits or opVar[-1] == ")"):
                opVar += f"*{funcionTrigonometrica}("
                latexDisplay += fr"\cdot {funcionTrigonometrica}("
                parentesisAbiertosUsados +=1   
            elif len(opVar)>1 and (opVar[-1] in listOperators or opVar[-1]=="(") :
                opVar += f"{funcionTrigonometrica}("
                latexDisplay += f"{funcionTrigonometrica}("
                parentesisAbiertosUsados +=1
            else:
                pass
        else:
            if len(opVar)>1 and (opVar[-1] in digits or opVar[-1] == ")"):
                opVar += f"*{funcionTrigonometrica}("
                latexDisplay += fr"\cdot {funcionTrigonometrica[-3:]}"+"^{-1}("
                parentesisAbiertosUsados +=1   
            elif len(opVar)>1 and (opVar[-1] in listOperators or opVar[-1]=="(") :
                opVar += f"{funcionTrigonometrica}("
                latexDisplay += fr"{funcionTrigonometrica[-3:]}"+"^{-1}("
                parentesisAbiertosUsados +=1
            else:
                pass
    else:
        print(f"La funcion trigonometrica: {funcionTrigonometrica} no es reconocida")

def specialVars(variable:str):
    global opVar, latexDisplay
    if variable in ["pi","euler"]:
        if variable == "pi":
            if len(opVar)>1:
                if opVar[-1] in digits or opVar[-1]==")":
                    opVar += f"*{variable}"
                    latexDisplay += fr"\cdot \{variable}"
                elif opVar[-1] in listOperators[:4] or opVar[-1] == "(":
                    opVar += f"{variable}"
                    latexDisplay += fr"\{variable}"
                else:
                    pass
        elif variable == "euler":
            if len(opVar)>1:
                if opVar[-1] in digits or opVar[-1]==")":
                    opVar += f"*{variable}"
                    latexDisplay += fr"\cdot {variable[0]}"
                elif opVar[-1] in listOperators[:4] or opVar[-1] == "(":
                    opVar += f"{variable}"
                    latexDisplay += fr"{variable[0]}"
                else:
                    pass
        else:
            pass
    else:
        print(f"la variable: {variable} no es reconocida")
