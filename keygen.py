import random as __rnd
import math as __math
import primegenerator as __pg
import json as __json
import sys as __sys
from datetime import datetime as __dt

def GenerateKeyPair(keysize):
    print("Loading 50.000.000 prime numbers from file")
    __pg.LoadPrimes()
    print("Loaded primes")

    print("")

    print("Generating p, q and n")
    n, p, q = __Internal_GenerateN(keysize)
    print("p = " + hex(p) + " (" + str(p.bit_length()) + " bits)")
    print("q = " + hex(q) + " (" + str(q.bit_length()) + " bits)")
    print("n = " + hex(n) + " (" + str(n.bit_length()) + " bits)")

    print("")
    
    print("Calculating λ(n)")
    tot = (p - 1) * (q - 1)
    print("λ(n) = " + hex(tot) + " (" + str(tot.bit_length()) + " bits)")

    print("")

    print("Generating public key")
    e = __Internal_GeneratePublicKey(tot, keysize)
    print("e = " + hex(e) + " (" + str(e.bit_length()) + " bits)")

    print("")

    print("Generating private key")
    d = __Internal_GeneratePrivateKey(e, tot)
    print("d = " + hex(d) + " (" + str(d.bit_length()) + " bits)")

    print("")

    return (n, p, q, tot, e, d)

def __Internal_GenerateN(keysize):
    
    byteLength = int((keysize / 2) / 8)

    p = __pg.GeneratePrime(byteLength)
    q = __pg.GeneratePrime(byteLength)

    # The prime numbers must not be the same
    while p == q:
        q = __pg.GeneratePrime(byteLength)

    return p * q, p, q

def __Internal_GeneratePublicKey(tot, keysize):    
    while True:
        e = __rnd.randint(2, tot - 1)
        if __math.gcd(e, tot) == 1:
            break
    return e

def __Internal_GeneratePrivateKey(e, tot):
    # Increase recursion limit before extended euclidean algorithm
    normalrecursionlimit = __sys.getrecursionlimit()
    __sys.setrecursionlimit(normalrecursionlimit * 10)
    d = __Internal_EGCD(e, tot)[1]
    __sys.setrecursionlimit(normalrecursionlimit)
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
    parser = argparse.ArgumentParser(description="RSA keygen", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-b', '--bits', dest='keysize', metavar="int", help="key size", type=int, default=1024)
    parser.add_argument('-n', '--name', dest='name', metavar="string", type=str)
    parser.add_argument('-e', '--email', dest='email', metavar="string", type=str)
    parser.add_argument('-c', '--comment', dest='comment', metavar="string", type=str)
    args = parser.parse_args()
    keyParameters = GenerateKeyPair(args.keysize)

    print("Writing keys")
    
    privatedata = {
        "primes": [
            hex(keyParameters[1]),
            hex(keyParameters[2])
        ],
        "tot": hex(keyParameters[3]),
        "d": hex(keyParameters[5])
    }
    publicdata = {
        "name": args.name,
        "email": args.email,
        "comment": args.comment,
        "keysize": args.keysize,
        "n": hex(keyParameters[0]),
        "e": hex(keyParameters[4])
    }

    privatekey = {
        "priv": privatedata,
        "pub": publicdata
    }

    publickey = {
        "pub": publicdata
    }

    exportdir = "generated_keys"

    if args.name:
        keyprefix = args.name
    else:
        keyprefix = __dt.now().strftime("%Y-%m-%d_%H%M%S")

    with open( exportdir + "/" + keyprefix + ".priv.json", "w") as private_key_file:
        __json.dump(privatekey, private_key_file, indent=2)
    
    with open( exportdir + "/" + keyprefix + ".pub.json", "w") as public_key_file:
        __json.dump(publickey, public_key_file, indent=2)

    print("Keys written to " + exportdir + "/" + keyprefix + ".priv.json and "  + exportdir + "/" + keyprefix + ".pub.json" )
