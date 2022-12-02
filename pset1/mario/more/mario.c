#include <stdio.h>
#include <cs50.h>

int main(void)
{
    int height;
    do
    {
        height = get_int("Height: ");
    }
    while (height < 1 || height > 8);

    for (int i = 0; i < height; i++)
    {
        //Prints left pyramid
        for (int j = 0; j < height - i - 1; j++)
        {
            printf(" ");
        }

        for (int k = 0; k < i + 1; k++)
        {
            printf("#");
        }

        //Prints two spaces in centre
        printf("  ");

        //Prints right pyramid
        for (int p = 0; p < i + 1; p++)
        {
            printf("#");
        }

        printf("\n");
    }
}