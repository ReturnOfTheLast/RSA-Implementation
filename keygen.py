import random as __rnd
import math as __math
import primegenerator as __pg

def GenerateKeyPair(keysize):
    print("Generating p, q and n")
    n, p, q = __Internal_GenerateN(keysize)
    print("p = " + str(p) + " (" + str(p.bit_length()) + " bits)")
    print("q = " + str(q) + " (" + str(q.bit_length()) + " bits)")
    print("n = " + str(n) + " (" + str(n.bit_length()) + " bits)")
    
    print("")
    
    print("Calculating λ(n) = lcm(p - 1, q - 1)")
    tot = __Internal_FindLeastCommonMultiple(p - 1, q - 1)
    print("λ(n) = " + str(tot) + " (" + str(tot.bit_length()) + " bits)")

    print("")

    print("Generating public key")
    e = __Internal_GeneratePublicKey(tot, keysize)
    print("e = " + str(e) + " (" + str(e.bit_length()) + " bits)")

    print("")

    print("Generating private key")
    d = __Internal_GeneratePrivateKey(e, tot)
    print("d = " + str(d) + " (" + str(d.bit_length()) + " bits)")

def __Internal_GenerateN(keysize):
    
    p = __pg.GeneratePrime(keysize / 2)
    q = __pg.GeneratePrime(keysize / 2)

    return p * q, p, q

def __Internal_FindLeastCommonMultiple(num1, num2):
    lcm = int((num1 * num2) / __math.gcd(num1, num2))
    return lcm

def __Internal_GeneratePublicKey(tot, keysize):    
    while True:
        e = __rnd.randint(2, tot - 1)
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

    return (g, x - (b // a) * y, y)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="RSA keygen")
    parser.add_argument('--bits', '-b', dest='keysize', type=int, default=1024)
    args = parser.parse_args()
    GenerateKeyPair(args.keysize)