#include <stdio.h>
#include <cs50.h>
#include <math.h>

int main(void)
{
    // Prompts user for non-negative float
    float dollars;
    do
    {
        dollars = get_float("Change owed: ");
    }
    while (dollars < 0);


    // Convert dollars to cents
    int cents = round(dollars * 100);
    printf("%i\n", cents);

    int counter = 0;

    while (cents > 0)
    {
        counter += (cents / 25);
        cents = (cents % 25);

        counter += (cents / 10);
        cents = (cents % 10);

        counter += (cents / 5);
        cents = (cents % 5);

        counter += (cents / 1);
        cents = (cents % 1);

    }
    printf("%i\n", counter);
}