#include <gmp.h>
#include <stdio.h>
#include <assert.h>

int main(){

    char inputStr[32768] = "11231231231123123123112312312311231231231123123123112312312311231231231123123123112312312311231231231123123123112312312311231231231123123123112312312311231231231123123123112312312311231231231123123123112312312311231231231123123123112312312311231231231123123123112312312311231231231123123123112312312311231231231123123123112312312311231231231123123123112312312311231231231123123123112312312311231231231123123123112312312311231231231123123123112312312311231";

    /* 1. Initialize the number */
    mpz_t n;
    mpz_init(n);
    mpz_set_ui(n,0);

    /* 2. Parse the input string as a base 10 number */
    int flag = mpz_set_str(n,inputStr, 10);
    assert (flag == 0); /* If flag is not 0 then the operation failed */

    /* 
    printf ("n = ");
    mpz_out_str(stdout,10,n);
    printf ("\n");


    mpz_add_ui(n,n,2); 


    printf (" n +1 = ");
    mpz_out_str(stdout,10,n);
    printf ("\n");



    mpz_mul(n,n,n); 


    printf (" (n +1)^2 = ");
    mpz_out_str(stdout,10,n);
    printf ("\n");
    */
    int count = 0;

    for(int i = 0; i < 10000; i++)
    {
        int prime = mpz_probab_prime_p(n, 25);

        if(prime == 1 || prime == 2){
           count++ ;
        } 

        mpz_add_ui(n, n, 2);
    }

    printf("primes: %i", count);

    /* 6. Clean up the mpz_t handles or else we will leak memory */
    mpz_clear(n);

    return 0;
    }