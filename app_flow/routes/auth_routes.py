from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from .. import db
from ..models import Usuario
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint('auth_routes', __name__)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        usuario = request.form['usuario']
        nombre_completo = request.form['nombre_completo']
        passwd = generate_password_hash(request.form['passwd'])
        if Usuario.query.filter_by(usuario=usuario).first():
            flash('Usuario ya existe')
            return redirect(url_for('auth_routes.register'))
        nuevo_usuario = Usuario(usuario=usuario, nombre_completo=nombre_completo, passwd=passwd)
        db.session.add(nuevo_usuario)
        db.session.commit()
        flash('Registro exitoso')
        return redirect(url_for('auth_routes.login'))
    return render_template('register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        passwd = request.form['passwd']
        user = Usuario.query.filter_by(usuario=usuario).first()
        if user and check_password_hash(user.passwd, passwd):
            session['usuario_id'] = str(user.id)
            flash('Login exitoso')
            return redirect(url_for('token_routes.manage_tokens'))
        flash('Credenciales incorrectas')
    return render_template('login.html')

@bp.route('/logout')
def logout():
    session.pop('usuario_id', None)
    flash('Sesión cerrada')
    return redirect(url_for('auth_routes.login'))
