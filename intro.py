from fastapi import FastAPI

app = FastAPI()

@app.get('/') # methodとendpointの指定
async def hello():
    return { "text": "hello world" }
