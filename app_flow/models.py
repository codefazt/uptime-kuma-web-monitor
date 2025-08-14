from . import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import func, Enum
import uuid

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre_completo = db.Column(db.String(255))
    create_date = db.Column(db.DateTime, server_default=func.now())
    update_date = db.Column(db.DateTime, onupdate=func.now())
    delete_date = db.Column(db.DateTime, nullable=True)
    usuario = db.Column(db.String(255), unique=True, nullable=False)
    passwd = db.Column(db.String(255), nullable=False)
    tokens = db.relationship('TokenMonitor', backref='usuario', lazy=True)
    logs = db.relationship('AppFlowLog', backref='usuario', lazy=True)

class TokenMonitor(db.Model):
    __tablename__ = 'token_monitor'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    usuario_id = db.Column(UUID(as_uuid=True), db.ForeignKey('usuarios.id'))
    token = db.Column(db.String(255), nullable=False)
    create_date = db.Column(db.DateTime, server_default=func.now())
    update_date = db.Column(db.DateTime, onupdate=func.now())
    delete_date = db.Column(db.DateTime, nullable=True)
    logs = db.relationship('AppFlowLog', backref='token_monitor', lazy=True)

class AppFlowLog(db.Model):
    __tablename__ = 'app_flow_logs'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    usuario_id = db.Column(UUID(as_uuid=True), db.ForeignKey('usuarios.id'))
    token_id = db.Column(UUID(as_uuid=True), db.ForeignKey('token_monitor.id'))
    log_msg = db.Column(db.Text, nullable=False)
    log_status = db.Column(Enum('ERROR', 'SUCCESS', 'WARNING', name='log_status_enum'))
    create_date = db.Column(db.DateTime, server_default=func.now())
    update_date = db.Column(db.DateTime, onupdate=func.now())
    delete_date = db.Column(db.DateTime, nullable=True)
