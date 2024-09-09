from connector import *


UIDUser = ""
dbOffline = {}

def returnDBStatus():
    global dbStatusOn
    return dbStatusOn

def login(email:str,password:str):
    global UIDUser
    if dbStatusOn == True:
        try:
            user = auth.sign_in_with_email_and_password(email,password)
            UIDUser = auth.get_account_info(user["idToken"])["users"][0]["localId"]
        except:
            return False
        else:
            return True
    else:pass

def registro(email:str,password:str):
    global UIDUser
    if dbStatusOn == True:
        try: #Crear Usuario
            user = auth.create_user_with_email_and_password(email,password)
            UIDUser = auth.get_account_info(user["idToken"])["users"][0]["localId"]
        except:
            return False
        else:
            db.reference(f"/Usuarios").update({UIDUser:{"Filler":True}})
            return True
            
    else:pass
    


def devolverDiccionarioCompleto():
    '''
    Para que la funcion funcione debe de haberse ejecutado login o registro primero
    '''
    global dbOffline
    if dbStatusOn == True:
        if type((db.reference(f"/Usuarios/").get())[UIDUser]) == type(None):
            return {}
        else:
            return (db.reference(f"/Usuarios/").get()[UIDUser])
    else:
        return dbOffline

def borrarNodo(llave:str): 
    '''
    llave debe de tener formato /Usuarios/UIDuser/Grafica
    '''
    global UIDUser,dbOffline
    if dbStatusOn == True:
        if list(db.reference(f"Usuarios/{UIDUser}/{llave}").get()) != "true":
            db.reference(f"Usuarios/{UIDUser}/{llave}").delete()
        else:
            pass
    else:
        if llave[0] == "/":
            del dbOffline[llave[1:]]

def editarNodo(llave:str,valor:str):
    global UIDUser,dbOffline
    if dbStatusOn == True:
        if llave in devolverDiccionarioCompleto():
            ref.update({llave:valor})
        else:
            print(f"La llave:{llave} no se encuentra en el diccionario")
    else:
        if llave in dbOffline:
            dbOffline[llave] = valor
        else:
            print(f"La llave:{llave} no se encuentra en el diccionario Offline")

def editarFuncionOLatexGrafica(numeroGrafica:int,tipo:str,parametro:str):
    '''
    Para que esta funcion funcione debe de haberse primero ejecutado la funcion login o registro
    
    '''
    global UIDUser, dbOffline
    tiposDisponibles = ["funcion","latexDisplay"]
    if dbStatusOn == True:
        if tipo in tiposDisponibles:
            if f"Grafica{numeroGrafica}" in devolverDiccionarioCompleto():
                print(UIDUser)
                db.reference(f"/Usuarios/{UIDUser}/Grafica{numeroGrafica}").update({tipo:parametro})
            else:
                print(f"Grafica{numeroGrafica} no se encuentra en la base de datos")
    else:
        if tipo in tiposDisponibles:
            if f"Grafica{numeroGrafica}" in dbOffline:
                dbOffline[f"Grafica{numeroGrafica}"][tipo] = parametro
            else:
                print(f"Grafica{numeroGrafica} no se encuentra en la base de datos offline")

def crearNodo(diccionario:dict): 
    global dbOffline
    if dbStatusOn == True:
        if list(diccionario)[0] in devolverDiccionarioCompleto():
            diccionarioDataBase = devolverDiccionarioCompleto()
            print(f"El inicio del nodo: {list(diccionario)[0]} ya se encuentra en diccionarioDataBase {diccionarioDataBase}")
        else:
            print(f"Se crea la grafica con los siguientes valores: {diccionario}")
            db.reference(f"/Usuarios/{UIDUser}/").update(diccionario)
    else:
        if list(diccionario)[0] in dbOffline:
            print(f"El inicio del nodo: {list(diccionario)[0]} ya se encuentra en diccionarioDataBaseOffline {dbOffline} ")
        else:
            print(f"Se crea la grafica con los siguientes valores: {diccionario}")
            for key in diccionario:
                dbOffline[key] = diccionario[key]

def borrarTodo():
    global dbOffline, UIDUser
    if dbStatusOn == True:
        for key in devolverDiccionarioCompleto():
            if key != "Filler":
                db.reference(f"/Usuarios/{UIDUser}/{key}").delete()
    else: dbOffline = {}

