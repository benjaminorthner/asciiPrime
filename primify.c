#include <gmp.h>
#include <stdio.h>
#include <assert.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>

// returns the probability that the prime was contained in the previously checked candidates
// the closer to 100%, the more likely it is that it will be found soon
double probabilityOfBeingFound(double primeProbability, int trialCount) {
    return 1 - pow((1 - primeProbability), (double) trialCount);
}

// takes a string of digits, check if they are prime, if not reassigns the digits within the luminoscity groups, repeating the process until a prime is found
char *primify(char *asciiImageString, int width, int height, int borderWidth, char *luminosityGroupsString, double primeProbability, int numberOfPrimeChecks) {

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
    clock_t start = clock();
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

        //print progress
        if (counter % 9 == 0) {
            float progress = 100 * probabilityOfBeingFound(primeProbability, counter);
            int hours = (int)((clock() - start) / (CLOCKS_PER_SEC * 3600));
            int minutes = (int)((clock() - start) / (CLOCKS_PER_SEC * 60)) % 60;
            
            // weird errors when I assigned the seconds to a variable, hence built into printf
            printf("\rProbability of prime having been found by now: [%.0f%%], Prime candidates tested: %d, Time elapsed: %02d:%02d:%02d", progress, counter, hours, minutes, (int)((clock() - start) / CLOCKS_PER_SEC) % 60);
            fflush(stdout);

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

// function that runs prime calc on asciiImageString multiple times, to estmate how long each prime calc takes
double estimateCalcDuration(char *asciiImageString, int numberOfPrimeChecks, int maxNumberOfTrials, int maxDuration) {
    // initialise GMP variables
    mpz_t primeCandidateGMP;
    mpz_init(primeCandidateGMP);

    // convert the primeCandidate string to a GMP number (in base 10), and check if it failed
    int flag = mpz_set_str(primeCandidateGMP, asciiImageString, 10);
    assert(flag == 0);

    // initialise variables
    double totalDuration = 0;
    double duration = 0;
    int trials = 0;

    // run prime calc multiple times, and calculate the average duration
    for (int i = 0; i < maxNumberOfTrials; i++) {
        // start timer
        clock_t start = clock();
        
        // check if the GMP number is prime (returns 2 if prime, 1 if probably prime and 0 if definitely not prime)
        int isPrime = mpz_probab_prime_p(primeCandidateGMP, numberOfPrimeChecks);

        // increse number by 2, to prevent compiler optimisation
        mpz_add_ui(primeCandidateGMP, primeCandidateGMP, 2);

        // stop timer
        clock_t end = clock();

        // calculate duration
        duration = (double)(end - start) / CLOCKS_PER_SEC;
        totalDuration += duration;

        trials++;

        // end if maxDuration is reached
        if (totalDuration > maxDuration) {
            break;
        }
    }

    // free GMP variables
    mpz_clear(primeCandidateGMP);

    // return the average duration
    return totalDuration / trials;
}