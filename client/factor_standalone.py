# Find the prime factors of a large 'semi-prime' number.
#
# This code runs standalone on an OctaPi client and is intended to
# show the difference in run time with similar code running on the
# Octapi cluster using Dispy.
#

# Primality test algorithms derived from code by Shay Margalit, 12 Dec 2013
# https://www.codeproject.com/articles/691200/primality-test-algorithms-prime-test-the-fastest-w
#
# License: The Code Project Open License (CPOL) 1.02, https://www.codeproject.com/info/cpol10.aspx
# The main points subject to the terms of the License are:
#   Source Code and Executable Files can be used in commercial applications;
#   Source Code and Executable Files can be redistributed; and
#   Source Code can be modified to create derivative works.
#   No claim of suitability, guarantee, or any warranty whatsoever is provided. The software is provided "as-is".
#   The Article(s) accompanying the Work may not be distributed or republished without the Author's consent

# All other original code: Crown Copyright 2016, 2017 


def find_factor(semi_prime, lower, upper):

    def naivePrimalityTest(number):
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


    # search between the lower and upper limits
    while (lower <= upper):
        factor1 = lower
        # only test prime numbers
        if MillerRabinPrimalityTest(factor1) and FermatPrimalityTest(factor1):
            if (semi_prime % factor1 == 0):
                factor2 = semi_prime // factor1
                
                # try this prime to see if it is a factor
                if (factor1 * factor2 == semi_prime):
                    #print ('%i * %i = %i' % (factor1, factor2, factor1*factor2))
                    return (factor1, factor2)

        lower = lower + 2    # skip even factors because they can't be prime

    # no factors found
    return (0, 0)


# main loop
if __name__ == '__main__':
    import random, math

    # this is the number we have been given to factor
    semi_prime = int( input( "What semi-prime number do you want to try and factor? " ) )
    # chunk size = chunk_scale * log(semi-prime)
    chunk_scale = int( input( "What scale of search chunk size do you want? (generally 100 - 1000) ") )

    # assume that the prime factors are roughly the same length
    # we can start our search from the square root
    lower = int( math.sqrt(semi_prime) )
    if (lower % 2) == 0: lower += 1    # make sure we start with an odd number (which could also be prime) 
    upper = semi_prime / 2             # make sure we seach far enough

    # the chunk size is the search space starting from 'lower'
    chunk = int ( chunk_scale * math.log(semi_prime) )

    # search for prime factors between the lower and upper limits
    found = False
    while (lower <= upper) and (found == False):
        print(('Attempting factors in range %i - %i, chunk size %i' % (lower, lower+chunk, chunk) ))

        factor1, factor2 = find_factor(semi_prime, lower, lower+chunk)

        # report the outcome
        if (factor1 != 0):
            print(('%i * %i = %i' % (factor1, factor2, factor1*factor2)))
            found = True

        # next chunk (make sure it's prime)
        lower += chunk
        if (lower % 2) == 0: lower += 1

    # report the outcome
    if (found == False): print ('no factors found')
