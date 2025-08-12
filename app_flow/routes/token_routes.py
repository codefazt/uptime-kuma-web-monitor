from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from app_flow.models import db, TokenMonitor, Usuario

bp = Blueprint('token_routes', __name__)

@bp.route('/tokens', methods=['GET', 'POST'])
def manage_tokens():
    if 'usuario_id' not in session:
        return redirect(url_for('auth_routes.login'))
    usuario = Usuario.query.get(session['usuario_id'])
    if request.method == 'POST':
        token = request.form['token']
        nuevo_token = TokenMonitor(usuario_id=usuario.id, token=token)
        db.session.add(nuevo_token)
        db.session.commit()
        flash('Token guardado')
    tokens = TokenMonitor.query.filter_by(usuario_id=usuario.id).all()
    return render_template('tokens.html', tokens=tokens)
