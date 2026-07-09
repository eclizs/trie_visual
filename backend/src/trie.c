#include<stdio.h>
#include<stdlib.h>
#include<stdbool.h>
#include<string.h>
#include<ctype.h>
#include<regex.h>
#include "trie.h"

#define MAX_WORD_COUNT 1000
#define MAX_WORD_LENGTH 100

#define INDEXES \
		INDEX("WHITE_SPACE") \
		INDEX("FRONT_SLASH") \
		INDEX("AT_SIGN") \
		INDEX("DOUBLE_QUOTES") \
		INDEX("COMMA") \
		INDEX("")

#define WHITE_SPACE_ASCII 32

typedef enum {
	WHITE_SPACE_IDX = 52,

};

bool wordIsValid(char* text)
{
	regex_t regex;

	const char* pattern = "^[a-zA-Z0-9\s/@\"-()]*$";

	regcomp(&regex, pattern, REG_EXTENDED);

	if(regexec(&regex, text, 0, NULL, 0) == 0)
	{
		regfree(&regex);
		return true;
	}
	else
	{
		regfree(&regex);
		return false;

	}
}

static int getIdx(char letter)
{
	if(isspace(letter)) return WHITE_SPACE_IDX;
	return (isupper(letter)) ? (letter - 'A') : (letter - 'a' + 26);
}

static char setChar(int idx)
{
	if(idx == WHITE_SPACE_IDX) return WHITE_SPACE_ASCII;
	return ((idx + 'A') > 90) ? (idx + 'A' + 6) : (idx + 'A');
}

TrieNode *createTrieNode()
{
	TrieNode *newNode = (TrieNode*)calloc(1,sizeof(TrieNode));

	if(newNode == NULL)
	{
		printf("Memory allocation failed! Program will be terminated.\n");
		exit(EXIT_FAILURE);
	}
	
	return newNode;
}

bool insertTrieNode(TrieNode **root, char *signedText, char *desc)
{
	if(strlen(signedText) == 0 || strlen(desc) == 0) return false;
	if(*root == NULL) *root = createTrieNode();
	
	unsigned char *text = (unsigned char*)signedText;
	
	TrieNode *temp = *root;
	int length = strlen(signedText);
	
	for(int i = 0 ; i < length; i++)
	{
		int index = getIdx(text[i]);
		if(temp->children[index] == NULL)
			temp->children[index] = createTrieNode();
			
		temp = temp->children[index];
	}
	
	if(temp->terminal == true)
	{
		free(temp->description);
		temp->description = strdup(desc);
		return false;
	}
	else
	{
		temp->terminal = true;
		temp->description = strdup(desc);
	}
	
	return temp->terminal;
}

static void printTrieNode_rec(TrieNode *node, unsigned char *buffer, int length, int *number)
{
	if(node == NULL) return;
	
	if(node->terminal)
	{
		printf("%d. %s\n", *number, buffer);
		*number += 1;
	}
	
	for(int i = 0; i < NUM_CHAR; i++)
	{
		if(node->children[i] != NULL)
		{
			// printf("DEBUG: i=%d, buffer=%s\n", i, buffer);
			buffer[length] = setChar(i);
			buffer[length+1] = '\0';
			printTrieNode_rec(node->children[i], buffer, length+1, number);
		}
	}
}

void printTrieNode(TrieNode *root, char *signedPrefix) //wrapper function
{
	if(root == NULL)
	{
		printf("There is no slang word in the dictionary.\n");
		return;
	}

	unsigned char buffer[MAX_WORD_LENGTH];

	TrieNode *node = NULL;
	int length;
	if(strlen(signedPrefix) > 0)
	{
		TrieNode *prefixNode = findPrefixNode(root, signedPrefix);
		unsigned char *prefix = (unsigned char*)signedPrefix;
		
		if(prefixNode == NULL) return;
		
		length = strlen(signedPrefix);
		memcpy(buffer, prefix, length);
		buffer[length] = '\0';

		node = prefixNode;
	}
	else 
	{
		buffer[0] = '\0';
		node = root;
		length = 0;
	}
	// printf("DEBUG:%s\n", buffer);

	int number = 1;
	printTrieNode_rec(node, buffer, length, &number);
}

static void findWords_rec(TrieNode *node, unsigned char *buffer, int length, Entry* entries, int *counter)
{
	if(node == NULL) return;
	if(*counter >= MAX_WORD_COUNT) return; // Prevent overflow of entries array
	
	if(node->terminal)
	{
		entries[*counter].word = strdup(buffer);
		entries[*counter].description = strdup(node->description);
		*counter += 1;
	}
	
	for(int i = 0; i < NUM_CHAR; i++)
	{
		if(node->children[i] != NULL)
		{
			// printf("DEBUG: i=%d, buffer=%s\n", i, buffer);
			buffer[length] = setChar(i);
			buffer[length+1] = '\0';
			findWords_rec(node->children[i], buffer, length+1, entries, counter);
		}
	}
}

WordList findWords(TrieNode *root, char *signedPrefix) //wrapper function
{
	if(root == NULL)
	{
		printf("There is no slang word in the dictionary.\n");
		return (WordList){NULL, 0};
	}

	unsigned char buffer[MAX_WORD_LENGTH];

	TrieNode *node = NULL;
	int length;
	if(strlen(signedPrefix) > 0)
	{
		TrieNode *prefixNode = findPrefixNode(root, signedPrefix);
		unsigned char *prefix = (unsigned char*)signedPrefix;
		
		if(prefixNode == NULL) return (WordList){NULL, 0};
		
		length = strlen(signedPrefix);
		memcpy(buffer, prefix, length);
		buffer[length] = '\0';

		node = prefixNode;
	}
	else 
	{
		buffer[0] = '\0';
		node = root;
		length = 0;
	}
	// printf("DEBUG:%s\n", buffer);

	int counter = 0;

	Entry* entries = (Entry*)calloc(MAX_WORD_COUNT, sizeof(Entry));
	findWords_rec(node, buffer, length, entries, &counter);
	return (WordList)
	{
		.entries = entries,
		.count = counter
	};
}

TrieNode* findPrefixNode(TrieNode *root, char *signedPrefix)
{
	TrieNode *temp = root;
	int length = strlen(signedPrefix);
	unsigned char *prefix = (unsigned char*)signedPrefix;
	
	for(int i = 0; i < length; i++)
	{
		if(temp == NULL || !isalpha(prefix[i])) return NULL;
		
		int index = getIdx(prefix[i]);
		temp = temp->children[index];
	}
	
	return temp;
}

bool nodeHasChildren(TrieNode *node)
{
	if(node == NULL) return false;

	for(int i = 0; i < NUM_CHAR; i++)
	{
		if(node->children[i] != NULL) return true;
	}
	return false;
}

static TrieNode* deleteWord_rec(TrieNode *node, unsigned char *text, bool *deleted)
{
	if(node == NULL) return node;

	if(*text == '\0')
	{
		if(node->terminal)
		{
			node->terminal = false;
			free(node->description);
			*deleted = true;

			if(!nodeHasChildren(node))
			{
				free(node);
				node = NULL;
			}
		}
		return node;
	}

	node->children[text[0] - 'A'] = deleteWord_rec(node->children[text[0] - 'A'], text + 1, deleted);

	if(*deleted && !nodeHasChildren(node) && !node->terminal)
	{
		free(node);
		node = NULL;
	}
	return node;
}

bool deleteWord(TrieNode **root, char *signedText)
{
	if(*root == NULL || strlen(signedText) == 0) return false;
	unsigned char *text = (unsigned char*)signedText;
	bool result = false;

	*root = deleteWord_rec(*root, text, &result);
	return result;
}

void destroyTrieNode(TrieNode **root)
{
	if(*root == NULL) return;

	for(int i = 0; i < NUM_CHAR; i++)
	{
		if((*root)->children[i] != NULL)
			destroyTrieNode(&(*root)->children[i]);
	}

	if((*root)->description) free((*root)->description);
	free(*root);
	*root = NULL;
}

void freeWordList(WordList wordList)
{
	if(!wordList.entries) return;

	for(int i = 0; i < wordList.count; i++)
	{
		free(wordList.entries[i].word);
		free(wordList.entries[i].description);
	}
	free(wordList.entries);
}

// int main()
// {
// 	TrieNode *root = NULL;
// 	insertTrieNode(&root, "hello", "greeting");
// 	printTrieNode(root, "");
// 	printf("\n");

// 	TrieNode *test = findPrefixNode(root, "hello");

// 	Entry arrWords[10];
// 	findWords(root, "", arrWords);

// 	for (size_t i = 0; i < 3; i++)
// 	{
// 		printf("%s - %s\n", arrWords[i].word, arrWords[i].description);
// 	}
	
// 	printf("%d\n", test->terminal);
// 	if(test != NULL) printf("test is not null\n");
// 	if(test->terminal) printf("Found prefix node: %s\n", test->description);
// }