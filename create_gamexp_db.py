#!/usr/bin/python
import psycopg2
from config import config

def create_tables():
    """ create tables in the PostgreSQL database"""
    tables = (
        """
        CREATE TABLE Pessoa(
            CPF VARCHAR(11),
            Email VARCHAR(20),
            Nome VARCHAR(30) NOT NULL,
            Senha VARCHAR(20) NOT NULL,
            Tipo VARCHAR(20),
            Permissoes INTEGER DEFAULT 0,
            PRIMARY KEY (CPF),
            UNIQUE (Email) 
        )
        """,
        """
        CREATE TABLE Jogador(
            CPF VARCHAR (11),
            Subtipo VARCHAR (20),
            Narrador_ou_comentarista VARCHAR (20),
            Nick VARCHAR (20),
            FOREIGN KEY (CPF) REFERENCES Pessoa(CPF) ON UPDATE CASCADE ON DELETE CASCADE,
            PRIMARY KEY (CPF),
            UNIQUE (Nick)
        )
        """,
        """
        CREATE TABLE Time(
            TAG VARCHAR (20),
            Nome VARCHAR (30),
            PRIMARY KEY (TAG),
            UNIQUE (Nome)
        )
        """,
        """
        CREATE TABLE Participa(
            Competidor VARCHAR (11),
            TAG VARCHAR (20),
            Capitao INTEGER DEFAULT (0),
            Reserva INTEGER DEFAULT (0),
            FOREIGN KEY (Competidor) REFERENCES Jogador(CPF) ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (TAG) REFERENCES Time(TAG) ON UPDATE CASCADE ON DELETE CASCADE,
            PRIMARY KEY (Competidor, TAG)
        )
        """,
        """
        CREATE TABLE Posicao(
            Competidor VARCHAR (11),
            TAG VARCHAR (20),
            Posicao VARCHAR (20),
            PRIMARY KEY (Competidor, TAG, Posicao)
        )
        """,
        """
        create table Arena(
            Nome VARCHAR (20),
            Local VARCHAR (20),
            Quantidade_cadeiras INTEGER,
            PRIMARY KEY (Nome)
        )
        """,
        """
        CREATE TABLE Jogo(
            Nome VARCHAR (20),
            SO VARCHAR (20),
            HD VARCHAR (20),
            RAM VARCHAR (20),
            Memoria_video VARCHAR (20),
            Dev VARCHAR (20),
            PRIMARY KEY (Nome)
        )
        """,
        """
        CREATE TABLE Empresa(
            CNPJ VARCHAR (14),
            Nome VARCHAR (20),
            PRIMARY KEY (CNPJ)
        )
        """,
        """
        CREATE TABLE Campeonato(
            Nome VARCHAR (20),
            Nome_jogo VARCHAR (20),
            Formato VARCHAR (20),
            Premiacao INTEGER,
            Empresa VARCHAR (14),
            PRIMARY KEY (Nome, Nome_jogo),
            FOREIGN KEY (Nome_jogo) REFERENCES Jogo(Nome) ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (Empresa) REFERENCES Empresa(CNPJ) ON UPDATE CASCADE ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE Inscricao(
            Id INTEGER,
            Nome_campeonato VARCHAR(20),
            Jogo VARCHAR(20),
            TAG VARCHAR(20),
            PRIMARY KEY (ID),
            FOREIGN KEY (Nome_campeonato, Jogo) REFERENCES Campeonato(Nome, Nome_jogo) ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (TAG) REFERENCES Time(TAG) ON UPDATE CASCADE ON DELETE CASCADE,
            UNIQUE (Nome_campeonato, Jogo, TAG)
        )
        """,
        """
        CREATE TABLE Partida(
            Id INTEGER,
            Hr_ini TIMESTAMP,
            Hr_fim TIMESTAMP,
            Nome_arena VARCHAR(20),
            Id1 INTEGER,
            Id2 INTEGER,
            Narrador VARCHAR(11),
            Comentarista VARCHAR(11),
            Adm VARCHAR(11) NOT NULL,
            Vencedor INTEGER,
            Pont_time1 INTEGER,
            Pont_time2 INTEGER,
            Rounds INTEGER,
            Inscricao1 INTEGER,
            Inscricao2 INTEGER,
            PRIMARY KEY (Id),
            FOREIGN KEY (Nome_arena) REFERENCES Arena(Nome),
            UNIQUE(Hr_ini, Hr_fim, Nome_arena),
            FOREIGN KEY (Id1) REFERENCES Partida(Id) ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (Id2) REFERENCES Partida(Id) ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (Narrador) REFERENCES Jogador(CPF) ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (Comentarista) REFERENCES Jogador(CPF) ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (Adm) REFERENCES Pessoa(CPF) ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (Vencedor) REFERENCES Inscricao(Id) ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (Inscricao1) REFERENCES Inscricao(Id) ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (Inscricao2) REFERENCES Inscricao(Id) ON UPDATE CASCADE ON DELETE CASCADE
        )
        """
    )

    return tables


def connect(tables):
    """ Connect to the PostgreSQL database server """
    connection = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        connection = psycopg2.connect(**params)
        cursor = connection.cursor()
        # create table one by one
        for table in tables:
            cursor.execute(table)
        # close communication with the PostgreSQL database server
        cursor.close()
        # commit the changes
        connection.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()
 
 
if __name__ == '__main__':
    tables = create_tables()
    connect(tables)

