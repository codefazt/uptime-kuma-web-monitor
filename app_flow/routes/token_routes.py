from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from .. import db
from ..models import TokenMonitor, Usuario, TokenStatus

bp = Blueprint('token_routes', __name__)

@bp.route('/tokens', methods=['GET', 'POST'])
def manage_tokens():
    if 'usuario_id' not in session:
        flash('Por favor, inicie sesión para continuar.', 'warning')
        return redirect(url_for('auth_routes.login'))

    usuario = Usuario.query.get(session['usuario_id'])
    if not usuario:
        session.pop('usuario_id', None)
        flash('Usuario no encontrado.', 'error')
        return redirect(url_for('auth_routes.login'))

    if request.method == 'POST':
        token_value = request.form.get('token')
        host_value = request.form.get('host')
        status_value = request.form.get('status')
        if not token_value or not host_value:
            flash('Los campos de host y token no pueden estar vacíos.', 'error')
        else:
            nuevo_token = TokenMonitor(usuario_id=usuario.id, host=host_value, token=token_value, status=status_value)
            db.session.add(nuevo_token)
            db.session.commit()
            flash('Token guardado exitosamente.', 'success')
        return redirect(url_for('token_routes.manage_tokens'))

    # Filtramos para no mostrar tokens borrados (soft-delete) y ordenamos por fecha
    tokens = TokenMonitor.query.filter_by(usuario_id=usuario.id, delete_date=None).order_by(TokenMonitor.create_date.desc()).all()
    return render_template('tokens.html', tokens=tokens, token_status=TokenStatus)

@bp.route('/tokens/update/<uuid:token_id>', methods=['GET', 'POST'])
def update_token(token_id):
    if 'usuario_id' not in session:
        flash('Por favor, inicie sesión para continuar.', 'warning')
        return redirect(url_for('auth_routes.login'))

    token_to_update = TokenMonitor.query.filter_by(id=token_id, usuario_id=session['usuario_id']).first_or_404()

    if request.method == 'POST':
        new_token_value = request.form.get('token')
        new_host_value = request.form.get('host')
        new_status_value = request.form.get('status')
        if not new_token_value or not new_host_value:
            flash('Los campos de host y token no pueden estar vacíos.', 'error')
        else:
            token_to_update.token = new_token_value
            token_to_update.host = new_host_value
            token_to_update.status = new_status_value
            db.session.commit()
            flash('Token actualizado exitosamente.', 'success')
            return redirect(url_for('token_routes.manage_tokens'))
    
    return render_template('update_token.html', token=token_to_update, token_status=TokenStatus)

@bp.route('/tokens/delete/<uuid:token_id>', methods=['POST'])
def delete_token(token_id):
    if 'usuario_id' not in session:
        flash('Por favor, inicie sesión para continuar.', 'warning')
        return redirect(url_for('auth_routes.login'))

    token_to_delete = TokenMonitor.query.filter_by(id=token_id, usuario_id=session['usuario_id']).first_or_404()
    
    db.session.delete(token_to_delete)
    db.session.commit()
    flash('Token eliminado exitosamente.', 'success')
    return redirect(url_for('token_routes.manage_tokens'))
