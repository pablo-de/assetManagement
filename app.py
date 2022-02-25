from email.policy import default
from flask import Flask, redirect, render_template, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = "Secret Key"

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/assetManagement'
app.config['SQALALCHEMY_TRACK_MODIFICATION'] = False

db = SQLAlchemy(app)


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
    eliminar = db.Column(db.Integer, default=0)

    def __init__(self, cliente, nombre, os, ip, hostname, ram, cpu, vga, disco, descripcion, tipo, comentarios, creado, modificado):
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


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login_page():
    return render_template('login.html')


@app.route('/asset')
def asset_page():
    data = Asset.query.all()
    return render_template('asset.html', asset=data)


@app.route('/insert', methods=['POST'])
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

        my_data = Asset(cliente, nombre, os, ip, hostname, ram,
                        cpu, vga, disco, descripcion, tipo, comentarios, creado, modificado)
        db.session.add(my_data)
        db.session.commit()

        flash(f"Agregado correctamente")
        return redirect(url_for('asset_page'))


@app.route('/update', methods=['GET', 'POST'])
def update():
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
        flash(f"Editado correctamente")
        return redirect(url_for('asset_page'))


@app.route('/delete/<id>/', methods=['GET', 'POST'])
def delete(id):
    data = Asset.query.get(id)
    data.eliminar = 1
    db.session.commit()
    flash("Eliminado correctamente")
    return redirect(url_for('asset_page'))


@app.errorhandler(404)
def page_not_found(error):
    return render_template("error.html", error="Página no encontrada..."), 404


if __name__ == '__main__':
    app.run(debug=True)
