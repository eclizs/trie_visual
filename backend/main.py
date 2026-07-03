import ctypes

from fastapi import FastAPI, Request
from pydantic import BaseModel
from backend.src.trie import TrieNode, Entry, init_trie
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    root, functions = init_trie()
    app.state.root = root
    app.state.functions = functions
    functions["insertTrieNode"](ctypes.byref(root), b"hello", b"greetings this is hello")
    functions["insertTrieNode"](ctypes.byref(root), b"world", b"greetings this is world")

    yield

class WordEntry(BaseModel):
    word: str
    description: str

app = FastAPI(lifespan=lifespan)

@app.get("/search")
async def search_word(prefix: str, request: Request):
    findWords = request.app.state.functions["findWords"]
    root = request.app.state.root


    word_list = findWords(root, prefix.encode('utf-8') )

    response = []
    
    for i in range(word_list.count):
        entry = word_list.entries[i]
        response.append(WordEntry(
                word=entry.word.decode('utf-8'),
                description=entry.description.decode('utf-8')
            ))
    
    if response == []:
        return {"message": "No matching words found."}
    return response

@app.get("/words/{word}")
async def get_word(word: str, request: Request):
    findPrefixNode = request.app.state.functions["findPrefixNode"]
    root = request.app.state.root

    node = findPrefixNode(root, word.encode('utf-8'))

    if not node:
        return {"message": "Word not found."}
    return {"word": word, "description": node.description.decode('utf-8')}

@app.post("/insert/")
async def insert_word(entry: WordEntry, request: Request):
    insertTrieNode = request.app.state.functions["insertTrieNode"]
    root = request.app.state.root
    insertTrieNode(ctypes.byref(root), entry.word.encode('utf-8'), entry.description.encode('utf-8'))

