from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Configuración de LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# Simulación de usuarios (puedes conectar a BD después)
users = {
    "admin": {"password": "1234"},
    "operativo": {"password": "1234"},
    "admin2": {"password": "1234"}
}

# Clase de usuario
class User(UserMixin):
    def __init__(self, username):
        self.id = username

@login_manager.user_loader
def load_user(user_id):
    if user_id in users:
        return User(user_id)
    return None

@app.route("/")
def home():
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username in users and users[username]["password"] == password:
            user = User(username)
            login_user(user)
            return redirect(url_for("dashboard"))
        else:
            flash("Usuario o contraseña incorrectos")
            return redirect(url_for("login"))
    return render_template("login.html")

@app.route("/dashboard")
@login_required
def dashboard():
    return f"Hola, {current_user.id}. Estás dentro del sistema. <a href='/logout'>Salir</a>"

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

    # trigger redeploy

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
