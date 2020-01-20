from tkinter import *
from tkinter import scrolledtext
from tkinter import W, E
from tkinter.ttk import Separator, Style
from tkinter import filedialog
from multiprocessing.connection import Client
from functools import partial
import csv
import time

address = ('localhost', 6000)
conn = Client(address, authkey=b'secret password')


def send_file_name():
    text = txtFrame.get("1.0", END)
    if (text[0] in "0123456789"):
        input_list = text.split("\n")
        for input in input_list:
            if (input == ''):
                input_list.remove(input)
        # print (input_list)
        input_list.pop()
        with open('inputs.csv', mode='w') as csv_file:
            fieldnames = ['process_id', 'arrival_time', 'burst_time','io_time']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            writer.writeheader()
            for row in input_list:
                row_list = row.split(" ")
                writer.writerow({'process_id': row_list[0], 'arrival_time': row_list[1], 'burst_time': row_list[2], 'io_time': row_list[3]})  
        
        conn.send("/home/milord/OS_Project/FCFS-SJF-RR-SRT-Algorithms/inputs.csv")
    else:
        conn.send(filename)
    
    conn.close()
    open_pickle_file = True
    while (open_pickle_file):
        try:
            cpus_file = open('cpus.obj', 'r') 
            cpus = pickle.load(cpus_file) 
            open_pickle_file = False
        except:
            time.sleep(1)
    print (cpus)
            
        

def clicked_on_browse():
    global filename
    filename =  filedialog.askopenfilename(initialdir = "/home/milord/OS_Project",title = "Select file",filetypes = (("csv files","*.csv"),("all files","*.*")))
    # print(filename)
filename = ""

window = Tk()
window.geometry('550x400')
window.title("Operating System Project")

#set the column and row configure
window.columnconfigure(0, pad=3)
window.columnconfigure(1, pad=3)
window.columnconfigure(2, pad=3)
window.columnconfigure(3, pad=3)
window.columnconfigure(4, pad=3)
window.columnconfigure(5, pad=3)

window.rowconfigure(0, pad=3)
window.rowconfigure(1, pad=3)
window.rowconfigure(2, pad=3)
window.rowconfigure(3, pad=3)
window.rowconfigure(4, pad=3)
window.rowconfigure(5, pad=3)
window.rowconfigure(6, pad=3)
window.rowconfigure(7, pad=3)

#lable to describe choose the csv file
label1 = Label(window, text="You can choose a csv file")
label1.grid(row=0, column=0, columnspan=2, padx = 10, sticky="w", pady=20)

label2 = Label(window, text="Choose your file ...")
label2.grid(row=1, column=1)

button1 = Button(window, text="Browse", command=clicked_on_browse)
button1.grid(row=1, column=2)

sep = Separator(window, orient=HORIZONTAL)
sep.grid(column=0, row=2,columnspan=8, sticky="ew", pady=20)

label3 = Label(window, text="You can enter your process here (in a right format)")
label3.grid(row=3, column=1, pady=10)

txtFrame = scrolledtext.ScrolledText(window,width=40,height=10)
txtFrame.grid(row=4, column=0, columnspan=2, padx=10)

exit_button = Button(window, text="Exit", command=window.quit)
exit_button.grid(row=5, column=5)


ok_button = Button(window, text="Ok", command=send_file_name)
ok_button.grid(row=5, column=6, padx=4)

window.mainloop()

