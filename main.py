from fastapi import FastAPI, Query, Path, Body
from typing import Optional, List
from pydantic import BaseModel, Field

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Helllo": "World"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q":q}

@app.get('/get/{path}')
async def path_and_query_params(
        path: str,
        query: int,
        default_none: Optional[str] = None):
    return { "text": "hello, {path}, {query} and {default_none}" }

@app.get('/validation/{path}')
async def validation(
        string: str = Query(None, min_length=2, max_length=5,
            regex=r'[a-c]+.'),
        integer: int = Query(..., gt=1, le=3),   # required
        alias_query: str = Query('default', alias='alias-query'),
        path: int = Path(10)):
    return {"string": string, "integer": integer, "alias-query": alias_query,
            "path": path}


class Data(BaseModel):
    """request data用の型ヒントがされたクラス"""
    string: str
    default_name: Optional[int] = None
    lists: List[int]

@app.post('/post')
async def declare_request_body(data: Data):
    return {"text": "hello, {data.string}, {data.default_none}, {data.lists}"}

@app.post('/post/embed')
async def declare_request_body(data: Data = Body(..., embed=True)):
    return {"text": "hello, {data.string}, {data.default_none}, {data.lists}"}

class subDict(BaseModel):
    strings: str
    integer: int

class NestedData(BaseModel):
    subData: subDict
    subDataList: List[subDict]

@app.post('/post/nested')
async def declare_nested_request_body(data: NestedData):
    return {"text": "hello, {data.subData}, {data.subDataList}"}

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
        return {"text": "hello, {data.subData}, {data.subDataList}"}

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
