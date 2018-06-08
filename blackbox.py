"""



It's Friday.

Andrew Huynh '20
Summer 2018

"""
try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

import ttk

from time import *


LARGE_FONT = ("Verdana", 12)




class BehaviorBox(tk.Tk):

    """ Base line code to initalize everything """


    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        
        tk.Tk.wm_title(self, "Behavior Box")
        
        container = tk.Frame(self) #Define frame/edge of window
        container.pack(side="top", fill="both", expand=True) #fill will fill space you have allotted pack. Expand will take up all white space.
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1) #0 sets minimum size weight sets priority

        self.frames = {}
        
        for F in (StartPage, PageOne, PageTwo, PageTen):

            frame = F(container, self)

            self.frames[F] = frame 

            frame.grid(row=0, column=0, sticky="nsew") #other choice than pack. Sticky alignment + stretch

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise() #raise to front


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Start Page", font=LARGE_FONT) #create object
        label.pack(pady=10, padx=10) #pack object into window

        button1 = ttk.Button(self, text="New Experiment", command=lambda: controller.show_frame(PageOne)) #create a button to start a new experiment       
        button1.pack()

        button2 = ttk.Button(self, text="Data Retrieval", command=lambda: controller.show_frame(PageTen)) #create a button to start a new experiment 
        button2.pack()

class PageOne(tk.Frame):

    """Allows experiement selection"""

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="New Experiement", font=LARGE_FONT) #create object
        label.pack(pady=10, padx=10) #pack object into window
        
        button1 = ttk.Button(self, text="Back to Home", command=lambda: controller.show_frame(StartPage)) #create a button to start a new experiment) 
        button1.pack()

        button2 = ttk.Button(self, text="Next", command=lambda: controller.show_frame(PageTwo)) #create a button to continue to exp time
        button2.pack()

class PageTwo(tk.Frame):

    """Allows run time selection"""

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Enter Run Time", font=LARGE_FONT) #create object
        label.grid(row=1, column=6, columnspan=100) #pack object into window
        self.grid_columnconfigure(6, minsize=20)
        self.grid_rowconfigure(2, minsize=20) 
        self.grid_rowconfigure(3, minsize=20) 
        self.grid_rowconfigure(4, minsize=20) 
        print("hello world")
        self.totaltime = str()
        
        button1 = ttk.Button(self, text="Back to Experiment Selection", command=lambda: controller.show_frame(PageOne)) #create a button to return to experiment selection
        button1.grid(row=7, column= 6, columnspan=100)

        """ Number Pad """
        btn_numbers = [ '7', '8', '9', '4', '5', '6', '1', '2', '3', '0', 'x', 'y']
        r = 1
        c = 5
        
        
        self.totaltimenumber = tk.Label(self, text = "", font=LARGE_FONT)
        self.totaltimenumber.grid(row = 10, column = 10)
         

        for num in btn_numbers:
            self.num = ttk.Button(self, text=num, width=5, command=lambda b = num: self.click(b))
            self.num.grid(row=r, column=c, sticky= "nsew")
            c += 1
            if c > 7:
                c = 5
                r += 1


    def click(self, z):
        currentnum = self.totaltime
        if currentnum == '0':
            self.totaltime = z
            print("newws %s" % self.totaltime)
        if z == 'x':
            self.totaltime = currentnum[:-1]
        else:
            self.totaltime = currentnum + z
        self.totaltimenumber.configure(text = "Run time: %s" % self.totaltime)


class PageTen(tk.Frame):

    """Allows data retrieval"""

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Data Retrieval", font=LARGE_FONT) #create object
        label.pack(pady=10, padx=10) #pack object into window
        
        button1 = ttk.Button(self, text="Back to Home", command=lambda: controller.show_frame(StartPage)) #create a button to return to home screen
        button1.pack()







app = BehaviorBox()
app.geometry("1280x720")
app.mainloop()


