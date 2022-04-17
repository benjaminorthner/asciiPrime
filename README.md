# asciiPrime
Converts images into numerical ascii art which is also a prime number. Primality is checked using the Rabin-Miller Strong Pseudoprime Test, as shown in section 4.5.4 algorithm P of Donald E. Knuth's “The Art of Computer Programming”, volume 2



# Installation and Setup
This guide is for the setup of _asciiPrime_ in Ubuntu via WSL.
It is assumed you have 
- Python 3
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
    rm gmp-6.2.1.tar.lz
    cd gmp-6.2.1
```
From here we use the GMP auto installer. Before we do that we must make sure our system is up to date with
```bash
    sudo apt-get update -y
    sudo apt-get upgrade -y
```
In order to create the autoinstaller makefile we must first run the configurator
```bash
    ./configure
```
Depending on your system this may fail, in which case you will have to research yourself why. In my case I had to additionally install _m4_ and then rerun the configurator
```bash
    sudo apt-get install m4
    ./configure
```

Then we can run the GMP installer and additionally run a check using
```bash
    make install
    make check
```
Even if the check fails, the code may still run without issues.

After verifying that the code runs you can delete the gmp-6.2.1 folder using
```bash
    rm -r gmp-6.2.1
```

## Compiling the C code
To compile the C code so that it can be used by the python wrapper function simply use
```bash
    make primify
```
# Theory

## Rabin-Miller Pseudoprime test

## Estimation of calc duration