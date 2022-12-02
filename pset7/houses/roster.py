# TODO
from sys import argv, exit
import csv
from cs50 import SQL

# Check for correct number of arguments
if len(argv) != 2:
    print("Incorrect number of arguments.")
    exit(1)

# Store house to be searched
query = argv[1]

# Link database to script
db = SQL("sqlite:///students.db")

# Select required columns from those in particular house, where each item in query_list is a dictionary
query_list = db.execute("SELECT first, middle, last, birth FROM students WHERE house = ? ORDER BY last, first", query)

# Iterate through each person in particular house
for person in query_list:
    # Store data in variables
    first = person['first']
    middle = person['middle']
    last = person['last']
    birth = person['birth']

    # Print required names in appropriate format
    if middle == None:
        print(first, last + ', born', birth)
    else:
        print(first, middle, last + ', born', birth)