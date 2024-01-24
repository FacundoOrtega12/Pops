#include <stdio.h>
#include <cs50.h>

void steps(int height);
void spaces(int height);


int main(void)
{
    // height of stairs positive integers only
    int height;
    do
    {
        height = get_int("Height: ");
    }
    while (height < 1);
    // number of blank spaces to left of stairs
    int blank = height - 1;

    for (int i = 0; i < height; i++)
    {
        spaces(blank);
        steps(i + 1);
        printf("  ");
        steps(i + 1);
        printf("\n");
        blank--;
    }
}

void steps(int height)
{
    int i = 0;
    while (i < height)
    {
        printf("#");
        i++;
    }
}

void spaces(int blank)
{
    int i = blank;
    while (i > 0)
    {
        printf(" ");
        i--;
    }
}
