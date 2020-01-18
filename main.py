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

    def setEndTime(self, time):
        self.end_time = time

    def getTurnaroundTime(self):
        return self.end_time - self.arrival_time

    def getWaittingTime(self):
        return self.getTurnaroundTime() - self.burst_time

    def getResponseTime(self):
        return self.start_time - self.arrival_time

    
    def __str__(self):
        return 'id:{} arrival_time:{} burst_time:{} io_time:{}'.format(self.id, self.arrival_time, self.burst_time, self.io_time)
class CPU: 
    
    def __init__(self, all_process):
        self.all_proccess = all_process
        self.ready_queue = Queue(maxsize = len (all_process)) 
        self.waiting_queue = Queue(maxsize = len(all_process))
        self.activ_list = []


    def FCFS(self):
        #ititial time and burst_time 
        self.time = 0
        self.total_burst_time = 0
        

        tmp = self.all_proccess[:]
        tmp.sort(key = lambda c: c.arrival_time, reverse= False)
        for process in tmp:
            self.ready_queue.put(process)
        while (self.ready_queue.qsize() != 0):
            p = self.ready_queue.get()
            if (p.arrival_time > self.time):
                self.time = p.arrival_time
            p.setStartTime(self.time)
            self.time += p.burst_time
            p.setEndTime(self.time)
            p.remaining_time = 0
            self.total_burst_time = self.total_burst_time + p.burst_time
        

        # for process in self.all_proccess:
        #     print (process)
        #     print (process.start_time)
        #     print (process.end_time)
        #     print ("ResponseTime: " , process.getResponseTime())
        #     print ("WatingTime: " , process.getWaittingTime())
        #     print ("TurnAroundTime: " , process.getTurnaroundTime())
        #     print ("==========================")

        # evaluate the CPU variables AWT, ATT, ART, Throughput, Utilization
        self.average_waiting_time = sum([x.getWaittingTime() for x in self.all_proccess]) / len(self.all_proccess)
        self.average_turnaround_time = sum([x.getTurnaroundTime() for x in self.all_proccess]) / len(self.all_proccess)
        self.average_response_time = sum([x.getResponseTime() for x in self.all_proccess]) / len(self.all_proccess)
        self.throughput = len(self.all_proccess)/ self.time
        self.cpu_utilization =  self.total_burst_time/self.time
        
        #print all CPU variables
        print (self.average_response_time)
        print (self.average_turnaround_time)
        print (self.average_response_time)
        print (self.throughput)
        print (self.cpu_utilization)



process = []
for i in range(5):
    str = input()
    str_list = str.split(" ") 
    process.append(Process(i+1,int (str_list[0]), int(str_list[1]), int(str_list[2])))

cpu1 = CPU(process)
cpu1.FCFS()