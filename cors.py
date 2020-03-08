from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# https://fastapi.tiangolo.com/tutorial/cors/
origins = [
    "http://localhost",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True, # Cookie support
    allow_methods=["*"],    # GET, POST, etc
    allow_headers=["*"],    # Accept, Content, Language, Type
)

@app.get("/")
async def main():
    return {"message": "Hello World"}
