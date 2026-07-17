#ifndef TRIE_H
#define TRIE_H

#include <stdbool.h>

#define NUM_CHAR 46 // 26 lowercase characters plus 20 special chars and digits

typedef struct TrieNode{
	struct TrieNode* children[NUM_CHAR];
	bool terminal;
	char* original;
} TrieNode;

typedef struct WordList{
	char** entries;
	int count;
} WordList;

int getNumChar();
TrieNode* createTrieNode();
int insertTrieNode(TrieNode** root, char* signedText);
WordList findWords(TrieNode* root, char* signedPrefix);
TrieNode* findPrefixNode(TrieNode* root, char* prefix);
bool deleteWord(TrieNode** root, char* signedText);
void destroyTrieNode(TrieNode** root);
void freeWordList(WordList wordList);

#endif
