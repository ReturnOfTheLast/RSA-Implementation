# Crack RSA keys
import keygen
import encrypt
import primegenerator

import string
import random
import json

triedPrimes = list()

# Custom primegenerator
def GeneratePrime(byteLength):
    while True:
        prime_candidate = primegenerator.__Internal_LowLevelPrime(byteLength)
        if prime_candidate in triedPrimes:
            return 0

        if not primegenerator.__Internal__MillerRabinTest(prime_candidate):
            continue
        else:
            return prime_candidate

# Primeloader
def LoadPrimes():
    # Pregenerated primes from file
    global primes
    
    with open("primenums.json", "r") as read_file:
        primes = json.load(read_file)

# LowLevelPrimeChecker
def LowLevelCheck(pc):
    global primes

    for divisor in primes:
        if pc % divisor == 0 and divisor**2 <= pc:
            break
        else: return True

    return False

def CheckKey(e, n, d, reps):
    for i in range(reps):
        plaindata = random.randbytes(8)
        
        print("Keycheck try " + str(i) + " ... ", end="")
        
        encrypteddata = encrypt.Crypt(plaindata, e, n)

        if encrypt.Crypt(encrypteddata, d, n) != plaindata:
            print("Failed")
            return False
        
        print("Succeed")
        return True

def GenPossibleKey(n, keysize):
    p = 0
    q = 0
    while p * q != n:
        try:
            p = GeneratePrime(int((keysize / 2) / 8))
        except:
            p = 0
        
        if p != 0:
            q = int(round(n / p))
            print("Trying " + str(p) + " and " + str(q))
            triedPrimes.append(p)
    
    return p, q

LoadPrimes()
primegenerator.LoadPrimes()