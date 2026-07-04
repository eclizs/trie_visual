from .init import *

root, func_dict = init_trie()

def insert_word(word: str):
    func_dict["insertWord"](root, word.encode("utf-8"))

def search_word(word: str):
    pass

def get_word(word: str):
    pass
