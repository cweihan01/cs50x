from cs50 import get_float

while True:
    change = get_float("Change owed: ")
    if change >= 0:
        break

# Converts dollars to cents
change = round(change * 100)

# Initialise coin counter
coins = 0

while change > 0:
    # Count quarters
    coins += change // 25
    change %= 25

    # Count dimes
    coins += change // 10
    change %= 10

    # Count nickels
    coins += change // 5
    change %= 5

    # Count pennies
    coins += change // 1
    change %= 1

print(coins)