import random as __rnd
import math as __math
from decimal import Decimal as __Deci

def GenerateKeyPair(keysize):
    print("Generating p, q and n")
    n, p, q = __Internal_GenerateN(keysize)
    print("n = " + str(n) + " (" + str(n.bit_length()) + " bits)")
    
    print("")
    
    print("Calculating λ(n) = lcm(p - 1, q - 1)")
    tot = __Internal_FindLeastCommonMultiple(p - 1, q - 1)
    print("λ(n) = " + str(tot) + " (" + str(tot.bit_length()) + " bits)")

    print("")

    print("Generating public key")
    e = __Internal_GeneratePublicKey(tot, keysize)
    print("e = " + str(e) + " (" + str(e.bit_length()) + " bits)")

    print("Generating private key")
    d = __Internal_GeneratePrivateKey(e, tot)
    print("d = " + str(d) + " (" + str(d.bit_length()) + " bits)")

def __Internal_GenerateN(keysize):
    
    p = __Internal_GetPrime(keysize)
    print("p = " + str(p) + " (" + str(p.bit_length()) + " bits)" + " " * 8)
    q = __Internal_GetPrime(keysize)
    print("q = " + str(q) + " (" + str(q.bit_length()) + " bits)" + " " * 8)

    return p * q, p, q

def __Internal_GetPrime(keysize):
    num = 0
    failedAttempts = 0
    while True:
        num = __rnd.randint(int(__Deci(2 ** (keysize - 1)).sqrt()), (2 ** (keysize / 2)) - 1)
        print(str(num) + " (" + str(failedAttempts) + " failed attempts)" + " " * 16 + "\r", end="")
        if __Internal_IsPrime(num): break
        else: failedAttempts += 1
    
    return num

def __Internal_IsPrime(num):
    if num < 2: return False
    if num == 2: return True
    if num & 0x01 == 0: return False
    n = int(num ** 0.5)
    for i in range(3, n, 2):
        if num % i == 0:
            return False
    
    return True

def __Internal_FindLeastCommonMultiple(num1, num2):
    lcm = int((num1 * num2) / __math.gcd(num1, num2))
    return lcm
ESOTERIC

        e = __rnd.randint(2 ** (keysize / 2), tot - 1)
        print(str(e) + " " * 8 + "\r", end="")
        if __math.gcd(e, tot) == 1:
            break
    return e

def __Internal_GeneratePrivateKey(e, tot):
    d = __Internal_EGCD(e, tot)[1]
    d = d % tot
    if d < 0:
        d += tot
    return d


# https://www.bloggerdrive.com/understanding-and-implementing-rsa-algorithm-in-python/
def __Internal_EGCD(a,b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = __Internal_EGCD(b % a, a)
        print(str(y) + " " * 8 + "\r", end="")

    return (g, x - (b // a) * y, y)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="RSA keygen")
    parser.add_argument('--bits', '-b', dest='keysize', default=128)
    args = parser.parse_args()
    GenerateKeyPair(int(args.keysize))