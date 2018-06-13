"""

Andrew Huynh '20
Summer 2018
Behavior Box Project

"""
try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
	from Tkinter import *
	import ttk
except:
	from tkinter import ttk
	from tkinter import *
	from tkinter.ttk import *
#import ttk as ttk
import tkMessageBox
import os
from time import *
from picamera import PiCamera

camera = PiCamera()

LARGE_FONT = ("Verdana", 12)
SMALL_FONT = ("Verdana", 8)





class Experiment():
	
	def __init__(self, expnumber):
		self.expnumber = expnumber
		self.exptype = str()
		self.exptime = int()
		self.capturerate=5
	def set_number(self, number):
		self.expnumber = str(number)
	def set_type(self, exptype):
		self.exptype = str(exptype)
	def set_exptime(self, totaltime):
		self.exptime = int(totaltime)
	
Appa = Experiment(str(40))

class BehaviorBox(tk.Tk, Experiment):

    """ Base line code to initialize everything """


    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        
        tk.Tk.wm_title(self, "Behavior Box")
        
        container = tk.Frame(self) #Define frame/edge of window
        container.pack(side="top", fill="both", expand=True) #fill will fill space you have allotted pack. Expand will take up all white space.
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1) #0 sets minimum size weight sets priority

        self.frames = {}
        
        for F in (StartPage, ExpNumPg, ExpSelPg, TimeSelPg, ConfirmPg, InsertPg, StimPrepPg, ExpRunPg, PageTen):

            frame = F(container, self)

            self.frames[F] = frame 

            frame.grid(row=0, column=0, sticky="nsew") #other choice than pack. Sticky alignment + stretch

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise() #raise to front
   
   #Save experiment number -> experiment type
    def show_frameAlpha(self, cont, usernumchoice):
        frame = self.frames[cont]
        Appa.set_number(usernumchoice) #create experiment object
        frame.tkraise() #raise to front
    
    #Save experiment type -> experiment time
    def show_frameBravo(self, cont, userexpchoice):
        frame = self.frames[cont]
        Appa.set_type(userexpchoice) #set experiment object's type to user's choice
        frame.tkraise() #raise to front
    
    #Save time choice -> confirmation
    def show_frameCharlie(self, cont, usertimechoice):
        frame = self.frames[cont]
        Appa.set_exptime(usertimechoice) #set experiment object's time to user's choice
        frame.label2confirm(Appa.expnumber)
        frame.label3confirm(Appa.exptype)
	frame.label4confirm(Appa.exptime)
        frame.tkraise() #raise to front
  
    #stim prep -> start imaging
    def show_frameDelta(self, cont,):
        frame = self.frames[cont]
        savetofile = "/home/pi/Desktop/Exp" + str(Appa.expnumber)
	ticker = 0
	while True:
    		if not os.path.exists(savetofile):
        		os.makedirs(savetofile)
        		break
    		else: #duplicated file
			ticker += 1
        		savetofile = savetofile + "(" + str(ticker) + ")"
	camera.start_preview(fullscreen=False, window=(0,0,1000,1000))
	sleep(2)
	
	#frame.tkraise() #raise to front
	
	#Image capturing
	for i in range(int(Appa.exptime/Appa.capturerate+1)):
    		camera.capture("/home/pi/Desktop/Exp" + str(Appa.expnumber) + "/image" + str(i) + ".jpg")

		if i != int(Appa.exptime/Appa.capturerate):
			sleep(Appa.capturerate)
	camera.stop_preview()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Start Page", font=LARGE_FONT) #create object
        label.pack(pady=10, padx=10) #pack object into window

        button1 = ttk.Button(self, text="New Experiment", command=lambda: controller.show_frame(ExpNumPg)) #create a button to start a new experiment       
        button1.pack()

        button2 = ttk.Button(self, text="Data Retrieval", command=lambda: controller.show_frame(PageTen)) #create a button to start a new experiment 
        button2.pack()

class ExpNumPg(tk.Frame, Experiment):

    """Gets user input for experiment number for name file todo: check to see if expnum taken"""
        

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Enter Experiment Number", font=LARGE_FONT) #create object
        label.grid(row=0, column=0, columnspan=100) #pack object into window
        self.grid_columnconfigure(1, minsize=20)
        self.grid_rowconfigure(2, minsize=20) 
        self.grid_rowconfigure(3, minsize=20) 
        self.grid_rowconfigure(4, minsize=20) 

	self.usernumchoice = str()
	
        button1 = ttk.Button(self, text="Back to\nMain Menu", command=lambda: controller.show_frame(StartPage)) #create a button to return to main menu
        button1.grid(row=7, column= 0, rowspan=100, sticky="nsew")
        
        button2 = ttk.Button(self, text="Next", command=lambda: controller.show_frameAlpha(ExpSelPg, self.usernumchoice)) #create a button to experiment type
        button2.grid(row=7, column= 6, columnspan=100, sticky="e")
        
        """Creates display for number inputed"""
        self.usernumtext = tk.Label(self, text = "", font=LARGE_FONT) 
        self.usernumtext.grid(row = 1, column = 0, sticky="w")
        self.usernumtext.configure(text = "Experiment Number: %.5s" % self.usernumchoice)

        """ Number Pad """
        btn_numbers = [ '7', '8', '9', '4', '5', '6', '1', '2', '3', ' ', '0', 'x'] #create list of numbers to be displayed
        r = 3
        c = 2
  

        for num in btn_numbers:
            if num == ' ':
                self.num = ttk.Button(self, text=num, width=5)
                self.num.grid(row=r, column=c, sticky= "nsew")
                c += 1

            else: 
                self.num = ttk.Button(self, text=num, width=5, command=lambda b = num: self.click(b))
                self.num.grid(row=r, column=c, sticky= "nsew")
                c += 1
            if c > 4:
                c = 2
                r += 1
    """method to save user inputs and display them"""
    def click(self, z):
        currentnum = self.usernumchoice
        if currentnum == '0':
            self.usernumchoice = z
        if z == 'x':
            self.usernumchoice = currentnum[:-1]
        else:
            if len(currentnum) > 2:
                tkMessageBox.showwarning("Error", "Number too long")
            else:
                self.usernumchoice = currentnum + z
        self.usernumtext.configure(text = "Experiment Number:  %.5s" % self.usernumchoice)


class ExpSelPg(tk.Frame, Experiment):

    """Allows experiment selection"""
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Select Experiment Type", font=LARGE_FONT) #create object
        label.grid(row=0, column=0, columnspan=100) #pack object into window
        
        self.userexpchoice = int()
        
        
	button1 = ttk.Button(self, text="Back to\nMain Menu", command=lambda: controller.show_frame(StartPage)) #create a button to return to run time
        button1.grid(row=7, column= 0, sticky="w")
        
        button2 = ttk.Button(self, text="Next", command=lambda: controller.show_frameBravo(TimeSelPg, self.userexpchoice)) #create a button to time entry
        button2.grid(row=7, column= 10, sticky="e")

        nonebutton = ttk.Radiobutton(self, text="None", variable = self.userexpchoice, value = 0) #indicatoron = 0)
        thermobutton = ttk.Radiobutton(self, text="Thermotaxis", variable = self.userexpchoice, value = 1) #indicatoron = 0)
        chemobutton = ttk.Radiobutton(self, text="Chemotaxis", variable = self.userexpchoice, value = 2) #indicatoron = 0)
        photobutton = ttk.Radiobutton(self, text="Photootaxis", variable = self.userexpchoice, value = 3) #indicatoron = 0)
	
	nonebutton.grid(row=2, column= 3, sticky="nsew")
        thermobutton.grid(row=3, column= 3, sticky="nsew")
        chemobutton.grid(row=4, column= 3, sticky="nsew")
        photobutton.grid(row=5, column= 3, sticky="nsew")
        
        """
        self.button3 = ttk.Button(self, text="Thermotaxis", command=lambda b = "t": self.exptype(b)) #create a button to thermotaxis
        self.button3.grid(row=2, column= 3, sticky="nsew")
        
        self.button4 = ttk.Button(self, text="Phototaxis", command=lambda b = "p": self.exptype(b)) #create a button to phototaxis
        self.button4.grid(row=3, column= 3, sticky="nsew")
        
        self.button5 = ttk.Button(self, text="Chemotaxis", command=lambda b = "c": self.exptype(b)) #create a button to chemotaxis
        self.button5.grid(row=4, column= 3, sticky="nsew")
        
        self.button6 = ttk.Button(self, text="None", command=lambda b = "n": self.exptype(b)) #create a button to control
        self.button6.grid(row=5, column= 3, sticky="nsew")
        """
        self.totaltimetext = tk.Label(self, text = "", font=LARGE_FONT) 
        self.totaltimetext.grid(row = 1, column = 0, sticky="w")

    # function to store exp type
    def exptype(self, expchoice):
    	if expchoice == "n":
    		self.userexpchoice = 0
    		self.button6.config(relief=SUNKEN)
    	elif expchoice == "t":
    		self.userexpchoice = 1
    		self.button3.config(relief=SUNKEN)
    	elif expchoice == "c":
    		self.userexpchoice = 2
    		self.button5.config(relief=SUNKEN)
    	elif expchoice == "p":
    		self.userexpchoice = 3
    		self.button4.config(relief=SUNKEN)

    



class TimeSelPg(tk.Frame):

    """Allows run time selection"""
        
    runtime = 0 # initialize class runtime variable
    
   

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Enter Run Time (seconds)", font=LARGE_FONT) #create object
        label.grid(row=0, column=0, columnspan=100) #pack object into window
        self.grid_columnconfigure(1, minsize=20)
        self.grid_rowconfigure(2, minsize=20) 
        self.grid_rowconfigure(3, minsize=20) 
        self.grid_rowconfigure(4, minsize=20) 
        
        self.totaltime = str()


        button1 = ttk.Button(self, text="Back to\nExperiment Selection", command=lambda: controller.show_frame(ExpSelPg)) #create a button to return to experiment selection
        button1.grid(row=7, column= 0, rowspan=100, sticky="nsew")
        
        button2 = ttk.Button(self, text="Next", command=lambda: controller.show_frameCharlie(ConfirmPg, self.totaltime)) #create a button to InsertPg
        button2.grid(row=7, column= 6, columnspan=100, sticky="e")
        
        """Creates display for time inputed"""
        self.totaltimetext = tk.Label(self, text = "", font=LARGE_FONT) 
        self.totaltimetext.grid(row = 1, column = 0, sticky="w")
        self.totaltimetext.configure(text = "Run time: %.5s" % self.totaltime)

        """ Number Pad """
        btn_numbers = [ '7', '8', '9', '4', '5', '6', '1', '2', '3', ' ', '0', 'x'] #create list of numbers to be displayed
        r = 3
        c = 2
  

        for num in btn_numbers:
            if num == ' ':
                self.num = ttk.Button(self, text=num, width=5)
                self.num.grid(row=r, column=c, sticky= "nsew")
                c += 1

            else: 
                self.num = ttk.Button(self, text=num, width=5, command=lambda b = num: self.click(b))
                self.num.grid(row=r, column=c, sticky= "nsew")
                c += 1
            if c > 4:
                c = 2
                r += 1
    """method to save user inputs and display them"""
    def click(self, z):
        currentnum = self.totaltime
        if currentnum == '0':
            self.totaltime = z
        if z == 'x':
            self.totaltime = currentnum[:-1]
        else:
            if len(self.totaltime) > 2:
                tkMessageBox.showwarning("Error", "Time too long")
            else:
                self.totaltime = currentnum + z
        self.totaltimetext.configure(text = "Run time:  %.5s" % self.totaltime)

    
class ConfirmPg(tk.Frame, Experiment):
	
	""" Displays chosen parameters for user to confirm"""
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent) 
        	self.label1 = tk.Label(self, text="Chosen Parameters", font=LARGE_FONT) #create object
        	self.label1.grid(row=0, column=5, columnspan=100) #grid object into window
        	
        	
        	self.label2 = tk.Label(self, text="", font=SMALL_FONT) #create object
        	self.label2.grid(row=2, column=5) #grid object into window
        
		self.label3 = tk.Label(self, text="", font=SMALL_FONT) #create object
        	self.label3.grid(row=4, column=5) #grid object into window
		
		self.label4 = tk.Label(self, text="", font=SMALL_FONT) #create object
        	self.label4.grid(row=5, column=5) #grid object into window


        	button1 = ttk.Button(self, text="Back to\nRun time", command=lambda: controller.show_frame(TimeSelPg)) #create a button to return to run time
        	button1.grid(row=7, column= 0, sticky="w")
        
        	button2 = ttk.Button(self, text="Next", command=lambda: controller.show_frame(InsertPg)) #Insert worms
        	button2.grid(row=7, column= 10, sticky="e")

        def label2confirm(self, expnumber):
            self.label2.configure(text = "Experiment number:" + str(expnumber))

        def label3confirm(self, exptype):
	    	words = str()
	    	if exptype == 0:
    			words = "None"
    		elif exptype == 1:
    			words = "Thermotaxis"
		elif exptype == 2:
    			words = "Chemotaxis"
		elif exptype == 3:
			words = "Phototaxis"
		else:
			print(exptype)
			print(type(exptype))
            
		self.label3.configure(text = "Experiment type: " + words)
            	
        def label4confirm(self, exptime):
            self.label4.configure(text = "Run time (s): " + str(exptime))
            

class InsertPg(tk.Frame):
    
    """Instructs user to insert worms"""
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Insert Worms", font=LARGE_FONT) #create object
        label.grid(row=0, column=5, columnspan=100) #grid object into window
        
        label2 = tk.Label(self, text="Select next once worms have settled down", font=SMALL_FONT) #create object
        label2.grid(row=5, column=5, columnspan=100) #grid object into window
        
        button1 = ttk.Button(self, text="Back to\nConfirmation Page", command=lambda: controller.show_frame(ConfirmPg)) #create a button to return to run time
        button1.grid(row=7, column= 0, sticky="w")
        
        button2 = ttk.Button(self, text="Next", command=lambda: controller.show_frame(StimPrepPg)) #prepstimuli
        button2.grid(row=7, column= 10, sticky="e")
        
        self.totaltimetext = tk.Label(self, text = "", font=LARGE_FONT) 
        self.totaltimetext.grid(row = 1, column = 0, sticky="w")
    

        
class StimPrepPg(tk.Frame):
    """
    Prepare stimuli
    expchoice from ExpSelPg
    
    check expchoice to see if need to insert stimuli
    
    none = 0
    ther = 1
    chem = 2
    photo = 3
    """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label1 = tk.Label(self, text="", font=LARGE_FONT) #create object
        label1.grid(row=0, column=5, columnspan=100) #grid object into window
        if Appa.exptype == 0 or 3:
        	words = "Ready"
        elif Appa.exptype == 1 or 2:
        	words = "Prepare/Insert Stimuli"
        else:
        	words = "guciiiiiii"
        label1.configure(text = words)
        
        label2 = tk.Label(self, text="Press 'Start' to begin experiment", font=LARGE_FONT) #create object
        label2.grid(row=3, column=5, columnspan=100) #grid object into window
        
        
        button1 = ttk.Button(self, text="Back to\nInsert Worms", command=lambda: controller.show_frame(InsertPg)) #create a button to return to InsertPg
        button1.grid(row=7, column= 0, sticky="w")
        
        button2 = ttk.Button(self, text="Start", command=lambda: controller.show_frameDelta(ExpRunPg)) #Start Experiment
        button2.grid(row=7, column= 10, sticky="e")

class ExpRunPg(tk.Frame, ExpSelPg, TimeSelPg, ExpNumPg):
    """
    Experiment capture
    
    
    usernumchoice from ExpNumPg
    totaltime from TimeSelPg
    userexpchoice from ExpSelPg
    
    
    check expchoice to see if need to turn on light
    
    none = 0
    ther = 1
    chem = 2
    photo = 3
    """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Experiment running", font=LARGE_FONT) #create object
        label.grid(row=0, column=5, columnspan=100) #grid object into window
    

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

