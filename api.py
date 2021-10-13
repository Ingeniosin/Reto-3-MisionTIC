import os

from flask import Flask, render_template, request, session
from flask_login import (LoginManager, current_user, login_required,
                         login_user, logout_user)
from werkzeug.utils import redirect

from app import App as Application
from src.model.input.IUserCredential import IUserCredential
from src.model.input.IUserRegister import IUserRegister

Application()

app = Flask(__name__)
app.secret_key = os.urandom(24)
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.unauthorized_handler
def unauthorized():
    return redirect("/auth/login")

@login_manager.user_loader
def load_user(id):
    from src.model.entity.User import User
    return None if id == None else  User.get_by_id(id)


@app.route('/auth/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect("/")
    isPost = request.method == "POST"
    form = IUserCredential(request.form if isPost else None)
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
    form = IUserRegister(request.form if isPost else None)
    if isPost:
        isValid = form.validate_on_submit()
        if isValid:
            from src.model.entity.User import User
            User.create(email = form.email.data, password = form.password.data, name = form.name.data).save()
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
    return render_template("MiInformacion.html")

@app.route('/')
@app.route('/dashboard')
@login_required
def Dashboard():
    return render_template("Dashboard.html")


@app.route('/gestionvuelos')
@login_required
def GestionVuelos():
    return render_template("GestionDeVuelos.html")

@app.route('/infopiloto')
@login_required
def InfoPiloto():
    from src.model.entity.User import User
    
    return render_template("InformacionPiloto.html")

