import ctypes

libtrie = ctypes.CDLL("/home/jason/projects/trie_visual/libtrie.so")

class TrieNode(ctypes.Structure):
    pass

TrieNode._fields_ = [("children", ctypes.POINTER(TrieNode) * 256),
                ("terminal", ctypes.c_bool),
                ("description", ctypes.c_char_p)]

createTrieNode = libtrie.createTrieNode
createTrieNode.argtypes = []
createTrieNode.restype = ctypes.POINTER(TrieNode)

insertTrieNode = libtrie.insertTrieNode
insertTrieNode.argtypes = [ctypes.POINTER(ctypes.POINTER(TrieNode)),
                           ctypes.c_char_p,
                           ctypes.c_char_p]
insertTrieNode.restype = ctypes.c_bool

printTrieNode = libtrie.printTrieNode
printTrieNode.argtypes = [ctypes.POINTER(TrieNode), ctypes.c_char_p]
printTrieNode.restype = None

findPrefixNode = libtrie.findPrefixNode
findPrefixNode.argtypes = [ctypes.POINTER(TrieNode), ctypes.c_char_p]
findPrefixNode.restype = ctypes.POINTER(TrieNode)

deleteWord = libtrie.deleteWord
deleteWord.argtypes = [ctypes.POINTER(ctypes.POINTER(TrieNode)), ctypes.c_char_p]
deleteWord.restype = ctypes.c_bool

destroyTrieNode = libtrie.destroyTrieNode
destroyTrieNode.argtypes = [ctypes.POINTER(ctypes.POINTER(TrieNode))]
destroyTrieNode.restype = None

root = createTrieNode()

insertTrieNode(ctypes.byref(root), b"hello", b"greetings this is hello")
insertTrieNode(ctypes.byref(root), b"hella", b"greetings this is hella")
insertTrieNode(ctypes.byref(root), b"helli", b"greeting this is helli")
insertTrieNode(ctypes.byref(root), b"hell", b"greeting this is hell")
test = findPrefixNode(root, b"hell")

print(test.contents.terminal)
if test.contents.description:
    printTrieNode(root, b"hell")
    print(test.contents.description.decode("utf-8"))

printTrieNode(root, b"hello")
deleteWord(ctypes.byref(root), b"hello")
printTrieNode(root, b"")
destroyTrieNode(ctypes.byref(root))
printTrieNode(root, b"")

