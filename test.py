import os
from pymongo import MongoClient
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import strawberry
from fastapi import FastAPI
from strawberry.asgi import GraphQL
from fastapi.middleware.cors import CORSMiddleware


client_id = '49b607371e524745b0200c82ae283fba'
client_secret = 'f8100708fd044216bf3dfd9cd4854558'
 
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

keyword = 'aa'


results = sp.search(q=keyword, limit=2, market="JP")
for idx, track in enumerate(results['tracks']['items']):
    print(idx + 1, track['name'], track)