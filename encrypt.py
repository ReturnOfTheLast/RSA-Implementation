import math as __math

def Encrypt(plain, e, n):
    cipher = pow(int.from_bytes(plain, byteorder="big"), e, n)
    return cipher.to_bytes(int(__math.ceil(cipher.bit_length() / 8 )) * 8, byteorder="big")

def Decrypt(cipher, d, n):
    plain = pow(int.from_bytes(cipher, byteorder="big"), d, n)
    return plain.to_bytes(int(__math.ceil(plain.bit_length() / 8)) * 8, byteorder="big")

def ExtractKeyParameters(keyfile):
    with open(keyfile, "r") as fp:
            return json.load(fp)

def __Internal_IsKeyLongEnough(keysize, input):
    if type(input) is str:
        return len(input.encode('utf-8')) * 8 < keysize
    
    return False

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

    if args.decrypt:
        output = Decrypt(int(args.input, 16).to_bytes(int(__math.ceil(int(args.input, 16).bit_length() / 8)) * 8, byteorder="big"), int(keyParameters["priv"]["d"], 16), int(keyParameters["pub"]["n"], 16)).decode('utf-8')
    else:
        if not __Internal_IsKeyLongEnough(int(keyParameters["pub"]["keysize"]), args.input):
            print("Error: Input to long for keysize")
            sys.exit(1)

        output = hex(int.from_bytes(Encrypt(args.input.encode('utf-8'), int(keyParameters["pub"]["e"], 16), int(keyParameters["pub"]["n"], 16)), byteorder="big"))

    print(output)