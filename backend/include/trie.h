#ifndef TRIE_H
#define TRIE_H

#include <stdbool.h>

#define NUM_CHAR 46 // 26 lowercase characters plus 20 special chars and digits

typedef struct TrieNode{
	struct TrieNode* children[NUM_CHAR];
	bool terminal;
	char* description;
	bool isCapitalized;
} TrieNode;

typedef struct Entry{
	char* word;
	char* description;
} Entry;

typedef struct WordList{
	Entry* entries;
	int count;
} WordList;

int getNumChar();
TrieNode* createTrieNode(bool isCapitalized);
int insertTrieNode(TrieNode** root, char* signedText, char* desc);
void printTrieNode(TrieNode* root, char* signedPrefix);
WordList findWords(TrieNode* root, char* signedPrefix);
TrieNode* findPrefixNode(TrieNode* root, char* prefix);
bool deleteWord(TrieNode** root, char* signedText);
void destroyTrieNode(TrieNode** root);
void freeWordList(WordList wordList);

#endif
