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

import matplotlib
matplotlib.use("TkAgg")

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import numpy as np


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
        
        for F in (StartPage, ExpNumPg, ExpSelPg, TimeSelPg, ConfirmPg, InsertPg, StimPrepPg, ExpFinishPg, PageTest, PageTen):

            frame = F(container, self)

            self.frames[F] = frame 

            frame.grid(row=0, column=0, sticky="nsew") #other choice than pack. Sticky alignment + stretch

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise() #raise to front
    def show_frameFish(self, cont):

        frame = self.frames[cont]
        #camera.start_preview(fullscreen=False, window=(250,0,1000,1000)) #this line starts the preview. TODO: insert coordinates and resize preview
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
  
  #conformation -> stim prep
    def show_frameDelta(self, cont):
        frame = self.frames[cont]
        frame.gettext()
        frame.tkraise() #raise to front
        
    #stim prep -> start imaging
    def show_frameEcho(self, cont,):
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
	camera.start_preview(fullscreen=False, window=(250,0,1000,1000))
	#sleep(.8)
	
	frame.tkraise() #raise to front
	
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

        nonebutton = ttk.Radiobutton(self, text="None", variable = "ExpOption", value = 0, command = lambda: self.qfb(0)) #indicatoron = 0)
        thermobutton = ttk.Radiobutton(self, text="Thermotaxis", variable = "ExpOption", value = 1, command = lambda: self.qfb(1)) #indicatoron = 0)
        chemobutton = ttk.Radiobutton(self, text="Chemotaxis", variable = "ExpOption", value = 2, command = lambda: self.qfb(2)) #indicatoron = 0)
        photobutton = ttk.Radiobutton(self, text="Phototaxis", variable = "ExpOption", value = 3, command = lambda: self.qfb(3)) #indicatoron = 0)
	
	nonebutton.grid(row=2, column= 3, sticky="nsew")
        thermobutton.grid(row=3, column= 3, sticky="nsew")
        chemobutton.grid(row=4, column= 3, sticky="nsew")
        photobutton.grid(row=5, column= 3, sticky="nsew")
        
    def qfb(self, ExpOptionChosen): #stores the selection
        self.userexpchoice = str(ExpOptionChosen)



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
        
        	button2 = ttk.Button(self, text="Next", command=lambda: controller.show_frameFish(InsertPg)) #Insert worms
        	button2.grid(row=7, column= 10, sticky="e")

        def label2confirm(self, expnumber):
            self.label2.configure(text = "Experiment number:" + str(expnumber))

        def label3confirm(self, exptype):
	    	words = str()
	    	if exptype == "0":
    			words = "None"
    		elif exptype == "1":
    			words = "Thermotaxis"
		elif exptype == "2":
    			words = "Chemotaxis"
		elif exptype == "3":
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
        
        button2 = ttk.Button(self, text="Next", command=lambda: controller.show_frameDelta(StimPrepPg)) #prepstimuli
        button2.grid(row=7, column= 10, sticky="e")
        
        self.totaltimetext = tk.Label(self, text = "", font=LARGE_FONT) 
        self.totaltimetext.grid(row = 1, column = 0, sticky="w")
        
        #Live preview of worms being inserted
	
    

        
class StimPrepPg(tk.Frame):
    """
    Instruct students to prepare stimuli
    
    check expchoice to see if need to insert stimuli
    Key: 0 = none; 1 = thermo; 2 = chemo; 3 = photo     
    
    """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.label1 = tk.Label(self, text="", font=LARGE_FONT) #create object
        self.label1.grid(row=0, column=5, columnspan=100) #grid object into window
    

        
        label2 = tk.Label(self, text="Press 'Start' to begin experiment", font=LARGE_FONT) #create object
        label2.grid(row=3, column=5, columnspan=100) #grid object into window
        
        
        button1 = ttk.Button(self, text="Back to\nInsert Worms", command=lambda: controller.show_frame(InsertPg)) #create a button to return to InsertPg
        button1.grid(row=7, column= 0, sticky="w")
        
        button2 = ttk.Button(self, text="Start", command=lambda: controller.show_frameEcho(ExpFinishPg)) #Start Experiment and raise experiment finished page
        button2.grid(row=7, column= 10, sticky="e")
    #Key: 0 = none; 1 = thermo; 2 = chemo; 3 = photo       
    def gettext(self):
        if Appa.exptype == "0" or Appa.exptype == "3":
        	words = "Ready"
        elif Appa.exptype == "1" or Appa.exptype == "2":
        	words = "Prepare/Insert Stimuli"
        else:
        	words = "guciiiiiii"
        self.label1.configure(text = words)

class ExpFinishPg(tk.Frame):
    """
    Experiment capture
    Allow user to go directly into data analysis or return to main menu
    
    Appa.expnumber
    Appa.exptype
    Appa.exptime
    
    
    check expchoice to see if need to turn on light
    
    none = 0
    ther = 1
    chem = 2
    photo = 3
    """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Experiment Finished", font=LARGE_FONT) #create object
        label.pack()
        #label.grid(row=0, column=5, columnspan=100) #grid object into window
        
    	button1 = ttk.Button(self, text="New Experiment", command=lambda: controller.show_frame(ExpNumPg)) #create a button to start a new experiment       
    	button1.pack()

        button2 = ttk.Button(self, text="Review This\nExperiment's Data", command=lambda: controller.show_frame(PageTest)) #create a button to start a new experiment 
        button2.pack()
    
class PageTest(tk.Frame):
	
	"""Data review page. Let's user choose whether or not to keep data"""
	
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		label = tk.Label(self, text = "Graph Page!", font=LARGE_FONT)
		label.grid(row = 0, column=1, columnspan = 2, sticky="NSEW")
		
		button1 = ttk.Button(self,text="Back", command=lambda: controller.show_frame(ExpFinishPg))
		button1.grid(row=1, column = 0)
		

		f = Figure(figsize = (8,8), dpi=100)#define figure		
		i=1
		for picture in  os.listdir("/home/pi/Desktop/PictureFolder/"):
			a = f.add_subplot(6,1,i) #add subplot RCP. Pth pos on grid with R rows and C columns
			img = mpimg.imread("/home/pi/Desktop/PictureFolder/" + picture) #read in image
			a.imshow(img) #Renders image
			i+=1
			
		#add canvas which is what we intend to render graph to and fill it with figure
		canvas = FigureCanvasTkAgg(f, self) 
		canvas.draw() #raise canvas
		canvas.get_tk_widget().grid(row=1, column=1, sticky="NS") #Fill options: BOTH, X, Y Expand options:  


		#Add scrollbar
		scrollbar = tk.Scrollbar(self)
		scrollbar.config(command=canvas.get_tk_widget().yview)
#		canvas.get_tk_widget().config(scrollregion=(canvas.get_tk_widget().bbox("all")))
		canvas.get_tk_widget().config(scrollregion=(0,0,100,400))
		scrollbar.grid(row=0, column=3, sticky="NS", rowspan = 2)
		canvas.get_tk_widget().config(yscrollcommand=scrollbar.set)

class PageTen(tk.Frame):

    """Allows data retrieval"""

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Data Review", font=LARGE_FONT) #create object
        label.pack(pady=10, padx=10) #pack object into window
        
        button1 = ttk.Button(self, text="Back to Home", command=lambda: controller.show_frame(StartPage)) #create a button to return to home screen
        button1.pack()
	
	self.yeehaw = []
	List1=Listbox(self)
	for item in ["zero","one", "two" ]:
		List1.insert(END, item)
		self.yeehaw.append(item)
	List1.pack()
	b = ttk.Button(self, text="Selectionnn", command = lambda List1=List1: self.asdf(List1))
	b.pack()

    def asdf(self, List1):
	#items = map(int, List1.curselection())
	#print(self.yeehaw[int(items)])
	#print(type(List1.curselection()[0]))


app = BehaviorBox()
app.geometry("1280x720")
app.mainloop()






