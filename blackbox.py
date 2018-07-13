"""

Andrew Huynh '20
Summer 2018
Behavior Box Project

"""
try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

import ttk
import tkMessageBox

import os
import shutil
import pickle

from time import *
from picamera import PiCamera

import matplotlib
matplotlib.use("TkAgg")

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.patches import Circle
from matplotlib.patches import Arc

from PIL import ImageTk, Image

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

from pictureanalysis import *

camera = PiCamera()

#Font Sizes
LARGE_FONT = ("Verdana", 36)
MEDIUM_FONT = ("Verdana", 28)
SMALL_FONT = ("Verdana", 24)
TINY_FONT = ("Verdana", 20)
VERYTINY_FONT = ("Verdana", 15)

appheight=400
appwidth=800

xspacer=appheight/80
yspacer=appheight/80




class Experiment():

    def __init__(self):
        self.expnumber = str()
        self.exptype = str()
        self.exptime = int()
        self.savefile = str()
        self.capturerate=2
        self.x = range(4)
        self.iscontrol = False
        self.controly = ["","",""]
        self.expy = []
    def set_number(self, number):
        self.expnumber = str(number)
    def set_type(self, exptype):
        self.exptype = str(exptype)
    def set_exptime(self, totaltime):
        self.exptime = int(totaltime)
    def set_savefile(self, savetofile):
        self.savefile = str(savetofile)


Appa = Experiment()

class BehaviorBox(tk.Tk, Experiment):

    """ Base line code to initialize everything """
    coi = []

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "Behavior Box") #Set window title

        self.container = tk.Frame(self) #Define frame/edge of window
        self.container.pack(side="top", fill="both", expand=True) #Fill will fill space you have allotted pack. Expand will take up all white space.
        self.container.grid_rowconfigure(0, weight=1) #Configure rows/grids. 0 sets minimum size weight sets priority
        self.container.grid_columnconfigure(0, weight=1) 

        self.frames = {}
        for F in (StartPage, ExpNumPg, ExpSelPg, TimeSelPg, ConfirmPg, InsertPg, StimPrepPg, ExpFinishPg, PageTest, DataDelPg, DataAnalysisImagePg, DataAnalysisPg, GraphPage, DataRetrievalType, DataGraphChoice, AnalysisTypeForNone):
            frame = F(self.container, self)
            self.frames[F] = frame 
            frame.grid(row=0, column=0, sticky="nsew") #other choice than pack. Sticky alignment + stretch
        self.show_frame(StartPage)

    #Initalize all pages
    def startfresh(self):
        for F in (StartPage, ExpNumPg, ExpSelPg, TimeSelPg, ConfirmPg, InsertPg, StimPrepPg, DataDelPg):
            frame = F(self.container, self)
            self.frames[F] = frame 
            frame.grid(row=0, column=0, sticky="nsew") #other choice than pack. Sticky alignment + stretch

    #Function to raise frame to the front
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise() #raise to front

    #Main menu -> new experiment. Resets all of Appa's values
    def show_frameAlpha(self, cont):
        #Reset all of experiment-class variables
        Appa.expnumber = str()
        Appa.exptype = str()
        Appa.exptime = int()
        Appa.savefile = str()
        Appa.expy = []
        app.startfresh() #Reinitalize all pages to starting state
        frame = self.frames[cont]
        frame.tkraise() #raise to front

    def show_frameZebra(self, cont):
        frame = self.frames[cont]
        camera.stop_preview()#this line stops the preview. 
        frame.tkraise() #raise to front
    def show_frameFish(self, cont):
        frame = self.frames[cont]
        camera.start_preview(fullscreen=False, window=(0,appheight/4,appwidth,appheight/2)) #this line starts the preview. 
        frame.tkraise() #raise to front

    #Save time choice -> confirmation and updates label values in confirmation based on previous user input
    def show_frameCharlie(self, cont):
        frame = self.frames[cont]
        frame.label2confirm(Appa.expnumber)
        frame.label3confirm(Appa.exptype)
        frame.label4confirm(Appa.exptime)

        frame.tkraise() #raise to front

  #conformation -> stim prep and displays either "Ready" or "Insert stimuli" based on experiment type
    def show_frameDelta(self, cont):
        frame = self.frames[cont]
        frame.gettext() #Displays either "Ready" or "Insert stimuli" based on experiment type
        frame.tkraise() #raise to front

    #stim prep -> start imaging
    def show_frameEcho(self, cont):
        frame = self.frames[cont]
        os.makedirs(Appa.savefile) #Create general folder for experiment 
        os.makedirs(Appa.savefile + "/ExpDataPictures") #Create folder for images from exp
        frame.tkraise() #raise to front

        #camera.start_preview(fullscreen=False, window=(250,0,1000,1000)) yeetyeet
        #Image capturing
        for i in range(int(Appa.exptime/Appa.capturerate+1)):
            camera.capture(Appa.savefile + "/ExpDataPictures/image" + str(i) + ".jpg")
            Appa.expy.append("")
            if i != int(Appa.exptime/Appa.capturerate):
                sleep(Appa.capturerate)
        camera.stop_preview()

    def show_frameFoxtrot(self, cont):
        frame = cont(self.container, self)
        self.frames[cont] = frame 
        frame.grid(row=0, column=0, sticky="nsew") #other choice than pack. Sticky alignment + stretch
        frame.tkraise() #raise to front

    def show_frameFoxtrot2(self, cont):
        result = tkMessageBox.askquestion("Warning", "All progess will be lost.\nProceed anyways?")
        if result == "yes":
            frame = cont(self.container, self)
            self.frames[cont] = frame 
            frame.grid(row=0, column=0, sticky="nsew") #other choice than pack. Sticky alignment + stretch
            frame.tkraise() #raise to front

    #Load Appa object for exp and pull up first image from chosen experiment        	 WHATWHAT
    def show_frameLima(self, cont, chosenexp):
        #create variable to store experiment object

        result = True       
        result2 = True
        global Momo
        Momo = getobject(chosenexp)
        if Momo.iscontrol: #analyzing control 
            if Momo.exptype != "0": #not first time analyzing
                result2 = tkMessageBox.askquestion("Warning", "This control experiment has already\nbeen analyzed as %s.\nChanges may overwrite exisiting data.\nProceed anyways?" % getpreviouslyanalyzed(Momo))
            if result2 != "no":
                frame = self.frames[AnalysisTypeForNone]
                for button in [frame.thermobutton, frame.chemobutton, frame.photobutton]:
                    if getpreviouslyanalyzed(Momo) == button['text']:
                        button.state(["focus","selected"])
                        print(getpreviouslyanalyzed(Momo))
                    else:
                        button.state(["!focus",'!selected'])
                        print(getpreviouslyanalyzed(Momo))
                frame.tkraise()


        else: #not control
            if Momo.expy[0] != "": #already analyzed
                result = tkMessageBox.askquestion("Warning", "The selected experiment has already been analyzed.\nChanges may overwrite exisiting data.\nProceed anyways?")
            if result != "no": 
                frame = cont(self.container, self)
                self.frames[cont] = frame 
                frame.grid(row=0, column=0, sticky="nsew")
                frame.ChangePic(1)
                frame.tkraise() #raise to front

    def show_frameBean(self, cont):
        frame = cont(self.container, self)
        self.frames[cont] = frame 
        frame.grid(row=0, column=0, sticky="nsew")
        frame.ChangePic(1)
        frame.tkraise() #raise to front

    def show_frameMarlin(self, cont):
        frame = self.frames[cont]
        i=0
        savefile = "/home/pi/Desktop/ExperimentFolder/Exp547/"
        numpics = len(os.listdir(Appa.savefile + "ExpDataPictures"))
        frame.imagelist=[]

            
        for picture in  os.listdir(Appa.savefile + "ExpDataPictures"):
            img = Image.open(Appa.savefile+ "ExpDataPictures/image" + str(i) + ".jpg", mode="r") #read in image
            img = img.resize((frame.canvaswidth, frame.canvasheight))
	    imwidth, imheight=img.size
            frame.tempimage = ImageTk.PhotoImage(img)
            frame.imagelist.append(frame.tempimage)
            frame.canvas.create_image(0,(imheight+10)*i,image=frame.imagelist[i],anchor="nw")
            i+=1
        """
        ye = frame.canvas.bbox("all")[3]
        he = frame.canvas.bbox("all")[2]
        for k in range(ye/100):
           frame.canvas.create_text(0, k*100, text=(str(k*100)))
        for w in range(he/100):
            frame.canvas.create_text(w*100, 0, text=(str(w*100)))
	"""

        scrollbar = tk.Scrollbar(frame)
        scrollbar.config(command=frame.canvas.yview)
        frame.canvas.config(scrollregion=(frame.canvas.bbox("all")))

        scrollbar.grid(row=1, column=1, rowspan = 2, sticky="NSEW")
        frame.canvas.config(yscrollcommand=scrollbar.set)

        frame.tkraise()

    def show_frameRhino(self, cont):
        frame = self.frames[cont]
        confirmdiscard(frame)


    #after keep data -> store appa object and reset appa	
    def show_frameStingray(self, cont, obj):
        saveobject(obj)
        frame = self.frames[cont]
        frame.tkraise() #raise to front


    def show_frameShark(self, cont, listofbuttons):
        frame = cont(self.container, self)
        self.frames[cont] = frame 

        ExpsToGraph = []
        expnames = []
        unanalyzedlist = []
        result = True

        #Get list of experiments to plot
        for button in listofbuttons:
            if button.instate(['selected']):
                    ExpsToGraph.append(getobject(button['text']))

        #Check to see if chose an experiment
        if len(ExpsToGraph) == 0: 
                tkMessageBox.showwarning("Error", "No experiments selected") #show warning
        else:
            #Check to see if all experiments selected have been analyzed
            for experiment in ExpsToGraph:
                if experiment.expy[0] == "":
                    unanalyzedlist.append(experiment.expnumber)
                else:
                    experiment.expy = list(map(int, experiment.expy))
                    #plt.plot(range(len(experiment.expy)),experiment.expy, label="Exp" + experiment.expnumber)
                    frame.a.plot(range(len(experiment.expy)),experiment.expy, label="Exp" + experiment.expnumber)
                    expnames.append(experiment.expnumber)

           #If unanalyzed experiments exist warn user
            if len(unanalyzedlist) > 0:
                unanalyzedlist = "Exp" + ", Exp".join(unanalyzedlist)
                result = tkMessageBox.askquestion("Warning", "The following experiments have\nnot been analyzed yet\nand will not be graphed\n\n" +unanalyzedlist+ "\n\nProceed anyways?")

            if result !=  "no":
                graphtitle = "Graph of Exp" + ", Exp".join(expnames)
                frame.grid(row=0, column=0, sticky="nsew") #other choice than pack. Sticky alignment + stretch
                frame.label.configure(text = graphtitle, font=LARGE_FONT)

                frame.a.legend(loc='best', fontsize=15)
                #plt.show()
                frame.canvas.draw() #raise canvas
                frame.tkraise() #raise to front			

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Start Page", font=LARGE_FONT) #Create label object
        label.grid(row=0, column=1, sticky="nsew") #pack label into window

        s = ttk.Style()
        s.configure("my.TButton", font=(SMALL_FONT))

        button1 = ttk.Button(self, text="New Experiment", style='my.TButton', command=lambda: controller.show_frameAlpha(ExpNumPg)) #Create a button to start a new experiment       
        button1.grid(row=1, column=1, sticky="nsew")

        button2 = ttk.Button(self, text="Data Retrieval", style='my.TButton', command=lambda: controller.show_frame(DataRetrievalType)) #Create a button to go to 'data retrieval' page
        button2.grid(row=2, column=1, sticky="nsew")

        button3 = ttk.Button(self, text="Delete Data", style='my.TButton', command=lambda: controller.show_frameFoxtrot(DataDelPg)) #Create a button to go to 'data deletion' page
        button3.grid(row=3, column=1, sticky="nsew")
        for i in range(4):
            self.grid_rowconfigure(i, minsize=100)
        self.grid_columnconfigure(0, minsize=20)
        self.grid_columnconfigure(1, minsize=760)

class ExpNumPg(tk.Frame, Experiment):

    """Gets user input for experiment number for name file"""

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Enter Experiment Number", font=MEDIUM_FONT) #create object
        label.grid(row=0, column=1, columnspan=3, sticky="NSEW") #pack object into window

        s = ttk.Style()
        s.configure("TINYFONT.TButton", font=(TINY_FONT))

        self.grid_rowconfigure(2, minsize=25) 
        self.grid_rowconfigure(7, weight=1)  
        for row in range (3,7):
            self.grid_rowconfigure(row, minsize=50) 
        for column in range(6):
            self.grid_columnconfigure(column, minsize=160, weight=1)
        self.grid_rowconfigure(8, minsize=appheight/3) #Configure rows/grids. 0 sets minimum size weight sets priority

        self.usernumchoice = str()

        button1 = ttk.Button(self, text="Back to\nMain Menu", style='TINYFONT.TButton', command=lambda: controller.show_frame(StartPage)) #create a button to return to main menu
        button1.grid(row=8, column= 0, columnspan=2, rowspan=1, sticky="nsew", padx=xspacer, pady=yspacer)

        button2 = ttk.Button(self, text="Next", style='TINYFONT.TButton', command=lambda: self.checkvalidexpnum(parent, controller)) #create a button to experiment type
        button2.grid(row=8, column= 3, columnspan=2, rowspan=1, sticky="nsew", padx=xspacer, pady=yspacer)

        """Creates display for number inputed"""
        self.usernumtext = tk.Label(self, text = "", font=SMALL_FONT) 
        self.usernumtext.grid(row = 1, column = 1, columnspan = 3, sticky="w")
        self.usernumtext.configure(text = "Experiment Number: %3s" % self.usernumchoice)
        #kitty

        """ Number Pad """
        btn_numbers = [ '7', '8', '9', '4', '5', '6', '1', '2', '3', ' ', '0', 'x'] #create list of numbers to be displayed
        r = 3
        c = 1


        for num in btn_numbers:
            if num == ' ':
                self.num = ttk.Button(self, text=num, width=5)
                self.num.grid(row=r, column=c, sticky= "nsew")
                c += 1

            else: 
                self.num = ttk.Button(self, text=num, width=5, style='TINYFONT.TButton', command=lambda b = num: self.click(b))
                self.num.grid(row=r, column=c, sticky= "nsew")
                c += 1
            if c > 3:
                c = 1
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
        self.usernumtext.configure(text = "Experiment Number:  %3s" % self.usernumchoice)

    def checkvalidexpnum(self, parent, controller):
        if len(self.usernumchoice) == 0: #user did not enter a number
            tkMessageBox.showwarning("Error", "Must enter an experiment number")
        else:
            savetofile = "/home/pi/Desktop/ExperimentFolder/Exp" + str(self.usernumchoice) + "/"
            if os.path.exists(savetofile): #file already exists
                tkMessageBox.showwarning("Error", "Experiment number already used")
            else: 
                Appa.set_savefile(savetofile)
                Appa.set_number(self.usernumchoice) #Configure experiment object's expnumber
                controller.show_frame(ExpSelPg)


class ExpSelPg(tk.Frame, Experiment):

    """Allows experiment selection"""
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Select Experiment Type", font=MEDIUM_FONT) #create object
        label.grid(row=0, column=0, columnspan=6, sticky="ew") #pack object into window

        self.userexpchoice = int()


        button1 = ttk.Button(self, text="Back to\nExperiment\nNumber", style="TINYFONT.TButton", command=lambda: controller.show_frame(ExpNumPg)) #create a button to return to run time
        button1.grid(row=8, column= 0, columnspan=2, sticky="nsew", padx=xspacer, pady=yspacer)

        button2 = ttk.Button(self, text="Next", style="TINYFONT.TButton", command=lambda: self.checkchosenexp(parent, controller)) #create a button to time entry
        button2.grid(row=8, column= 5, sticky="nsew", padx=xspacer, pady=yspacer)

        self.grid_columnconfigure(0, minsize=appwidth/2.5*.9) #back button
        self.grid_columnconfigure(1, minsize=appwidth/2.5*.1) #back button
        self.grid_columnconfigure(5, minsize=appwidth/2.5) #next button
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(8, minsize=appheight/3) #Next/back button rows

        self.grid_rowconfigure(1, weight=1)	#spacer
        self.grid_rowconfigure(7, weight=1) #spacer




        s = ttk.Style()
        s.configure("radio.TRadiobutton", font=(SMALL_FONT))

        nonebutton = ttk.Radiobutton(self, text="None", style="radio.TRadiobutton", variable = "ExpOption", value = 0, command = lambda: self.qfb(0)) #indicatoron = 0)
        thermobutton = ttk.Radiobutton(self, text="Thermotaxis", style="radio.TRadiobutton", variable = "ExpOption", value = 1, command = lambda: self.qfb(1)) #indicatoron = 0)
        chemobutton = ttk.Radiobutton(self, text="Chemotaxis", style="radio.TRadiobutton", variable = "ExpOption", value = 2, command = lambda: self.qfb(2)) #indicatoron = 0)
        photobutton = ttk.Radiobutton(self, text="Phototaxis", style="radio.TRadiobutton", variable = "ExpOption", value = 3, command = lambda: self.qfb(3)) #indicatoron = 0)
        for button in [nonebutton, thermobutton, chemobutton, photobutton]:
            button.state(["!focus",'!selected'])

        nonebutton.grid(row=2, column= 1, columnspan=5, sticky="w")
        thermobutton.grid(row=3, column= 1, columnspan=5, sticky="w")
        chemobutton.grid(row=4, column= 1, columnspan=5, sticky="w")
        photobutton.grid(row=5, column= 1, columnspan=5, sticky="w")

    def qfb(self, ExpOptionChosen): #stores the selection
        self.userexpchoice = str(ExpOptionChosen)
    def checkchosenexp(self, parent, controller):
        if self.userexpchoice == int():
            tkMessageBox.showwarning("Error", "Must select an experiment type")
        else:
            if self.userexpchoice == "0":
                Appa.iscontrol = True
            Appa.set_type(self.userexpchoice) #set experiment object's type to user's choice
            controller.show_frame(TimeSelPg)




class TimeSelPg(tk.Frame):

    """Allows run time selection"""

    runtime = 0 # initialize class runtime variable

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Enter Run Time (seconds)", font=MEDIUM_FONT) #create object
        label.grid(row=0, column=1, columnspan=3, sticky="NSEW") #pack object into window



        self.grid_rowconfigure(2, minsize=25) 
        self.grid_rowconfigure(7, weight=1)  
        for row in range (3,7):
            self.grid_rowconfigure(row, minsize=50) 
        for column in range(6):
            self.grid_columnconfigure(column, minsize=appwidth/5, weight=1)
        self.grid_rowconfigure(8, minsize=appheight/3) #Configure rows/grids. 0 sets minimum size weight sets priority

        self.totaltime = str()

        button1 = ttk.Button(self, text="Back to\nExperiment\nSelection", style="TINYFONT.TButton", command=lambda: controller.show_frame(ExpSelPg)) #create a button to return to experiment selection
        button1.grid(row=8, column= 0, columnspan=2, rowspan=1, sticky="nsew", padx=xspacer, pady=yspacer)

        button2 = ttk.Button(self, text="Next", style="TINYFONT.TButton", command=lambda: self.checkvalidexptime(parent, controller)) #create a button to InsertPg
        button2.grid(row=8, column= 3, columnspan=2, rowspan=1, sticky="nsew", padx=xspacer, pady=yspacer)

        """Creates display for time inputed"""
        self.totaltimetext = tk.Label(self, text = "", font=SMALL_FONT) 
        self.totaltimetext.grid(row = 1, column = 1, columnspan=3, sticky="W")
        self.totaltimetext.configure(text = "Run time: %.5s" % self.totaltime)

        """ Number Pad """
        btn_numbers = [ '7', '8', '9', '4', '5', '6', '1', '2', '3', ' ', '0', 'x'] #create list of numbers to be displayed
        r = 3
        c = 1


        for num in btn_numbers:
            if num == ' ':
                self.num = ttk.Button(self, text=num, width=5)
                self.num.grid(row=r, column=c, sticky= "nsew")
                c += 1

            else: 
                self.num = ttk.Button(self, text=num, width=5, style='TINYFONT.TButton', command=lambda b = num: self.click(b))
                self.num.grid(row=r, column=c, sticky= "nsew")
                c += 1
            if c > 3:
                c = 1
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
    def checkvalidexptime(self, parent, controller):
        if len(self.totaltime) == 0: #user did not enter a number
            tkMessageBox.showwarning("Error", "Must enter an experiment duration")
        else:
            Appa.set_exptime(self.totaltime) #create experiment object
            controller.show_frameCharlie(ConfirmPg)

class ConfirmPg(tk.Frame, Experiment):

    """ Displays chosen parameters for user to confirm"""

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent) 

        self.grid_rowconfigure(1, minsize=appheight/8) #Next/back button rows
        self.grid_rowconfigure(6, weight=1) #Next/back button rows

        self.grid_rowconfigure(7, minsize=appheight/3) #Next/back button rows
        self.grid_columnconfigure(0, minsize=appwidth/2.5*.6) #back button
        self.grid_columnconfigure(1, minsize=appwidth/2.5*.4) #back button
        self.grid_columnconfigure(3, minsize=appwidth/2.5) #next button
        self.grid_columnconfigure(2, weight=1) #next button

        self.label1 = tk.Label(self, text="Chosen Parameters", font=LARGE_FONT) #create object
        self.label1.grid(row=0, column=0, columnspan=4, sticky="ew") #grid object into window

        self.label2 = tk.Label(self, text="", font=SMALL_FONT) #create object
        self.label2.grid(row=2, column=1, columnspan=3, sticky="w") #grid object into window

        self.label3 = tk.Label(self, text="", font=SMALL_FONT) #create object
        self.label3.grid(row=4, column=1, columnspan=3, sticky="w") #grid object into window

        self.label4 = tk.Label(self, text="", font=SMALL_FONT) #create object
        self.label4.grid(row=5, column=1, columnspan=3, sticky="w") #grid object into window


        button1 = ttk.Button(self, text="Back to\nRun time", style="TINYFONT.TButton", command=lambda: controller.show_frame(TimeSelPg)) #create a button to return to run time
        button1.grid(row=7, column= 0, columnspan=2, sticky="nsew", padx=xspacer, pady=yspacer)

        button2 = ttk.Button(self, text="Next", style="TINYFONT.TButton", command=lambda: controller.show_frameFish(InsertPg)) #Insert worms
        button2.grid(row=7, column= 3, sticky="nsew", padx=xspacer, pady=yspacer)




    def label2confirm(self, expnumber):
        self.label2.configure(text = "Experiment number: " + str(expnumber))

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

        self.grid_rowconfigure(3, minsize=appheight/3) #Next/back button rows       
        self.grid_rowconfigure(2, weight=1) #Next/back button rows       
        self.grid_columnconfigure(0, minsize=appwidth/2.5) #next button
        self.grid_columnconfigure(2, minsize=appwidth/2.5) #next button
        self.grid_columnconfigure(1, weight=1) #next button

        label = tk.Label(self, text="Insert Worms", font=MEDIUM_FONT) #create object
        label.grid(row=0, column=0, columnspan=3) #grid object into window

        label2 = tk.Label(self, text="Select next once worms have settled down", font=SMALL_FONT) #create object
        label2.grid(row=1, column=0, columnspan=3) #grid object into window

        button1 = ttk.Button(self, text="Back to\nConfirmation Page", style="TINYFONT.TButton", command=lambda: controller.show_frameZebra(ConfirmPg)) #create a button to return to run time
        button1.grid(row=3, column= 0, sticky="nsew", padx=xspacer, pady=yspacer)

        button2 = ttk.Button(self, text="Next", style="TINYFONT.TButton", command=lambda: controller.show_frameDelta(StimPrepPg)) #prepstimuli
        button2.grid(row=3, column= 2, sticky="nsew", padx=xspacer, pady=yspacer)

        #self.totaltimetext = tk.Label(self, text = "", font=LARGE_FONT) 
        #self.totaltimetext.grid(row = 1, column = 0, sticky="w")
        #What is this???





class StimPrepPg(tk.Frame):
    """
    Instruct students to prepare stimuli

    check expchoice to see if need to insert stimuli
    Key: 0 = none; 1 = thermo; 2 = chemo; 3 = photo     

    """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)


        self.grid_rowconfigure(3, minsize=appheight/3) #Next/back button rows       
        self.grid_rowconfigure(2, weight=1) #Next/back button rows       
        self.grid_columnconfigure(0, minsize=appwidth/2.5) #next button
        self.grid_columnconfigure(2, minsize=appwidth/2.5) #next button
        self.grid_columnconfigure(1, weight=1) #next button


        self.label1 = tk.Label(self, text="", font=MEDIUM_FONT) #create object
        self.label1.grid(row=0, column=0, columnspan=3) #grid object into window



        label2 = tk.Label(self, text="Press 'Start' to begin experiment", font=SMALL_FONT) #create object
        label2.grid(row=1, column=0, columnspan=3) #grid object into window


        button1 = ttk.Button(self, text="Back to\nInsert Worms", style="TINYFONT.TButton", command=lambda: controller.show_frame(InsertPg)) #create a button to return to InsertPg
        button1.grid(row=3, column= 0, sticky="nsew", padx=xspacer, pady=yspacer)

        button2 = ttk.Button(self, text="Start", style="TINYFONT.TButton", command=lambda: controller.show_frameEcho(ExpFinishPg)) #Start Experiment and raise experiment finished page
        button2.grid(row=3, column= 2, sticky="nsew", padx=xspacer, pady=yspacer)
    #Key: 0 = none; 1 = thermo; 2 = chemo; 3 = photo       
    def gettext(self):
        if Appa.exptype == "0" or Appa.exptype == "3":
            words = "Ready"
        elif Appa.exptype == "1" or Appa.exptype == "2":
            words = "Prepare/Insert Stimuli"
        else:
            words = "Error"
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
        self.grid_columnconfigure(0, weight=1)	

        label = tk.Label(self, text="Experiment Finished", font=MEDIUM_FONT) #create object
        label.grid(row=0, column=0) #grid object into window

        button2 = ttk.Button(self, text="Continue to\nreview this\nexperiment's data", style="TINYFONT.TButton", command=lambda: controller.show_frameMarlin(PageTest)) #create a button to start a new experiment 
        button2.grid(row=2, column=0) #grid object into window

class PageTest(tk.Frame, BehaviorBox):

    """Data review page. Let's user choose whether or not to keep data"""

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "Keep This Experiment's Data?", font=LARGE_FONT)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, minsize=30)
        label.grid(row = 0, column=0, columnspan = 3, sticky="NSEW")

        button2 = ttk.Button(self,text="Keep", style="TINYFONT.TButton", command=lambda: controller.show_frameStingray(StartPage, Appa)) 
        button2.grid(row=1, column = 2, sticky= "NS", padx=xspacer, pady=yspacer)

        button3 = ttk.Button(self,text="Discard", style="TINYFONT.TButton", command=lambda: controller.show_frameRhino(StartPage)) 
        button3.grid(row=2, column = 2, sticky="NS", padx=xspacer, pady=yspacer)
	
	self.canvaswidth=appwidth*8/10
        self.canvasheight=appheight*8/10
        self.canvas=tk.Canvas(self, width=self.canvaswidth, height=self.canvasheight)
        self.canvas.grid(row=1, column=0, rowspan=2)
        
        





def confirmdiscard(frame):
    result = tkMessageBox.askquestion("Discard", "Are you sure you want \nto discard these data?")
    if result == "yes":
        shutil.rmtree(Appa.savefile)
        frame.tkraise() #raise to front

class DataRetrievalType(tk.Frame):

    """Choose what to do with data"""

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        label = tk.Label(self, text="Choose an Option", font=LARGE_FONT) #Create label object
        label.grid(row=0, column=0, sticky="nsew") #pack label into window

        for i in range(1,4):
            self.grid_rowconfigure(i, weight=1) 
        self.grid_columnconfigure(0, weight=1)

        button1 = ttk.Button(self, text="Back to Start Page", style='my.TButton', command=lambda: controller.show_frame(StartPage)) #Create a button to start a new experiment       
        button1.grid(row=1, column=0, sticky="nsew", padx=xspacer, pady=yspacer)

        button2 = ttk.Button(self, text="Analyze an Experiment", style='my.TButton', command=lambda: controller.show_frameFoxtrot(DataAnalysisPg)) #Create a button to go to 'data retrieval' page
        button2.grid(row=2, column=0, sticky="nsew", padx=xspacer, pady=yspacer)

        button3 = ttk.Button(self, text="Graph Experiments", style='my.TButton', command=lambda: controller.show_frameFoxtrot(DataGraphChoice)) #Create a button to go to 'data deletion' page
        button3.grid(row=3, column=0, sticky="nsew", padx=xspacer, pady=yspacer)




class DataAnalysisPg(tk.Frame):

    """Let's user choose experiment to analyze"""

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, minsize=appwidth/30)
        label = tk.Label(self, text="Data Analysis \n Please choose experiment to analyze", font=MEDIUM_FONT) #create object
        label.grid(row = 0, column=0, columnspan = 4, sticky="NSEW")

        button1 = ttk.Button(self, text="Back to\nPrevious Page", style='TINYFONT.TButton', command=lambda: controller.show_frame(DataRetrievalType)) #create a button to return to home screen
        button1.grid(row=1, column = 0, sticky="NSEW", padx=xspacer)

        scrollbar = tk.Scrollbar(self)
        scrollbar.grid(row=1, column=2, rowspan=2, sticky="NSEW")

        self.List1=tk.Listbox(self, font=TINY_FONT, yscrollcommand = scrollbar.set)
        self.List1.grid(row=1, column=1, rowspan = 2, sticky="NSEW", padx=xspacer)
        self.List1.config(scrollregion=self.List1.bbox("active"))
        scrollbar.config(command=self.List1.yview)
        
#        button2 = ttk.Button(self, text="Continue", style='TINYFONT.TButton', command=lambda List1=self.List1: controller.show_frameLima(DataAnalysisImagePg, self.asdf(List1)))

        button2 = ttk.Button(self, text="Continue", style='TINYFONT.TButton', command=lambda List1=self.List1: self.asdf(parent, controller, List1))
        button2.grid(row=1, column = 3, sticky="NSEW", padx=xspacer)
        
        self.explist = []
        i=0

        for item in os.listdir("/home/pi/Desktop/ExperimentFolder/"):
            self.explist.append(item)
        self.explist.sort()
        for experiment in self.explist:
            self.List1.insert(i, experiment)
            i+=1
    """
    def asdf(self, List1):
        items = map(int, List1.curselection())
        itemindex = List1.curselection()[0]
        return(self.explist[itemindex])
    """
    def asdf(self, parent, controller, List1):
        if List1.curselection() == ():
            tkMessageBox.showwarning("Error", "Must select an experiment to analyze")
        else:
            itemindex = List1.curselection()[0]
            controller.show_frameLima(DataAnalysisImagePg, self.explist[itemindex])
            
class DataAnalysisImagePg(tk.Frame):

    #WIll pull up images and super impose circles

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)


        button1 = ttk.Button(self, text="Next\nPicture", command=lambda: self.ChangePic(1)) #create a button to return to home screen
        button1.grid(row=10, column=6, sticky="NESW", rowspan=4, columnspan=3)

        self.button2 = ttk.Button(self, text="Previous\nPicture", command=lambda: self.ChangePic(-1)) #create a button to return to home screen
        self.button2.grid(row=10, column=3, sticky="NESW", rowspan=4, columnspan=3)

        self.button3 = ttk.Button(self, text="Save\nand\nFinish", command=lambda: controller.show_frameStingray(StartPage, Momo)) #create a button to return to home screen
        self.button3.grid(row=10, column=6, sticky="NESW", rowspan=4, columnspan=3)

        self.button4 = ttk.Button(self, text="Back to\nExperiment\nSelection", command=lambda: controller.show_frameFoxtrot2(DataAnalysisPg)) #create a button to return to experiment selection
        self.button4.grid(row=10, column=3, sticky="NESW", rowspan=4, columnspan=3)


        """Creates display for worms counted"""
        self.wormscounted = ""
        self.wormscountedtext = tk.Label(self, text = "", font=VERYTINY_FONT) 
        self.wormscountedtext.grid(row=2, column=3, rowspan=2, columnspan=7, sticky="EW")
        self.wormscountedtext.configure(text = "Number of worms:\n%.5s" % self.wormscounted)

        """Creates display for page currently on"""
        self.currentimagenum = -1
        self.imagenumtext = tk.Label(self, text = "", font=VERYTINY_FONT) 
        self.imagenumtext.grid(row=0, column=3, rowspan=2, columnspan=7, sticky="EW")
        self.imagenumtext.configure(text = "Image Number:\n%.3i of %.3i" % (self.currentimagenum+1, 5))

        self.grid_columnconfigure(2, minsize=50) #spacer
        for column in range(3,9):
            self.grid_columnconfigure(column, minsize=30) 

        self.f = Figure(figsize = (1,1))#define figure		
        self.placesubplot()             
        self.canvas = FigureCanvasTkAgg(self.f, self) #add canvas which is what we intend to render graph to and fill it with figure
        self.canvas.draw() #bring canvas to front
        self.canvas.get_tk_widget().grid(row=0, column=0, rowspan = 15) #Fill options: BOTH, X, Y Expand options:  
        self.canvas.get_tk_widget().config(width=450, height=480)


        """ Number Pad """
        btn_numbers = [ '7', '8', '9', '4', '5', '6', '1', '2', '3', ' ', '0', 'x'] #create list of numbers to be displayed
        r = 5 
        c = 3
        for num in btn_numbers:
            if num == ' ':
                self.num = ttk.Button(self, text=num, width=5)
                self.num.grid(row=r, column=c, sticky= "nsew", columnspan=2)
                c += 2
            else: 
                self.num = ttk.Button(self, text=num, width=5, command=lambda b = num: self.click(b))
                self.num.grid(row=r, column=c, sticky= "nsew", columnspan=2)
                c += 2
            if c > 7:
                c = 3
                r += 1

    """method to save user inputs and display them"""
    def click(self, z):
        currentnum = self.wormscounted
        if currentnum == '0':
            self.wormscounted = z
        if z == 'x':
            self.wormscounted = currentnum[:-1]
        else:
            if len(self.wormscounted) > 2:
                tkMessageBox.showwarning("Error", "There's no way that there are that many worms")
            else:
                self.wormscounted = currentnum + z
        Momo.expy[self.currentimagenum]=self.wormscounted #store number of counted worms
        self.wormscountedtext.configure(text = "Number of worms:\n%.5s" % str(Momo.expy[self.currentimagenum])) #configure text so user can see what they entered



    def ChangePic(self, direction):

        #Go to next screen
        self.button3.lower()
        self.button2.lift()
        if self.currentimagenum != -1 and self.wormscounted == "" and direction == 1: #Make sure they entered a number
            tkMessageBox.showwarning("Error", "Must enter a number")

        else: #they did enter a number
            self.currentimagenum = self.currentimagenum + direction #change index depending on if user chose next image or previous image
            self.wormscountedtext.configure(text = "Number of worms:\n%.5s" % str(Momo.expy[self.currentimagenum])) #configure text so user can see any previously entered values 
            self.wormscounted = Momo.expy[self.currentimagenum] #store value of just entered number
            self.f.clf() #clear plot
            self.placesubplot() #place plot again
            img = mpimg.imread(Momo.savefile + "/ExpDataPictures/image" + str(self.currentimagenum) + ".jpg") #read in image
            self.a.imshow(img) #Renders image

            if Momo.exptype == "0":
                #words = "None"
                    circ = Circle((200,400),150, fill=False, edgecolor = "R")
                    shape = circ
            elif Momo.exptype == "1":
                #words = "Thermotaxis"
                    shape = Circle((200,400),150, fill=False, edgecolor = "R")
            elif Momo.exptype == "2":
                #words = "Chemotaxis"
                    shape = Circle((200,400),150, fill=False, edgecolor = "R")
            elif Momo.exptype == "3":
                #words = "Phototaxis"
                    shape = Arc((200,400), width=200, height=200, theta1=0, theta2=180, edgecolor = "B")
                    self.a.plot([100,300], [400,400], color = "B")	
            self.a.add_patch(shape)

            self.canvas.draw()
            self.imagenumtext.configure(text = "Image Number:\n%.3i of %.3i" % (self.currentimagenum+1, len(Momo.expy))) #Update text so user knows what image number they are on
            if self.currentimagenum == len(Momo.expy)-1: #if last image show "generate graph" button
                self.button3.lift()
            if self.currentimagenum == 0: #first image
                self.button4.lift()
    
    def placesubplot(self):
        self.a = self.f.add_subplot(1,1,1) #add subplot RCP. Pth pos on grid with R rows and C columns
        self.a.xaxis.set_visible(False)
        self.a.yaxis.set_visible(False)
        self.a.set_position([0,0,1,1])
        self.a.set_aspect(1)


class DataGraphChoice(tk.Frame):

    """Allows user to choose experiments to graph"""

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Graph Data \n Please choose experiment(s) to graph", font=LARGE_FONT) #create object
        label.grid(row = 0, column=0, columnspan = 4, sticky="NSEW")

        button1 = ttk.Button(self, text="Back to\nPrevious Page", command=lambda: controller.show_frame(DataRetrievalType)) #create a button to return to home screen
        button1.grid(row=1, column = 0, sticky="NS")

        button2 = ttk.Button(self, text="Continue", command = lambda: controller.show_frameShark(GraphPage, self.listofbuttons))
        button2.grid(row=1, column = 3, sticky="NS")

        self.explist = []
        self.listofbuttons = []


        self.canvas = tk.Canvas(self, bg = "white", height=100, width=100, highlightthickness=0)
        self.frame = tk.Frame(self.canvas, background="#ffffff")
        self.vscrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vscrollbar.set)

        self.canvas.grid(row=1, column=1, rowspan = 2, columnspan=1, sticky="NSEW")
        self.vscrollbar.grid(row=1, column=2, sticky="NSW", rowspan=2, columnspan=2)      


        self.canvas.create_window((4,4), window=self.frame, anchor="center", tags="self.frame")

        self.frame.bind("<Configure>", self.onFrameConfigure)





        i=0
        for item in os.listdir("/home/pi/Desktop/ExperimentFolder/"):
            self.explist.append(item)
        self.explist.sort()

        for experiment in self.explist:
            cb = ttk.Checkbutton(self.frame, text=experiment, variable=self.explist[i])
            cb.grid(row=2*i, column=0, rowspan=2, sticky="NSEW")
            self.listofbuttons.append(cb)
            i+=1
        for button in self.listofbuttons:
            button.state(["!focus",'!selected'])




    def onFrameConfigure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))			



class GraphPage(tk.Frame):

    """Page to generate graph"""

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.label = tk.Label(self, text = "Graph of" , font=LARGE_FONT)
        self.label.grid(row = 0, column=1, columnspan = 2, sticky="NSEW")

        button1 = ttk.Button(self,text="Back", command=lambda: controller.show_frameFoxtrot(DataGraphChoice))
        button1.grid(row=1, column = 0, sticky="NS")

        button2 = ttk.Button(self,text="Back to home", command=lambda: controller.show_frame(StartPage)) 
        button2.grid(row=1, column = 4, sticky= "NS")

        button3 = ttk.Button(self,text="Save Graph??", command=lambda: controller.show_frame(StartPage))  #stingray
        button3.grid(row=2, column = 4, sticky="NS")

        f = Figure(figsize = (1,1))#define figure		
        self.a = f.add_subplot(1,1,1) #add subplot RCP. Pth pos on grid with R rows and C columns

        self.a.xaxis.set_visible(True)
        self.a.yaxis.set_visible(True)
        self.a.set_position([0,0,1,1])

        #add canvas which is what we intend to render graph to and fill it with figure
        self.canvas = FigureCanvasTkAgg(f, self) 
        self.canvas.get_tk_widget().grid(row=1, column=1, rowspan = 3, sticky="NS") #Fill options: BOTH, X, Y Expand options:  
        self.canvas.get_tk_widget().config(width=580, height=480)




class DataDelPg(tk.Frame):

    """Allows data deletion"""

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Data Review \n Please choose experiment to delete", font=LARGE_FONT) #create object
        label.grid(row = 0, column=0, columnspan = 4, sticky="NSEW")

        button1 = ttk.Button(self, text="Back to Home", command=lambda: controller.show_frame(StartPage)) #create a button to return to home screen
        button1.grid(row=1, column = 0, sticky="NS")

        button2 = ttk.Button(self, text="Continue", command = lambda: self.yoga())
        button2.grid(row=1, column = 3, sticky="NS")

        self.explist = []
        self.listofbuttons = []



        self.canvas = tk.Canvas(self, bg = "white", height=100, width=100, highlightthickness=0)
        self.frame = tk.Frame(self.canvas, background="#ffffff")
        self.vscrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vscrollbar.set)

        self.canvas.grid(row=1, column=1, rowspan = 2, columnspan=1, sticky="NSEW")
        self.vscrollbar.grid(row=1, column=2, sticky="NSW", rowspan=2, columnspan=2)      


        self.canvas.create_window((4,4), window=self.frame, anchor="center", tags="self.frame")

        self.frame.bind("<Configure>", self.onFrameConfigure)





        i=0
        for item in os.listdir("/home/pi/Desktop/ExperimentFolder/"):
            self.explist.append(item)
        self.explist.sort()

        for experiment in self.explist:
            cb = ttk.Checkbutton(self.frame, text=experiment, variable=self.explist[i])
            cb.grid(row=2*i, column=0, rowspan=2, sticky="NSEW")
            self.listofbuttons.append(cb)
            i+=1
        for button in self.listofbuttons:
            button.state(["!focus",'!selected'])

    def yoga(self):
        result = tkMessageBox.askquestion("Discard", "Are you sure you want \nto discard these data?")
        if result == "yes":
            for button in self.listofbuttons:
                if button.instate(['selected']):
                    shutil.rmtree("/home/pi/Desktop/ExperimentFolder/" + button['text'] + "/")
                    app.show_frameFoxtrot(DataDelPg)

    def onFrameConfigure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))			


class AnalysisTypeForNone(tk.Frame, Experiment):

    """Allows experiment selection if control"""

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="This experiment had no stimulus.\nChoose analysis type to be done.", font=LARGE_FONT) #create object
        label.grid(row=0, column=0, columnspan=100) #pack object into window

        self.userexpchoice = int()


        button1 = ttk.Button(self, text="Back to\nChoose an Experiment\nto Analyze", command=lambda: controller.show_frameFoxtrot2(DataAnalysisPg)) #create a button to return to run time
        button1.grid(row=7, column= 0, sticky="w")

        button2 = ttk.Button(self, text="Next", command=lambda: self.checkchosenexp(parent, controller)) #create a button to time entry
        button2.grid(row=7, column= 10, sticky="e")

        self.thermobutton = ttk.Radiobutton(self, text="Thermotaxis", variable = "ExpOption", value = 1, command = lambda: self.qfb(1)) #indicatoron = 0)
        self.chemobutton = ttk.Radiobutton(self, text="Chemotaxis", variable = "ExpOption", value = 2, command = lambda: self.qfb(2)) #indicatoron = 0)
        self.photobutton = ttk.Radiobutton(self, text="Phototaxis", variable = "ExpOption", value = 3, command = lambda: self.qfb(3)) #indicatoron = 0)
        for button in [self.thermobutton, self.chemobutton, self.photobutton]:
            button.state(["!focus",'!selected'])


        self.thermobutton.grid(row=3, column= 3, sticky="nsew")
        self.chemobutton.grid(row=4, column= 3, sticky="nsew")
        self.photobutton.grid(row=5, column= 3, sticky="nsew")

    def qfb(self, ExpOptionChosen): #stores the selection
        self.userexpchoice = str(ExpOptionChosen)
    def checkchosenexp(self, parent, controller):
        if self.userexpchoice == int():
            tkMessageBox.showwarning("Error", "Must select an experiment type")
        else:
            Momo.set_type(self.userexpchoice) #set experiment object's type to user's choice
            controller.show_frameBean(DataAnalysisImagePg)
            #endoftimes




















app = BehaviorBox()
app.attributes('-fullscreen', True)
app.bind("<Escape>", lambda e: app.destroy())
app.mainloop()







