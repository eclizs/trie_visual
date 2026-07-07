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
        raise HTTPException(status_code=404, detail=f"{word} not found")
    return WordEntry(
        word=word,
        description= node.contents.description.decode('utf-8')
    )

@app.post("/insert")
async def insert_word(word: str, desc: str, request: Request):
    insertTrieNode = request.app.state.functions["insertTrieNode"]
    findPrefixNode = request.app.state.functions["findPrefixNode"]
    root = request.app.state.root

    if not word.isalpha():
        raise HTTPException(status_code=400, detail=f"\"{word}\" has unsupported characters")
    c_word = word.encode('utf-8')
    c_desc = desc.encode('utf-8')

    node = findPrefixNode(root, c_word)
    wordExists = False
    if node and node.contents.terminal:
        wordExists = True
    result = insertTrieNode(ctypes.byref(root), word.encode('utf-8'), desc.encode('utf-8'))


    if result == False and wordExists == True:
        return {"message": "successfully updated an existing word"}
    elif result == True and wordExists == False:
        return {"message": "successfully inserted a new word"}

