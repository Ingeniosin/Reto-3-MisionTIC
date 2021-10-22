from random import randrange
from flask import Flask, render_template, request, Markup, session, json
from flask_login import (LoginManager, current_user, login_required, login_user, logout_user)
from werkzeug.utils import redirect
from datetime import timedelta
from app import App as Application

Application()
app = Flask(__name__)
app.secret_key = 'asdasdasdasddsadssaasdsa'
login_manager = LoginManager()
login_manager.init_app(app)
app.jinja_env.add_extension('jinja2.ext.loopcontrols')
app.jinja_env.add_extension('jinja2.ext.do')

from src.model.Input import *
from src.model.Entity import *

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
    ciudades = getApp().lugares
    ciudadesString = Markup(list(map(lambda x: x.nombre, ciudades)))
    usuarioVuelos = [t for t in list(UsuarioVuelo.select())]
    comentarios = [t for t in list(Comentarios.select())]
    cantidadDestinos = Markup(list(map(lambda x: getCantidadPasajerosByLugar(x, usuarioVuelos), ciudades)))
    calificaciones = Markup(list(map(lambda x: getCalificacionByLugar(x, comentarios), ciudades)))
    return render_template("Dashboard.html", ciudades = ciudadesString, cantidadDestinos = cantidadDestinos, calificaciones = calificaciones)


@app.route('/api/gestionvuelos', methods=["POST", "PUT", "DELETE", "GET"])
@login_required
def GestionVuelosApi():
    if request.method == "POST":
        form = GestionCrearVuelo(request.form)        
        codigo = generateRandomCode()
        Vuelo.create(codigo = codigo,  origen = form.origen.data,  destino = form.destino.data,estado = "Disponible",capacidad = form.capacidad.data,avion = form.avion.data,fecha_salida = form.fechaSalida.data,fecha_llegada = form.fechaSalida.data + timedelta(minutes = int(form.tiempoVuelo.data)),piloto = form.piloto.data).save()
        return ok("El vuelo fue generado correctamente! | | * El codigo es: "+codigo)
    elif request.method == "PUT":
        form = GestionCrearVuelo(request.form)        
        vuelo: Vuelo = Vuelo.select().where(Vuelo.id == int(form.id.data)).get()
        vuelo.origen = form.origen.data
        vuelo.destino = form.destino.data
        vuelo.avion = form.avion.data
        vuelo.fecha_salida = form.fechaSalida.data
        vuelo.fecha_llegada = form.fechaSalida.data + timedelta(minutes = int(form.tiempoVuelo.data))
        vuelo.piloto = form.piloto.data
        vuelo.save()
        return render_template("EditarVueloPartial.html", form = GestionCrearVuelo().fill(vuelo))
    elif request.method == "DELETE":
        Vuelo.delete_by_id(request.form.get("vueloId"))
        return ok()
    elif request.method == "GET":
        vueloId = request.args.get('vueloId')
        if vueloId is not None:
            return render_template("EditarVueloPartial.html", form = GestionCrearVuelo().fill(Vuelo.get_by_id(vueloId)))
        return ok(list(map(lambda x: [x.id, x.codigo],  getApp().getVuelos())))
    

@app.route('/gestionvuelos', methods=["GET"])
@login_required
def GestionVuelos():
    if current_user.role.id != 3:
        return redirect("/")    
    return render_template("GestionDeVuelos.html", createForm = GestionCrearVuelo())

@app.route('/infopiloto')
@login_required
def InfoPiloto():    
    return render_template("InformacionPiloto.html")

@app.route('/vervuelo')
@login_required
def vervuelo():   
    return render_template("VerVuelo.html")

@app.route('/informacionvuelos')
@login_required
def informacionvuelos():   
    vuelos = [t for t in list(Vuelo.select())]
    comentarios = [t for t in list(Comentarios.select())]
    for vuelo in vuelos:
        vuelo.calificacion = getCalificacionByVuelo(vuelo, comentarios)
    return render_template("InformacionVuelos.html", vuelos = vuelos)    

def getCalificacionByLugar(lugar: Lugar, comentarios):
    calificaciones = list(map(lambda x: x.calificacion, list(filter(lambda x: x.vuelo.destino.id == lugar.id, comentarios))))
    return sum(calificaciones)/len(calificaciones) if len(calificaciones) > 0 else 0

def getCalificacionByVuelo(vuelo:Vuelo, comentarios):
    calificaciones = list(map(lambda x: x.calificacion, list(filter(lambda x: x.vuelo.id == vuelo.id, comentarios))))
    return sum(calificaciones)/len(calificaciones) if len(calificaciones) > 0 else 0

def getCantidadPasajerosByLugar(lugar: Lugar, usuarioVuelos):
    cantidad = len(list(filter(lambda x: x.vuelo.destino.id == lugar.id, usuarioVuelos)))
    return cantidad if not None else 0


def generateRandomCode():
    return str(randrange(1000, 10000))

def error(msg = ""):
    return json.dumps(msg), 400, {'ContentType':'application/json'}

def ok(msg = ""):
    return json.dumps(msg), 200, {'ContentType':'application/json'}