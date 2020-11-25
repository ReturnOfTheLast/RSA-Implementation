# Inspired by https://www.geeksforgeeks.org/how-to-generate-large-prime-numbers-for-rsa-algorithm/

import os as __os
import random as __rnd

def LoadPrePrimes():
    # Pregenerated primes from file
    f = open("primenums.txt", "r")
    lines = f.readlines()
    f.close()

    global primes
    primes = list()

    for line in lines:
        primes.append(int(line.strip()))

def __Internal__RandomNumber(byteLength):
    return int.from_bytes(__os.urandom(byteLength), byteorder="big")

def __Internal_LowLevelPrime(byteLength):
    global primes
    while True:
        pc = __Internal__RandomNumber(byteLength)

        for divisor in primes:
            if pc % divisor == 0 and divisor**2 <= pc:
                break
            else: return pc

def __Internal__MillerRabinTest(mrc):
    maxDivisionsByTwo = 0
    ec = mrc - 1
    while ec % 2 == 0:
        ec >>= 1
        maxDivisionsByTwo += 1
    
    assert(2 ** maxDivisionsByTwo * ec == mrc - 1)

    def trialComposite(round_tester):
        if pow(round_tester, ec, mrc) == 1:
            return False
        for i in range(maxDivisionsByTwo):
            if pow(round_tester, 2 ** i * ec, mrc) == mrc - 1:
                return False
        return True
    
    numberOfRabinTrials = 20
    for _ in range(numberOfRabinTrials):
        round_tester = __rnd.randint(2, mrc - 1)
        if trialComposite(round_tester):
            return False
    return True

def GeneratePrime(byteLength):
    while True:
        prime_candidate = __Internal_LowLevelPrime(byteLength)
        if not __Internal__MillerRabinTest(prime_candidate):
            continue
        else:
            return prime_candidate