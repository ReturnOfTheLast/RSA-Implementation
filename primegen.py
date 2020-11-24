if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate prime numbers. NOTE: This will take up a lot of memory and swap is therefore highly suggested")
    parser.add_argument('-n', action='store', type=int, required=True, dest='amount')

    args = parser.parse_args()

    primes = list()
    primes.append(2)
    primes.append(3)
    num = 3

    while len(primes) < args.amount:
        num += 1
        is_prime = True
        
        for prime in primes:
            if prime > num / 2:
                break
            
            if num % prime == 0:
                is_prime = False
                break
        
        if is_prime:
            primes.append(num)

    f = open("primenums.txt", "w")
    f.write(str(primes).replace('[', '').replace(']', '').replace(', ', '\n'))
    f.close()