from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

"""


# ミドルウェアを追加
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 許可するオリジンを指定。安全な設定に注意してください。
    allow_credentials=True,
    allow_methods=["*"],  # 許可するHTTPメソッドを指定。必要に応じて調整してください。
    allow_headers=["*"],  # 許可するHTTPヘッダーを指定。必要に応じて調整してください。
)


"""


# ルートエンドポイントの定義
@app.get("/")
def read_root():
    return {"message": "Hello, World!"}
