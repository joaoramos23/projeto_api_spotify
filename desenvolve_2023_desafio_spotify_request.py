"""
Banco de dados utilizado: SQL Server.
Criar DATABASE: 'CREATE DATABASE MUSICAS_SPOTIFY;'
É necessario criar um APP no site do spotify, para conseguir a client_id e o client_secret.
"""


import requests
import json
import conexao_db


def create_table(cursor):
    cursor.execute(""" USE MUSICAS_SPOTIFY; 
        DROP TABLE MUSICAS_TODAS_BELEZA;    
        CREATE TABLE MUSICAS_TODAS_BELEZA(
        ID VARCHAR(50) PRIMARY KEY,
        NAME_MUSIC VARCHAR(250),
        RELEASE_DATE VARCHAR(10),
        NAME_ARTISTS VARCHAR(250),
        POPULARITY INT
        );
        """)

def request_access_token(client_id, client_secret):
    uri = 'https://accounts.spotify.com/api/token'
    header = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {'client_secret': client_secret,
            'client_id': client_id,
            'grant_type': 'client_credentials'}
    response = requests.post(uri, data=data, headers=header)
    response = response.json()
    access_token = response['access_token']
    return access_token

def search_music(access_token, cursor):
    global offset
    limit = 50
    uri_search = 'https://api.spotify.com/v1/search'
    header = {'Authorization': 'Bearer ' + access_token}

    while (offset < 1000):
        params = {'q': 'beleza', 'type': 'track',
                  'market': 'BR', 'limit': limit, 'offset': offset}
        result = requests.get(uri_search, headers=header, params=params)
        result = result.json()
        for track in result['tracks']['items']:
            id_music = track['id']
            name_music = track['name']
            release_date = track['album']['release_date']
            name_artists = ", ".join(artists['name']
                                     for artists in track['artists'])
            popularity = track['popularity']
            cursor.execute("""
                USE MUSICAS_SPOTIFY;
                INSERT INTO MUSICAS_TODAS_BELEZA VALUES (?,?,?,?,?);
            """, id_music, name_music, release_date, name_artists, popularity)
        offset = offset + limit
        print("Adicionando:",offset)
        search_music(access_token, cursor)

def main_function():
    connect = conexao_db.connect_db("MUSICAS_SPOTIFY")
    cursor = conexao_db.create_cursor(connect)
    create_table(cursor)
    access_token = request_access_token(client_id, client_secret)
    search_music(access_token, cursor)

offset = 0
client_id = 'CLIENT-ID'
client_secret = 'CLIENT-SECRET'

main_function()
