import os as __os
import random as __rnd
import json as __json

##
# Dette program generere primtal
# En stordel af dette program er ændret versioner af funktionerne
# beskrevet i https://www.geeksforgeeks.org/how-to-generate-large-prime-numbers-for-rsa-algorithm/
# Undtagen MillerRabinTest der ikke er ændret
##

# Funktion der laver og fylder listen "primes" med de første 50000000 primtal fra https://primes.utm.edu/lists/small/millions/
# Disse hentes fra en json-fil, der skal hentes fra https://lyngbyekolbe.dk/RSA_Implementation/primenums.zip
def LoadPrimes():
    # Lav en global liste "primes"
    global primes
    
    # Læs listen
    with open("primenums.json", "r") as read_file:
        primes = __json.load(read_file)

# Generere tilfældigt tal med en special mængde bytes
def __Internal__RandomNumber(byteLength):
    return int.from_bytes(__os.urandom(byteLength), byteorder="big")

# Generere et lavt niveau primtal
def __Internal_LowLevelPrime(byteLength):
    
    # Hent primtalslisten
    global primes

    # Fortsæt med generere tal indtil at tallet ikke kan deles af et primtal fra "primes"
    while True:
        pc = __Internal__RandomNumber(byteLength)

        for divisor in primes:
            if pc % divisor == 0 and divisor**2 <= pc:
                break
            else: return pc

# Funktionen er taget fra https://www.geeksforgeeks.org/how-to-generate-large-prime-numbers-for-rsa-algorithm/
# Jeg er ikke fuldt ud klar over hvordan denne implementation virker,
# men den har ikke fejlet i at lave et primtal.
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

# Primær funktion til at generere primtal
def GeneratePrime(byteLength):
    while True:
        prime_candidate = __Internal_LowLevelPrime(byteLength)
        if not __Internal__MillerRabinTest(prime_candidate):
            continue
        else:
            return prime_candidate