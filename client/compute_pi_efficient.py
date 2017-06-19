# This computes the value of Pi using the 'dartboard' algorithm. This is 
# a Monte Carlo method using many trials to estimate the area of a 
# quarter circle inside a unit square.
#
# This code uses Dispy on OctaPi using the recommended method for managing
# jobs efficiently. For more information, visit the Dispy website. 
#
# Reference: Arndt & Haenel, "Pi Uneashed", Springer-Verlag, 
# ISBN 978-3-540-66572-4, 2006, 
# English translation Catriona and David Lischka, pp. 39-41

# Dispy:
# Giridhar Pemmasani, "dispy: Distributed and parallel Computing with/for Python",
# http://dispy.sourceforge.net, 2016

# All other original code: Crown Copyright 2016, 2017 

# 'compute' is distributed to each node running 'dispynode'
def compute(s, n):
    import time, random

    inside = 0

    # set the random seed on the server from that passed by the client
    random.seed(s)

    # for all the points requested
    for i in range(n):
        # compute position of the point
        x = random.uniform(0.0, 1.0)
        y = random.uniform(0.0, 1.0)
        z = x*x + y*y
        if (z<=1.0):
            inside = inside + 1    # this point is inside the unit circle

    return(s, inside)

# dispy calls this function to indicate change in job status
def job_callback(job): # executed at the client
    global pending_jobs, jobs_cond
    global total_inside

    if (job.status == dispy.DispyJob.Finished  # most usual case
        or job.status in (dispy.DispyJob.Terminated, dispy.DispyJob.Cancelled,
                          dispy.DispyJob.Abandoned)):
        # 'pending_jobs' is shared between two threads, so access it with
        # 'jobs_cond' (see below)
        jobs_cond.acquire()
        if job.id: # job may have finished before 'main' assigned id
            pending_jobs.pop(job.id)
            if (job.id % 1000 == 0):
                dispy.logger.info('job "%s" returned %s, %s jobs pending', job.id, job.result, len(pending_jobs))

            # extract the results for each job as it happens
            ran_seed, inside = job.result # returns results from job
            total_inside += inside        # count the num of points inside quarter circle

            if len(pending_jobs) <= lower_bound:
                jobs_cond.notify()
        jobs_cond.release()

# main 
if __name__ == '__main__':
    import dispy, random, argparse, resource, threading, logging, decimal

    # set lower and upper bounds as appropriate
    # lower_bound is at least num of cpus and upper_bound is roughly 3x lower_bound
    # lower_bound, upper_bound = 352, 1056
    lower_bound, upper_bound = 32, 96

    resource.setrlimit(resource.RLIMIT_STACK, (resource.RLIM_INFINITY, resource.RLIM_INFINITY) )
    resource.setrlimit(resource.RLIMIT_DATA, (resource.RLIM_INFINITY, resource.RLIM_INFINITY) )

    parser = argparse.ArgumentParser()
    parser.add_argument("no_of_points", type=int, help="number of random points to include in each job")
    parser.add_argument("no_of_jobs", type =int, help="number of jobs to run")
    args = parser.parse_args()

    no_of_points = args.no_of_points
    no_of_jobs = args.no_of_jobs
    server_nodes ='192.168.1.*'

    # use Condition variable to protect access to pending_jobs, as
    # 'job_callback' is executed in another thread
    jobs_cond = threading.Condition()
    cluster = dispy.JobCluster(compute, nodes=server_nodes, callback=job_callback, loglevel=logging.INFO)
    pending_jobs = {}

    print(('submitting %i jobs of %i points each to %s' % (no_of_jobs, no_of_points, server_nodes)))
    total_inside = 0
    i = 0
    while i <= no_of_jobs:
        i += 1

        # schedule execution of 'compute' on a node (running 'dispynode')
        ran_seed = random.randint(0,65535) # define a random seed for each server using the client RNG
        job = cluster.submit(ran_seed, no_of_points)

        jobs_cond.acquire()

        job.id = i # associate an ID to the job

        # there is a chance the job may have finished and job_callback called by
        # this time, so put it in 'pending_jobs' only if job is pending
        if job.status == dispy.DispyJob.Created or job.status == dispy.DispyJob.Running:
            pending_jobs[i] = job
            # dispy.logger.info('job "%s" submitted: %s', i, len(pending_jobs))
            if len(pending_jobs) >= upper_bound:
                while len(pending_jobs) > lower_bound:
                    jobs_cond.wait()
        jobs_cond.release()

    cluster.wait()

    # calclate the estimated value of Pi
    total_no_of_points = no_of_points * no_of_jobs
    decimal.getcontext().prec = 100  # override standard precision
    Pi = decimal.Decimal(4 * total_inside / total_no_of_points)
    print(('value of Pi is estimated to be %s using %i points' % (Pi, total_no_of_points) ))

    cluster.print_status()
    cluster.close()
