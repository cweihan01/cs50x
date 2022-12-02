#include <stdio.h>
#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <string.h>

int main(void)
{
    // get user's text and stores length of text
    string text = get_string("Text: ");
    int text_length = strlen(text);

    // initialise counter variables
    int letter_count = 0;
    int word_count = 1;
    int sentence_count = 0;

    // iterate through each char in text
    for (int i = 0; i < text_length; i++)
    {
        // save current char as variable
        char c = text[i];

        // count letters
        if (isalpha(c) != 0)
        {
            letter_count++;
        }

        // count words
        if (isspace(c) != 0)
        {
            word_count++;
        }

        // count sentences
        if (c == '.' || c == '?' || c == '!')
        {
            sentence_count++;
        }
    }

    // calculate average letters and sentences per 100 words
    float avg_letters = ((float)letter_count / (float)word_count) * 100;
    float avg_sentences = ((float)sentence_count / (float)word_count) * 100;

    // calculate readability using Coleman-Liau index
    int index = round(0.0588 * avg_letters - 0.296 * avg_sentences - 15.8);

    // report readability grade
    if (index > 16)
    {
        printf("Grade 16+\n");
    }
    else if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %i\n", index);
    }

    /* debugging
    printf("Letter count: %i\n", letter_count);
    printf("Word count: %i\n", word_count);
    printf("Sentence count: %i\n", sentence_count);

    printf("Average letters: %f\n", avg_letters);
    printf("Average sentences: %f\n", avg_sentences);

    printf("Index is %i\n", index);
    */
}
