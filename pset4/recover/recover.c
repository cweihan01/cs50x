#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

int main(int argc, char *argv[])
{
    // Ensure proper usage
    if (argc != 2)
    {
        fprintf(stderr, "Usage: ./recover image\n");
        return 1;
    }

    // Open image file for reading
    FILE *infile = fopen(argv[1], "r");
    if (infile == NULL)
    {
        fprintf(stderr, "Could not open file.\n");
        return 2;
    }

    // Create variables
    unsigned char buffer[512];  // file buffer
    int counter = 0;            // jpeg counter
    char jpegName[8];           // jpeg file name (xyz.jpg\0)
    bool is_open = false;       // whether jpeg file exists
    FILE *outfile = NULL;       // JPEG writing file

    // Read image file while not EOF
    while (fread(buffer, 512, 1, infile) == 1)
    {
        // Check for new jpeg file
        if (buffer[0] == 0xff &&
            buffer[1] == 0xd8 &&
            buffer[2] == 0xff &&
            (buffer[3] & 0xf0) == 0xe0)
        {
            // If a jpeg file exists, close current one
            if (is_open)
            {
                fclose(outfile);
                is_open = false;
            }

            // Create a new jpeg file and open for writing
            sprintf(jpegName, "%.3i.jpg", counter);
            outfile = fopen(jpegName, "w");

            // Update tracker variables
            is_open = true;
            counter++;
        }

        // Write to jpeg file (if it exists)
        if (is_open)
        {
            fwrite(buffer, 512, 1, outfile);
        }
    }

    // Close file when EOF is reached
    fclose(outfile);

    return 0;
}
