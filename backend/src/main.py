import ctypes

from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from .init import init_trie
from contextlib import asynccontextmanager

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
async def search_word(prefix: str, request: Request):
    findWords = request.app.state.functions["findWords"]
    freeWordList = request.app.state.functions["freeWordList"]
    root = request.app.state.root


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

@app.get("/words/{word}")
async def get_word(word: str, request: Request):
    findPrefixNode = request.app.state.functions["findPrefixNode"]
    root = request.app.state.root

    node = findPrefixNode(root, word.encode('utf-8'))

    if not node or not node.contents.terminal:
        raise HTTPException(status_code=404, detail="Word not found")
    return {"word": word, "description": node.contents.description.decode('utf-8')}

@app.post("/insert")
async def insert_word(word: str, desc: str, request: Request):
    insertTrieNode = request.app.state.functions["insertTrieNode"]
    root = request.app.state.root
    insertTrieNode(ctypes.byref(root), word.encode('utf-8'), desc.encode('utf-8'))

