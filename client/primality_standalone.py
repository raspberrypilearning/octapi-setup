# Primality test algorithms
# This code generates an endless list of prime numbers from a starting value
# provided at run time. Both Miller-Rabin and Fermat have to be true for the
# value to be assumed to be prime. It runs on the OctaPi client standalone
# and is intended to check that the primality testing code used in several
# other apps is working correctly.
#
# Derived from code by Shay Margalit, 12 Dec 2013
# https://www.codeproject.com/articles/691200/primality-test-algorithms-prime-test-the-fastest-w
#
# Suggested test value: 99194853094755497
#
# License: The Code Project Open License (CPOL) 1.02, https://www.codeproject.com/info/cpol10.aspx
# The main points subject to the terms of the License are:
#   Source Code and Executable Files can be used in commercial applications;
#   Source Code and Executable Files can be redistributed; and
#   Source Code can be modified to create derivative works.
#   No claim of suitability, guarantee, or any warranty whatsoever is provided. The software is provided "as-is".
#   The Article(s) accompanying the Work may not be distributed or republished without the Author's consent

# All other original code: Crown Copyright 2016, 2017 


def naivePrimaryTest(number):
    import math

    if number == 2:
       return true
    if number % 2 == 0:
        return False
    
    i = 3
    sqrtOfNumber = math.sqrt(number)
    
    while i <= sqrtOfNumber:
        if number % i == 0:
            return False
        i = i+2
        
    return True


def FermatPrimalityTest(number):
    import random, math

    # if number != 1
    if (number > 1):
        # repeat the test few times
        for time in range(3):
            # Draw a RANDOM number in range of number ( Z_number )
            randomNumber = random.randint(2, number)-1
            
            # Test if a^(n-1) = 1 mod n
            if ( pow(randomNumber, number-1, number) != 1 ):
                return False
        
        return True
    else:
        # case number == 1
        return False

def MillerRabinPrimalityTest(number):
    import random, math
    
    # because the algorithm input is ODD number than if we get
    # even and it is the number 2 we return TRUE ( spcial case )
    # if we get the number 1 we return false and any other even 
    # number we will return false.
    
    if number == 2:
        return True
    elif number == 1 or number % 2 == 0:
        return False
    
    # first we want to express n as : 2^s * r ( were r is odd )
    
    # the odd part of the number
    oddPartOfNumber = number - 1
    
    # The number of time that the number is divided by two
    timesTwoDividNumber = 0
    
    # while r is even divid by 2 to find the odd part
    while oddPartOfNumber % 2 == 0:
        oddPartOfNumber = oddPartOfNumber // 2
        timesTwoDividNumber = timesTwoDividNumber + 1 
     
    
    # since there are number that are cases of "strong liar" we 
    # need to check more then one number
    
    for time in range(3):
        
        # choose "Good" random number
        while True:
            # Draw a RANDOM number in range of number ( Z_number )
            randomNumber = random.randint(2, number)-1
            if randomNumber != 0 and randomNumber != 1:
                break
        
        # randomNumberWithPower = randomNumber^oddPartOfNumber mod number 
        randomNumberWithPower = pow(randomNumber, oddPartOfNumber, number)
        
        # if random number is not 1 and not -1 ( in mod n ) 
        if (randomNumberWithPower != 1) and (randomNumberWithPower != number - 1):
            # number of iteration
            iterationNumber = 1
            
            # while we can squre the number and the squered number is not -1 mod number
            while (iterationNumber <= timesTwoDividNumber - 1) and (randomNumberWithPower != number - 1):
                # squre the number
                randomNumberWithPower = pow(randomNumberWithPower, 2, number)
                
                # inc the number of iteration
                iterationNumber = iterationNumber + 1
                
            # if x != -1 mod number then it because we did not found strong witnesses
            # hence 1 have more then two roots in mod n ==>
            # n is composite ==> return false for primality
            
            if (randomNumberWithPower != (number - 1)):
                return False
            
    # well the number pass the tests ==> it is probably prime ==> return true for primality
    return True 


# main loop
# get number to test
print("Enter the number you want to start from:")
number = int(eval(input()))

if (number == 0):    # avoid zero
     number = 1
elif (number % 2) == 0:    # make sure we start with an odd number
     number += 1 

while True:
    
    # test for primility
    if MillerRabinPrimalityTest(number) and FermatPrimalityTest(number):
        print(number)

    number += 2