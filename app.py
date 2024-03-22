from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(16)  # Necesario para el manejo de sesiones

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost:3306/usuarios'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    correo = db.Column(db.String(255), nullable=False, unique=True)
    contraseña = db.Column(db.String(255), nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/login.html", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        correo = request.form["correo"]
        contraseña = request.form["contraseña"]

        # Verificar las credenciales en la base de datos
        usuario = Usuario.query.filter_by(correo=correo).first()

        if usuario and check_password_hash(usuario.contraseña, contraseña):
            return redirect(url_for("sesactiva"))  # Redirigir a la página de sesion activa
        else:
            flash("Credenciales incorrectas. Por favor, inténtalo de nuevo.", "error")  # Mostrar mensaje de error

    return render_template("login.html")

@app.route('/logout')
def logout():
    # No necesitas eliminar la sesión de usuario aquí
    return redirect(url_for('index'))

@app.route('/sesactiva')
def sesactiva():
    return render_template('sesactiva.html')

@app.route('/register.html', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        contraseña = request.form['contraseña']

        # Hashear la contraseña antes de almacenarla en la base de datos
        contraseña_hasheada = generate_password_hash(contraseña)

        nuevo_usuario = Usuario(nombre=nombre, correo=correo, contraseña=contraseña_hasheada)
        db.session.add(nuevo_usuario)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
