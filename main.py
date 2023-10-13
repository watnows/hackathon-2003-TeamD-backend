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


@strawberry.type
class User:
    name: str
    age: int


@strawberry.type
class Song:
    song_name: str
    categories : List[str]


@strawberry.type
class Room:
    room_id: int
    user_id: List[int]
    name: str
    

@strawberry.type
class RegisterComplete:
    user_id : int
    categories : List[str]


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
    categories : List[str]


@strawberry.type
class Query:
    @strawberry.field
    def song(self, room_id: int) -> List[Song]:
        room = db["RoomTable"].find_one({'room_id':room_id})
        print(room)
        menber_categories_list = []
        
        user_ids = room["user_id"]
        
        for user_id in user_ids:
            try:
                user = db["UserTable"].find_one({"user_id":user_id})
                categories = user["categories"]
            except TypeError:
                continue
            for c in categories:
                menber_categories_list.append(c)
            

        song_categories = defaultdict(set)  

        for k in menber_categories_list:
            results = sp.search(q=k, limit=3, market="JP", type="playlist")

            for idx, playlist in enumerate(results["playlists"]["items"]):
                playlisturl = str(playlist["href"]).split("/")
                # URLの最後の要素が欲しいので分割
                playlistID = playlisturl[len(playlisturl)-1]
                # URLの最後の部分がプレイリストID
                playListTrack = sp.playlist(playlist_id=playlistID, market="JP")

                for i, track in enumerate(playListTrack["tracks"]["items"]):
                    name = track["track"]["name"]
                    song_categories[name].add(k)  

        songs = [Song(song_name=name, categories=list(song_categories[name])) for name in song_categories.keys()]

        songs.sort(key=lambda x: len(x.categories), reverse=True)
        sliced_song = songs[:30]
                
        return sliced_song


@strawberry.type
class Mutation:
    @strawberry.field
    def create_room(self, room: CreateRoom) -> Room:
        new_room = Room(
            room_id=random.randint(1, 10000),
            user_id=[room.user_id],
            name=room.room_name,
        )
        collection = db["RoomTable"]
        collection.insert_one(new_room.__dict__)
        return new_room

    @strawberry.field
    def join_room(self, join: JoinRoom) -> Room:
        collection = db["RoomTable"]
        collection.update_one(
            {"room_id": join.room_id}, {"$push": {"user_id": join.user_id}}
        )
        room = collection.find_one(filter={"room_id": join.room_id})
        return Room(room_id=room["room_id"], user_id=room["user_id"], name=room["name"])
    

    @strawberry.field
    def register(self, regist:Register) -> RegisterComplete:
        collection = db["UserTable"]
        collection.insert_one(regist.__dict__)
        return regist



schema = strawberry.Schema(query=Query, mutation=Mutation)

sdl = str(schema)

with open("schema.graphql", "w") as f:
    f.write(sdl)

graphql_app = GraphQL(schema)

app = FastAPI()


app.add_route("/graphql", graphql_app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello")
async def root():
    return {"message": "Hello"}
