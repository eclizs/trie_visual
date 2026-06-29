import ctypes
import os
from parser import parse_header

path = os.path.abspath(os.path.dirname(__file__))

libtrie = ctypes.CDLL(os.path.join(path, "libtrie.so"))

class TrieNode(ctypes.Structure):
    pass

TrieNode._fields_ = [("children", ctypes.POINTER(TrieNode) * 256),
                ("terminal", ctypes.c_bool),
                ("description", ctypes.c_char_p)]

class Word(ctypes.Structure):
    _fields_ = [("word", ctypes.c_char_p),
                ("description", ctypes.c_char_p)]
    
def init_function(name, argtypes: list, restype):
    func = getattr(libtrie, name)
    func.argtypes = argtypes
    func.restype = restype
    return func



functions = [
    ("createTrieNode", [], ctypes.POINTER(TrieNode)),
    ("insertTrieNode", [ctypes.POINTER(ctypes.POINTER(TrieNode)), ctypes.c_char_p, ctypes.c_char_p], ctypes.c_bool),
    ("printTrieNode", [ctypes.POINTER(TrieNode), ctypes.c_char_p], None),
    ("findPrefixNode", [ctypes.POINTER(TrieNode), ctypes.c_char_p], ctypes.POINTER(TrieNode)),
    ("deleteWord", [ctypes.POINTER(ctypes.POINTER(TrieNode)), ctypes.c_char_p], ctypes.c_bool),
    ("destroyTrieNode", [ctypes.POINTER(ctypes.POINTER(TrieNode))], None),
    ("findWords", [ctypes.POINTER(TrieNode), ctypes.c_char_p, ctypes.POINTER(Word)], None)
]


for func_name, argtypes, restype in functions:
    globals()[func_name] = init_function(func_name, argtypes, restype)

root = createTrieNode()

insertTrieNode(ctypes.byref(root), b"hello", b"greetings this is hello")
insertTrieNode(ctypes.byref(root), b"hella", b"greetings this is hella")
insertTrieNode(ctypes.byref(root), b"helli", b"greeting this is helli")
# insertTrieNode(ctypes.byref(root), b"hell", b"greeting this is hell")
test = findPrefixNode(root, b"hell")

print(test.contents.terminal)
if test.contents.description:
    printTrieNode(root, b"hell")
    print(test.contents.description.decode("utf-8"))

arrWords = (Word * 10)()
findWords(root, b"", arrWords)

result = arrWords[:5]

for word in result:
    if word.word is None: break
    print(f"{word.word.decode('utf-8')} - {word.description.decode('utf-8')}")

printTrieNode(root, b"hello")
deleteWord(ctypes.byref(root), b"hello")
printTrieNode(root, b"")
destroyTrieNode(ctypes.byref(root))
printTrieNode(root, b"")

