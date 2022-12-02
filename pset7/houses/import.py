# TODO
from sys import argv, exit
import csv
from cs50 import SQL

# Check for correct number of arguments
if len(argv) != 2:
    print("Incorrect number of arguments.")
    exit(1)

# Link database to script
db = SQL("sqlite:///students.db")

# Open and read from characters.csv file
with open(argv[1], 'r') as csvfile:
    # Create reader pointer
    reader = csv.DictReader(csvfile)

    # Iterate through csvfile
    for row in reader:
        # Store data of particular row
        # name is a list of words making up each person's full name
        name = row['name'].split()
        house = row['house']
        birth = row['birth']

        # If person has a middle name, insert middle and last names
        if len(name) == 3:
            db.execute("INSERT INTO students (first, middle, last, house, birth) VALUES(?, ?, ?, ?, ?)",
                       name[0], name[1], name[2], house, birth)

        # If person does not have a middle name, leave middle name field empty
        elif len(name) == 2:
            db.execute("INSERT INTO students (first, middle, last, house, birth) VALUES(?, ?, ?, ?, ?)",
                       name[0], None, name[1], house, birth)