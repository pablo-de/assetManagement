from app import *
from app.models import *

from datetime import datetime
from flask import redirect, render_template, request, url_for, flash, session
from flask_login import login_user, login_required, logout_user, current_user


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
@login_required
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
            return redirect(url_for('usuarios'))
    else:
        flash(f"No tiene suficientes privilegios para ingresar.", category='danger')
        return redirect(url_for('asset_page'))

    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'Error creando el usuario: {err_msg}', category='danger')

    return render_template('registrar.html', form=form)


@app.route('/changepwd', methods=['GET', 'POST'])
@login_required
def changepwd():
    if current_user.admin:
        if request.method == 'POST':
            data = Usuario.query.get(request.form.get('id'))

            if request.form['password'] != '':
                if request.form['password'] == request.form['password2']:
                    hashed_password = bcrypt.generate_password_hash(
                        request.form['password'])
                    data.password = hashed_password

                    db.session.commit()
                    flash(f"Contraseña editada correctamente", category='success')
                    return redirect(url_for('usuarios'))
                else:
                    flash(f"Las contraseñas no coinciden", category='danger')
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
        if current_user.id != id:
            user = Usuario.query.get(id)
            db.session.delete(user)
            db.session.commit()
            flash("Usuario eliminado correctamente", category='success')
            return redirect(url_for('usuarios'))
        else:
            flash(f"No puede eliminar su propio usuario", category='danger')
            return redirect(url_for('usuarios'))
    else:
        flash(f"No tiene suficientes privilegios para ingresar.", category='danger')
        return redirect(url_for('asset_page'))


@app.route('/asset')
@login_required  
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