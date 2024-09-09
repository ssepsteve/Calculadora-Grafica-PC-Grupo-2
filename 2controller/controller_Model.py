import sys
sys.path.insert(1,"C:/Users/stves/Documents/GitHub/Proyecto-Programacion-De-Computadores/CALCULADORA GRAFICA/1model")
import funcionesDB

def login(email:str,password:str):
    return funcionesDB.login(email,password)

def register(email:str,password:str):
    return funcionesDB.registro(email,password)

def devolverEstadoConexion():
    return funcionesDB.returnDBStatus()

def devolverTodoElDiccionario(): #Getter
    return funcionesDB.devolverDiccionarioCompleto()

def devolverNumeroUltimaGrafica(): #Getter
    
    if funcionesDB.devolverDiccionarioCompleto() != {}:
        diccionarioActualDB = funcionesDB.devolverDiccionarioCompleto()
        if funcionesDB.returnDBStatus() == True:
            diccionarioActualDB.pop("Filler")
        diccionarioActualLlaves = list(diccionarioActualDB.keys())
        listaNumerosGraficas = [] 
        for key in diccionarioActualLlaves:
            listaNumerosGraficas.append(int(key[7:]))
        listaNumerosGraficas.sort()
        if listaNumerosGraficas != []:
            valorUltimaGrafica = listaNumerosGraficas[-1]
        else: valorUltimaGrafica = 0
        return valorUltimaGrafica
    else:
        print("La base de datos esta vacia")
        return 0

def cambiarGrafica(numeroGrafica:int,funcion:str,latexDisplay:str): #Setter
    funcionesDB.editarFuncionOLatexGrafica(numeroGrafica,"funcion",funcion)
    funcionesDB.editarFuncionOLatexGrafica(numeroGrafica,"latexDisplay",latexDisplay)

def añadirUnaNuevaGrafica(funcion:str,color:str,parentesisAbiertosUsados:int,parentesisCerradosUsados:int,igualesUsados:int,numeroGrafica:int,nomenclatura:str,latexDisplay:str):
    if parentesisAbiertosUsados==parentesisCerradosUsados and igualesUsados==1:
        diccionarioGrafica = {f"Grafica{numeroGrafica}":
                                {"color":color,
                                 "funcion":funcion,             
                                 "igualesUsados":igualesUsados,
                                 "parentesisAbiertosUsados":parentesisAbiertosUsados,
                                 "parentesisCerradosUsados":parentesisCerradosUsados,
                                 "nomenclatura":nomenclatura, 
                                 "latexDisplay":latexDisplay}
                            }
        funcionesDB.crearNodo(diccionarioGrafica)
    else:
        print("Error al añadir una nueva grafica")

def borrarGrafica(numeroGrafica):
    if (f"Grafica{numeroGrafica}") in funcionesDB.devolverDiccionarioCompleto():
        nodo = str(f"/Grafica{numeroGrafica}")
        funcionesDB.borrarNodo(nodo)
    else: pass

def borrarTodasLasGraficas():
    funcionesDB.borrarTodo()