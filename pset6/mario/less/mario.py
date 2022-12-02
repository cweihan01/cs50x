from cs50 import get_int

# Gets a number between 1 and 8
while True:
    height = get_int("Height: ")
    if height > 0 and height < 9:
        break

# Iterate through each row
for row in range(height):
    # Print spaces at front
    for i in range(height - row - 1):
        print(" ", end="")
    # Print hashes at back
    for j in range(row + 1):
        print("#", end="")
    # Insert new line
    print()