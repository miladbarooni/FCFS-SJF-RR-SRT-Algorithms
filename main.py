from queue import Queue 
class CPU:
    
    def __init__(self, all_process):
        self.all_proccess = all_process.sort(key=lambda x: x.arrival_time)
        self.ready_queue = Queue(maxsize = len (all_process)) 
        self.waiting_queue = Queue(maxsize = len(all_process))
    # def FCFS(self):


