import math as __math

# krypteringsfunktion tager bytes, eksponent og n som input
# Returnere de (de)kryptede bytes
def Crypt(inp, k, n):
    out = pow(int.from_bytes(inp, byteorder="big"), k, n)
    return out.to_bytes(int(__math.ceil(out.bit_length() / 8 )) * 8, byteorder="big")

# Hjælpe funktion der læser nøgler fra json filer
def ExtractKeyParameters(keyfile):
    with open(keyfile, "r") as fp:
            return json.load(fp)

# Funktion der tjekker om 
def __Internal_IsKeyLongEnough(keysize, input):
    if type(input) is str:
        return len(input.encode('utf-8')) * 8 < keysize
    
    return False

# Kommando linje kald af programmet bruger argumenter som opsættes her
if __name__ == "__main__":
    import argparse
    import json
    import sys

    parser = argparse.ArgumentParser(description="Encrypt and decrypt with RSA keys")
    parser.add_argument('-d', '--decrypt', dest="decrypt", help="Enable decryption", action="store_true")
    parser.add_argument(dest="input", help="text or integer", metavar="input", action="store")
    parsekeygroup = parser.add_mutually_exclusive_group(required=True)
    parsekeygroup.add_argument('-prk', '--private-key', dest="privatekey", help="", metavar="file", action="store")
    parsekeygroup.add_argument('-puk', '--public-key', dest="publickey", help="", metavar="file", action="store")
    args = parser.parse_args()

    output = ""

    if args.privatekey:
        keyParameters = ExtractKeyParameters(args.privatekey)
    
    elif args.publickey:
        if args.decrypt:
            print("Error: Private key must be used for decryption")
            sys.exit(1)
        
        keyParameters = ExtractKeyParameters(args.publickey)
    
    else:
        sys.exit(1)

    # Hokus pokus sker her, omdanning af bytes til integers og tilbage sker her.
    # Argumenterne bliver passeret til de rigtige funktioner med de rigtige typer.
    # Denne del kunne godt rodes op hvis jeg havde tid, men det har jeg desværre ikke.
    if args.decrypt:
        output = Crypt(int(args.input, 16).to_bytes(int(__math.ceil(int(args.input, 16).bit_length() / 8)) * 8, byteorder="big"), int(keyParameters["priv"]["d"], 16), int(keyParameters["pub"]["n"], 16)).decode('utf-8')
    else:
        if not __Internal_IsKeyLongEnough(int(keyParameters["pub"]["keysize"]), args.input):
            print("Error: Input to long for keysize")
            sys.exit(1)

        output = hex(int.from_bytes(Crypt(args.input.encode('utf-8'), int(keyParameters["pub"]["e"], 16), int(keyParameters["pub"]["n"], 16)), byteorder="big"))

    print(output)