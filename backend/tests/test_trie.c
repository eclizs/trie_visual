#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#include "trie.h"

static void expect_true(bool condition, const char *message)
{
    if (!condition)
    {
        fprintf(stderr, "FAIL: %s\n", message);
        exit(EXIT_FAILURE);
    }
}

static void assert_word_list_contains(WordList list, const char *expected_word, const char *expected_desc)
{
    bool found = false;

    expect_true(list.count > 0, "word list should not be empty");

    for (int i = 0; i < list.count; i++)
    {
        if (strcmp(list.entries[i].word, expected_word) == 0 &&
            strcmp(list.entries[i].description, expected_desc) == 0)
        {
            found = true;
            break;
        }
    }

    expect_true(found, "expected word/description pair was not returned");
}

static void test_insert_find_and_delete(void)
{
    TrieNode *root = NULL;
    char word[] = "Hello";
    char desc[] = "greeting";
    char prefix[] = "h";
    char delete_word[] = "Hello";

    int result = insertTrieNode(&root, word, desc);
    expect_true(result == 201, "insert should return 201 for a new word");
    expect_true(root != NULL, "root trie should be initialized");

    TrieNode *node = findPrefixNode(root, word);
    expect_true(node != NULL, "findPrefixNode should resolve the inserted word");
    expect_true(node->terminal, "resolved node should be terminal");

    WordList found = findWords(root, prefix);
    expect_true(found.count == 1, "prefix search should return exactly one match");
    assert_word_list_contains(found, "hello", "greeting");
    freeWordList(found);

    expect_true(deleteWord(&root, delete_word), "deleteWord should remove the inserted word");

    WordList empty = findWords(root, prefix);
    expect_true(empty.count == 0, "deleted word should no longer be returned");
    freeWordList(empty);

    destroyTrieNode(&root);
}

static void test_duplicate_insert_updates_description(void)
{
    TrieNode *root = NULL;
    char first_word[] = "hello";
    char first_desc[] = "first description";
    char second_word[] = "Hello";
    char second_desc[] = "updated description";
    char prefix[] = "hello";

    int first = insertTrieNode(&root, first_word, first_desc);
    int second = insertTrieNode(&root, second_word, second_desc);

    expect_true(first == 201, "first insert should create a new word");
    expect_true(second == 200, "second insert should update the description for an existing word");

    WordList found = findWords(root, prefix);
    expect_true(found.count == 1, "duplicate insert should not create a second entry");
    expect_true(strcmp(found.entries[0].word, "hello") == 0, "word should be normalized to lowercase form");
    expect_true(strcmp(found.entries[0].description, "updated description") == 0, "description should be updated");

    freeWordList(found);
    destroyTrieNode(&root);
}

static void test_invalid_and_empty_inputs(void)
{
    TrieNode *root = NULL;
    char invalid_word[] = "bad:word";
    char valid_desc[] = "desc";
    char empty_word[] = "";
    char empty_desc_word[] = "word";
    char empty_desc[] = "";
    char prefix[] = "";

    int invalid_insert = insertTrieNode(&root, invalid_word, valid_desc);
    expect_true(invalid_insert == 400, "insert should reject unsupported characters");

    int empty_err = insertTrieNode(&root, empty_word, valid_desc);
    expect_true(empty_err == 400, "insert should reject empty words");

    int empty_desc_result = insertTrieNode(&root, empty_desc_word, empty_desc);
    expect_true(empty_desc_result == 400, "insert should reject empty descriptions");

    WordList empty = findWords(root, prefix);
    expect_true(empty.count == 0, "findWords should return no entries for an empty trie");
    freeWordList(empty);

    destroyTrieNode(&root);
}

int main(void)
{
    test_insert_find_and_delete();
    test_duplicate_insert_updates_description();
    test_invalid_and_empty_inputs();

    puts("All trie tests passed.");
    return EXIT_SUCCESS;
}
