from cs50 import get_string

# Get user input
text = get_string("Text: ")
text_length = len(text)

# Initialise counter variables
letter_count = 0
word_count = 1
sentence_count = 0

# Iterate through each letter in text
for letter in text:
    # Count letters
    if letter.isalnum():
        letter_count += 1
    # Count words
    elif letter.isspace():
        word_count += 1
    # Count sentences
    elif letter in ".?!":
        sentence_count += 1

# Calculate avg letters and sentences per 100 words of text
avg_letters = (letter_count / word_count) * 100
avg_sentences = (sentence_count / word_count) * 100

# Calculate readability using Coleman-Liau index
index = round(0.0588 * avg_letters - 0.296 * avg_sentences - 15.8)

# Report readability grade
if index < 1:
    print("Before Grade 1")
elif index >= 16:
    print("Grade 16+")
else:
    print(f"Grade {index}")