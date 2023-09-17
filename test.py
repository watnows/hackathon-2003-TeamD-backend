import os
from pymongo import MongoClient
from typing import List
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import strawberry
from fastapi import FastAPI
from strawberry.asgi import GraphQL
from fastapi.middleware.cors import CORSMiddleware
import random
from collections import defaultdict


load_dotenv()

client = MongoClient(os.environ["MONGO_URL"])
db = client["RoomDB"]


client_id = "49b607371e524745b0200c82ae283fba"
client_secret = "f8100708fd044216bf3dfd9cd4854558"

sp = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(
        client_id=client_id, client_secret=client_secret
    )
)


# (2) User型を定義する
@strawberry.type
class User:
    name: str
    age: int


@strawberry.type
class Song:
    song_name: str
    category : List[str]


@strawberry.type
class Room:
    room_id: int
    user_id: List[int]
    name: str
    

@strawberry.type
class RegisterComplete:
    user_id : int
    category : List[str]


@strawberry.input
class CreateRoom:
    user_id: int
    room_name: str


@strawberry.input
class JoinRoom:
    user_id: int
    room_id: int
    
@strawberry.input
class Register:
    user_id : int
    category : List[str]


    
