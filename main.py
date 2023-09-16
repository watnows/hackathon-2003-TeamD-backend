# (1) 必要なライブラリをインポートする
import strawberry
from fastapi import FastAPI
from strawberry.asgi import GraphQL
from fastapi.middleware.cors import CORSMiddleware


# (2) User型を定義する
@strawberry.type
class User:
    name: str
    age: int


# (3) Query(データの読み込み)を行うクラスを定義する
@strawberry.type
class Query:
    @strawberry.field
    def user(self) -> User:
        return User(name="Shota", age=22)


# (4) スキーマを定義する
schema = strawberry.Schema(query=Query)

# (5) GraphQLエンドポイントを作成する
graphql_app = GraphQL(schema)

# (6) FastAPIアプリのインスタンスを作る
app = FastAPI()


# (7) /graphqlでGraphQL APIへアクセスできるようにし、適切なレスポンスを出力
app.add_route("/graphql", graphql_app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 許可するオリジンを指定。安全な設定に注意してください。
    allow_credentials=True,
    allow_methods=["*"],  # 許可するHTTPメソッドを指定。必要に応じて調整してください。
    allow_headers=["*"],  # 許可するHTTPヘッダーを指定。必要に応じて調整してください。
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello")
async def root():
    return {"message": "Hello"}
