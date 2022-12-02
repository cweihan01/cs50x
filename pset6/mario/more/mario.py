from cs50 import get_int


def main():
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

        # Print pyramids
        print_pyramid(row + 1)
        print("  ", end="")
        print_pyramid(row + 1)

        # Insert new line
        print()


# Prints n hashes in row n
def print_pyramid(n):
    for i in range(n):
        print("#", end="")


if __name__ == "__main__":
    main()