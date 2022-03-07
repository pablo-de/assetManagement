from datetime import datetime, timedelta
from flask import Flask, redirect, render_template, request, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user, user_logged_in
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
from getpass import getpass

app = Flask(__name__)
app.secret_key = "Secret Key"

bcrypt = Bcrypt(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/assetManagement'
app.config['SQALALCHEMY_TRACK_MODIFICATION'] = False

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))


@app.before_request
def make_session_permanent():
    session.permanent = True

class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(20), nullable=False)
    apellido = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    cargo = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    admin = db.Column(db.Integer, default=0)

class LoginForm(FlaskForm):
    email = StringField(validators=[InputRequired(), Length(
        min=10, max=50)], render_kw={"placeholder": "Email"})
    password = PasswordField(validators=[InputRequired(), Length(
        min=5, max=16)], render_kw={"placeholder": "Password"})
    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    nombre = StringField(validators=[InputRequired(), Length(
        min=4, max=15)], render_kw={"placeholder": "Nombre"})
    apellido = StringField(validators=[InputRequired(), Length(
        min=4, max=15)], render_kw={"placeholder": "Apellido"})
    email = StringField(validators=[InputRequired(), Length(
        min=10, max=50)], render_kw={"placeholder": "Email"})
    cargo = StringField(validators=[InputRequired(), Length(
        min=4, max=15)], render_kw={"placeholder": "Cargo"})
    password = PasswordField(validators=[InputRequired(), Length(
        min=5, max=16)], render_kw={"placeholder": "Contraseña"})
    admin = BooleanField(label=('Usuario admin?'))
    submit = SubmitField('Registrar')

    def validate_email(self, email):
        existing_user_email = Usuario.query.filter_by(email=email.data).first()
        if existing_user_email:
            raise ValidationError(
                "El mail ingresado ya se encuentra registrado.")


class Asset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente = db.Column(db.String(100))
    nombre = db.Column(db.String(50))
    os = db.Column(db.String(50))
    ip = db.Column(db.String(50))
    hostname = db.Column(db.String(50))
    ram = db.Column(db.String(50))
    cpu = db.Column(db.String(50))
    vga = db.Column(db.String(50))
    disco = db.Column(db.String(50))
    descripcion = db.Column(db.String(1024))
    tipo = db.Column(db.String(50))
    comentarios = db.Column(db.String(1024))
    creado = db.Column(db.String(50))
    modificado = db.Column(db.String(50))
    creador = db.Column(db.String(50))
    eliminar = db.Column(db.Integer, default=0)

    def __init__(self, cliente, nombre, os, ip, hostname, ram, cpu, vga, disco, descripcion, tipo, comentarios, creado, modificado, creador):
        self.cliente = cliente
        self.nombre = nombre
        self.os = os
        self.ip = ip
        self.hostname = hostname
        self.ram = ram
        self.cpu = cpu
        self.vga = vga
        self.disco = disco
        self.descripcion = descripcion
        self.tipo = tipo
        self.comentarios = comentarios
        self.creado = creado
        self.modificado = modificado
        self.creador = creador


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/registrar', methods=['GET', 'POST'])
# @login_required
def registrar():
    if current_user.admin:
        form = RegisterForm()
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data)
            new_user = Usuario(nombre=form.nombre.data, apellido=form.apellido.data,
                               email=form.email.data, cargo=form.cargo.data, password=hashed_password, admin=form.admin.data)
            db.session.add(new_user)
            db.session.commit()
            flash('Registrado correctamente', category='success')
            return redirect(url_for('login'))
    else:
        return redirect(url_for('asset_page'))

    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'Error creando el usuario: {err_msg}', category='danger')

    return render_template('registrar.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('asset_page'))

    if form.validate_on_submit():
        user = Usuario.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash(
                f'Acceso exitoso, logueado como {user.email}', category='success')
            return redirect(url_for('asset_page'))
        else:
            flash(f'Usuario o contraseña incorrecto. Intente nuevamente.',
                  category='danger')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash('Saliendo...', category='info')
    return redirect(url_for("login"))


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


@app.route('/asset')
@login_required  # Requiere estar logueado para visualizar
def asset_page():
    query = Asset.query.all()
    return render_template('asset.html', asset=query)


@app.route('/insert', methods=['POST'])
@login_required
def insert():
    if request.method == 'POST':
        cliente = request.form['cliente']
        nombre = request.form['nombre']
        os = request.form['os']
        ip = request.form['ip']
        hostname = request.form['hostname']
        ram = request.form['ram']
        cpu = request.form['cpu']
        vga = request.form['vga']
        disco = request.form['disco']
        descripcion = request.form['descripcion']
        tipo = request.form['tipo']
        comentarios = request.form['comentarios']
        creado = datetime.now().strftime('%d-%m-%Y - %H:%M')
        modificado = " "
        creador = current_user.apellido

        my_data = Asset(cliente, nombre, os, ip, hostname, ram,
                        cpu, vga, disco, descripcion, tipo, comentarios, creado, modificado, creador)
        db.session.add(my_data)
        db.session.commit()

        flash(f"Agregado correctamente", category='success')
        return redirect(url_for('asset_page'))


@app.route('/update_asset', methods=['GET', 'POST'])
@login_required
def update_asset():
    if request.method == 'POST':
        data = Asset.query.get(request.form.get('id'))
        data.cliente = request.form['cliente']
        data.nombre = request.form['nombre']
        data.os = request.form['os']
        data.ip = request.form['ip']
        data.hostname = request.form['hostname']
        data.ram = request.form['ram']
        data.cpu = request.form['cpu']
        data.vga = request.form['vga']
        data.disco = request.form['disco']
        data.descripcion = request.form['descripcion']
        data.tipo = request.form['tipo']
        data.comentarios = request.form['comentarios']
        data.modificado = datetime.now().strftime('%d-%m-%Y - %H:%M')

        db.session.commit()
        flash(f"Editado correctamente", category='success')
        return redirect(url_for('asset_page'))


@app.route('/delete_asset/<id>/', methods=['GET', 'POST'])
@login_required
def delete_asset(id):
    data = Asset.query.get(id)
    data.eliminar = 1
    db.session.commit()
    flash("Eliminado correctamente", category='success')
    return redirect(url_for('asset_page'))


@app.route('/usuarios')
@login_required 
def usuarios():
    if current_user.admin:
        query = Usuario.query.all()
        return render_template('usuarios.html', users=query)
    else:
        return redirect(url_for('asset_page'))

@app.route('/update_user', methods=['GET', 'POST'])
@login_required
def update_user():
    if current_user.admin:
        if request.method == 'POST':
            data = Usuario.query.get(request.form.get('id'))
            data.nombre = request.form['nombre']
            data.apellido = request.form['apellido']
            data.email = request.form['email']
            data.cargo = request.form['cargo']
            #data.password = request.form['password']

            db.session.commit()
            flash(f"Usuario editado correctamente", category='success')
            return redirect(url_for('usuarios'))
    else:
        return redirect(url_for('asset_page'))

@app.route('/delete_user/<id>/', methods=['GET', 'POST'])
@login_required
def delete_user(id):
    if current_user.admin:
        user = Usuario.query.get(id)
        db.session.delete(user)
        db.session.commit()
        flash("Usuario eliminado correctamente", category='success')
        return redirect(url_for('usuarios'))
    else:
        return redirect(url_for('asset_page'))

@app.route('/credentials')
@login_required
def credentials():
    return render_template('credentials.html')


@app.route('/clientes')
@login_required
def clientes():
    return render_template('clientes.html')


@app.errorhandler(404)
def page_not_found(error):
    return render_template("error.html", error="Página no encontrada..."), 404


if __name__ == '__main__':
    app.run(debug=True)
