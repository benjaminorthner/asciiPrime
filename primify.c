#include <gmp.h>
#include <stdio.h>
#include <assert.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <unistd.h>


// takes a string of digits, check if they are prime, if not reassigns the digits within the luminoscity groups, repeating the process until a prime is found
char *primify(char *asciiImageString, int width, int height, int borderWidth, char *luminosityGroupsString, int numberOfPrimeChecks) {

    // count the number of occurances of '-' in the luminosity groups string
    int numberOfGroups = 1;
    for (int i = 0; i < strlen(luminosityGroupsString); i++) {
        if (luminosityGroupsString[i] == '-') {
            numberOfGroups++;
        }
    }

    // change luminosity groups string into a 2d array, where each row is separated by a '-'
    char luminosityGroups[numberOfGroups][10];
    int groupIndex = 0;
    int groupLength = 0;
    for (int i = 0; i < strlen(luminosityGroupsString); i++) {
        if (luminosityGroupsString[i] == '-') {
            luminosityGroups[groupIndex][groupLength] = '\0';
            groupIndex++;
            groupLength = 0;
        } else {
            luminosityGroups[groupIndex][groupLength] = luminosityGroupsString[i];
            groupLength++;
        }
    }

    // loop until a prime is found, changing the digits in the image after each failed attempt
    int isPrime = 0;
    int estimatedChecks = strlen(asciiImageString) * log(10);
    int counter = 0;
    while (isPrime == 0) {

        // ---------------- Change the digits in the image ----------------

        // loop over asciiImageString and replace each digit with a random one from the same luminousity group, except the border digits
        for (int index = 0; index < strlen(asciiImageString); index++) {
            int i = index / width;
            int j = index % width;
            if(i < borderWidth || i >= height - borderWidth || j < borderWidth || j >= width - borderWidth) {
                //print current digit
                continue;
            }

            // find out in which element of luminosityGroups the current digit is
            int groupNumber = 0;
            for (int i = 0; i < numberOfGroups; i++) {
                if (strchr(luminosityGroups[i], asciiImageString[index]) != NULL) {
                    groupNumber = i;
                    break;
                }
            }

            // replace current digit with a random one from the same luminosity group
            int randomNumber = rand() % strlen(luminosityGroups[groupNumber]);
            asciiImageString[index] = luminosityGroups[groupNumber][randomNumber];
        }   

        // ---------------- Check if asciiImageString is prime ----------------

        // initialise GMP variables
        mpz_t primeCandidateGMP;
        mpz_init(primeCandidateGMP);

        // convert the primeCandidate string to a GMP number (in base 10), and check if it failed
        int flag = mpz_set_str(primeCandidateGMP, asciiImageString, 10);
        assert(flag == 0);

        // check if the GMP number is prime (returns 2 if prime, 1 if probably prime and 0 if definitely not prime)
        isPrime = mpz_probab_prime_p(primeCandidateGMP, numberOfPrimeChecks);
        counter++;

        //print progressbar
        if (counter % 51 == 0) {
            float progress = (counter * 100) / estimatedChecks;
            printf("\rProgress: [%.0f%%], Prime candidates tested: %d", progress, counter);
            fflush(stdout);

            // print primeCandidateGMP using gmp_printf
            // gmp_printf("%Zd\n", primeCandidateGMP);
        }

        if (isPrime != 0) {
            // free GMP variables
            mpz_clear(primeCandidateGMP);
        }
    }

    printf("\n");
    
    // return the prime image string
    return asciiImageString;
}