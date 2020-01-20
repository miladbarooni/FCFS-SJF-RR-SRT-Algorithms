from tkinter import *
from tkinter import scrolledtext
from tkinter import W, E
from tkinter.ttk import Separator, Style
from tkinter import filedialog
from multiprocessing.connection import Client

filename = ""
address = ('localhost', 6000)
conn = Client(address, authkey='secret password')
def send_file_name(filename):
    conn.send(filename)





def clicked_on_ok():
    filename =  filedialog.asksaveasfilename(initialdir = "/home/milord",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
    send_file_name(filename)
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

button1 = Button(window, text="Browse", command=clicked_on_ok)
button1.grid(row=1, column=2)

sep = Separator(window, orient=HORIZONTAL)
sep.grid(column=0, row=2,columnspan=8, sticky="ew", pady=20)

label3 = Label(window, text="You can enter your process here (in a right format)")
label3.grid(row=3, column=1, pady=10)

txt = scrolledtext.ScrolledText(window,width=40,height=10)
txt.grid(row=4, column=0, columnspan=2, padx=10)

exit_button = Button(window, text="Exit")
exit_button.grid(row=5, column=5)


ok_button = Button(window, text="Ok")
ok_button.grid(row=5, column=6, padx=4)
window.mainloop()

conn.close()