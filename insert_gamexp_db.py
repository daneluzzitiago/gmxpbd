import psycopg2
from config import config

def insert_tables():
    """ insert multiple vendors into the vendors table  """
    tables_info = {}

    pessoa = "INSERT INTO Pessoa VALUES(%s, %s, %s, %s, %s, %s)"
    pessoa_info = [
        ('11111111111', 'jorgejesus@gmail.com', 'Jorge', '123abc', 'jogador', '0',),
        ('22222222222', 'tiagoleme@gmail.com', 'Tiago', 'abc123', 'ADM', '3',),
        ('33333333333', 'ana@gmail.com', 'Ana', '123456', 'Jogador', '0',),
        ('44444444444', 'igor@gmail.com', 'Igor', '7891011', 'Jogador', '0',),
        ('55555555555', 'pedro@gmail.com', 'Pedro', 'abcdefg', 'Jogador', '0',),
        ('66666666666', 'livia@gmail.com', 'Livia', 'abreaporta', 'ADM', '3',)
    ]
    tables_info[pessoa] = pessoa_info

    time = "INSERT INTO Time VALUES(%s, %s)"
    time_info = [
        ('EC2k19', 'ENGCOMP2k19',),
        ('BSI', 'BSI2k19',)
    ]
    tables_info[time] = time_info

    jogador = "INSERT INTO Jogador VALUES(%s, %s, NULL, %s)"
    jogador_info = [
        ('11111111111', 'Competição', 'Jesus',),
        ('33333333333', 'Competição', 'An4',),
    ]
    tables_info[jogador] = jogador_info
    jogador2 = "INSERT INTO Jogador VALUES(%s, %s, %s, %s)"
    jogador_info2 = [
        ('44444444444', 'Transmissão', 'narrador', 'Iguinho',),
        ('55555555555', 'Transmissão', 'comentarista', 'Pedra',)
    ]
    tables_info[jogador2] = jogador_info2

    participa = "INSERT INTO Participa VALUES(%s, %s, %s, %s)"
    participa_info = [
        ('11111111111', 'EC2k19', 1, 0,),
        ('33333333333', 'BSI', 0, 1,)
    ]
    tables_info[participa] = participa_info

    posicao = "INSERT INTO Posicao VALUES(%s, %s, %s)"
    posicao_info = [
        ('11111111111', 'ENGCOMP2K19', 'mid',),
        ('11111111111', 'ENGCOMP2K19', 'sup',),
        ('33333333333', 'BSI2K19', 'jungle',)
    ]
    tables_info[posicao] = posicao_info

    arena = "INSERT INTO Arena VALUES(%s, %s, %s)"
    arena_info = [
        ('Arena CAASO', 'CAASO', '10',),
        ('Arena Federal', 'Federal', '500',)
    ]
    tables_info[arena] = arena_info

    jogo = "INSERT INTO Jogo VALUES(%s, %s, %s, %s, %s, %s)"
    jogo_info = [
        ('LOL', 'Windows', 'Trinta GB', '500 MB', 'Um GB', 'Riot',),
        ('CS', 'Windows', 'Dez GB', '500 MB', 'Um GB', 'Valve',)
    ]
    tables_info[jogo] = jogo_info

    empresa = "INSERT INTO Empresa VALUES(%s, %s)"
    empresa_info = [
        ('11111111111111', 'Responde Ai',),
        ('22222222222222', 'McDonalds',)
    ]
    tables_info[empresa] = empresa_info

    campeonato = "INSERT INTO Campeonato VALUES(%s, %s, %s, %s, %s)"
    campeonato_info = [
        ('CS CAASO', 'CS', '5vs5', '1000', '11111111111111',),
        ('LOL Federal', 'LOL', '5vs5', '10', '22222222222222',),
    ]
    tables_info[campeonato] = campeonato_info

    campeonato2 = "INSERT INTO Campeonato VALUES(%s, %s, %s, %s, NULL)"
    campeonato_info2 = [
        ('Liga de CS', 'CS', '1x1', '5000'),
        ('CS Federupa', 'CS', '5x5', '505')
    ]
    tables_info[campeonato2] = campeonato_info2

    inscricao = "INSERT INTO Inscricao VALUES(%s, %s, %s, %s)"
    inscricao_info = [
        ('10', 'CS CAASO', 'CS', 'EC2k19',),
        ('30', 'CS CAASO', 'CS', 'BSI',),
        ('20', 'LOL Federal', 'LOL', 'BSI',),
        ('40', 'LOL Federal', 'LOL', 'EC2k19',)
    ]
    tables_info[inscricao] = inscricao_info

    partida = "INSERT INTO Partida VALUES (%s, TO_TIMESTAMP(%s, %s), TO_TIMESTAMP(%s, %s), %s, NULL, NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    partida_info = [
        ('1', '2019-11-23 10:00:00', 'YYYY-MM-DD HH24:MI:SS', '2019-11-23 12:00:00', 'YYYY-MM-DD HH24:MI:SS', 'Arena CAASO', '44444444444', '55555555555', '22222222222', '10', '5', '6', '11', '10', '30',),
        ('2', '2019-11-23 10:00:00', 'YYYY-MM-DD HH24:MI:SS', '2019-11-23 12:00:00', 'YYYY-MM-DD HH24:MI:SS', 'Arena Federal', '44444444444', '55555555555', '66666666666', '20', '5', '0', '5', '20', '40',),
        ('3', '2019-11-24 14:00:00', 'YYYY-MM-DD HH24:MI:SS', '2019-11-24 18:00:00', 'YYYY-MM-DD HH24:MI:SS', 'Arena CAASO', '44444444444', '55555555555', '22222222222', '20', '15', '8', '4', '20', '40'),
        ('4', '2019-11-24 04:00:00', 'YYYY-MM-DD HH24:MI:SS', '2019-11-24 06:00:00', 'YYYY-MM-DD HH24:MI:SS', 'Arena CAASO', '44444444444', '55555555555', '66666666666', '30', '9', '12', '6', '10', '30')
    ]
    tables_info[partida] = partida_info

    return tables_info

def connect(tables_info):
    """ Connect to the PostgreSQL database server """
    connection = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        connection = psycopg2.connect(**params)
        # create a new cursor
        cursor = connection.cursor()
        # execute the INSERT statement
        for table in tables_info:
            cursor.executemany(table, tables_info[table])
        # commit the changes to the database
        connection.commit()
        # close communication with the database
        cursor.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()

if __name__ == "__main__":
    tables_info = insert_tables()
    connect(tables_info)