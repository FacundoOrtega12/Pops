#include <cs50.h>
#include <stdio.h>

int sum_digits(int i);
void check_validity(int sum, int length, int start_pair);

int main(void)
// MasterCard: 5105105105105100
// American Express: 371449635398431
// VISA: 4012888888881881
{
    // get_long("Card Card Number: ");
    long credit = get_long("Card Card Number: "); // long int number
    int credit_length; //add 1 every loop to get length
    int checksum = 0;
    int start_pair; // used for final check

    for (credit_length = 0; credit > 0; credit_length++)
    {
        int number = credit % 10; // isolates last number

        if (credit_length % 2 != 0) //checks if even
        {
            number = number * 2;
            number = sum_digits(number);
            checksum = checksum + number;
        }
        else
        {
            checksum = checksum + number;
        }

        if (credit < 100 && credit >= 10)
        {
            start_pair = credit;
        }

        credit = credit / 10; // gets rid of last digit, int truncates decimals (DOES NOT ROUND)
    }
    // printf("%i\n%i\n%i\n", checksum, credit_length, start_pair);
    check_validity(checksum, credit_length, start_pair); // checks if valid and prints name of card: VISA, MasterCard, American Express, and "INVALID"
}

int sum_digits(int i)
{
    if (i >= 10)
    {
        int ones = i % 10; // will give remainder (ones position)
        int tens = i / 10; // "int" will truncate decimal leaving the tens position
        int digit_sum = ones + tens;
        return digit_sum;
    }
    else
    {
        return i;
    }
}

void check_validity(int sum, int length, int start_pair)
// starting numbers
{
    int first = start_pair / 10;
    if (sum % 10 == 0)
    {
        // VISA: 4 (l= 13 & 16)
        if (length == 13)
        {
            if (first == 4)
            {
                printf("VISA\n");
            }
            else
            {
                printf("INVALID\n");
            }
        }
        // MC: 51, 52, 53, 54, or 55 (l= 16)
        else if (length == 16)
        {
            if (first == 4)
            {
                printf("VISA\n");
            }
            else if (start_pair == 51 || start_pair == 52 || start_pair == 53 || start_pair == 54 || start_pair == 55)
            {
                printf("MASTERCARD\n");
            }
            else
            {
                printf("INVALID\n");
            }

        }

    // AMEX: 34 or 37 (l= 15)
        else if (length == 15)
        {
                if (start_pair == 34 || start_pair == 37)
            {
                printf("AMEX\n");
            }
            else
            {
                printf("INVALID\n");
            }
        }

        else
        {
            printf("INVALID\n");
        }
    }
    else
    {
        printf("INVALID\n");
    }
}
