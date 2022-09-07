import random
import math


def prime_test(N, k):
    # This is main function, that is connected to the Test button. You don't need to touch it.
    return fermat(N,k), miller_rabin(N,k)

# TIME COMPLEXITY: O(n^3)
# SPACE COMPLEXITY: O(n^2)
def mod_exp(x, y, N):
    # If the exponent is 0, then 1 can be returned and no calculations necessary
    if y == 0:
        return 1
    # Recursively call mod_exp for x and half of
    # the exponent y.
    z = mod_exp(x, math.floor(y/2), N)
    # If y is even, then return z squared mod N
    if (y % 2) == 0:
        return math.pow(z, 2) % N
    # If y is odd, return x times z squared mod N
    else:
        return (x * (math.pow(z, 2))) % N

# TIME COMPLEXITY: O(1)
# SPACE COMPLEXITY: O(1)
def fprobability(k):
    return 1.00 - (1 / (math.pow(2, k)))

# TIME COMPLEXITY: O(1)
# SPACE COMPLEXITY: O(1)
def mprobability(k):
    return 1.00 - (1 / (math.pow(4, k)))

# TIME COMPLEXITY: O(n^3)
# SPACE COMPLEXITY: O(n^2)
def fermat(N,k):
    randvals = []
    # For k amount of times, generate a random integer from 2 -> N-1
    # and put it into the randvals list. || TIME COMPLEXITY: O(k)
    for i in range(k):
        randvals.insert(i, random.randint(2, N - 1))
    # For each of the randvals, calculate the mod_exp of it with N-1. If this does not equal 1,
    # then the number is composite. || TIME COMPLEXITY: O(k)
    for a in randvals:
        if (mod_exp(a, N - 1, N)) != 1: # TIME COMPLEXITY: O(n^3)
            return 'composite'
    # If the above loop never returns, this means that all the
    # random numbers passed and that the number is prime.
    return 'prime'

# TIME COMPLEXITY: O(n^4)
# SPACE COMPLEXITY: O(n^3)
def miller_rabin(N,k):
    randvals = []
    # For k amount of times, generate a random integer from 2 -> N-1 and put it
    # into the randvals list. || TIME COMPLEXITY: O(k)
    for i in range(k):
        randvals.insert(i, random.randint(2, N - 1))

    for a in randvals:
        # For each of the randvals, calculate the mod_exp of it with N-1. If this does not equal 1,
        # then the number is composite. || TIME COMPLEXITY: O(k)
        x = mod_exp(a, N - 1, N) # TIME COMPLEXITY: O(n^3)
        # If the mod_exp of the randval and N-1 is not 1, return composite.
        if x != 1:
            return 'composite'
        # This exp value is for tracking the changing exponent which starts as N-1
        exp = N - 1
        # Continue this process while exp is even, and each loop
        # divide exp by 2.
        while (exp % 2) == 0: # TIME COMPLEXITY: O(n)
            exp /= 2
            # Calculate x to the exp power mod N. If this does not equal -1 or 1,
            # then the number is composite. || TIME COMPLEXITY: O(n^3) <----
            x = mod_exp(x, exp, N)
            if x != -1 and x != 1:
                return 'composite'
    # If the above loop doesn't trigger any returns, then the number must be prime.
    return 'prime'
