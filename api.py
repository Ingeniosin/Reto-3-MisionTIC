from flask import Flask, render_template, request
from werkzeug.utils import redirect
from entity.UserCredential import UserCredential
from entity.UserRegister import UserRegister
import os

from entity.UserRegister import UserRegister

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/')
def home():
    return render_template("_Layout.html")

@app.route('/auth/login' , methods=["GET","POST"])
def login():
    isPost = request.method=="POST";
    form = UserCredential(request.form if isPost else None) 
    if isPost:
        isValid = form.validate_on_submit();
        if isValid:
            return redirect("/")
    return render_template("Login.html", form = form)

@app.route('/auth/registro', methods=["GET","POST"])
def registro():
    isPost = request.method=="POST";
    form = UserRegister(request.form if isPost else None) 
    if isPost:
        isValid = form.validate_on_submit();
        if isValid:
            return redirect("login")
    return render_template("Registro.html", form = form)


@app.route('/miinformacion', methods=["GET","POST"])
def MiInformacion():
    return render_template("MiInformaciona.html")

@app.route('/dashboard')
def Dashboard():
    return render_template("Dashboard.html")