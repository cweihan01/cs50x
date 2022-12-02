#include "helpers.h"
#include <math.h>
#include <stdio.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    int gray;

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            gray = round((image[i][j].rgbtRed + image[i][j].rgbtGreen + image[i][j].rgbtBlue) / 3.00);

            // Set new values to avg
            image[i][j].rgbtRed = gray;
            image[i][j].rgbtGreen = gray;
            image[i][j].rgbtBlue = gray;
        }
    }
    return;
}

// Sets maximum RGB value to 255 if it exceeds
int rgblimit(int rgbvalue)
{
    if (rgbvalue > 255)
    {
        rgbvalue = 255;
    }

    return rgbvalue;
}


// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    // Create variables
    int sepiaRed, sepiaGreen, sepiaBlue;

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Calculate new pixel values using formula
            sepiaRed = rgblimit(round(0.393 * image[i][j].rgbtRed + 0.769 * image[i][j].rgbtGreen + 0.189 * image[i][j].rgbtBlue));
            sepiaGreen = rgblimit(round(0.349 * image[i][j].rgbtRed + 0.686 * image[i][j].rgbtGreen + 0.168 * image[i][j].rgbtBlue));
            sepiaBlue = rgblimit(round(0.272 * image[i][j].rgbtRed + 0.534 * image[i][j].rgbtGreen + 0.131 * image[i][j].rgbtBlue));

            // Replace each pixel with new values
            image[i][j].rgbtRed = sepiaRed;
            image[i][j].rgbtGreen = sepiaGreen;
            image[i][j].rgbtBlue = sepiaBlue;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    // Temp buffer array
    RGBTRIPLE buffer[width];

    for (int i = 0; i < height; i++)
    {
        // Copy each row into buffer array, backwards
        for (int j = 0; j < width; j++)
        {
            buffer[width - j - 1] = image[i][j];
        }

        // Replace initial image with reversed row
        for (int k = 0; k < width; k++)
        {
            image[i][k] = buffer[k];
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // Create variables
    int sumRed, sumGreen, sumBlue, counter;
    RGBTRIPLE copy[height][width];

    // Create a copy of original image to calculate values
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            copy[i][j] = image[i][j];
        }
    }

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            sumRed = sumGreen = sumBlue = counter = 0;

            // Iterate through neighbouring rows and columns
            for (int r = -1; r <= 1; r++)
            {
                for (int c = -1; c <= 1; c++)
                {
                    // Skips over current iteration if there are no neighbouring pixels
                    if (i + r < 0 || j + c < 0 || i + r >= height || j + c >= width)
                    {
                        continue;
                    }

                    // Calculates total RGB values of neighbouring pixels
                    sumRed += copy[i + r][j + c].rgbtRed;
                    sumGreen += copy[i + r][j + c].rgbtGreen;
                    sumBlue += copy[i + r][j + c].rgbtBlue;
                    counter++;
                }
            }

            // Replace original image with new values
            image[i][j].rgbtRed = round(sumRed / (float) counter);
            image[i][j].rgbtGreen = round(sumGreen / (float) counter);
            image[i][j].rgbtBlue = round(sumBlue / (float) counter);
        }
    }
    return;
}
