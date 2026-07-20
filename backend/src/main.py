import ctypes
import re

from typing import Annotated
from fastapi import FastAPI, Query, Request, HTTPException
from fastapi.templating import Jinja2Templates
from .init import init_trie
from contextlib import asynccontextmanager

re.ASCII

async def word_is_valid(word: str):
    return bool(re.match(r'^[-a-zA-Z0-9 /@"()+.,]*$', word))

@asynccontextmanager
async def lifespan(app: FastAPI):
    root, functions = init_trie()
    app.state.root = root
    app.state.functions = functions

    yield

app = FastAPI(lifespan=lifespan)

templates = Jinja2Templates(directory="templates")

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
    return templates.TemplateResponse(request, "home.html", {"words": response})

@app.post("/insert")
async def insert_word(word: Annotated[ str, Query(max_length=100, pattern=r'^[-a-zA-Z0-9 /@"()+.,]*$') ], request: Request):
    insertTrieNode = request.app.state.functions["insertTrieNode"]
    root = request.app.state.root

    if not await word_is_valid(word):
        raise HTTPException(status_code=400, detail=f"'{word}' has unsupported characters")
    c_word = word.encode('utf-8')

    result = insertTrieNode(ctypes.byref(root), c_word)

    if result == 400:
        raise HTTPException(status_code=400, detail=f"'{word}' is empty")
    elif result == 409:
        raise HTTPException(status_code=409, detail=f"'{word}' already exists")
    elif result == 201:
        return {"message": f"successfully inserted '{word}'"}
    

# @app.post("/insert_excel")
# async def insert_excel(filename: str, request: Request)
#     with open(filename, "r") as f:
#         f.read()

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

