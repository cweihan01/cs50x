// Implements a dictionary's functionality

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include <ctype.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 10000;

// Hash table
node *table[N];

// Size of dictionary
int SIZE = 0;


// Hashes word to a number
// djb2 hash function, obtained from http://www.cse.yorku.ca/~oz/hash.html
unsigned int hash(const char *word)
{
    unsigned long hash = 5381;

    for (int i = 0; i < strlen(word); i++)
    {
        hash = ((hash << 5) + hash) + word[i]; // hash * 33 + c
    }

    return hash % N;
}


// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // Initialise all buckets in hashtable
    for (int i = 0; i < N; i++)
    {
        table[i] = NULL;
    }

    // Open dictionary file
    FILE *dict = fopen(dictionary, "r");
    if (dict == NULL)
    {
        return false;
    }

    // Buffer array to read each word in dictionary to
    char word[LENGTH + 1];

    // Copy each word in dictionary to buffer
    while (fscanf(dict, "%s", word) != EOF)
    {
        // Create a new node
        node *tmp = malloc(sizeof(node));
        if (tmp == NULL)
        {
            free(tmp);
            return false;
        }

        // Initialise values for new node
        strcpy(tmp->word, word);
        tmp->next = NULL;

        // Hash word to obtain its respective bucket in hashtable
        unsigned int index = hash(word);

        // If no list in bucket, create new list
        if (table[index] == NULL)
        {
            table[index] = tmp;
        }

        // There must be a list in table, so we add to it
        else
        {
            tmp->next = table[index];
            table[index] = tmp;
        }

        SIZE++;
    }

    fclose(dict);
    return true;
}


// Returns true if word is in dictionary else false
bool check(const char *word)
{
    // Converts word to lowercase to check against dictionary
    int len = strlen(word);
    char copy[len + 1];
    for (int i = 0; i < len; i++)
    {
        copy[i] = tolower(word[i]);
    }
    copy[len] = '\0';

    // Hash word and find appropriate bucket in table
    unsigned int index = hash(copy);
    node *tmp = table[index];

    // Traverse through linked list in bucket and compare words
    while (tmp != NULL)
    {
        // Word found in dictionary
        if (strcasecmp(tmp->word, copy) == 0)
        {
            return true;
        }

        tmp = tmp->next;
    }

    // Word not found in dictionary
    return false;
}


// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    return SIZE;
}


// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    // For each bucket in hashtable
    for (int i = 0; i < N; i++)
    {
        node *head = table[i];

        // Free each item in list, starting from head
        while (head != NULL)
        {
            node *tmp = head;
            head = tmp->next;
            free(tmp);
        }
    }

    return true;
}