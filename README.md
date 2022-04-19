# asciiPrime
Converts images into numerical ascii art which is also a prime number. Primality is checked using the Rabin-Miller Strong Pseudoprime Test, as shown in section 4.5.4 algorithm P of Donald E. Knuth's “The Art of Computer Programming”, volume 2

# Usage Instructions

# Theory

## Rabin-Miller Pseudoprime test

## Estimation of calculation duration
The prime counting function, which for any positive integer x gives a fairly good estimate of the number of primes below x is given by$$\pi(x) = \frac{x}{\ln(x)}$$

We would like to know the probability is of any particular reconfiguration of our ascii image being prime. If our ascii image has $p$ digits, then we can assume that our possible primes will be in between $x=10^{p+1}$ and $x=10^p$.

So the probability $P$ of any ascii image with $p$ digits being prime is
$$ P(p) = \frac{\pi(10^{p+1}) - \pi(10^p)}{10^{p+1} - 10^p} = \frac{9p - 1}{9p(p+1)\ln(10)}$$
Because our code only ever checks odd numbered ascii images the probability of finding a prime is twice as large and

$$P(p) = \frac{2(9p - 1)}{9p(p+1)\ln(10)}$$

Thus the probability $S$ of finding a prime after $n$ trails is given by
$$ S = 1 - (1 - P(p))^n$$
Which when solved for n gives, the number of trails necessary to find a prime ascii image with $p$ digits with a probability of $S$
$$n(p,S) = \frac{\ln(1-S)}{\ln(1-P(p))}$$

This is then multiplied with the average duration of 1 primality test to give the estimated computation times.
# Installation and Setup
This guide is for the setup of _asciiPrime_ in Ubuntu via WSL.
It is assumed you have 
- Python3, pip3
- The python packages _numpy_ and _pillow_
- gcc (c - compiler)

already installed.

## Downloading source code
Navigate to the directory which should contain _asciiPrime_, then clone the git repository using
```bash
    git clone https://github.com/benjaminorthner/asciiPrime.git
```
This should set up a new folder _asciiPrime_ containing the source code


## Installing GMP Library
In order to achieve reasonable speeds, we will use C to perform the primality checks. Because we are dealing with integers bigger than 64 bits we use the GNU Multiple Precision Arithmetic Library GMP. It just so happens to already contain an implementation of the Rabin-Miller Pseudoprime test, so we can avoid reimplementing this ourselves aswell. This C function is called within a python script using _ctypes_.

In order to install GMP, you must first download it's latest release from the [GMP website](https://www.gmplib.org/#DOWNLOAD). Or alternatively use the following command within a folder of your choosing
```bash
  wget https://gmplib.org/download/gmp/gmp-6.2.1.tar.lz
```
Now unpack the downloaded file and navigate into it using
```bash
  sudo apt-get install lzip
  tar --lzip -xvf gmp-6.2.1.tar.lz
  rm -f gmp-6.2.1.tar.lz
  cd gmp-6.2.1
```
From here we use the GMP auto installer. Before we do that we must make sure our system is up to date with
```bash
  sudo apt-get update -y
  sudo apt-get upgrade -y
```
In order to create the autoinstaller makefile we must first run the configuratorm which itself requires the installation of _m4_
```bash
  sudo apt-get install m4
  ./configure
```

Then we can run the GMP installer and additionally run a check using
```bash
  sudo make install
  sudo make check
```
Even if the check fails, the code may still run without issues.

After verifying that the code runs you can delete the gmp-6.2.1 folder using
```bash
  cd ..
  sudo rm -rf gmp-6.2.1
```

## Compiling the C code
To compile the C code so that it can be used by the python wrapper function simply use
```bash
  make primify
```