import ctypes
import re

from typing import Annotated
from fastapi import FastAPI, Query, Request, HTTPException
from pydantic import BaseModel
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

class WordEntry(BaseModel):
    word: str
    description: str

app = FastAPI(lifespan=lifespan)

@app.get("/search")
async def search_word(request: Request, prefix: Annotated[ str | None, Query(max_length=10, pattern=r'^[-a-zA-Z0-9 /@"()+.,]*$')] = None,):
    findWords = request.app.state.functions["findWords"]
    freeWordList = request.app.state.functions["freeWordList"]
    root = request.app.state.root

    if(not prefix):
        prefix = ""

    word_list = findWords(root, prefix.encode('utf-8'))

    response = []
    
    for i in range(word_list.count):
        entry = word_list.entries[i]
        response.append(WordEntry(
                word=entry.word.decode('utf-8'),
                description=entry.description.decode('utf-8')
            ))
        
    freeWordList(word_list)
    return response

@app.get("/words")
async def get_word(word: str, request: Request):
    findPrefixNode = request.app.state.functions["findPrefixNode"]
    root = request.app.state.root

    node = findPrefixNode(root, word.encode('utf-8'))  

    if not node or not node.contents.terminal:
        raise HTTPException(status_code=404, detail=f"{word} not found")

    return WordEntry(
        word=word,
        description= node.contents.description.decode('utf-8')
    )

@app.post("/insert")
async def insert_word(word: str, desc: str, request: Request):
    insertTrieNode = request.app.state.functions["insertTrieNode"]
    root = request.app.state.root

    if not await word_is_valid(word):
        raise HTTPException(status_code=400, detail=f"'{word}' has unsupported characters")
    c_word = word.encode('utf-8')
    c_desc = desc.encode('utf-8')

    result = insertTrieNode(ctypes.byref(root), c_word, c_desc)


    if result == False:
        return {"message": "successfully updated an existing word"}
    else:
        return {"message": "successfully inserted a new word"}

