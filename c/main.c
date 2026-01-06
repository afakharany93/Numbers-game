#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#define DIGITS 5
#define PRINT 0    //if 1 it will print the generated number in the first of the game

int random_between(int min, int max);   //function to produce random numbers
void printa(int arr[], int size);   //function to print array
void entery(int arr[], int size);   //function to take entery from user
void score_cal(int try);     //function to calculate score

int main()
{
    //deceleration
    int i, j, b, a, value, order, try = 0, score ;
    int num[DIGITS], dummy[DIGITS], pred[DIGITS];       /*num is array holding the true number,
                                                        dummy is a dummy array for operations,
                                                        pred is the array where the user's predictions are saved
                                                        */
    char c, r;  //r is used for replay
    time_t t;

    //opening text
     printf(" Number Discovery Game\n*****************\nThis game is made by : Ahmed Essam El Fakharany\n afakharany93@gmail.com \n*****************\nThe Rules:\n ");
 printf("The computer will generate a random 5 digit number.\n");
     printf("Your mission is to guess the number in the least amount of tries.\n");
     printf("Each try you'll input a 5 digit number as a guess the computer will compare \n");
     printf("your guess to the number and it will give you an answer in the form of \n");
     printf("(Number1/Number2).\n");
     printf("The First number denotes The amount of numbers from your guess \n");
     printf("that actually exist in the random generated number.\n");
     printf("The Second Number Denotes the amount of numbers that not only exist in the \n");
     printf("randomly generated number but also have the correct position in the 5 digit \n");
     printf("number.\n");
    printf(" Example:\n");
     printf("The Computer Generates a random number : 28461\n");
     printf("your initial guess is 2 6 7 9 8\n");
     printf("The computer will Reply 3/1 The 3 Denotes that 2 6 and 7 were part of the guess\n");
     printf("The 1 Denotes that the 2 was not only in the guess but also in the correct \n");
    printf(" position.\n");
     printf("Rules The Computer are limited by In generating the random number.\n");
     printf("1- The number may never start with a 0.\n");
     printf("2- A single number may never repeat in the random number.\n");
     printf("The Following are examples of numbers that will never be generated.\n");
     printf("Ex1: 02314 Can't start with a 0.\n");
     printf("Ex2: 22314 Can't generate same number twice.\n");
     printf("Method of input:\n");
     printf("If you are guessing 12345 you will type 12345 and then you will press enter.\n");
     printf("If you enter three zeros 000, the number will be revealed and you loose.\n");

      printf("Press Enter to start\n ");
      printf("*******************************************************************************");

    //number generation
    fflush(stdin);
    scanf("%c", &c);
    do{
            try = 0;
    srand((unsigned) time(&t));

    num[0] = random_between(1, 9);

    for( i = 1; i < DIGITS; i++)
    {

     num[i] = random_between(0, 9);


    }

    for(b = 0; b < DIGITS; b++)                 /*nested loops to gurantee that an integer isn't used more than one time within the array*/
    {
    for( a = 0; a < DIGITS; a++)
    {
        dummy[a] = num[a];

    }
    for( i = 0; i < DIGITS; i++)
    {
        for( j = 0; j < DIGITS; j++)
        {
         if(i == j)
         {
             continue;
         }
         if(dummy[j] == num[i])
         {
             num[i] = random_between(1, 9);
         }
        }
    }
    }
#if PRINT == 1
    printa(num, DIGITS);
    #endif // PRINT

    //user entery and processing and output


    do{
            value = 0;
    order = 0;
    printf("%d) ", (try+1));
    entery(pred, DIGITS);
    if((pred[0] == 0) && (pred[1] == 0) && (pred[2] == 0)) //if the user enters three zeros the number will be revealed and the user losses
    {
        printf("\nthe number is ");
        printa(num, DIGITS);
        printf("you lose :( \n");
        value = DIGITS;
        order = DIGITS;
    }
    else
        {
    for(i = 0; i < DIGITS; i++)
    {
        for(j = 0; j < DIGITS; j++)
        {
        if(pred[j] == num[i])
        {
            value++;
        if(i == j)
        {
            order++;
        }
        }
        }
    }
    printf("The Output %d / %d \n\n", value, order);
    try++;
    if((value == DIGITS) && (order == DIGITS))
    {
     printf(" you win :) \n");
    printf(" number of tries = %d \n", try);
    score_cal(try);
    }
        }
    }
    while((value != DIGITS) || (order != DIGITS));

    printf("Do you want to replay ? (y/n)\n ");
    fflush(stdin);
    scanf("%c", &r);
    printf("*******************************************************************************\n");

    }
    while((r == 'Y') || (r == 'y'));


    return 0;
}


//function to produce random numbers
int random_between(int min, int max)
 {

    return rand() % (max - min + 1) + min;
}

//function to print array
void printa(int arr[], int size)
{
    int i;
    for(i = 0; i < size; i++)
    {
        printf("%d ", arr[i]);
    }
    printf("\n");
}


//function to take entery from user
void entery(int arr[], int size)
{
    int i, input;
    printf("enter your guess \n");

    fflush(stdin);
    scanf("%d", &input);
    for(i = (size - 1); i >= 0; i--)
    {
        arr[i] = input % 10;
        input = input / 10;
    }
    printf("your guess is \t");
    printa(arr, DIGITS);

}


//function to calculate score
void score_cal(int try)
{

    int  score, m = (-100/99);

        score = (m*try)-m+100;

    printf("your score = %d / 100 \n", score);


}
