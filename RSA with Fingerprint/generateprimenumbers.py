def is_prime(minutiae_count):
    #Returns True if n is a prime number, False otherwise.
    if minutiae_count < 2:
        return False
    for i in range(2, int(minutiae_count ** 0.5) + 1):
        if minutiae_count % i == 0:
            return False
    return True

def get_nearest_primes(minutiae_count):
    #Returns the two nearest prime numbers before and after n.
    # Find the nearest prime number before n
    prime_before = None
    for i in range(minutiae_count - 1, 1, -1):
        if is_prime(i):
            prime_before = i
            break
    
    # Find the nearest prime number after n
    prime_after = None
    i = minutiae_count + 1
    while True:
        if is_prime(i):
            prime_after = i
            break
        i += 1
    
    return prime_before, prime_after
#prime_before, prime_after = get_nearest_primes(int(minutiae_count))
# Get input from user
#n = int(input("Enter a number: "))
# Get nearest prime numbers


# Print the results
#print(f"The nearest prime number before {n} are: {prime_before}")
#print(f"The nearest prime number after {n} are: {prime_after}")

