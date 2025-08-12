-- Script de inicialización para la base de datos APPFLOW
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS usuarios (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    nombre_completo VARCHAR(255),
    create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_date TIMESTAMP,
    delete_date TIMESTAMP,
    usuario VARCHAR(255) UNIQUE NOT NULL,
    passwd VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS token_monitor (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    usuario_id UUID REFERENCES usuarios(id),
    token VARCHAR(255) NOT NULL,
    create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_date TIMESTAMP,
    delete_date TIMESTAMP
);

CREATE TYPE log_status_enum AS ENUM ('ERROR', 'SUCCESS', 'WARNING');

CREATE TABLE IF NOT EXISTS app_flow_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    usuario_id UUID REFERENCES usuarios(id),
    token_id UUID REFERENCES token_monitor(id),
    log_msg TEXT NOT NULL,
    log_status log_status_enum,
    create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_date TIMESTAMP,
    delete_date TIMESTAMP
);
