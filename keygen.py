import random as __rnd
import math as __math
import primegenerator as __pg
import json as __json
import sys as __sys
from datetime import datetime as __dt

##
# Dette program generere parametre til brug i RSA kryptering
# Herunder primtal 'p' og 'q', deres produkt 'n', totienten 'Φ(n)',
# og eksponenterne 'e', 'd'
##

# Primære funktion der kalder andre funktioner
# Returner (n, p, q, tot, e, d)
def GenerateKeyPair(keysize):

    # Start primtals generatoren og hent lave primtal
    print("Loading 50.000.000 prime numbers from file")
    __pg.LoadPrimes()
    print("Loaded primes")

    print("")

    # Generere 'n', 'p' og 'q'
    print("Generating p, q and n")
    n, p, q = __Internal_GenerateN(keysize)
    print("p = " + hex(p) + " (" + str(p.bit_length()) + " bits)")
    print("q = " + hex(q) + " (" + str(q.bit_length()) + " bits)")
    print("n = " + hex(n) + " (" + str(n.bit_length()) + " bits)")

    print("")
    
    # Udregn totienten
    print("Calculating Φ(n)")
    tot = (p - 1) * (q - 1)
    print("Φ(n) = " + hex(tot) + " (" + str(tot.bit_length()) + " bits)")

    print("")

    # Generere en offendtlig eksponent
    print("Generating public key")
    e = __Internal_GeneratePublicKey(tot)
    print("e = " + hex(e) + " (" + str(e.bit_length()) + " bits)")

    print("")

    # Generere den private eksponent
    print("Generating private key")
    d = __Internal_GeneratePrivateKey(e, tot)
    print("d = " + hex(d) + " (" + str(d.bit_length()) + " bits)")

    print("")

    # Returner parameter
    return (n, p, q, tot, e, d)

# Funktion til at generere 'n', 'p' og 'q'
# Returnere 'n', 'p' og 'q'
def __Internal_GenerateN(keysize):
    
    # Udregn hvor mange bytes der skal bruges pr. primtal
    byteLength = int((keysize / 2) / 8)

    # Kald primtalsgeneratoren
    p = __pg.GeneratePrime(byteLength)
    q = __pg.GeneratePrime(byteLength)

    # Generere en ny 'q' hvis 'p' og 'q' er ens
    while p == q:
        q = __pg.GeneratePrime(byteLength)

    # Returner 'n' (p * q), 'p' og 'q'
    return p * q, p, q

# Funktion til at generere den offendlige eksponent
# Returnere 'e'
def __Internal_GeneratePublicKey(tot):
    
    # Fortsæt med at vælge tilfældige tal mellem 2 og Φ(n) - 1 indtil at 'e'
    # er indbyrdes primisk med Φ(n)
    while True:
        e = __rnd.randint(2, tot - 1)
        if __math.gcd(e, tot) == 1:
            break
    
    # Returner 'e'
    return e

# Funktion til at udregne den private eksponent
# Returnere 'd'
def __Internal_GeneratePrivateKey(e, tot):
    # Forhøj recursion grænsen før at Extended Euclidean Algorithm bliver brugt
    normalrecursionlimit = __sys.getrecursionlimit()
    __sys.setrecursionlimit(normalrecursionlimit * 10)

    # Udregn 'd' med Extended Euclidean Algorithm, med 'e' og 'Φ(n)' som input
    d = __Internal_EGCD(e, tot)[1]
    
    # Sæt recursion grænsen tilbage
    __sys.setrecursionlimit(normalrecursionlimit)
    
    # Ret 'd' til sådan at den passer inden for 0 til Φ(n) 
    d = d % tot
    if d < 0:
        d += tot
    
    # Returner 'd'
    return d

# Extended Euclidean Algorithm fra https://www.bloggerdrive.com/understanding-and-implementing-rsa-algorithm-in-python/
# Returner (g, x, y)
def __Internal_EGCD(a,b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = __Internal_EGCD(b % a, a)

    return (g, x - (b // a) * y, y)

# Hvis programmet ikke bliver importet af et andet program
# så kør programmet med argumenter givet på kommandolinjen
# 
# Se README.md
if __name__ == "__main__":
    
    # Opsæt argumenter
    import argparse
    parser = argparse.ArgumentParser(description="RSA keygen", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-b', '--bits', dest='keysize', metavar="int", help="key size", type=int, default=1024)
    parser.add_argument('-n', '--name', dest='name', metavar="string", type=str)
    parser.add_argument('-e', '--email', dest='email', metavar="string", type=str)
    parser.add_argument('-c', '--comment', dest='comment', metavar="string", type=str)
    args = parser.parse_args()
    
    # Generere nøgle-parametre
    keyParameters = GenerateKeyPair(args.keysize)

    print("Writing keys")
    
    # Opsæt json-strukturer
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

    # Generere præfiskt til filerne
    if args.name:
        keyprefix = args.name
    else:
        keyprefix = __dt.now().strftime("%Y-%m-%d_%H%M%S")

    # Gem nøglere
    with open( exportdir + "/" + keyprefix + ".priv.json", "w") as private_key_file:
        __json.dump(privatekey, private_key_file, indent=2)
    
    with open( exportdir + "/" + keyprefix + ".pub.json", "w") as public_key_file:
        __json.dump(publickey, public_key_file, indent=2)

    print("Keys written to " + exportdir + "/" + keyprefix + ".priv.json and "  + exportdir + "/" + keyprefix + ".pub.json" )
