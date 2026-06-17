#ifndef TRIE_H
#define TRIE_H

#include<stdbool.h>

#define NUM_CHAR 256

typedef struct TrieNode{
	struct TrieNode *children[NUM_CHAR];
	bool terminal;
	char *description;
} TrieNode;

TrieNode *createTrieNode();
bool insertTrieNode(TrieNode **root, char *signedText, char *desc);
void printTrieNode(TrieNode *root, char *signedPrefix);
TrieNode *findPrefixNode(TrieNode *root, char *prefix);
bool deleteWord(TrieNode **root, char *signedText);
void destroyTrieNode(TrieNode **root);

#endif
