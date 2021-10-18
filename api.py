import os
from random import randrange

from flask import Flask, render_template, request
from flask_login import (LoginManager, current_user, login_required, login_user, logout_user)
from werkzeug.utils import redirect
from datetime import timedelta
from app import App as Application
from src.model.Input import *
Application()
from src.model.Entity import *

app = Flask(__name__)
app.secret_key = 'asdasdasdasddsadssaasdsa'
login_manager = LoginManager()
login_manager.init_app(app)

vuelos = []

def getApp():
    return Application.__instance__

@login_manager.unauthorized_handler
def unauthorized():
    return redirect("/auth/login")

@login_manager.user_loader
def load_user(id):
    return None if id == None else  Usuario.get_by_id(id)

@app.route('/auth/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect("/")
    isPost = request.method == "POST"
    form = LoginForm(request.form if isPost else None)
    if isPost:
        isValid = form.validate_on_submit()      
        if isValid:
            login_user(form.user)
            return redirect("/")
    return render_template("Login.html", form=form)

@app.route('/auth/registro', methods=["GET", "POST"])
def registro():
    if current_user.is_authenticated:
        return redirect("/")
    isPost = request.method == "POST"
    form = RegistroForm(request.form if isPost else None)
    if isPost:
        isValid = form.validate_on_submit()
        if isValid:
            Usuario.create(correo = form.email.data, contrasena = form.password.data, nombre = form.name.data, role = getApp().defaultRole).save()
            return redirect("login")
    return render_template("Registro.html", form=form)

@app.route('/auth/logout', methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect("/auth/login")

@app.route('/miinformacion', methods=["GET", "POST"])
@login_required
def MiInformacion():
    return render_template("InformacionPiloto.html")

@app.route('/')
@app.route('/dashboard')
@login_required
def Dashboard():
    return render_template("Dashboard.html")


@app.route('/gestionvuelos', methods=["GET", "POST", "DELETE"])
@app.route('/gestionvuelos/<arg>' , methods=["POST"])
@login_required
def GestionVuelos(arg = None):
    if current_user.role != Application.__instance__.adminRole:
        return redirect("/")    
    isPost = request.method == "POST"
    isDelete = arg == "d"
    isModify = arg == "m"
    isModifyAndSave = arg == "ms"
    createForm = GestionCrearVuelo(request.form if isPost else None) 
    deleteForm = GestionEliminarVuelo(request.form if isDelete else None)
    modifyForm = GestionModificarVuelo(request.form if isModify else None)
    modifySaveForm = GestionCrearVuelo(request.form if isModifyAndSave else None) 
    if isModify or isModifyAndSave:
        if isModify:
            lugares = list(map(lambda x: (x.id, x.nombre), [t for t in list(Lugar.select())]))
            pilotos = list(map(lambda x: (x.id, x.nombre), [t for t in list(Usuario.select().where(Usuario.role == getApp().pilotRole))]))
            aviones = list(map(lambda x: (x.id, x.nombre), [t for t in list(Avion.select())]))
            modifySaveForm.init(listaLugares = lugares, listaPiloto = pilotos, listaAvion = aviones).fill(Vuelo.get_by_id(modifyForm.vuelos.data))
            return render_template("EditarVueloPartial.html",  modifyInnerForm = modifySaveForm)
        else:
            createForm = modifySaveForm
            vuelo: Vuelo = Vuelo.select().where(Vuelo.id == int(createForm.id.data)).get()
            vuelo.origen = createForm.origen.data
            vuelo.destino = createForm.destino.data
            vuelo.avion = createForm.avion.data
            vuelo.fecha_salida = createForm.fechaSalida.data
            vuelo.fecha_llegada = createForm.fechaSalida.data + timedelta(minutes = int(createForm.tiempoVuelo.data))
            vuelo.piloto = createForm.piloto.data
            vuelo.save()
            return redirect("/gestionvuelos")
    elif isDelete:
        Vuelo.delete_by_id(deleteForm.vuelos.data)
        return redirect("/gestionvuelos")
    elif isPost:
        Vuelo.create(
                codigo = generateRandomCode(), 
                origen = createForm.origen.data, 
                destino = createForm.destino.data,
                estado = "Disponible",
                capacidad = 999,
                avion = createForm.avion.data,
                fecha_salida = createForm.fechaSalida.data,
                fecha_llegada = createForm.fechaSalida.data + timedelta(minutes = int(createForm.tiempoVuelo.data)),
                piloto = createForm.piloto.data
                ).save()
        return redirect("/gestionvuelos")
    else:
        lugares = list(map(lambda x: (x.id, x.nombre), [t for t in list(Lugar.select())]))
        pilotos = list(map(lambda x: (x.id, x.nombre), [t for t in list(Usuario.select().where(Usuario.role == getApp().pilotRole))]))
        aviones = list(map(lambda x: (x.id, x.nombre), [t for t in list(Avion.select())]))
        vuelos = list(map(lambda x: (x.id, x.codigo), [t for t in list(Vuelo.select())]))
        deleteForm.init(vuelos)
        createForm.init(listaLugares = lugares, listaPiloto = pilotos, listaAvion = aviones)
        modifyForm.init(vuelos)
    return render_template("GestionDeVuelos.html", createForm = createForm, deleteForm = deleteForm, modifyForm = modifyForm)

@app.route('/infopiloto')
@login_required
def InfoPiloto():    
    return render_template("InformacionPiloto.html")

@app.route('/vervuelo')
@login_required
def vervuelo():   
    return render_template("VerVuelo.html")

def generateRandomCode():
    return str(randrange(1000, 10000))