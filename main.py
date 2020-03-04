from fastapi import FastAPI, Query, Path
from typing import Optional

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
