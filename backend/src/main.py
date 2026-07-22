import ctypes
import re

from typing import Annotated
from fastapi import FastAPI, Query, Request, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from .init import init_trie
from contextlib import asynccontextmanager

from pandas import read_csv

re.ASCII

@asynccontextmanager
async def lifespan(app: FastAPI):
    root, functions = init_trie()
    app.state.root = root
    app.state.functions = functions

    yield

app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
async def root():
    return FileResponse("frontend/index.html")

@app.get("/search",)
async def search_word(request: Request, prefix: Annotated[ str | None, Query(max_length=100, pattern=r'^[-a-zA-Z0-9 /@"()+.,]*$') ] = None,):
    findWords = request.app.state.functions["findWords"]
    freeWordList = request.app.state.functions["freeWordList"]
    root = request.app.state.root

    if not prefix:
        prefix = ""

    word_list = findWords(root, prefix.encode('utf-8'))

    response = []
    
    for i in range(word_list.count):
        entry = word_list.entries[i]
        response.append(entry.decode('utf-8'))
        
    freeWordList(word_list)
    return {"words": response}

@app.post("/insert")
async def insert_word(word: Annotated[ str, Query(max_length=100, pattern=r'^[-a-zA-Z0-9 /@"()+.,]*$') ], request: Request):
    insertTrieNode = request.app.state.functions["insertTrieNode"]
    root = request.app.state.root

    c_word = word.encode('utf-8')

    result = insertTrieNode(ctypes.byref(root), c_word)

    if result == 400:
        raise HTTPException(status_code=400, detail=f"'{word}' is empty")
    elif result == 409:
        raise HTTPException(status_code=409, detail=f"'{word}' already exists")
    elif result == 201:
        return {"message": f"successfully inserted '{word}'"}
    

@app.post("/insert_excel", include_in_schema=False)
async def insert_excel(filename: str, request: Request):
    df = read_csv(filename, header=None)

    fields = ['location', 'code', 'name', 'quantity', 'quantifier', 'total']

    df = df.set_axis(fields, axis=1)

    names = list(df['name'])

    names = [name.strip('"') if name.startswith('"') or name.endswith('"') else name
            for name in names]

    for name in names:
        await insert_word(name, request)

    

@app.delete("/delete")
async def delete_word(word: Annotated[ str, Query(max_length=100, pattern=r'^[-a-zA-Z0-9 /@"()+.,]*$') ], request: Request):
    deleteWord = request.app.state.functions["deleteWord"]
    root = request.app.state.root

    c_word = word.encode('utf-8')

    result = deleteWord(ctypes.byref(root), c_word)

    if result == False:
        raise HTTPException(status_code=404, detail=f"'{word}' not found")
    else:
        return {"message": f"successfully deleted '{word}'"}

