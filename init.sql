CREATE DATABASE IF NOT EXISTS univesp_pi;

USE univesp_pi;

CREATE TABLE IF NOT EXISTS dados_vacinas_araras (
        `INDEX` INT PRIMARY KEY NOT NULL,
        CNES_ESTABELECIMENTO VARCHAR(255),
        CODIGO_LOTE VARCHAR(255),
        DATA_APLICACAO_VACINA DATE,
        DATA_APRAZAMENTO DATE,
        DATA_NASCIMENTO_PACIENTE DATE,
        DATA_REGISTRO_VACINA DATETIME,
        DATA_VALIDADE_LOTE DATE,
        DOSE VARCHAR(255),
        DOSE_ADICIONAL VARCHAR(255),
        ESTRATEGIA VARCHAR(255),
        ETNIA_PACIENTE VARCHAR(255),
        GRUPO_ATENDIMENTO VARCHAR(255),
        GVE VARCHAR(255),
        IDADE INT,
        IMUNOBIOLOGICO VARCHAR(255),
        MAE VARCHAR(255),
        MUNCP_ESTABELECIMENTO VARCHAR(255),
        MUNICIPIO_RESIDENCIA_PACIENTE VARCHAR(255),
        PACIENTE_GESTANTE VARCHAR(255),
        PACIENTE_PUERPERE VARCHAR(255),
        RACA_COR_PACIENTE VARCHAR(255),
        SEXO_PACIENTE VARCHAR(255),
        SIGLA_UF_RESIDENCIA_PACIENTE VARCHAR(255)
    );

set global local_infile=1;

LOAD DATA LOCAL INFILE 'data.csv'
INTO TABLE dados_vacinas_araras 
FIELDS TERMINATED BY ';' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n' 
IGNORE 1 ROWS;
