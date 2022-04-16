import random
import numpy as np

def bigrandom (n=1000000):
    return random.randrange(2, n)
# Primality tests from Knuth Vol.II 4.5.4
# Algorithm P, etc.
#
# Return false if n is composite, true if n may be prime
#

def modular_pow(base, exponent, modulus):
    if modulus == 1:
        return 0
    #Assert :: (modulus - 1)*(modulus - 1) does not overflow base
    result = 1
    base = base % modulus
    while exponent > 0:
        if (exponent % 2 == 1):
            result = (result * base) % modulus
        exponent = exponent // 2
        base = (base * base) % modulus
    return result


def maybeprime(n):
    if (n & 1) == 0:
        return 0 # n is even.. definitely not prime

    # find q and k, such that n = q*(2**k)+1
    q = n - 1
    k = 0
    while (q & 1) == 0:
        k += 1
        q >>= 1

    x = bigrandom (n) # get a random number for this test

    y = modular_pow(x, q, n)
    if y == 1 or y == n-1:
        return 1 # n may be prime

    for j in range(1, k+1):
        y =  modular_pow(y, 2, n) 
        if y == 1: return 0 # n is definitely not prime
        if y == n-1: return 1 # n may be prime

    return 0 # n is definitely not prime
    # end maybeprime
# Return false if n is composite, true if n is very probably prime.
# The reliablity of the test is increased by increasing t
#
def isprime(n, t=25):
    for j in range(t):
        if not maybeprime(n):
            return 0 # n is known to be composite
    return 1 # n has survived t primality tests, is probably prime
# end isprime
print(isprime(111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111116000808880608061111111111111111111111111111111111111111111111111111111111866880886008008088868888011111111111111111111111111111111111111111111111116838888888801111111188006080011111111111111111111111111111111111111111111110808080811111111111111111111111118860111111111111111111111111111111111111110086688511111111111111111111111116688888108881111111111111111111111111111111868338111111111111111111111111111880806086100808811111111111111111111111111183880811111111111111111100111111888580808086111008881111111111111111111111111888081111111111111111111885811188805860686088111118338011111111111111111111188008111111111111111111111888888538888800806506111111158500111111111111111111883061111111111111111111116580088863600880868583111111118588811111111111111118688111111111001111111111116880850888608086855358611111111100381111111111111160831111111110880111111111118080883885568063880505511111111118088111111111111588811111111110668811111111180806800386888336868380511108011111006811111111111111088600008888688861111111108888088058008068608083888386111111108301111111116088088368860808880860311111885308508868888580808088088681111111118008111111111388068066883685808808331111808088883060606800883665806811111111116800111111581108058668300008500368880158086883888883888033038660608111111111111088811111838110833680088080888568608808808555608388853680880658501111111111111108011118008111186885080806603868808888008000008838085003008868011111111111111186801110881111110686850800888888886883863508088688508088886800111111111111111118881183081111111665080050688886656806600886800600858086008831111111111111111118881186581111111868888655008680368006880363850808888880088811111111111111111110831168881111118880838688806888806880885088808085888808086111111111111111111118831188011111008888800380808588808068083868005888800368806111111111111111111118081185311111111380883883650808658388860008086088088000868866808811111111111118881168511111111111180088888686580088855665668308888880588888508880800888111118001188081111111111111508888083688033588663803303686860808866088856886811111115061180801111111111111006880868608688080668888380580080880880668850088611111110801188301111111111110000608808088360888888308685380808868388008006088111111116851118001111111111188080580686868000800008680805008830088080808868008011111105001116800111111118888803380800830868365880080868666808680088685660038801111180881111808111111100888880808808660883885083083688883808008888888386880005011168511111688811111111188858888088808008608880856000805800838080080886088388801188811111138031111111111111110006500656686688085088088088850860088888530008888811111111106001111111111111111110606880688086888880306088008088806568000808508611111111118000111111111111111111133888000508586680858883868000008801111111111111111111111860311111111111111111108088888588688088036081111860803011111111863311111111111188881111111111111111100881111160386085000611111111888811111108833111111111111118888811111111111111608811111111188680866311111111111811111888861111111111111111688031111111111118808111111111111188860111111111111111118868811111111111111111118850811111111115861111111111111111888111111111111111080861111111111111111111111880881111111108051111111111111111136111111111111188608811111111111111111111111116830581111008011111111111111111118111111111116880601111111111111111111111111111183508811088111111111111111111111111111111088880111111111111111111111111111111111600010301111111111111111111111111111688685811111111111111111111111111111111111111110811801111111111111111111158808806881111111111111111111111111111111111111111181110888886886338888850880683580011111111111111111111111111111111111111111111111111008000856888888600886680111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111))