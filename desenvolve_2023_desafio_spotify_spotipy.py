"""
Banco de dados utilizado: SQL Server.
Criar DATABASE: 'CREATE DATABASE MUSICAS_SPOTIFY;'
Utilização da biblioteca spotipy.
É necessario criar um APP no site do spotify, para conseguir a client_id e o client_secret.
"""

import conexao_db
import json
import spotipy  # pip install spotipy --upgrade
from spotipy.oauth2 import SpotifyClientCredentials


def create_table(cursor):
    cursor.execute(""" USE MUSICAS_SPOTIFY; 
        DROP TABLE MUSICAS_BELEZA;    
        CREATE TABLE MUSICAS_BELEZA(
        ID VARCHAR(50) PRIMARY KEY,
        NAME_MUSIC VARCHAR(250),
        RELEASE_DATE VARCHAR(10),
        NAME_ARTISTS VARCHAR(250),
        POPULARITY INT
        );
        """)


def request(client_id, client_secret):
    access_key = spotipy.client.Spotify(client_credentials_manager=SpotifyClientCredentials(
        client_id, client_secret))
    return access_key


def search_music(access_key, music):
    result = access_key.search(q=music, type='track', market='BR', limit='2')
    return result


def put_music_tracks(result, cursor):
    for track in result['tracks']['items']:
        id_music = track['id']
        name_music = track['name']
        release_date = track['album']['release_date']
        name_artists = ", ".join(artists['name']
                                 for artists in track['artists'])
        popularity = track['popularity']
        cursor.execute("""
            USE MUSICAS_SPOTIFY;
            INSERT INTO MUSICAS_BELEZA VALUES (?,?,?,?,?);""", id_music, name_music, release_date, name_artists, popularity)


def main_function():
    connect = conexao_db.connect_db("MUSICAS_SPOTIFY")
    cursor = conexao_db.create_cursor(connect)
    create_table(cursor)
    access_key = request(client_id, client_secret)
    result = search_music(access_key, music)
    put_music_tracks(result, cursor)


client_id = 'CLIENT-ID'
client_secret = 'CLIENT-SECRET'
music = 'beleza'

main_function()
