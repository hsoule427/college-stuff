import random as r
import time as t
from threading import Timer

std_no = 3043
k = std_no%3+2
finished_jobs = []


class Job():
    def __init__(self, arrival_time, run_time):
        self.arrival_time = arrival_time
        self.run_time = run_time
        self.wait_time = 0
        self.finish_time = 0
        self.start_time = 0
        self.remaing_time = 0
        self.running = False
        self.in_q = False


class Processor():
    def __init__(self):
        self.is_empty = True
        self.time_till_free = 0
        self.current_job = None
        self.wait_q = []

    def load_job(self, job, current_time):
        self.is_empty = False
        self.current_job = job
        self.current_job.start_time = current_time
        self.time_till_free = current_time + self.current_job.run_time
        self.current_job.running = True


    def release(self, job, current_time):
        job.finish_time = current_time
        self.is_empty = True
        self.current_job = None
        finished_jobs.append(job)
        pending_jobs.remove(job)


    def pop_from_q(self):
        job = self.wait_q[0]
        del self.wait_q[0]
        job.in_q = False
        return job



processors = [Processor() for i in range(k)]


def find_empty(processors):
    for i in range(len(processors)):
        if processors[i].is_empty:
            return i
            break



def check_processors(current_time):
    for p in processors:
        if not p.is_empty:
            if p.time_till_free <= current_time:
                p.release(p.current_job, current_time)
                if p.wait_q:
                    p.load_job(p.pop_from_q(), current_time)


def turnaround_time(finished_jobs):
    finished_jobs.sort(key=lambda x: x.arrival_time)
    start_time = finished_jobs[0].arrival_time
    finished_jobs.sort(key=lambda x: x.finish_time)
    end_time = finished_jobs[len(finished_jobs)-1].finish_time
    return end_time - start_time


def print_output(times):
    times.sort()
    n = len(times)
    avg = sum(times, 0)/n

    std_dev = 0
    for t in times:
        dev = avg-t
        if dev<0: dev = dev*-1
        std_dev += dev

    std_dev = std_dev/n
    min = times[0]
    max = times[len(times)-1]
    output = open('output.txt', 'w')
    output.write("Results:\n")
    output.write("Maximum Turnaround Time = " + str(max) + "\n")
    output.write("Minimum Turnaround Time = "+ str(min) + "\n")
    output.write("Average = " + str(avg) + "\n")
    output.write("Standard Deviation = " + str(std_dev) + "\n")


def circular_simulation(jobs, processors):
    j = 0
    current_time = 0
    while jobs:
        check_processors(current_time)
        for job in jobs:
            if not job.running or not job.in_q:
                if current_time == job.arrival_time:
                    if processors[j].is_empty:
                        processors[j].load_job(job, job.arrival_time)
                        j = (j + 1) % k
                    else:
                        processors[j].wait_q.append(job)
                        j = (j + 1) % k
        current_time += 1




def shortest_remaining_time(jobs, processors):
    waiting = []
    for i in range(len(jobs)):
        current_time = jobs[i].arrival_time
        for p in processors:
            if not p.is_empty:
                job = p.current_job
                if current_time>job.finish_time: p.release(p.current_job, current_time)
                else:
                    job.run_time = job.finish_time - current_time
                    job.finish_time = current_time + job.run_time
        j = find_empty(processors)
        if j == None:
            pass
        else:
            processors[j].load_job(jobs[i], current_time)

times = []
for i in range(100):
    finished_jobs = []
    pending_jobs = [Job(i, r.randint(1,20)) for i in range(10)]
    circular_simulation(pending_jobs, processors)
    times.append(turnaround_time(finished_jobs))

    




