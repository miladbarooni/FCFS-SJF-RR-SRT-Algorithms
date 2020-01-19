from queue import Queue, PriorityQueue
import threading
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection

class Process :

    def __init__(self, identity, arrival_time, burst_time, io_time):
        self._identity = identity
        self._arrival_time = arrival_time
        self._burst_time = burst_time
        self._io_time = io_time
        self._remaining_time = burst_time
        self._start_time = -1

    @property
    def arrival_time(self):
        return self._arrival_time

    @property
    def burst_time(self):
        return self._burst_time

    @property
    def io_time(self):
        return self._io_time

    @property
    def identity(self):
        return self._identity

    def getRemainingTime(self):
        return self._remaining_time

    def getTurnaroundTime(self):
        return self._end_time - self._arrival_time

    def getWaittingTime(self):
        return self.getTurnaroundTime() - self._burst_time

    def getResponseTime(self):
        return self._start_time - self._arrival_time

    def run(self, time, sec):
        new_time = time
        if (self._remaining_time > 0):
            self._remaining_time -= sec
            new_time += sec
        if(self._start_time == -1):
            self._start_time = time
        if(self._remaining_time == 0):
            self._end_time = new_time
        return new_time

    def isFinished(self):
        return self._remaining_time == 0


    
    def __str__(self):
        return 'identity:{} arrival_time:{} burst_time:{} io_time:{}'.format(self._identity, self._arrival_time, self._burst_time, self._io_time)

class CPU: 
    
    def __init__(self, all_process):
        self._running_sequence = []
        self.all_proccess = []
        self.ready_queue = Queue(maxsize = len (all_process)) 
        self.waiting_queue = Queue(maxsize = len(all_process))
        # self.active_list = []
        for p in all_process:
            self.all_proccess.append(Process(p.identity, p.arrival_time, p.burst_time, p.io_time))

    def FCFS(self):
        #ititial time and burst_time 
        self.time = 0
        self.total_burst_time = 0
        

        tmp = self.all_proccess[:]
        tmp.sort(key = lambda c: c.arrival_time, reverse = False)
        for process in tmp:
            self.ready_queue.put(process)
        while not self.ready_queue.empty() or not self.waiting_queue.empty():
            p = self.ready_queue.get()
            if (p.arrival_time > self.time):
                self.time = p.arrival_time
            running_frame = [self.time]
            self.time = p.run(self.time, p.burst_time)
            running_frame += [self.time, "p" + '{}'.format(p.identity)]
            self._running_sequence.append(running_frame)
            self.total_burst_time += p.burst_time

        # evaluate the CPU variables AWT, ATT, ART, Throughput, Utilization
        self.average_waiting_time = sum([x.getWaittingTime() for x in self.all_proccess]) / len(self.all_proccess)
        self.average_turnaround_time = sum([x.getTurnaroundTime() for x in self.all_proccess]) / len(self.all_proccess)
        self.average_response_time = sum([x.getResponseTime() for x in self.all_proccess]) / len(self.all_proccess)
        self.throughput = len(self.all_proccess)/ self.time
        self.cpu_utilization =  self.total_burst_time/self.time
        
        #print all CPU variables
        print ("FCFS:")
        print ("Avg. W.T.: ", self.average_waiting_time)
        print ("Avg. T.T.: ", self.average_turnaround_time)
        print ("Avg. R.T: ", self.average_response_time)
        print ("Throughput: ", self.throughput)
        print ("CPU Utilization: ", self.cpu_utilization)
        return self.plot("FCFS")

    def SJF(self):
        #ititial time and burst_time 
        self.time = 0
        self.total_burst_time = 0
        sorted_on_arrival_time = self.all_proccess[:]
        sorted_on_arrival_time.sort(key = lambda c: c.arrival_time, reverse = False)
        
        sorted_on_burst_time = []

        while (len(sorted_on_arrival_time) != 0 or len(sorted_on_burst_time) != 0):
            tmp = sorted_on_arrival_time[:]
            for p in tmp:
                if (p.arrival_time <= self.time):
                    sorted_on_burst_time.append(p)
                    sorted_on_arrival_time.remove(p)
                if (p.arrival_time > self.time):
                    next_arrival_time = p.arrival_time
                    break

            sorted_on_burst_time.sort(key = lambda c: c.burst_time, reverse = True)
            
            if (len(sorted_on_burst_time) == 0):
                self.time = next_arrival_time
                continue
            else:
                p = sorted_on_burst_time.pop()
                running_frame = [self.time]
                self.time = p.run(self.time, p.burst_time)
                running_frame += [self.time, "p" + '{}'.format(p.identity)]
                self._running_sequence.append(running_frame)
                self.total_burst_time += p.burst_time

        #printAllProcess()

        # evaluate the CPU variables AWT, ATT, ART, Throughput, Utilization
        self.average_waiting_time = sum([x.getWaittingTime() for x in self.all_proccess]) / len(self.all_proccess)
        self.average_turnaround_time = sum([x.getTurnaroundTime() for x in self.all_proccess]) / len(self.all_proccess)
        self.average_response_time = sum([x.getResponseTime() for x in self.all_proccess]) / len(self.all_proccess)
        self.throughput = len(self.all_proccess)/ self.time
        self.cpu_utilization =  self.total_burst_time/self.time

        #print all CPU variables
        print ("SJF:")
        print ("Avg. W.T.: ", self.average_waiting_time)
        print ("Avg. T.T.: ", self.average_turnaround_time)
        print ("Avg. R.T: ", self.average_response_time)
        print ("Throughput: ", self.throughput)
        print ("CPU Utilization: ", self.cpu_utilization)
        return self.plot("SJF")

    def RR(self):
        sorted_on_arrival_time = Queue(maxsize=len(self.all_proccess))
        #ititial time and burst_time 
        self.time = 0
        self.total_burst_time = 0
        

        sorted_on_arrival_time = self.all_proccess[:]
        sorted_on_arrival_time.sort(key = lambda c: c.arrival_time, reverse= False)
        
        
        while (not self.ready_queue.empty() or len(sorted_on_arrival_time)!=0):
            
            if (self.ready_queue.empty()):
                p = sorted_on_arrival_time[0]
                self.time = p.arrival_time
                self.ready_queue.put(p)
                sorted_on_arrival_time.remove(p)
            
                    
                    
            p = self.ready_queue.get()
                
            if (p.getRemainingTime() > 5):
                running_frame = [self.time]
                self.time = p.run(self.time, 5)
                running_frame += [self.time, "p" + '{}'.format(p.identity)]
                self._running_sequence.append(running_frame)
                self.total_burst_time = self.total_burst_time + 5
            else:
                running_frame = [self.time]
                self.time = p.run(self.time, p.getRemainingTime())
                running_frame += [self.time, "p" + '{}'.format(p.identity)]
                self._running_sequence.append(running_frame)
                self.total_burst_time += p.getRemainingTime()
     
            tmp = sorted_on_arrival_time[:]
            for process in tmp:
                if (process.arrival_time<=self.time):
                    self.ready_queue.put(process)
                    sorted_on_arrival_time.remove(process)
            if(not p.isFinished()):
                self.ready_queue.put(p)

        #printAllProcess()

        # evaluate the CPU variables AWT, ATT, ART, Throughput, Utilization
        self.average_waiting_time = sum([x.getWaittingTime() for x in self.all_proccess]) / len(self.all_proccess)
        self.average_turnaround_time = sum([x.getTurnaroundTime() for x in self.all_proccess]) / len(self.all_proccess)
        self.average_response_time = sum([x.getResponseTime() for x in self.all_proccess]) / len(self.all_proccess)
        self.throughput = len(self.all_proccess)/ self.time
        self.cpu_utilization =  self.total_burst_time/self.time

        #print all CPU variables
        print ("RR:")
        print ("Avg. W.T.: ", self.average_waiting_time)
        print ("Avg. T.T.: ", self.average_turnaround_time)
        print ("Avg. R.T: ", self.average_response_time)
        print ("Throughput: ", self.throughput)
        print ("CPU Utilization: ", self.cpu_utilization)
        return self.plot("RR")

    def SRT(self):
        #ititial time and burst_time 
        self.time = 0
        self.total_burst_time = 0

        sorted_on_arrival_time = self.all_proccess[:]
        sorted_on_arrival_time.sort(key = lambda c: c.arrival_time, reverse= False)
        
        sorted_on_burst_time = []

        while (len(sorted_on_arrival_time) != 0 or len(sorted_on_burst_time) != 0):
            tmp = sorted_on_arrival_time[:]
            for p in tmp:
                if (p.arrival_time <= self.time):
                    sorted_on_burst_time.append(p)
                    sorted_on_arrival_time.remove(p)
                if (p.arrival_time > self.time):
                    next_arrival_time = p.arrival_time
                    break
            
            sorted_on_burst_time.sort(key = lambda c: c.burst_time, reverse= True)

            if (len(sorted_on_burst_time) == 0):
                self.time = next_arrival_time
                continue    
            else:
                p = sorted_on_burst_time.pop()
                running_frame = [self.time]
                self.time = p.run(self.time, 1)
                running_frame += [self.time, "p" + '{}'.format(p.identity)]
                if (len(self._running_sequence) == 0 or self._running_sequence[-1][2] != running_frame[2]):
                    self._running_sequence.append(running_frame)
                else:
                    self._running_sequence[-1][1] = running_frame[1]

                if (not p.isFinished()):
                    sorted_on_burst_time.append(p)
                self.total_burst_time += 1
                

        #printAllProcess()

        # evaluate the CPU variables AWT, ATT, ART, Throughput, Utilization
        self.average_waiting_time = sum([x.getWaittingTime() for x in self.all_proccess]) / len(self.all_proccess)
        self.average_turnaround_time = sum([x.getTurnaroundTime() for x in self.all_proccess]) / len(self.all_proccess)
        self.average_response_time = sum([x.getResponseTime() for x in self.all_proccess]) / len(self.all_proccess)
        self.throughput = len(self.all_proccess)/ self.time
        self.cpu_utilization =  self.total_burst_time/self.time

        #print all CPU variables
        print ("SRT:")
        print ("Avg. W.T.: ", self.average_waiting_time)
        print ("Avg. T.T.: ", self.average_turnaround_time)
        print ("Avg. R.T: ", self.average_response_time)
        print ("Throughput: ", self.throughput)
        print ("CPU Utilization: ", self.cpu_utilization)
        return self.plot("SRT")

    def printAllProcess(self) :
        # print all process attributes
        for process in self.all_proccess:
            print (process)
            print (process.start_time)
            print (process.end_time)
            print ("ResponseTime: " , process.getResponseTime())
            print ("WatingTime: " , process.getWaittingTime())
            print ("TurnAroundTime: " , process.getTurnaroundTime())
            print ("==========================")
    
    def getRunningSequence(self):
        return self._running_sequence

    def plot(self, algo_name):
        cats = {}
        colormapping = {}
        p_name = []
        p_num = []
        i = 0
        for p in self.all_proccess:
            cats["p" + '{}'.format(p.identity)] = i
            colormapping["p" + '{}'.format(p.identity)] = "C" + '{}'.format(i % 10)
            p_name.append("p" + '{}'.format(p.identity))
            p_num.append(i)
            i += 1

        verts = []
        colors = []
        for d in self._running_sequence:
            v =  [(d[0], cats[d[2]]-.45),
                  (d[0], cats[d[2]]+.45),
                  (d[1], cats[d[2]]+.45),
                  (d[1], cats[d[2]]-.45),
                  (d[0], cats[d[2]]-.45)]
            verts.append(v)
            colors.append(colormapping[d[2]])

        bars = PolyCollection(verts, facecolors=colors)

        fig, ax = plt.subplots()
        fig.canvas.set_window_title(algo_name)
        ax.set_xlabel("Time (ms)")
        #ax.set_xlim(0,self.time)
        plt.xticks([k for k in range(self.time + 1)])
        ax.add_collection(bars)
        ax.autoscale()

        ax.set_yticks(p_num)
        ax.set_yticklabels(p_name)
        return plt


process = []
number_of_process = int(input(""))
for i in range(number_of_process):
    str = input()
    str_list = str.split(" ") 
    process.append(Process(i+1,int (str_list[0]), int(str_list[1]), int(str_list[2])))

cpu1 = CPU(process)
cpu2 = CPU(process)
cpu3 = CPU(process)
cpu4 = CPU(process)

SJF = threading.Thread(target = cpu2.SJF())
FCFS = threading.Thread(target = cpu1.FCFS())
RR = threading.Thread(target = cpu3.RR())
SRT = threading.Thread(target = cpu4.SRT())

SJF.start()
FCFS.start()
RR.start()
SRT.start()

FCFS.join()
SJF.join()
RR.join()
SRT.join()

print("FCFS: ", cpu1.getRunningSequence())
print("SJF: ", cpu2.getRunningSequence())
print("RR: ", cpu3.getRunningSequence())
print("SRT: ", cpu4.getRunningSequence())
