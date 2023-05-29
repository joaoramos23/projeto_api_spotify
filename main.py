"""
Banco de dados utilizado: Postegres.
Criar DATABASE: 'CREATE DATABASE MUSICAS_SPOTIFY;'
É necessario criar um APP no site do spotify, para conseguir a client_id e o client_secret.

"""
import requests
import json
import psycopg2
import psycopg2.extras as extras
from dotenv import load_dotenv
import os


# Função que gera o token access do spotify.
def token_access():
    header = {'Content-Type': 'application/x-www-form-urlencoded'}
    params = {f'grant_type': 'client_credentials',
              'client_id': {client_id},
              'client_secret': {client_secret}}
    token = requests.post(
        'https://accounts.spotify.com/api/token', params=params, headers=header)
    token = token.json()
    autorization = (token['token_type'] + ' ' + token['access_token'])
    return autorization

# Função que faz a procura da musica solicitada e percorre as paginas do resultado.
def search_tracks():
    resultado = []
    url = 'https://api.spotify.com/v1/search?'
    autorization = token_access()
    header = {"Authorization": autorization}
    params = {'q': 'beleza', 'type': 'track',
              'market': 'BR', 'limit': 50}
    response = requests.get(url, headers=header, params=params)
    data = response.json()
    resultado.extend(data['tracks']['items'])
    while 'next' in data['tracks'] and data['tracks']['next'] is not None:
        next_url = data['tracks']['next']
        response = requests.get(next_url, headers=header)
        data = response.json()
        resultado.extend(data['tracks']['items'])
    return resultado

def connect_db():  # conexão com o banco.
    conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="USER",
        password="SENHA")
    conn.autocommit=True
    if conn.closed == 0:
        print("Conexão estabelecida.")
    else:
        print("A conexão está fechada.")
    return conn

def create_cursor(cnxn):
    cursor = cnxn.cursor()  # criando cursor para executar no banco.
    return cursor

def create_table(cursor, conn):
    cursor.execute("""DROP TABLE IF EXISTS musicas_beleza;    
        CREATE TABLE musicas_beleza(
        ID VARCHAR(50) PRIMARY KEY,
        NAME_MUSIC VARCHAR(250),
        RELEASE_DATE VARCHAR(10),
        NAME_ARTISTS VARCHAR(250),
        POPULARITY INT
        );""")

def insert_db(all_pages,cursor,conn):
    dados = []
    for track in all_pages:
        tuplas = ()
        id_music = track['id']
        name_music = track['name']
        release_date = track['album']['release_date']
        name_artists = ", ".join(artists['name']
                                 for artists in track['artists'])
        popularity = track['popularity']
        tuplas = (id_music, name_music, release_date, name_artists, popularity)
        dados.append(tuplas)
    extras.execute_values(cursor,f"""INSERT INTO musicas_beleza VALUES %s;""",dados)

def main_function():
    cxnx = connect_db()  # conexao com o banco de dados postgres.
    cursor = create_cursor(cxnx)  # criando cursor.
    create_table(cursor, cxnx)
    all_pages = search_tracks()
    insert_db(all_pages,cursor,cxnx)


load_dotenv("env")
# variavel para armazenar o client_id
client_id = os.getenv("CLIENT_ID")
# variavel para armazenar o client_secret
client_secret = os.getenv("CLIENT_SECRET")
main_function()