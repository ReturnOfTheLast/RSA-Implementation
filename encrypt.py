def EncryptText(text, e, n):
    ctext = [pow(ord(char), e, n) for char in text]
    return ctext

def DecryptText(ctext, d, n):
    try:
        text = [chr(pow(char, d, n)) for char in ctext]
        return "".join(text)
    except TypeError as e:
        print(e)

def ExtractKeyParameters(keyfile):
    with open(keyfile, "r") as fp:
            return json.load(fp)

if __name__ == "__main__":
    import argparse
    import json
    import sys

    parser = argparse.ArgumentParser(description="Encrypt and decrypt with RSA keys")
    parser.add_argument('-d', '--decrypt', dest="decrypt", help="Enable decryption", action="store_true")
    parser.add_argument(dest="input", help="text or integer list", type=str, metavar="input", action="store")
    parsekeygroup = parser.add_mutually_exclusive_group(required=True)
    parsekeygroup.add_argument('-prk', '--private-key', dest="privatekey", help="", metavar="file", action="store")
    parsekeygroup.add_argument('-puk', '--public-key', dest="publickey", help="", metavar="file", action="store")
    args = parser.parse_args()

    output = ""

    if args.privatekey:
        keyParameters = ExtractKeyParameters(args.privatekey)

        if args.decrypt:
            inp = str(args.input).replace("[", "").replace("]", "").split(",")
            ctext = list()
            for i in inp:
                ctext.append(int(i))

            output = DecryptText(ctext, keyParameters["priv"]["d"], keyParameters["pub"]["n"])
        else:
            output = EncryptText(str(args.input), keyParameters["pub"]["e"], keyParameters["pub"]["n"])

    else:
        if args.decrypt:
            print("Error: Private key must be used for decryption")
            sys.exit(1)
        
        keyParameters = ExtractKeyParameters(args.publickey)

        output = EncryptText(str(args.input), keyParameters["e"], keyParameters["n"])

    print(output)