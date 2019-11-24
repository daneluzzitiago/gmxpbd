#!/usr/bin/python
import psycopg2
from config import config

def execute_query(query):
    """ query data from the vendors table """
    connection = None
    try:
        params = config()
        connection = psycopg2.connect(**params)
        cursor = connection.cursor()

        for query in queries:
            cursor.execute(query)
            print("Numero de linhas encontradas: ", cursor.rowcount)
            row = cursor.fetchone()
    
            while row is not None:
                print(row)
                row = cursor.fetchone()
            
            print()

        cursor.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()

if __name__ == "__main__":
    queries = [
        "select C.Nome_jogo, count(*) from Jogo J join Campeonato C on J.Nome = C.Nome_jogo group by C.Nome_jogo",
        "select P.Nome, Pa.TAG, Po.Posicao from Pessoa P join Jogador J on P.CPF = J.CPF join Participa Pa on J.CPF = Pa.Competidor join Posicao Po on Pa.Competidor = Po.competidor",
        "select C.Nome, T.Nome, Pe.Nome from Campeonato C join Inscricao I on C.Nome = I.Nome_campeonato AND C.Nome_jogo = I.Jogo join Time T on I.TAG = T.TAG join Participa Pa on T.TAG = Pa.TAG join Pessoa Pe on Pe.CPF = Pa.Competidor where Pa.Capitao = 1",
        "select C.Nome, avg(P.Pont_time1) as PT1, avg(P.Pont_time2) as PT2 from Campeonato C join Inscricao I on C.Nome = I.Nome_campeonato AND C.Nome_jogo = I.Jogo join  Partida P on P.Inscricao1 = I.Id OR P.Inscricao2 = I.Id group by (C.Nome_jogo, C.Nome)",
        "select I.TAG, count(*) from Partida P join Inscricao I on P.Vencedor = I.Id group by I.TAG having count(*) >= 3"
    ]
    execute_query(queries)