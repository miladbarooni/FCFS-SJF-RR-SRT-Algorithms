from queue import Queue 
class Process :

    def __init__(self, id, arrival_time, burst_time, io_time):
        self.id = id
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.io_time = io_time
        self.remaining_time = burst_time

    def setStartTime(self, time):
        self.start_time = time

    def setTurnaroundTime(self, time):
        self.turnaround_time = time

    def getWaittingTime():
        return self.turnaround_time - self.arrival_time - self.burst_time

    def getResponseTime():
        return self.start_time - self.arrival_time

    def getTurnaroundTime():
        return self.turnaround_time
        
class CPU:
    
    def __init__(self, all_process):
        self.all_proccess = all_process.sort(key=lambda x: x.arrival_time)
        self.ready_queue = Queue(maxsize = len (all_process)) 
        self.waiting_queue = Queue(maxsize = len(all_process))
    # def FCFS(self):


