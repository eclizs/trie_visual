#ifndef TRIE_H
#define TRIE_H

#include<stdbool.h>

#define NUM_CHAR 256

typedef struct TrieNode{
	struct TrieNode* children[NUM_CHAR];
	bool terminal;
	char* description;
} TrieNode;

typedef struct Word{
	char* word;
	char* description;
} Word;

TrieNode* createTrieNode();
bool insertTrieNode(TrieNode** root, char* signedText, char* desc);
void printTrieNode(TrieNode* root, char* signedPrefix);
void findWords(TrieNode* root, char* signedPrefix, Word* arrWords);
TrieNode* findPrefixNode(TrieNode *root, char* prefix);
bool deleteWord(TrieNode** root, char* signedText);
void destroyTrieNode(TrieNode** root);

#endif
