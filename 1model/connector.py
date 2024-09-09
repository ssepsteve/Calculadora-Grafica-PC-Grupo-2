import firebase_admin
import firebase_admin.exceptions
import firebase_admin.firestore
import pyrebase
from firebase_admin import credentials,db
import timeit

def fireBaseInitializeCreds():
    cred = credentials.Certificate("C:/Users/stves/Documents/GitHub/Proyecto-Programacion-De-Computadores/CALCULADORA GRAFICA/1model/certificates.json")    
    firebase_admin.initialize_app(cred, {
                'databaseURL': 'https://calc-graficadora-v-experiment-default-rtdb.firebaseio.com'
    })
    ref = db.reference('/')
    ref.get()

def initializeAuth():
    global auth
    firebaseConfig = {
        "apiKey": "AIzaSyDjwFcPsfplapZYKbNugyGfFKQXyhE-os4",
        "authDomain": "calc-graficadora-v-experiment.firebaseapp.com",
        "databaseURL": "https://calc-graficadora-v-experiment-default-rtdb.firebaseio.com",
        "projectId": "calc-graficadora-v-experiment",
        "storageBucket": "calc-graficadora-v-experiment.appspot.com",
        "messagingSenderId": "900247884273",
        "appId": "1:900247884273:web:a4ef8561f544af10bef450",
        "measurementId": "G-NE8D5B6S8J"
    }
    firebase = pyrebase.initialize_app(firebaseConfig)
    auth = firebase.auth()

dbStatusOn = True

def checkFirebase():
    try:
        tiempoDemora = timeit.timeit(stmt="fireBaseInitializeCreds()",setup="from connector import fireBaseInitializeCreds",number=1)
        if float(tiempoDemora) > 6:
            print(f"Tiempo De Conexion A Firebase Excedido {round(float(tiempoDemora),2)} Segundos")
            return False
    except Exception as e:
        print(f"Error De Conexion a Firebase: {e} ")
        return False
    else:
        return True

def checkAuth():
    global dbStatusOn
    if dbStatusOn == True:
        try: 
            tiempoDemora = timeit.timeit(stmt="initializeAuth()",setup="from connector import initializeAuth",number=1)
            if float(tiempoDemora) > 5:
                print(f"Tiempo De Conexion A Authentication Excedido: {round(float(tiempoDemora),2)} Segundos")
                return False
        except Exception as e:
            print(f"Error de conexion a authentication: {e}")
            return False
        else: 
            return True
    else:
        return False 

def checkBoth():
    global dbStatusOn
    dbStatusOn = checkFirebase()
    if dbStatusOn == True and checkAuth() == True:
        return True
    else: return False

dbStatusOn = checkBoth()

