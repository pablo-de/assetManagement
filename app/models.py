from app import *

from flask import  session
from flask_login import LoginManager, UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)
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
            raise ValidationError("El mail ingresado ya se encuentra registrado.")


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

db.create_all()

admin_user = Usuario(nombre="administrator", apellido="administrator", email="admin@admin.com", cargo="administrator", password=bcrypt.generate_password_hash("123456"), admin=1)

existing_user_email = Usuario.query.filter_by(email="admin@admin.com").first()
if not existing_user_email:
    db.session.add(admin_user)
    db.session.commit()