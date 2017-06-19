# This computes the value of Pi using the 'dartboard' algorithm. This is 
# a Monte Carlo method using many trials to estimate the area of a 
# quarter circle inside a unit square.
#
# This code runs standalone on the client and allows you to compare
# runtime with the version running on OctaPi using Dispy. 
#
# Reference: Arndt & Haenel, "Pi Uneashed", Springer-Verlag, 
# ISBN 978-3-540-66572-4, 2006, 
# English translation Catriona and David Lischka, pp. 39-41

# Dispy:
# Giridhar Pemmasani, "dispy: Distributed and parallel Computing with/for Python",
# http://dispy.sourceforge.net, 2016

# All other original code: Crown Copyright 2016, 2017 

# 'compute' is the core calculation
def compute(s, n):
    import time, random

    inside = 0

    # for all the points requested
    for i in range(n):
        # compute position of the point
        x = random.uniform(0.0, 1.0)
        y = random.uniform(0.0, 1.0)
        z = x*x + y*y
        if (z<=1.0):
            inside = inside + 1    # this point is inside the unit circle

    return(inside)


# main 
if __name__ == '__main__':
    import random, argparse, decimal

    parser = argparse.ArgumentParser()
    parser.add_argument("no_of_points", type=int, help="number of random points to include in each job")
    parser.add_argument("no_of_jobs", type =int, help="number of jobs to run")
    args = parser.parse_args()

    no_of_points = args.no_of_points
    no_of_jobs = args.no_of_jobs

    print(('doing %s jobs of %s points each' % (no_of_jobs, no_of_points)))
    total_inside = 0
    for i in range(no_of_jobs):
        # execute 'compute' standalone
        ran_seed = random.randint(0,65535) # define a random seed for each job 
        inside = compute(ran_seed, no_of_points)

        total_inside += inside

        if (i % 1000 == 0): 
            print(('executed job %i using %i with result %i' % (i, ran_seed, inside)))

    # calclate the estimated value of Pi
    total_no_of_points = no_of_points * no_of_jobs
    decimal.getcontext().prec = 100  # override standard precision
    Pi = decimal.Decimal(4 * total_inside / total_no_of_points)
    print(('value of Pi is estimated to be %s using %s points' % (+Pi, total_no_of_points) ))
