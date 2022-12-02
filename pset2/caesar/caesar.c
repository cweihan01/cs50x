#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

int main(int argc, string argv[])
{
    // checks for 2 arguments
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    // checks if key is valid
    for (int i = 0; i < strlen(argv[1]); i++)
    {
        if (!isdigit(argv[1][i]))
        {
            printf("Usage: ./caesar key\n");
            return 1;
        }
    }

    // converts string to integer
    int k = atoi(argv[1]) % 26;

    // prompt use for input
    string plaintext = get_string("plaintext: ");

    printf("ciphertext: ");

    // iterate through each char in plaintext
    for (int i = 0; i < strlen(plaintext); i++)
    {
        // store current char in c
        char c = plaintext[i];

        // if char is not an alphabet, print it as it is
        if (!isalpha(c))
        {
            printf("%c", c);
        }

        // if char is uppercase letter, print encrypted letter
        if (isupper(c))
        {
            printf("%c", (c - 65 + k) % 26 + 65);
        }

        // if char is lowercase letter, print encrypted letter
        if (islower(c))
        {
            printf("%c", (c - 97 + k) % 26 + 97);
        }
    }

    printf("\n");
    return 0;
}