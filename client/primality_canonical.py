# Primality test algorithms
# This code generates a list of prime numbers in a user specified range
# provided at run time. The user can select from naive, Miller-Rabin, or
# Fermat primality tests. Only the specified test is run.
#
# This code uses Dispy on OctaPi in canonical form.
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

# Dispy:
# Giridhar Pemmasani, "dispy: Distributed and parallel Computing with/for Python",
# http://dispy.sourceforge.net, 2016

# All other original code: Crown Copyright 2016, 2017 

# naive primality test
def naivePrimalityTest(number):
    import math

    if number == 2:  # obvious special case
       return (True, number)
    if number % 2 == 0:
        return (False, number)
    
    i = 3
    sqrtOfNumber = math.sqrt(number)
    
    while i <= sqrtOfNumber:
        if number % i == 0:
            return (False, number)
        i = i+2
        
    return (True, number)

# Fermat primality test
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
                return (False, number)
        
        return (True, number)
    else:
        # case number == 1
        return (False, number)


# Miller-Rabin primality test
def MillerRabinPrimalityTest(number):
    import random, math
    
    # because the algorithm input is ODD number than if we get
    # even and it is the number 2 we return TRUE ( spcial case )
    # if we get the number 1 we return false and any other even 
    # number we will return false.
    
    if number == 2:   # obvious special case
        return (True, number)
    elif number == 1 or number % 2 == 0:
        return (False, number)
    
    # first we want to express n as : 2^s * r ( were r is odd )
    
    # the odd part of the number
    oddPartOfNumber = number - 1
    
    # The number of time that the number is divided by two
    timesTwoDividNumber = 0
    
    # while r is even divid by 2 to find the odd part
    while oddPartOfNumber % 2 == 0:
        oddPartOfNumber = oddPartOfNumber / 2
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
                return (False, number)
            
    # well the number pass the tests ==> it is probably prime ==> return true for primality
    return (True, number) 


# main 
if __name__ == '__main__':
    import dispy, random, argparse, resource

    resource.setrlimit(resource.RLIMIT_STACK, (resource.RLIM_INFINITY, resource.RLIM_INFINITY) )
    resource.setrlimit(resource.RLIMIT_DATA, (resource.RLIM_INFINITY, resource.RLIM_INFINITY) )

    parser = argparse.ArgumentParser()
    parser.add_argument("lower_limit", type=int, help="lowest putative prime to test")
    parser.add_argument("upper_limit", type =int, help="largest putative prime to test")
    parser.add_argument("primality", type =int, help="algorithm to use; 0=naive, 1=Fermat, 2=Miller Rabin")
    args = parser.parse_args()

    lower_limit = args.lower_limit
    upper_limit = args.upper_limit
    primality = args.primality
    server_nodes ='192.168.1.*'

    # choose your algorthm
    if (primality == 0):
       cluster = dispy.JobCluster(naivePrimalityTest, nodes=server_nodes)
       print('Naive primality test selected')
    elif (primality == 1):
       cluster = dispy.JobCluster(FermatPrimalityTest, nodes=server_nodes)
       print('Fermat primality test selected')
    elif (primality == 2):
       cluster = dispy.JobCluster(MillerRabinPrimalityTest, nodes=server_nodes)
       print('Miller-Rabin primality test selected')

    print(('Finding prime numbers in the range %i - %i on cluster %s' % (lower_limit, upper_limit, server_nodes)))
    jobs = []

    if lower_limit % 2 == 0:    # make sure we start with an odd number
        lower_limit += 1 

    for i in range(lower_limit, upper_limit, 2):
        # schedule execution of desired primality test on a node (running 'dispynode')
        job = cluster.submit(i)
        job.id = i # associate an ID to the job
        jobs.append(job)

    for job in jobs:
        isprime, number = job() # waits for job to finish and returns results

        if (isprime):
            print(number)

    cluster.print_status()
    cluster.close()
