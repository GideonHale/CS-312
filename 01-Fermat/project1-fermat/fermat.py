import random

# This is main function that is connected to the Test button. You don't need to touch it.
def prime_test(num, numIter):
    return fermat(num, numIter), miller_rabin(num, numIter)

# perform modular exponentiation
def mod_exp(base, exponent, modulus):

    if exponent == 0: return 1
    
    z = mod_exp(base, exponent // 2, modulus)
    
    if exponent % 2 == 0: return (z**2) % modulus
    else: return (base * z**2) % modulus

# using Fermat's Little Theorem, find out to a certain probability if primeCandidate is prime
def fermat(queryNum, numIter):

    for i in range(numIter):
        base = random.randint(1, queryNum - 1)

        if mod_exp(base, queryNum - 1, queryNum) != 1: return "composite"

    return "prime"

# determine the probability that fermat() actually produces a correct answer
def fprobability(numIter):
    return 1.0 - (1 / 2)**numIter

# using the Miller-Rabin Test, find out to a certain probability if primeCandidate is prime
def miller_rabin(queryNum, numIter):

    for i in range(numIter):
        base = random.randint(1, queryNum - 1)\

        runningExp = queryNum - 1
        runningModExp = 1
        while runningModExp == 1:

            runningModExp = mod_exp(base, runningExp, queryNum)

            if runningModExp != 1:
                if runningModExp != queryNum - 1: return "composite"
            
            if runningExp % 2 != 0:
                break

            runningExp = runningExp / 2

    return "prime"

# determine the probability that miller_rabin() actually produces a correct answer
def mprobability(numIter):
    return 1.0 - (1 / 4)**numIter

# test for mod_exp()
# x = int(input("Value of x: "))
# y = int(input("Value of y: "))
# N = int(input("Value of N: "))
# print("mod_exp(", x, ",", y, ",", N, "): ", mod_exp(x, y, N))

# test for fprobability() and mprobablility()
# k = int(input("number of random numbers: "))
# print("fprob:", fprobability(k))
# print("mprob:", mprobability(k))

# test for fermat()
# print("Fermat Primality Test")
# N, k = input("Give N and k values: ").split()
# for i in range(0, 30):
#     print('\t', f"{i + 1:2}", ":", N, "is", fermat(int(N), int(k)), "with probability", f"{fprobability(int(k)):.15f}")

# test for miller_rabin()
# print("Miller-Rabin Primality Test")
# N, k = input("Give N and k values: ").split()
# for i in range(0, 30):
#     print('\t', f"{i + 1:2}", ":", N, "is", miller_rabin(int(N), int(k)), "with probability", f"{mprobability(int(k)):.15f}")