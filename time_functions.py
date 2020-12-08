# https://www.pythoncentral.io/time-a-python-function/

from timeit import timeit as __ti
import json

# Variables
trialCount = 1000

# --- wrapper ---
def wrapper(func, *args):
    def wrapped():
        return func(*args)
    return wrapped

# --- Wrap and time functions ---

# Prime generator 
import primegenerator as __pg
__pg.LoadPrimes()
print(" ---- Primegenerator -----")

# - __Internal_LowLevelPrime(byteLength)

#def __LowLevelPrimeTime(byteLength):
#    wrapped = wrapper(__pg.__Internal_LowLevelPrime, byteLength)
#    total=__ti(wrapped, number=trialCount)
#    average=total/trialCount
#
#    print("__Internal_LowLevelPrime(" + str(byteLength) + ") (" + str(byteLength * 8) + " bits) with " + str(trialCount) + " runs: " + str(total) + " seconds total (" + str(average) + "seconds average)")
#
## 32 bits (4 bytes)
#__LowLevelPrimeTime(4)
#
## 64 bits (8 bytes)
#__LowLevelPrimeTime(8)
#
## 128 bits (16 bytes)
#__LowLevelPrimeTime(16)
#
## 256 bits (32 bytes)
#__LowLevelPrimeTime(32)
#
## 512 bits (64 bytes)
#__LowLevelPrimeTime(64)
#
## 1024 bits (128 bytes)
#__LowLevelPrimeTime(128)
#
## 2048 bits (256 bytes)
#__LowLevelPrimeTime(256)
#
## 4096 bits (512 bytes)
#__LowLevelPrimeTime(512)
#
#print("")

# - GeneratePrime(byteLength)

gPBytelengths = list()
gPTotals = list()
gPAverages = list()

def __GeneratePrimeTime(byteLength):
    wrapped = wrapper(__pg.GeneratePrime, byteLength)
    total=__ti(wrapped, number=trialCount)
    average=total/trialCount

    print("GeneratePrime(" + str(byteLength) + ") (" + str(byteLength * 8) + " bits) with " + str(trialCount) + " runs: " + str(total) + " seconds total (" + str(average) + " seconds average)")

    gPBytelengths.append(byteLength)
    gPTotals.append(total)
    gPAverages.append(average)


# 32 bits (4 bytes)
__GeneratePrimeTime(4)

# 64 bits (8 bytes)
__GeneratePrimeTime(8)

# 128 bits (16 bytes)
__GeneratePrimeTime(16)

# 256 bits (32 bytes)
__GeneratePrimeTime(32)

# 512 bits (64 bytes)
__GeneratePrimeTime(64)

## 1024 bits (128 bytes)
#__GeneratePrimeTime(128)

## 2048 bits (256 bytes)
#__GeneratePrimeTime(256)

## 4096 bits (512 bytes)
#__GeneratePrimeTime(512)

# Keygen
import keygen as __kg

print(" ---- Keygen ----")

# - __Internal_GenerateN(keysize)

gNKeysizes = list()
gNTotals = list()
gNAverages = list()

def __GenerateNTime(keysize):
    wrapped = wrapper(__kg.__Internal_GenerateN, keysize)
    total=__ti(wrapped, number=trialCount)
    average=total/trialCount

    print("__Internal_GenerateN(" + str(keysize) + ") with " + str(trialCount) + " runs: " + str(total) + " seconds total (" + str(average) + " seconds average)")

    gNKeysizes.append(keysize)
    gNTotals.append(total)
    gNAverages.append(average)


# 64 bits (keysize)
__GenerateNTime(64)

# 128 bits (keysize)
__GenerateNTime(128)

# 256 bits (keysize)
__GenerateNTime(256)

# 512 bits (keysize)
__GenerateNTime(512)

# 1024 bits (keysize)
__GenerateNTime(1024)

## 2048 bits (keysize)
#__GenerateNTime(2048)
#
## 4096 bits (keysize)
#__GenerateNTime(4096)

# - __Internal_GeneratePublicKey(tot)

gPUKKeysizes = list()
gPUKTotals = list()
gPUKAverages = list()

def __GeneratePUKTime(keysize):
    _, p, q = __kg.__Internal_GenerateN(keysize)
    tot = (p - 1) * (q - 1)
    wrapped = wrapper(__kg.__Internal_GeneratePublicKey, tot)
    total=__ti(wrapped, number=trialCount)
    average=total/trialCount

    print("__Internal_GeneratePublicKey(" + hex(tot) + ") (" + str(keysize) + " bits) with " + str(trialCount) + " runs: " + str(total) + " seconds total (" + str(average) + " seconds average)")

    gPUKKeysizes.append(keysize)
    gPUKTotals.append(total)
    gPUKAverages.append(average)

# 64 bits (keysize)
__GeneratePUKTime(64)

# 128 bits (keysize)
__GeneratePUKTime(128)

# 256 bits (keysize)
__GeneratePUKTime(256)

# 512 bits (keysize)
__GeneratePUKTime(512)

# 1024 bits (keysize)
__GeneratePUKTime(1024)

# 2048 bits (keysize)
__GeneratePUKTime(2048)

# 4096 bits (keysize)
__GeneratePUKTime(4096)

# - __Internal_GeneratePrivateKey(e, tot)

gPRKKeysizes = list()
gPRKTotals = list()
gPRKAverages = list()

def __GeneratePRKTime(keysize):
    _, p, q = __kg.__Internal_GenerateN(keysize)
    tot = (p - 1) * (q - 1)
    e = __kg.__Internal_GeneratePublicKey(tot)
    wrapped = wrapper(__kg.__Internal_GeneratePrivateKey, e, tot)
    total=__ti(wrapped, number=trialCount)
    average=total/trialCount

    print("__Internal_GeneratePrivateKey(" + hex(e) + ", " + hex(tot) + ") (" + str(keysize) + " bits) with " + str(trialCount) + " runs: " + str(total) + " seconds total (" + str(average) + " seconds average)")

    gPRKKeysizes.append(keysize)
    gPRKTotals.append(total)
    gPRKAverages.append(average)

# 64 bits (keysize)
__GeneratePRKTime(64)

# 128 bits (keysize)
__GeneratePRKTime(128)

# 256 bits (keysize)
__GeneratePRKTime(256)

# 512 bits (keysize)
__GeneratePRKTime(512)

# 1024 bits (keysize)
__GeneratePRKTime(1024)

# 2048 bits (keysize)
__GeneratePRKTime(2048)

# 4096 bits (keysize)
__GeneratePRKTime(4096)

# write results
results = {
    "primegenerator": {
        "GeneratePrime": {
            "bytelength": gPBytelengths,
            "totals": gPTotals,
            "averages": gPAverages
        }
    },
    "keygen": {
        "GenerateN": {
            "keysizes": gNKeysizes,
            "totals": gNTotals,
            "averages": gNAverages
        },
        "GeneratePublicKey": {
            "keysizes": gPUKKeysizes,
            "totals": gPUKTotals,
            "averages": gPUKAverages
        },
        "GeneratePrivateKey": {
            "keysizes": gPRKKeysizes,
            "totals": gPRKTotals,
            "averages": gPRKAverages
        }
    }
}

with open('timeresults.json', 'w') as write_file:
    json.dump(results, write_file, indent=4)