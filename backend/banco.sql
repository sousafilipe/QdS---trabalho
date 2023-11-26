CREATE DATABASE itadelivery;

\c itadelivery;

CREATE TABLE clientes (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    cpf VARCHAR(11) UNIQUE NOT NULL,
    telefone VARCHAR(14),
    genero VARCHAR(20),
    senha VARCHAR(255) NOT NULL
);

-- cadastrar veículo

CREATE TABLE veiculos (
    id SERIAL PRIMARY KEY,
    tipo VARCHAR(255) NOT NULL,
    marca VARCHAR(255) NOT NULL,
    modelo VARCHAR(255) NOT NULL,
    ano INTEGER NOT NULL,
    placa VARCHAR(8) UNIQUE NOT NULL
);

-- cadastrar entregador

CREATE TABLE entregadores (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    cpf VARCHAR(11) UNIQUE NOT NULL,
    telefone VARCHAR(14),
    genero VARCHAR(20),
    senha VARCHAR(255) NOT NULL,
    disponibilidade BOOLEAN,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION
);

-- tabela pedidos

CREATE TABLE pedidos (
    id SERIAL PRIMARY KEY,
    cliente_id INTEGER NOT NULL,
    endereco_entrega VARCHAR(255) NOT NULL,
    entregador_id INTEGER,
    status VARCHAR(50),
    FOREIGN KEY (cliente_id) REFERENCES clientes(id),
    FOREIGN KEY (entregador_id) REFERENCES entregadores(id)
);

-- tabela cartoes

CREATE TABLE cartoes (
    id SERIAL PRIMARY KEY,
    cliente_id INTEGER,
    tipo VARCHAR(10),
    numero VARCHAR(16),
    CONSTRAINT fk_cliente FOREIGN KEY (cliente_id)
        REFERENCES clientes (id)
);
