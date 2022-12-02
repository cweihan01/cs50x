from sys import argv, exit
import csv

# Check for correct command line arguments
if len(argv) != 3:
    exit("Usage: python dna.py data.csv sequence.txt")

# Open sequence file and stores string in [sequence]
with open(argv[2], "r") as sequencefile:
    sequence = sequencefile.read()
    seq_len = len(sequence)

# Open csv (database) file
with open(argv[1], "r") as csvfile:
    # Create a reader object
    reader = csv.reader(csvfile)

    # Stores the list of DNA STRs in [dna_list]
    dna_list = next(reader)
    dna_list.pop(0)
    dna_count = len(dna_list)

    # Create a list of lists containing each person's DNA sequences
    database = []
    for row in reader:
        database.append(row)

# print(dna_list)
# print(database)

# Create a dictionary to store max number of DNA repetitions in given sequence
seq_dict = {}

# Iterate through each DNA in given sequence and store results in [seq_dict]
for i in range(dna_count):
    # Variables for current DNA
    dna = dna_list[i]
    l = len(dna)

    # Counter variables
    max_counter = 0
    counter = 0

    # Iterate through sequence
    for j in range(seq_len):
        # Prevent repeated counting
        while counter > 0:
            counter -= 1
            continue

        # Only count if sequence matches current DNA and is repeated
        if sequence[j:j+l] == dna:
            while sequence[j-l:j] == sequence[j:j+l]:
                counter += 1
                j += l

            # Update max counter (most number of repetitions)
            if counter > max_counter:
                max_counter = counter

    # Save results in [seq_dict]
    seq_dict[dna] = max_counter + 1

# print(seq_dict)

# Search through database for given DNA sequence
for person in database:
    # [person] refers to a list containing each person's name and number of each DNA
    # print(person)

    # Variables
    match = 0
    found = False

    # Check if number of each DNA is the same
    for i in range(dna_count):
        dna = dna_list[i]
        if int(person[i+1]) == seq_dict[dna]:
            match += 1

    # If all DNA matches, we have found the person and can break
    if match == dna_count:
        found = True
        print(person[0])
        break

# No one in database matches given DNA sequence
if not found:
    print("No match")