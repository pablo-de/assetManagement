from datetime import datetime, timedelta
from flask import Flask, redirect, render_template, request, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user, user_logged_in
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = "Secret Key"

bcrypt = Bcrypt(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/assetManagement_test'
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
    submit = SubmitField('Ingresar')


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


class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    razonSocial = db.Column(db.String(100))
    direccion = db.Column(db.String(100))
    localidad = db.Column(db.String(100))
    codigoPostal = db.Column(db.String(50))
    documento = db.Column(db.String(50))
    telefono = db.Column(db.String(50))
    comentarios = db.Column(db.String(1024))
    creado = db.Column(db.String(50))
    modificado = db.Column(db.String(50))
    creador = db.Column(db.String(50))
    eliminar = db.Column(db.Integer, default=0)
    asset = db.relationship('Asset', backref='cliente')
    credential = db.relationship('Credential', backref='cliente')

    def __init__(self, nombre, razonSocial, direccion, localidad, codigoPostal, documento, telefono, comentarios, creado, modificado, creador):
        self.nombre = nombre
        self.razonSocial = razonSocial
        self.direccion = direccion
        self.localidad = localidad
        self.codigoPostal = codigoPostal
        self.documento = documento
        self.telefono = telefono
        self.comentarios = comentarios
        self.creado = creado
        self.modificado = modificado
        self.creador = creador

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'razonSocial': self.razonSocial,
            'direccion': self.direccion,
            'localidad': self.localidad,
            'codigoPostal': self.codigoPostal,
            'documento': self.documento,
            'telefono': self.telefono,
            'comentarios': self.comentarios,
            'creado': self.creado,
            'modificado': self.modificado,
            'creador': self.creador,
            'eliminado': self.eliminar
        }


class Asset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'))
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
    credential = db.relationship('Credential', backref='asset')

    def __init__(self, cliente_id, nombre, os, ip, hostname, ram, cpu, vga, disco, descripcion, tipo, comentarios, creado, modificado, creador):
        self.cliente_id = cliente_id
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

    def to_dict(self):
        return {
            'id': self.id,
            'cliente': self.cliente.nombre,
            'nombre': self.nombre,
            'os': self.os,
            'ip': self.ip,
            'hostname': self.hostname,
            'ram': self.ram,
            'cpu': self.cpu,
            'vga': self.vga,
            'disco': self.disco,
            'descripcion': self.descripcion,
            'tipo': self.tipo,
            'comentarios': self.comentarios,
            'creado': self.creado,
            'modificado': self.modificado,
            'creador': self.creador,
            'eliminado': self.eliminar
        }
        
class Credential(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'))
    asset_id = db.Column(db.Integer, db.ForeignKey('asset.id'))
    tipo = db.Column(db.String(50))
    nombre = db.Column(db.String(50))
    user = db.Column(db.String(50))
    password = db.Column(db.String(50))
    comentarios = db.Column(db.String(1024))
    creado = db.Column(db.String(50))
    modificado = db.Column(db.String(50))
    creador = db.Column(db.String(50))
    eliminar = db.Column(db.Integer, default=0)

    def __init__(self, cliente_id, asset_id, tipo, nombre, user, password, comentarios, creado, modificado, creador):
        self.cliente_id = cliente_id
        self.asset_id = asset_id
        self.tipo = tipo
        self.nombre = nombre
        self.user = user
        self.password = password
        self.comentarios = comentarios
        self.creado = creado
        self.modificado = modificado
        self.creador = creador

    def to_dict(self):
        return {
            'id': self.id,
            'cliente': self.cliente.nombre,
            'asset': self.asset.nombre,
            'tipo': self.tipo,
            'nombre': self.nombre,
            'user': self.user,
            'password': self.password,
            'comentarios': self.comentarios,
            'creado': self.creado,
            'modificado': self.modificado,
            'creador': self.creador,
            'eliminado': self.eliminar
        }


@app.route('/', methods=['GET', 'POST'])
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
                f'Acceso exitoso, logueado como {user.email} ({user.nombre} {user.apellido})', category='success')
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


@app.route('/profile/<id>', methods=['GET', 'POST'])
@login_required
def profile(id):
    user = Usuario.query.filter_by(id=id).first()
    return render_template('profile.html', user=user)


@app.route('/update_profile', methods=['GET', 'POST'])
@login_required
def update_profile():
    if current_user.is_authenticated:
        if request.method == 'POST':
            data = Usuario.query.get(request.form.get('id'))
            data.nombre = request.form['nombre']
            data.apellido = request.form['apellido']
            data.email = request.form['email']
            data.cargo = request.form['cargo']
            db.session.commit()
            flash(f"Datos del usuario editados correctamente", category='success')
            return redirect(url_for('asset_page'))
    else:
        return redirect(url_for('login'))


@app.route('/usuarios')
@login_required
def usuarios():
    if current_user.admin:
        query = Usuario.query.all()
        return render_template('usuarios.html', users=query)
    else:
        flash(f"No tiene suficientes privilegios para ingresar.", category='danger')
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
            data.admin = request.form['admin']
            db.session.commit()
            flash(f"Datos del usuario editados correctamente", category='success')
            return redirect(url_for('usuarios'))
    else:
        flash(f"No tiene suficientes privilegios para ingresar.", category='danger')
        return redirect(url_for('asset_page'))


@app.route('/registrar', methods=['GET', 'POST'])
# @login_required - Sacar comentario en prod
def registrar():
    # if current_user.admin:
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = Usuario(nombre=form.nombre.data, apellido=form.apellido.data,
                           email=form.email.data, cargo=form.cargo.data, password=hashed_password, admin=form.admin.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Registrado correctamente', category='success')
        return redirect(url_for('usuarios'))
    # else:
    #    flash(f"No tiene suficientes privilegios para ingresar.", category='danger')
 #   return redirect(url_for('asset_page'))

    # if form.errors != {}:
    #    for err_msg in form.errors.values():
    #        flash(f'Error creando el usuario: {err_msg}', category='danger')

    return render_template('registrar.html', form=form)


@app.route('/changepwd', methods=['GET', 'POST'])
@login_required
def changepwd():
    if current_user.admin:
        if request.method == 'POST':
            data = Usuario.query.get(request.form.get('id'))

            if request.form['password'] != '':
                hashed_password = bcrypt.generate_password_hash(
                    request.form['password'])
                data.password = hashed_password

                db.session.commit()
                flash(f"Contraseña cambiada correctamente", category='success')
                return redirect(url_for('usuarios'))
            else:
                flash(f"La contraseña no puede estar vacia", category='danger')
                return redirect(url_for('usuarios'))
    else:
        flash(f"No tiene suficientes privilegios para ingresar.", category='danger')
        return redirect(url_for('asset_page'))


@app.route('/delete_user/<id>', methods=['GET', 'POST'])
@login_required
def delete_user(id):
    if current_user.admin:
        user = Usuario.query.get(id)
        db.session.delete(user)
        db.session.commit()
        flash("Usuario eliminado correctamente", category='success')
        return redirect(url_for('usuarios'))
    else:
        flash(f"No tiene suficientes privilegios para ingresar.", category='danger')
        return redirect(url_for('asset_page'))


@app.route('/asset')
@login_required  # Requiere estar logueado para visualizar
def asset_page():
    data = Cliente.query.all()
    return render_template('asset_tabla.html', clientes=data)


@app.route('/api/asset')
@login_required
def asset():
    if current_user.is_authenticated:
        return {'data': [asset.to_dict() for asset in Asset.query]}
    else:
        flash(f"No tiene suficientes privilegios para ingresar.", category='danger')
        return redirect(url_for('asset_page'))


@app.route('/list_asset_delete')
@login_required
def list_asset_delete():
    query = Asset.query.all()
    return render_template('asset_delete.html', assets=query)


@app.route('/insert_asset', methods=['POST'])
@login_required
def insert_asset():
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
        modificado = ""
        creador = current_user.nombre + ' ' + current_user.apellido

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
        data.cliente_id = request.form['cliente']
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


@app.route('/delete_asset/<id>', methods=['GET', 'POST'])
@login_required
def delete_asset(id):
    data = Asset.query.get(id)
    data.eliminar = 1
    db.session.commit()
    flash("Eliminado correctamente", category='success')
    return redirect(url_for('asset_page'))


@app.route('/restore_asset/<id>', methods=['GET', 'POST'])
@login_required
def restore_asset(id):
    data = Asset.query.get(id)
    data.eliminar = 0
    db.session.commit()
    flash("Restaurado correctamente", category='success')
    return redirect(url_for('asset_page'))


@app.route('/asset/view/<id>', methods=['GET', 'POST'])
@login_required
def asset_view(id):
    asset = Asset.query.filter_by(id=id).first()
    return render_template('asset_view.html', data=asset)


@app.route('/asset/edit/<id>', methods=['GET', 'POST'])
@login_required
def asset_edit(id):
    asset = Asset.query.filter_by(id=id).first()
    data = Cliente.query.all()
    return render_template('asset_edit.html', data=asset, clientes=data)


@app.route('/clientes')
@login_required
def clientes_page():
    return render_template('clientes_tabla.html')


@app.route('/api/clientes')
@login_required
def cliente():
    if current_user.is_authenticated:
        return {'data': [cliente.to_dict() for cliente in Cliente.query]}
    else:
        flash(f"No tiene suficientes privilegios para ingresar.", category='danger')
        return redirect(url_for('clientes_page'))


@app.route('/list_clientes_delete')
@login_required
def list_clientes_delete():
    query = Cliente.query.all()
    return render_template('clientes_delete.html', clients=query)


@app.route('/insert_cliente', methods=['POST'])
@login_required
def insert_cliente():
    if request.method == 'POST':
        nombre = request.form['nombre']
        razonSocial = request.form['razonSocial']
        direccion = request.form['direccion']
        localidad = request.form['localidad']
        codigoPostal = request.form['codigoPostal']
        documento = request.form['documento']
        telefono = request.form['telefono']
        comentarios = request.form['comentarios']
        creado = datetime.now().strftime('%d-%m-%Y - %H:%M')
        modificado = ""
        creador = current_user.nombre + ' ' + current_user.apellido

        my_data = Cliente(nombre, razonSocial, direccion, localidad, codigoPostal,
                          documento, telefono, comentarios, creado, modificado, creador)
        db.session.add(my_data)
        db.session.commit()

        flash(f"Agregado correctamente", category='success')
        return redirect(url_for('clientes_page'))


@app.route('/update_cliente', methods=['GET', 'POST'])
@login_required
def update_cliente():
    if request.method == 'POST':
        data = Cliente.query.get(request.form.get('id'))
        data.nombre = request.form['nombre']
        data.razonSocial = request.form['razonSocial']
        data.direccion = request.form['direccion']
        data.localidad = request.form['localidad']
        data.codigoPostal = request.form['codigoPostal']
        data.documento = request.form['documento']
        data.telefono = request.form['telefono']
        data.comentarios = request.form['comentarios']
        data.modificado = datetime.now().strftime('%d-%m-%Y - %H:%M')

        db.session.commit()
        flash(f"Editado correctamente", category='success')
        return redirect(url_for('clientes_page'))


@app.route('/delete_cliente/<id>', methods=['GET', 'POST'])
@login_required
def delete_cliente(id):
    data = Cliente.query.get(id)
    data.eliminar = 1
    db.session.commit()
    flash("Eliminado correctamente", category='success')
    return redirect(url_for('clientes_page'))


@app.route('/restore_cliente/<id>', methods=['GET', 'POST'])
@login_required
def restore_cliente(id):
    data = Cliente.query.get(id)
    data.eliminar = 0
    db.session.commit()
    flash("Restaurado correctamente", category='success')
    return redirect(url_for('clientes_page'))


@app.route('/cliente/view/<id>', methods=['GET', 'POST'])
@login_required
def cliente_view(id):
    cliente = Cliente.query.filter_by(id=id).first()
    return render_template('clientes_view.html', data=cliente)


@app.route('/cliente/edit/<id>', methods=['GET', 'POST'])
@login_required
def cliente_edit(id):
    cliente = Cliente.query.filter_by(id=id).first()
    return render_template('clientes_edit.html', data=cliente)


@app.route('/credentials')
@login_required
def credentials_page():
    cliente = Cliente.query.all()
    asset = Asset.query.all()
    return render_template('credentials_tabla.html', clientes=cliente, assets=asset)


@app.route('/api/credentials')
@login_required
def credentials():
    if current_user.is_authenticated:
        return {'data': [credentials.to_dict() for credentials in Credential.query]}
    else:
        flash(f"No tiene suficientes privilegios para ingresar.", category='danger')
        return redirect(url_for('credentials_page'))


@app.route('/list_credentials_delete')
@login_required
def list_credentials_delete():
    query = Credential.query.all()
    return render_template('credentials_delete.html', clients=query)


@app.route('/insert_credential', methods=['POST'])
@login_required
def insert_credential():
    if request.method == 'POST':
        cliente = request.form['cliente']
        asset = request.form['asset']
        tipo = request.form['tipo']
        nombre = request.form['nombre']
        user = request.form['user']
        password = request.form['password']
        comentarios = request.form['comentarios']
        creado = datetime.now().strftime('%d-%m-%Y - %H:%M')
        modificado = ""
        creador = current_user.nombre + ' ' + current_user.apellido

        my_data = Credential(cliente, asset, tipo, nombre, user, password, comentarios, creado, modificado, creador)
        db.session.add(my_data)
        db.session.commit()

        flash(f"Agregado correctamente", category='success')
        return redirect(url_for('credentials_page'))


@app.route('/update_credential', methods=['GET', 'POST'])
@login_required
def update_credential():
    if request.method == 'POST':
        data = Credential.query.get(request.form.get('id'))
        data.cliente_id = request.form['cliente']
        data.asset_id = request.form['asset']
        data.tipo = request.form['tipo']
        data.nombre = request.form['nombre']
        data.user = request.form['user']
        data.password = request.form['password']
        data.comentarios = request.form['comentarios']
        data.modificado = datetime.now().strftime('%d-%m-%Y - %H:%M')

        db.session.commit()
        flash(f"Editado correctamente", category='success')
        return redirect(url_for('credentials_page'))


@app.route('/delete_credential/<id>', methods=['GET', 'POST'])
@login_required
def delete_credential(id):
    data = Credential.query.get(id)
    data.eliminar = 1
    db.session.commit()
    flash("Eliminado correctamente", category='success')
    return redirect(url_for('credentials_page'))


@app.route('/restore_credential/<id>', methods=['GET', 'POST'])
@login_required
def restore_credential(id):
    data = Credential.query.get(id)
    data.eliminar = 0
    db.session.commit()
    flash("Restaurado correctamente", category='success')
    return redirect(url_for('credentials_page'))


@app.route('/credential/view/<id>', methods=['GET', 'POST'])
@login_required
def credentials_view(id):
    credential = Credential.query.filter_by(id=id).first()
    return render_template('credentials_view.html', data=credential)


@app.route('/credential/edit/<id>', methods=['GET', 'POST'])
@login_required
def credentials_edit(id):
    credential = Credential.query.filter_by(id=id).first()
    cliente = Cliente.query.all()
    asset = Asset.query.all()
    return render_template('credentials_edit.html', data=credential, clientes=cliente, assets=asset)


@app.errorhandler(404)
def page_not_found(error):
    return render_template("error.html"), 404


if __name__ == '__main__':
    app.run(debug=True)
