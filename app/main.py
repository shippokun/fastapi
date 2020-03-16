from fastapi import FastAPI, Query, Path, Body, HTTPException, BackgroundTasks
from typing import Optional, List
from pydantic import BaseModel, Field
from starlette.responses import Response
from starlette.status import HTTP_201_CREATED
from starlette.middleware.cors import CORSMiddleware
import graphene
from starlette.graphql import GraphQLApp
from time import sleep
from enum import Enum
from datetime import datetime
from app.db import session # DBと接続するためのセッション
from app.model import UserTable, User # 使用するモデルをインポート

app = FastAPI(
    title="Sample fastAPI Project",
    description="これはfastAPIを使ってみたかっただけで作っているプロジェクトです",
    varsion="1.0.0",
    openapi_url="/api/v1/openapi.json",
    docs_url="/docs",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Querys(graphene.ObjectType):
    hello = graphene.String(name=graphene.String(default_value="stranger"))

    def resole_hello(self, info, name):
        return "Hello " + name

app.add_route("/", GraphQLApp(schema=graphene.Schema(query=Querys)))


@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/users")
async def read_users():
    users = session.query(UserTable).all()
    return users

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q":q}

@app.get('/get/{path}')
async def path_and_query_params(
        path: str,
        query: int,
        default_none: Optional[str] = None):
    return { "text": f"hello, {path}, {query} and {default_none}" }

@app.get('/validation/{path}')
async def validation(
        string: str = Query(None, min_length=2, max_length=5,
            regex=r'[a-c]+.'),
        integer: int = Query(..., gt=1, le=3),   # required
        alias_query: str = Query('default', alias='alias-query'),
        path: int = Path(10)):
    return {"string": string, "integer": integer, "alias-query": alias_query,
            "path": path}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

@app.get("/model/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learnig FTW!"}
    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}
    return {"model_name": model_name, "message": "Have seen residuals"}

@app.get("/files/{file_path:path}")
async def read_user_me(file_path: str):
    return {"file_path": file_path}

class Data(BaseModel):
    """request data用の型ヒントがされたクラス"""
    string: str
    default_name: Optional[int] = None
    lists: List[int]

@app.post('/post')
async def declare_request_body(data: Data):
    return {"text": f"hello, {data.string}, {data.default_none}, {data.lists}"}

@app.post('/post/embed')
async def declare_request_body(data: Data = Body(..., embed=True)):
    return {"text": f"hello, {data.string}, {data.default_none}, {data.lists}"}

class subDict(BaseModel):
    strings: str
    integer: int

class NestedData(BaseModel):
    subData: subDict
    subDataList: List[subDict]

@app.post('/post/nested')
async def declare_nested_request_body(data: NestedData):
    return {"text": f"hello, {data.subData}, {data.subDataList}"}

class ValidatatedSubData(BaseModel):
    # 正規表現で先頭にrつけるとエスケープシーケンスは無効
    strings: str = Field(None, min_length=2, max_length=5, regex=r'[a-b]+.')
    integer: int = Field(..., gt=1, le=3) # required

class ValidatedNestedData(BaseModel):
    subData: ValidatatedSubData = Field(..., example={"strings": "aaa",
        "integer":2 })
    subDataList: List[ValidatatedSubData] = Field(...)

@app.post('/validation')
async def validation(data: ValidatedNestedData):
    async def validation(data: ValidatedNestedData):
        return {"text": f"hello, {data.subData}, {data.subDataList}"}

class ItemOut(BaseModel):
    strings: str
    aux: int = 1
    text: str

@app.get('/', response_model=ItemOut)
async def response(strings: str, integer: int):
    return {"text": "hello world", "strings": strings, "integer": integer}

# 辞書に存在しない場合にresponse_modelのattributesのデフォルト値を”入れない”
@app.get('/unset', response_model=ItemOut, response_model_exclude_unset=True)
async def response_exclude_unset(strings: str, integer: int):
    return {"text": "hello world!", "strings": strings, "integer": integer}

# response_modelの"strings", "aux"を無視 -> "text"のみ返す
@app.get('/exclude', response_model=ItemOut, response_model_exclude={"strings",
    "aux"})
async def response_exclude(strings: str, integer: int):
    return {"text": "hello world!", "strings": strings, "integer": integer}

# response_modelの"text"のみ考慮する -> "text"のみ返す
@app.get('/include', response_model=ItemOut, response_model_include={"text"})
async def response_include(text: str, strings: str, integer: int):
    return {"text": text, "strings": strings, "integer": integer}

@app.get('/status', status_code=200) # default status code指定
async def response_status_code(integer: int, response: Response):
    if integer > 5:
        # error handring
        raise HTTPException(status_code=404, detail="this is error message")
    elif integer == 1:
        # set manually
        response.status_code = HTTP_201_CREATED
        return {"text": "hello world, created!"}
    else:
        # defalut status code
        return {"text": "hello world!"}

def time_bomb(count: int):
    sleep(count)
    print(f'bomb!!! {datetime.utcnow()}')

@app.get('/{count}')
async def back(count: int, background_tasks: BackgroundTasks):
    background_tasks.add_task(time_bomb, count)
    return {"text": "finish"}   # time_bombの終了を待たずにレスポンスを返す
