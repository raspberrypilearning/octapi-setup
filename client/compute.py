# This is the simple example provided in the Dispy documentation
# If this code runs, it means your OctaPi cluster is working correctly
# You should see a result similar to this:
#
#                           Node |  CPUs |    Jobs |    Sec/Job | Node Time Sec
#------------------------------------------------------------------------------
# 192.168.1.49 (raspberrypi)     |     4 |       4 |     16.040 |        64.160
# 192.168.1.202 (raspberrypi)    |     4 |       2 |     12.031 |        24.062
# 192.168.1.191 (raspberrypi)    |     4 |       2 |     13.029 |        26.058
# 192.168.1.223 (raspberrypi)    |     4 |       0 |      0.000 |         0.000
# 192.168.1.116 (raspberrypi)    |     4 |       2 |     10.025 |        20.050
# 192.168.1.27 (raspberrypi)     |     4 |       2 |     15.535 |        31.070
# 192.168.1.167 (raspberrypi)    |     4 |       4 |     14.537 |        58.148
# 192.168.1.50 (raspberrypi)     |     4 |       0 |      0.000 |         0.000
#
#Total job time: 223.548 sec, wall time: 20.245 sec, speedup: 11.042

# Dispy:
# Giridhar Pemmasani, "dispy: Distributed and parallel Computing with/for Python",
# http://dispy.sourceforge.net, 2016


# 'compute' is distributed to each node running 'dispynode'
def compute(n):
    import time, socket
    time.sleep(n)
    host = socket.gethostname()
    return (host, n)

if __name__ == '__main__':
    import dispy, random, socket
    # fetch the IP address of the client
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80)) # doesn't matter if 8.8.8.8 can't be reached
    cluster = dispy.JobCluster(compute,ip_addr=s.getsockname()[0], nodes='192.168.1.*')
    jobs = []
    for i in range(16):
        # schedule execution of 'compute' on a node (running 'dispynode')
        # with a parameter (random number in this case)
        job = cluster.submit(random.randint(5,20))
        job.id = i # optionally associate an ID to job (if needed later)
        jobs.append(job)
    # cluster.wait() # waits for all scheduled jobs to finish
    for job in jobs:
        host, n = job() # waits for job to finish and returns results
        print('%s executed job %s at %s with %s' % (host, job.id, job.start_time, n))
        # other fields of 'job' that may be useful:
        # print(job.stdout, job.stderr, job.exception, job.ip_addr, job.start_time, job.end_time)
    cluster.print_status()
    cluster.close()
