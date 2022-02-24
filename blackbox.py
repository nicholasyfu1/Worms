#!/usr/bin/env python
"""

Andrew Huynh '20 ahuynh1@swarthmore.edu
Summer 2018
Behavior Box Project

This program is to run experiments on the black box. It is designed to be run on a 800x480 screen.
The UI is designed using TKinter.
Basic overview:
	Create experiment object that stores experiment parameters
	Create class pages
	Buttons on page use specific "show_frame<name.()" commands to raise the next page as well as start 
	fuctions such as imaging
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

import datetime
from time import *
from picamera import PiCamera

import matplotlib
matplotlib.use("TkAgg")

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.patches import Circle
from matplotlib.patches import Arc
from matplotlib.patches import Rectangle

from PIL import ImageTk, Image

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

camera = PiCamera(resolution=(640,480))
camera.awb_mode='off'
camera.awb_gains=(0.5,1.2)

# Font Sizes
LARGE_FONT = ("Lato", 36)
MEDIUM_FONT = ("Lato", 28)
SMALL_FONT = ("Lato", 24)
TINY_FONT = ("Lato", 20)
VERYTINY_FONT = ("Lato", 15)

appheight=400
appwidth=800

xspacer=appheight/80
yspacer=appheight/80

imagecapturerate = 2 # How often a picture is taken in seconds

if not os.path.exists( "/home/pi/Desktop/ExperimentFolder/"): #Makes folder for data if doesn't exist
	os.makedirs( "/home/pi/Desktop/ExperimentFolder/")

class Experiment():

	def __init__(self):
		self.expnumber = str()
		self.exptype = str()
		self.exptime = int()
		self.savefile = str()
		self.capturerate = imagecapturerate
		self.iscontrol = False
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
	#coi = [] not sure if this is needed

	def __init__(self, *args, **kwargs):

		tk.Tk.__init__(self, *args, **kwargs)

		tk.Tk.wm_title(self, "Behavior Box") # Set window title

		self.container = tk.Frame(self) # Define frame/edge of window
		self.container.pack(side="top", fill="both", expand=True) # Fill will fill space you have allotted pack. Expand will take up all white space.
		self.container.grid_rowconfigure(0, weight=1) # Configure rows/grids. 0 sets minimum size weight sets priority
		self.container.grid_columnconfigure(0, weight=1) 

		# Initalize/render all pages
		self.frames = {}
		for F in (StartPage, ExpSelPg, TimeSelPg, ConfirmPg, InsertPg, StimPrepPg, ExpFinishPg, ReviewData, DataDelPg, DataAnalysisImagePg, DataAnalysisPg, GraphPage, DataMenu, DataGraphChoice, AnalysisTypeForNone, CameraPreviewPg):
			frame = F(self.container, self)
			self.frames[F] = frame 
			frame.grid(row=0, column=0, sticky="nsew")         
		self.show_frame(StartPage) # Raise Start Page
	

		# Create button styles/fontsizes
		s = ttk.Style()
		s.configure("VERYTINYFONT.TButton", font=(VERYTINY_FONT))
		s.configure("TINYFONT.TButton", font=(TINY_FONT))
		s.configure("my.TButton", font=(SMALL_FONT))
		s.configure("checkbuttonstyle.TCheckbutton", font=(TINY_FONT), background="white")
		s.configure("radio.TRadiobutton", font=(SMALL_FONT))


	def startfresh(self):
		"""Reinitalize pages that have updating values"""
		for F in (StartPage, ExpSelPg, TimeSelPg, ConfirmPg, InsertPg, StimPrepPg, DataDelPg):
			frame = F(self.container, self)
			self.frames[F] = frame 
			frame.grid(row=0, column=0, sticky="nsew") #other choice than pack. Sticky alignment + stretch

	def show_frame(self, cont):
		"""Basic function to raise frame to front"""
		frame = self.frames[cont]
		frame.tkraise() #raise to front

	def show_frameAlpha(self, cont):
		"""Main menu -> new experiment. Resets all of Appa's values"""
		#Reset all of experiment-class variables
		Appa.expnumber = str()
		Appa.exptype = str()
		Appa.exptime = int()
		Appa.savefile = str()
		Appa.expy = []
		app.startfresh() #Reinitalize all necessary pages to starting state
		frame = self.frames[cont]
		frame.tkraise() #raise to front
	
	def show_frameZebra(self, cont):
		"""Confirm Page <- Insert Page; ends camera preview"""
		frame = self.frames[cont]
		camera.stop_preview()#Stops the preview window
		frame.tkraise() #raise to front

	def show_frameFish(self, cont):
		"""Confirm Page -> Insert Page; starts camera preview"""
		frame = self.frames[cont]
		camera.start_preview(fullscreen=False, window=(0,appheight/4,appwidth,appheight/2)) #this line starts the preview. 
		frame.tkraise()

	def show_frameCharlie(self, cont):
		"""TimeSelPg -> Confirm Pg; 
			save time choice -> confirmation and updates label values in confirmation based on previous user   
			input
		"""
		frame = self.frames[cont]
		frame.confirmlabels()
		frame.tkraise()

	def show_frameDelta(self, cont):
		"""InsertPg -> StimPrepPg and displays either "Ready" or "Insert stimuli" based on experiment type"""
		frame = self.frames[cont]
		frame.gettext() #Displays either "Ready" or "Insert stimuli" based on experiment type
		frame.tkraise()

	def show_frameEcho(self, cont):
		"""StimPrepPg -> start imaging and count down"""
		self.frames[StimPrepPg].button1.grid_remove()
		self.frames[StimPrepPg].button2.grid_remove()
		self.frames[StimPrepPg].label1.configure(text="Experiment in progress")
		frame = self.frames[cont]

		os.makedirs(Appa.savefile) # Create general folder for experiment 
		os.makedirs(Appa.savefile + "/ExpDataPictures") # Create folder for images from exp

		#Image capturing
		imgnum=0
		for i in range(Appa.exptime+1):
			start_time = clock()
			remaining = Appa.exptime-i # Calculate countdown
			self.frames[StimPrepPg].label2.configure(text="Time remaining: %d" % remaining) # Set countdown
			self.frames[StimPrepPg].update_idletasks() # Refresh page            
			if i%Appa.capturerate == 0: # Calculate if need to capture pic
				#camera.resolution = (640,480) 
				camera.capture(Appa.savefile + "/ExpDataPictures/image" + str(imgnum) + ".jpg", resize=(640,480))
				Appa.expy.append("") # Append empty place holder for future analyssi
				imgnum+=1
			sleep(1-(clock()-start_time))

		camera.stop_preview()
		frame.tkraise() 

	def show_frameFoxtrot(self, cont):
		"""Reinitalize a page without prompting for confirmation""" 
		frame = cont(self.container, self)
		self.frames[cont] = frame 
		frame.grid(row=0, column=0, sticky="nsew")
		frame.tkraise()
	
	def show_frameFoxtrot2(self, cont):
		"""Confirm if want to reinitalize page and the reinitalize"""
		result = tkMessageBox.askquestion("Warning", "All progess will be lost.\nProceed anyways?")
		if result == "yes":
			frame = cont(self.container, self)
			self.frames[cont] = frame 
			frame.grid(row=0, column=0, sticky="nsew") 
			frame.tkraise() 

	def show_frameLima(self, cont, chosenexp):
		"""DataAnalysisPg -> DataAnalysisImagePg; load Appa object for exp and pull up first image from chosen experiment"""
		result = True       
		result2 = True
		global Momo # Create variable to store experiment object
		Momo = getobject(chosenexp)
		
		# Case of analyzing control
		if Momo.iscontrol: 
			if Momo.exptype != "0": # Not first time analyzing
				result2 = tkMessageBox.askquestion("Warning", "This control experiment has already\nbeen analyzed as %s.\nChanges may overwrite exisiting data.\nProceed anyways?" % getpreviouslyanalyzed(Momo))
			if result2 != "no": # First time analyzing or want to override
				frame = self.frames[AnalysisTypeForNone] # Go to AnalysisTypeForNone to get type to analyze as
				for button in [frame.thermobutton, frame.chemobutton, frame.photobutton]:
					if getpreviouslyanalyzed(Momo) == button['text']: # Turn on button if that was the previous analysis
						button.state(["focus","selected"])
					else:
						button.state(["!focus",'!selected'])
				frame.tkraise()

		# Case of not control
		else: 
			if Momo.expy[0] != "": # Already analyzed
				result = tkMessageBox.askquestion("Warning", "The selected experiment has already been analyzed.\nChanges may overwrite exisiting data.\nProceed anyways?")
			if result != "no": # First time analyzing or want to override
				if Momo.exptype != "4": # Not strunching
					frame = cont(self.container, self)
					self.frames[cont] = frame 
					frame.grid(row=0, column=0, sticky="nsew")
					frame.ChangePic(1) # Go to first picture
					frame.tkraise() 
				else:
					tkMessageBox.showwarning("Scrunching analysis not implimented yet") #show warning
					"""
					frame = SrunchingAnalysis(self.container, self) # Create fresh page in case of old data
					self.frames[cont] = frame 
					frame.grid(row=0, column=0, sticky="nsew")
					frame.tkraise() 
					"""

	def show_frameBean(self, cont):
		"""AnalysisTypeForNone -> DataAnalysisImagePg"""
		frame = cont(self.container, self)
		self.frames[cont] = frame 
		frame.grid(row=0, column=0, sticky="nsew")
		frame.ChangePic(1) # Go to first picture
		frame.tkraise() 


	def show_frameMarlin(self, cont): 
		"""ExpFinishPg -> ReviewData. Configures ReviewData to display all images taken during experiment"""
		frame = cont(self.container, self)
		self.frames[cont] = frame 
		frame.grid(row=0, column=0, sticky="nsew") 

		i=0
		frame.imagelist=[]
		numpics = len(os.listdir(Appa.savefile + "ExpDataPictures"))
		
		for picture in  os.listdir(Appa.savefile + "ExpDataPictures"):
			img = Image.open(Appa.savefile+ "ExpDataPictures/image" + str(i) + ".jpg", mode="r") #read in image
			#img = img.resize((frame.canvaswidth, frame.canvasheight))
			imwidth, imheight = img.size
			frame.tempimage = ImageTk.PhotoImage(img)
			frame.imagelist.append(frame.tempimage)
			frame.canvas.create_image(0,(imheight+10)*i,image=frame.imagelist[i],anchor="nw")
			i+=1

		frame.canvas.config(scrollregion=(frame.canvas.bbox("all")))
		scrollbar = tk.Scrollbar(frame)
		scrollbar.config(command=frame.canvas.yview)
		scrollbar.grid(row=1, column=1, rowspan = 2, sticky="NSEW")
		frame.canvas.config(yscrollcommand=scrollbar.set)

		frame.tkraise()


	def show_frameStingray(self, cont, obj):
		"""ReviewData(keep) -> StartPage; stores data"""
		saveobject(obj)
		tkMessageBox.showwarning("Done", "Data has been saved for:" + obj.expnumber) #show warning
		frame = self.frames[cont]
		frame.tkraise() #raise to front

	def show_frameRhino(self, cont):
		"""ReviewData(discard) -> StartPage; deletes data"""
		frame = self.frames[cont]
		result = tkMessageBox.askquestion("Discard", "Are you sure you want \nto discard these data?")
		if result == "yes":
			shutil.rmtree(Appa.savefile)
			frame.tkraise() 

	def show_frameShark(self, cont, listofbuttons):
		"""DataGraphChoice -> GraphPage; checks to see if experiments were chosen to graph and will graph"""
		frame = cont(self.container, self)
		self.frames[cont] = frame 

		ExpsToGraph = []
		expnames = []
		unanalyzedlist = []
		result = True

		# Get list of experiments to plot
		for button in listofbuttons:
			if button.instate(['selected']):
					ExpsToGraph.append(getobject(button['text']))

		if len(ExpsToGraph) == 0: # Did not choose an experiment to graph
				tkMessageBox.showwarning("Error", "No experiments selected")
		else:
			# Check to see if all experiments selected have been analyzed
			for experiment in ExpsToGraph:
				if experiment.expy[0] == "":
					unanalyzedlist.append(experiment.expnumber)
				else:
					experiment.expy = list(map(int, experiment.expy))
					frame.a.plot(range(len(experiment.expy)),experiment.expy, label=experiment.expnumber)
					expnames.append(experiment.expnumber)


			if len(unanalyzedlist) > 0: # If unanalyzed experiments exist warn user
				unanalyzedlist = ", ".join(unanalyzedlist)
				result = tkMessageBox.askquestion("Warning", "The following experiments have\nnot been analyzed yet\nand will not be graphed\n\n" +unanalyzedlist+ "\n\nProceed anyways?")

			if result !=  "no": # Override or all experiments have been analyzed                
				frame.grid(row=0, column=0, sticky="nsew") 
				frame.a.legend(loc='upper right', fontsize=8)
				frame.canvas.draw() 
				frame.tkraise() 

	def show_frameSquid(self, cont):
			"""Main menu -> CameraPreviewPg; starts preview and raises frame"""
			frame = self.frames[cont]
			frame.tkraise() 
			camera.start_preview(fullscreen=False, window=(appwidth/800, appheight/4, appwidth-(2*appwidth/800), appheight*9/10)) # This line starts the preview. 
			
			
class StartPage(tk.Frame):
	"""Main menu"""   
	def __init__(self, parent, controller):
		tk.Frame.__init__(self,parent)
		for i in range(1,5):
			self.grid_rowconfigure(i, weight=1)
		self.grid_columnconfigure(0, weight=1)
		
		label = tk.Label(self, text="Main Menu", font=LARGE_FONT) 
		label.grid(row=0, column=0, sticky="nsew") 
		
		button1 = ttk.Button(self, text="New Experiment", style='my.TButton', command=lambda: controller.show_frameAlpha(ExpSelPg)) 
		button1.grid(row=1, column=0, sticky="nsew", padx=xspacer, pady=yspacer)

		button2 = ttk.Button(self, text="Data Menu", style='my.TButton', command=lambda: controller.show_frame(DataMenu))
		button2.grid(row=2, column=0, sticky="nsew", padx=xspacer, pady=yspacer)

		button3 = ttk.Button(self, text="Preview Camera", style='my.TButton', command=lambda: controller.show_frameSquid(CameraPreviewPg))
		button3.grid(row=3, column=0, sticky="nsew", padx=xspacer, pady=yspacer)

		button4 = ttk.Button(self, text="Quit", style='my.TButton', command=lambda: app.destroy())
		button4.grid(row=4, column=0, sticky="nsew", padx=xspacer, pady=yspacer)

class ExpSelPg(tk.Frame, Experiment):
	"""Choose experiment type to run"""
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.grid_columnconfigure(0, minsize=appwidth/2.5*.9) # Back button
		self.grid_columnconfigure(1, minsize=appwidth/2.5*.1) # Back button
		self.grid_columnconfigure(2, weight=1) # Central column with options
		self.grid_columnconfigure(5, minsize=appwidth/2.5) # Next button
		self.grid_rowconfigure(8, minsize=appheight/3) # Next/back button rows
		self.grid_rowconfigure(1, weight=1)	# Spacer
		self.grid_rowconfigure(7, weight=1) #Spacer
		
		self.userexpchoice = int()
		
		label = tk.Label(self, text="Select Experiment Type", font=MEDIUM_FONT) #create object
		label.grid(row=0, column=0, columnspan=6, sticky="ew") #pack object into window

		button1 = ttk.Button(self, text="Back to\nMain Menu", style="TINYFONT.TButton", command=lambda: controller.show_frame(StartPage)) 
		button1.grid(row=8, column= 0, columnspan=2, sticky="nsew", padx=xspacer, pady=yspacer)

		button2 = ttk.Button(self, text="Next", style="TINYFONT.TButton", command=lambda: self.checkchosenexp(parent, controller)) # Check experiment then go to time entry
		button2.grid(row=8, column=5, sticky="nsew", padx=xspacer, pady=yspacer)

		nonebutton = ttk.Radiobutton(self, text="No Stimulus", style="radio.TRadiobutton", variable = "ExpOption", value = 0, command = lambda: self.qfb(0)) 
		thermobutton = ttk.Radiobutton(self, text="Thermotaxis", style="radio.TRadiobutton", variable = "ExpOption", value = 1, command = lambda: self.qfb(1)) 
		chemobutton = ttk.Radiobutton(self, text="Chemotaxis", style="radio.TRadiobutton", variable = "ExpOption", value = 2, command = lambda: self.qfb(2)) 
		photobutton = ttk.Radiobutton(self, text="Phototaxis", style="radio.TRadiobutton", variable = "ExpOption", value = 3, command = lambda: self.qfb(3)) 
		scrunchbutton = ttk.Radiobutton(self, text="Scrunching", style="radio.TRadiobutton", variable = "ExpOption", value = 4, command = lambda: self.qfb(4)) 

		rownum = 2
		for button in [nonebutton, thermobutton, chemobutton, photobutton, scrunchbutton]:
			button.state(["!focus",'!selected'])
			button.grid(row=rownum, column=1, columnspan=5, sticky="w")
			rownum += 1
		
	def qfb(self, ExpOptionChosen): 
		"""Store the selection"""
		self.userexpchoice = str(ExpOptionChosen)

	def checkchosenexp(self, parent, controller): 
		"""Check if chose an experiment. If yes, store values"""
		if self.userexpchoice == int():
			tkMessageBox.showwarning("Error", "Must select an experiment type")
		else:
			if self.userexpchoice == "0":
				Appa.iscontrol = True
				typeofexp = "N"
			elif self.userexpchoice == "1":
				typeofexp = "T"
			elif self.userexpchoice == "2":
				typeofexp = "C"
			elif self.userexpchoice == "3":
				typeofexp = "P"
			elif self.userexpchoice == "4":
				typeofexp = "S"                                

			currtime = datetime.datetime.now()
			dateandtime = currtime.strftime("%Y%m%d-%H%M")
			savetofile = "/home/pi/Desktop/ExperimentFolder/" + typeofexp + dateandtime + "/"
			Appa.set_savefile(savetofile) # Save file address
			Appa.set_number(typeofexp + dateandtime) # Save exp identifier          
			Appa.set_type(self.userexpchoice) # Save experiment type
			controller.show_frame(TimeSelPg)


class TimeSelPg(tk.Frame):
	"""Enter time to run experiment for"""
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		for row in range (3,7):
			self.grid_rowconfigure(row, minsize=50) 
		for column in range(6):
			self.grid_columnconfigure(column, minsize=appwidth/5, weight=1)
		self.grid_rowconfigure(8, minsize=appheight/3) # Next/back button row
		self.grid_rowconfigure(0, weight=1) # Title row
		self.grid_rowconfigure(2, weight=1) # Spacer row
		self.grid_rowconfigure(7, weight=1)  # Spacer row
		
		self.totaltime = str()
		
		label = tk.Label(self, text="Enter Experiment Duration (seconds)", font=MEDIUM_FONT) 
		label.grid(row=0, column=0, columnspan=5, sticky="NSEW") 
		
		self.totaltimetext = tk.Label(self, text = "", font=SMALL_FONT) 
		self.totaltimetext.grid(row = 1, column = 1, columnspan=3, sticky="w")
		self.totaltimetext.configure(text = "Duration: %.5s" % self.totaltime)
		
		button1 = ttk.Button(self, text="Back to\nExperiment\nSelection", style="TINYFONT.TButton", command=lambda: controller.show_frame(ExpSelPg)) 
		button1.grid(row=8, column= 0, columnspan=2, sticky="nsew", padx=xspacer, pady=yspacer)

		button2 = ttk.Button(self, text="Next", style="TINYFONT.TButton", command=lambda: self.checkvalidexptime(parent, controller)) # Make sure entered a valid time then go to confirmation page
		button2.grid(row=8, column= 3, columnspan=2, rowspan=1, sticky="nsew", padx=xspacer, pady=yspacer)

		"""Number Pad """
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

	def click(self, z):
		"""Display user's inputs"""
		currentnum = self.totaltime
		if currentnum == '0': # Replace value if time = 0
			self.totaltime = z
		if z == 'x': # Delete last entered value
			self.totaltime = currentnum[:-1]
		else:
			if len(self.totaltime) > 2:
				tkMessageBox.showwarning("Error", "Time too long")
			else:
				self.totaltime = currentnum + z
		self.totaltimetext.configure(text = "Duration:  %.5s" % self.totaltime)
	
	def checkvalidexptime(self, parent, controller):
		"""Check to see if time entered is valid, save the time, then show confirmation page"""
		if len(self.totaltime) == 0: # User did not enter a number
			tkMessageBox.showwarning("Error", "Must enter an experiment duration")
		if self.totaltime == "0": # User entered 0
			tkMessageBox.showwarning("Error", "Duration can not be 0")
		if len(self.totaltime) != 0 and self.totaltime != "0":
			Appa.set_exptime(self.totaltime)
			controller.show_frameCharlie(ConfirmPg)


class ConfirmPg(tk.Frame, Experiment):
	""" Displays chosen parameters for user to confirm"""
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent) 
		self.grid_rowconfigure(1, minsize=appheight/8) # Spacer
		self.grid_rowconfigure(6, weight=1) # Spacer
		self.grid_rowconfigure(7, minsize=appheight/3) # Next/back button rows
		self.grid_columnconfigure(0, minsize=appwidth/2.5*.5) # Back button
		self.grid_columnconfigure(1, minsize=appwidth/2.5*.5) # Back button
		self.grid_columnconfigure(3, minsize=appwidth/2.5) # Next button
		self.grid_columnconfigure(2, weight=1) # Central column

		self.label1 = tk.Label(self, text="Chosen Parameters", font=LARGE_FONT) 
		self.label1.grid(row=0, column=0, columnspan=4, sticky="ew") 

		self.label2 = tk.Label(self, text="", font=SMALL_FONT) # Label for experiment name
		self.label2.grid(row=2, column=1, columnspan=3, sticky="w") 
		self.label3 = tk.Label(self, text="", font=SMALL_FONT) # Label for experiment type
		self.label3.grid(row=4, column=1, columnspan=3, sticky="w") 
		self.label4 = tk.Label(self, text="", font=SMALL_FONT) # Label for experiment duration
		self.label4.grid(row=5, column=1, columnspan=3, sticky="w") 

		button1 = ttk.Button(self, text="Back to\nRun time", style="TINYFONT.TButton", command=lambda: controller.show_frame(TimeSelPg)) 
		button1.grid(row=7, column= 0, columnspan=2, sticky="nsew", padx=xspacer, pady=yspacer)
		
		button2 = ttk.Button(self, text="Next", style="TINYFONT.TButton", command=lambda: controller.show_frameFish(InsertPg)) # Go to insert worms page
		button2.grid(row=7, column= 3, sticky="nsew", padx=xspacer, pady=yspacer)

	def confirmlabels(self):
		"""Configure labels to reflect what user chose"""
		words = getpreviouslyanalyzed(Appa)
		self.label2.configure(text = "Experiment number: " + str(Appa.expnumber))
		self.label3.configure(text = "Experiment type: " + words)
		self.label4.configure(text = "Run time (s): " + str(Appa.exptime))       


class InsertPg(tk.Frame):
	"""Instruct user to insert worms"""
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.grid_rowconfigure(3, minsize=appheight/3) # Next/back button rows       
		self.grid_rowconfigure(2, weight=1) # Spacer     
		self.grid_columnconfigure(0, minsize=appwidth/2.5) # Back button
		self.grid_columnconfigure(2, minsize=appwidth/2.5) # Next button
		self.grid_columnconfigure(1, weight=1) # Central column

		label = tk.Label(self, text="Insert Worms", font=MEDIUM_FONT) 
		label.grid(row=0, column=0, columnspan=3) 

		label2 = tk.Label(self, text="Select next once worms have settled down", font=SMALL_FONT) 
		label2.grid(row=1, column=0, columnspan=3) 

		button1 = ttk.Button(self, text="Back to\nConfirmation Page", style="TINYFONT.TButton", command=lambda: controller.show_frameZebra(ConfirmPg)) 
		button1.grid(row=3, column= 0, sticky="nsew", padx=xspacer, pady=yspacer)

		button2 = ttk.Button(self, text="Next", style="TINYFONT.TButton", command=lambda: controller.show_frameDelta(StimPrepPg)) 
		button2.grid(row=3, column= 2, sticky="nsew", padx=xspacer, pady=yspacer)


class StimPrepPg(tk.Frame):
	"""
	Instruct students to prepare stimuli

	check expchoice to see if need to insert stimuli
	Key: 0 = none; 1 = thermo; 2 = chemo; 3 = photo     

	"""
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		
		self.grid_rowconfigure(3, minsize=appheight/3) #Next/back button rows       
		self.grid_rowconfigure(2, weight=1) # Spacer   
		self.grid_columnconfigure(0, minsize=appwidth/2.5) # Back button
		self.grid_columnconfigure(2, minsize=appwidth/2.5) # Next button
		self.grid_columnconfigure(1, weight=1) # Central column

		self.label1 = tk.Label(self, text="", font=MEDIUM_FONT) #create object
		self.label1.grid(row=0, column=0, columnspan=3) #grid object into window

		self.label2 = tk.Label(self, text="Press 'Start' to begin experiment", font=SMALL_FONT) #create object
		self.label2.grid(row=1, column=0, columnspan=3) #grid object into window
		
		self.button1 = ttk.Button(self, text="Back to\nInsert Worms", style="TINYFONT.TButton", command=lambda: controller.show_frame(InsertPg)) #create a button to return to InsertPg
		self.button1.grid(row=3, column= 0, sticky="nsew", padx=xspacer, pady=yspacer)

		self.button2 = ttk.Button(self, text="Start", style="TINYFONT.TButton", command=lambda: self.beginexp(parent, controller)) #Start Experiment and raise experiment finished page
		self.button2.grid(row=3, column= 2, sticky="nsew", padx=xspacer, pady=yspacer)
		
	def beginexp(self, parent, controller):
		camera.stop_preview()
		result = tkMessageBox.askquestion("Start Experiment", "This experiment will run for \n%s seconds. Once started, you\ncan not quit.\nBegin experiment?" %Appa.exptime)
		if result == "yes":
			camera.start_preview(fullscreen=False, window=(appwidth/800, appheight/4, appwidth-(2*appwidth/800), appheight*9/10)) # This line starts the preview. 
			controller.show_frameEcho(ExpFinishPg)
		else:
			camera.start_preview(fullscreen=False, window=(0, appheight/4, appwidth, appheight/2)) #this line starts the preview. 
			
	def gettext(self):
		"""Configure text depending on if user needs to insert simulus
		Key: 0=none; 1=thermo; 2=chemo; 3=photo; 4=scrunching
		"""
		if Appa.exptype == "0" or Appa.exptype == "3":
			words = "Ready"
		elif Appa.exptype == "1" or Appa.exptype == "2":
			words = "Prepare/Insert Stimulus"
		elif Appa.exptype == "4":
			words = "Prepare to cut worm"
		self.label1.configure(text = words)
		
class ExpFinishPg(tk.Frame):
	"""Allow user to go directly into data analysis or return to main menu"""
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.grid_columnconfigure(0, weight=1)	

		label = tk.Label(self, text="Experiment Finished", font=MEDIUM_FONT) 
		label.grid(row=0, column=0)

		button2 = ttk.Button(self, text="Continue to\nreview this\nexperiment's data", style="TINYFONT.TButton", command=lambda: controller.show_frameMarlin(ReviewData)) # Go to data review
		button2.grid(row=2, column=0)

class ReviewData(tk.Frame, BehaviorBox):
	"""Data review page. Lets user choose whether or not to keep data"""
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.grid_columnconfigure(0, weight=1)
		self.grid_columnconfigure(1, minsize=30)

		label = tk.Label(self, text = "Keep This Experiment's Data?", font=LARGE_FONT)
		label.grid(row = 0, column=0, columnspan = 3, sticky="NSEW")

		button2 = ttk.Button(self,text="Keep", style="TINYFONT.TButton", command=lambda: controller.show_frameStingray(StartPage, Appa)) # Save object then show start page
		button2.grid(row=1, column = 2, sticky= "NS", padx=xspacer, pady=yspacer)

		button3 = ttk.Button(self,text="Discard", style="TINYFONT.TButton", command=lambda: controller.show_frameRhino(StartPage)) # Delete entire date folder then show start page
		button3.grid(row=2, column = 2, sticky="NS", padx=xspacer, pady=yspacer)
	
		self.canvaswidth=appwidth*8/10
		self.canvasheight=appheight*8/10
		self.canvas=tk.Canvas(self, width=self.canvaswidth, height=self.canvasheight)
		self.canvas.grid(row=1, column=0, rowspan=2)
		
		
class DataMenu(tk.Frame):
	"""Choose what to do with data"""
	def __init__(self, parent, controller):
		tk.Frame.__init__(self,parent)
		for i in range(1,5): # Button rows
			self.grid_rowconfigure(i, weight=1) 
		self.grid_columnconfigure(0, weight=1) # Central column

		label = tk.Label(self, text="Choose an Option", font=LARGE_FONT) 
		label.grid(row=0, column=0, sticky="nsew") 

		button1 = ttk.Button(self, text="Analyze an Experiment", style='my.TButton', command=lambda: controller.show_frameFoxtrot(DataAnalysisPg)) # Choose specific experiment to analyze
		button1.grid(row=1, column=0, sticky="nsew", padx=xspacer, pady=yspacer)

		button2 = ttk.Button(self, text="Graph Experiments", style='my.TButton', command=lambda: controller.show_frameFoxtrot(DataGraphChoice)) # Graph experiment(s)
		button2.grid(row=2, column=0, sticky="nsew", padx=xspacer, pady=yspacer)

		button3 = ttk.Button(self, text="Delete Data", style='my.TButton', command=lambda: controller.show_frameFoxtrot(DataDelPg)) 
		button3.grid(row=3, column=0, sticky="nsew", padx=xspacer, pady=yspacer)

		button4 = ttk.Button(self, text="Back to Main Menu", style='my.TButton', command=lambda: controller.show_frame(StartPage))   
		button4.grid(row=4, column=0, sticky="nsew", padx=xspacer, pady=yspacer)


class DataAnalysisPg(tk.Frame):
	"""Lets user choose experiment to analyze"""
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.grid_columnconfigure(1, weight=1) # Listbox column
		self.grid_columnconfigure(2, minsize=appwidth/30) # Scrollbar column
		
		label = tk.Label(self, text="Data Analysis \n Please choose experiment to analyze", font=MEDIUM_FONT)
		label.grid(row = 0, column=0, columnspan = 4, sticky="NSEW")

		button1 = ttk.Button(self, text="Back to\nPrevious Page", style='TINYFONT.TButton', command=lambda: controller.show_frame(DataMenu))
		button1.grid(row=1, column = 0, sticky="NSEW", padx=xspacer)

		scrollbar = tk.Scrollbar(self)
		scrollbar.grid(row=1, column=2, rowspan=2, sticky="NSEW")

		self.List1=tk.Listbox(self, font=TINY_FONT, yscrollcommand = scrollbar.set)
		self.List1.grid(row=1, column=1, rowspan = 2, sticky="NSEW")
		self.List1.config(scrollregion=self.List1.bbox("active"))
		scrollbar.config(command=self.List1.yview)
		
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

	def asdf(self, parent, controller, List1):
		if List1.curselection() == ():
			tkMessageBox.showwarning("Error", "Must select an experiment to analyze")
		else:
			itemindex = List1.curselection()[0]
			controller.show_frameLima(DataAnalysisImagePg, self.explist[itemindex])
			
class DataAnalysisImagePg(tk.Frame):
	"""Pull up images and get worm counts"""
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)    
		for column in range(3,9):
			self.grid_columnconfigure(column, weight=1)
		self.grid_columnconfigure(2, minsize=xspacer) # Spacer
		self.grid_columnconfigure(9, minsize=xspacer) # Spacer
		
		self.button1 = ttk.Button(self, text="Next\nPicture", style="TINYFONT.TButton", command=lambda: self.ChangePic(1)) 
		self.button1.grid(row=10, column=6, sticky="NESW", padx=xspacer, rowspan=4, columnspan=3)

		self.button2 = ttk.Button(self, text="Previous\nPicture", style="TINYFONT.TButton", command=lambda: self.ChangePic(-1))
		self.button2.grid(row=10, column=3, sticky="NESW", padx=xspacer, rowspan=4, columnspan=3)

		self.button3 = ttk.Button(self, text="Save\nand\nFinish", style="TINYFONT.TButton", command=lambda: self.finalpic(controller)) # Save data and provide options
		self.button3.grid(row=10, column=6, sticky="NESW", padx=xspacer, rowspan=4, columnspan=3)

		self.button4 = ttk.Button(self, text="Back to\nExperiment\nSelection", style="VERYTINYFONT.TButton", command=lambda: controller.show_frameFoxtrot2(DataAnalysisPg))
		self.button4.grid(row=10, column=3, sticky="NESW", padx=xspacer, rowspan=4, columnspan=3)

#        self.button3.lower() # Save and finish
#        self.button2.lift() # Previous picture


		# Label for number of worms counted
		self.wormscounted = ""
		self.wormscountedtext = tk.Label(self, text = "", font=VERYTINY_FONT) 
		self.wormscountedtext.grid(row=2, column=3, rowspan=2, columnspan=7, sticky="EW")
		self.wormscountedtext.configure(text = "Number of worms:\n%.5s" % self.wormscounted)

		# Label for current image number
		self.currentimagenum = -1
		self.imagenumtext = tk.Label(self, text = "", font=VERYTINY_FONT) 
		self.imagenumtext.grid(row=0, column=3, rowspan=2, columnspan=7, sticky="EW")
		self.imagenumtext.configure(text = "Image Number:\n%.3i of %.3i" % (self.currentimagenum+1, 5))

		self.f = Figure(figsize = (1,1))
		self.placesubplot() # Add subplot to figure
		self.canvas = FigureCanvasTkAgg(self.f, self) # Render canvas and fill it with figure
		self.canvas.draw() #bring canvas to front
		self.canvas.get_tk_widget().grid(row=0, column=0, rowspan = 15) #Fill options: BOTH, X, Y Expand options:  
		self.canvas.get_tk_widget().config(width=450, height=480) # TODO


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


	def click(self, z):
		"""Save user inputs and display them"""                
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
		Momo.expy[self.currentimagenum]=self.wormscounted # Store number of counted worms
		self.wormscountedtext.configure(text = "Number of worms:\n%.5s" % str(Momo.expy[self.currentimagenum])) # Configure text so user can see what they entered

	def ChangePic(self, direction):
		"""Go to next or previous screen"""
		flag=True
		self.button3.lower() # Save and finish
		self.button2.lift() # Previous picture
		if self.currentimagenum != -1 and self.wormscounted == "" and direction == 1: # Prohibit going forward without enter a number first
			tkMessageBox.showwarning("Error", "Must enter a number")
		else: # If user did enter a number
			# The next 3 if statements make sure the user can not break the program by hitting next/back too quickly
			if self.currentimagenum + direction < 0:
				self.currentimagenum=0
				flag=False
			if self.currentimagenum + direction > len(Momo.expy)-1:
				self.currentimagenum=len(Momo.expy)-1
				flag=False
			if flag:
				self.currentimagenum = self.currentimagenum + direction # Set current image index to next/previous depending on button clicked
			self.wormscountedtext.configure(text = "Number of worms:\n%.5s" % str(Momo.expy[self.currentimagenum])) # Configure text so user can see any previously entered values 
			self.wormscounted = Momo.expy[self.currentimagenum] # Get any previously entered value for current image index or "" if first time entering
			self.f.clf() # Clear plot
			self.placesubplot() # Place plot again
			img = mpimg.imread(Momo.savefile + "/ExpDataPictures/image" + str(self.currentimagenum) + ".jpg") # Read in image based on current image index
			self.a.imshow(img) # Renders image
			if Momo.exptype == "1": # Thermotaxis
				shape = Circle((200,400),150, fill=False, edgecolor="R")
			elif Momo.exptype == "2": # Chemotaxis
				shape = Circle((200,400),150, fill=False, edgecolor="R")
			elif Momo.exptype == "3": # Phototaxis
				shape = Rectangle((80,200), width=200, height=200, fill=False, edgecolor="R")
			elif Momo.exptype == "4": # Scrunching
				shape = Circle((200,400),150, fill=False, edgecolor="R")
			
			self.a.add_patch(shape)
			self.canvas.draw()
			self.imagenumtext.configure(text = "Image Number:\n%.3i of %.3i" % (self.currentimagenum+1, len(Momo.expy))) # Update text so user knows what image number they are on. +1 accounts for index starting at 0
			if self.currentimagenum == len(Momo.expy)-1: # If last image, show "generate graph" button
				self.button3.lift()
			if self.currentimagenum == 0: # If first image, show "back to experiment selection" button
				self.button4.lift()                
				
	def placesubplot(self):
		"""Add subplot to figure"""
		self.a = self.f.add_subplot(1,1,1) #add subplot RCP. Pth pos on grid with R rows and C columns
		self.a.xaxis.set_visible(False)
		self.a.yaxis.set_visible(False)
		self.a.set_position([0,0,1,1])
		self.a.set_aspect(1)
		
	def finalpic(self, controller):
		if self.wormscounted == "": # Prohibit going forward without enter a number first
			tkMessageBox.showwarning("Error", "Must enter a number")
		else:
			self.wormscounted = Momo.expy[self.currentimagenum] # Store value of just entered number
			controller.show_frameStingray(DataMenu, Momo) 

		
class DataGraphChoice(tk.Frame):
	"""Allows user to choose experiments to graph"""
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.grid_columnconfigure(1, weight=1)
		self.grid_columnconfigure(2, minsize=appwidth/30)
		
		label = tk.Label(self, text="Graph Data \n Please choose experiment(s) to graph", font=MEDIUM_FONT)
		label.grid(row = 0, column=0, columnspan = 4, sticky="NSEW", ipadx=xspacer, pady=yspacer)

		button1 = ttk.Button(self, text="Back to\nPrevious Page", style='TINYFONT.TButton', command=lambda: controller.show_frame(DataMenu)) # Go back to the data menu
		button1.grid(row=1, column = 0, sticky="NSEW", padx=xspacer)

		button2 = ttk.Button(self, text="Continue", style='TINYFONT.TButton', command = lambda: controller.show_frameShark(GraphPage, self.listofbuttons))
		button2.grid(row=1, column = 3, sticky="NSEW", padx=xspacer)

		self.explist = []
		self.listofbuttons = []

		self.canvas = tk.Canvas(self, bg = "white", height=appheight/2, width=appwidth/2, highlightthickness=0)
		self.frame = tk.Frame(self.canvas, background="#ffffff")
		self.vscrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
		self.canvas.configure(yscrollcommand=self.vscrollbar.set)
		self.canvas.grid(row=1, column=1, rowspan = 2, columnspan=1, sticky="NSEW")
		self.canvas.grid_columnconfigure(0, weight=1)
		self.vscrollbar.grid(row=1, column=2, sticky="NSEW", rowspan=2)      
		self.canvas.create_window((0,0), window=self.frame, anchor="nw", tags="self.frame")
		self.frame.bind("<Configure>", self.onFrameConfigure)
		
		# Generate checkbuttons
		i=0
		for item in os.listdir("/home/pi/Desktop/ExperimentFolder/"):
			self.explist.append(item)
		self.explist.sort()
		
		for experiment in self.explist:
			cb = ttk.Checkbutton(self.frame, text=experiment, style="checkbuttonstyle.TCheckbutton", variable=self.explist[i])
			cb.grid(row=2*i, column=0, rowspan=2, sticky="NSEW")
			self.listofbuttons.append(cb)
			i+=1
		for button in self.listofbuttons: # Set default to off
			button.state(["!focus",'!selected'])

	def onFrameConfigure(self, event):
		self.canvas.configure(scrollregion=self.canvas.bbox("all"))			

class GraphPage(tk.Frame):
	"""Page to generate graph"""
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.grid_columnconfigure(1, weight=1) # Graph column
		self.grid_rowconfigure(1, weight=1) # Graph row
		self.grid_rowconfigure(2, weight=1) # Graph row
		self.grid_rowconfigure(3, minsize=yspacer*1) # Spacer            

		self.label = tk.Label(self, text = "Graph of worms vs time" , font=LARGE_FONT)
		self.label.grid(row = 0, column=0, columnspan = 3, sticky="NSEW")
		
		button1 = ttk.Button(self,text="Back to\nExperiment\nSelection", style='TINYFONT.TButton', command=lambda: controller.show_frameFoxtrot(DataGraphChoice))
		button1.grid(row=1, column = 0, sticky="NSEW", padx=xspacer, pady=yspacer)

		button2 = ttk.Button(self,text="Main\nMenu", style='TINYFONT.TButton', command=lambda: self.returntomenu(controller)) 
		button2.grid(row=1, column = 2, sticky= "NSEW", padx=xspacer, pady=yspacer)

		button3 = ttk.Button(self,text="Save\nGraph", style='TINYFONT.TButton', command=lambda: self.savethegraph(controller))  # Save graph then show start page
		button3.grid(row=2, column = 2, sticky="nsew", padx=xspacer, pady=yspacer)

		self.f = Figure(figsize = (1,1), tight_layout=True) # tight_layout to scale
		self.a = self.f.add_subplot(1,1,1) # Add subplot to figure
		self.a.spines["top"].set_color("none")
		self.a.spines["right"].set_color("none")
		self.a.set_ylabel("Number of Worms")
		self.a.set_xlabel("Time")
		self.a.set_position([0,0,1,1])
		self.canvas = FigureCanvasTkAgg(self.f, self) # Create canvas and fill with figure
		self.canvas.get_tk_widget().grid(row=1, column=1, rowspan = 2, sticky="NSEW", pady=yspacer) 
	
	def returntomenu(self, controller):
		result = tkMessageBox.askquestion("Warning", "Returning to main menu will\nnot save the graph.\nReturn to main menu?")
		if result == "yes":
			controller.show_frame(StartPage)
	def savethegraph(self, controller):
		"""Create file name based on date and time and save graph"""
		ticker=1
		currtime = datetime.datetime.now()
		dateandtime = currtime.strftime("%Y%m%d-%H%M")
		tempaddress = "/home/pi/Desktop/Graph" +dateandtime
		nextattempt = tempaddress
		while True:
			if os.path.exists(nextattempt + ".png"): # File name already used
				nextattempt = tempaddress +"(" + str(ticker) + ")"
				ticker += 1
			else: # File name not used
				self.f.savefig(nextattempt + ".png", dpi=300) # Save graph as png
				tkMessageBox.showwarning("Done", "Graph saved to desktop as:\n"+ "'" + nextattempt[17:] + "'")
				controller.show_frame(StartPage)
				break


class DataDelPg(tk.Frame):
	"""Lets user delete selected experiments"""
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.grid_columnconfigure(2, minsize=appwidth/30)
		self.grid_columnconfigure(1, weight=1)

		label = tk.Label(self, text="Data Deletion \n Please choose experiment to delete", font=MEDIUM_FONT) 
		label.grid(row = 0, column=0, columnspan = 4, sticky="NSEW")

		button1 = ttk.Button(self, text="Main\nMenu", style='TINYFONT.TButton', command=lambda: controller.show_frame(StartPage)) 
		button1.grid(row=1, column = 0, sticky="NS", padx=xspacer)

		button2 = ttk.Button(self, text="Continue", style='TINYFONT.TButton', command = lambda: self.yoga())
		button2.grid(row=1, column = 3, sticky="NSEW", padx=xspacer)

		# Create canvas and scrollbar
		self.canvas = tk.Canvas(self, bg = "white", height=appheight/2, width=100, highlightthickness=0)
		self.frame = tk.Frame(self.canvas, background="#ffffff")
		self.vscrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
		self.canvas.configure(yscrollcommand=self.vscrollbar.set)
		self.canvas.grid(row=1, column=1, rowspan = 2, columnspan=1, sticky="NSEW")
		self.vscrollbar.grid(row=1, column=2, sticky="NSEW", rowspan=2)      
		self.canvas.create_window((0,0), window=self.frame, anchor="nw", tags="self.frame")
		self.frame.bind("<Configure>", self.onFrameConfigure)

		self.explist = []
		self.listofbuttons = []
		i=0
		for item in os.listdir("/home/pi/Desktop/ExperimentFolder/"):
			self.explist.append(item)
		self.explist.sort()

		# Add checkbuttons to canvas
		for experiment in self.explist:
			cb = ttk.Checkbutton(self.frame, text=experiment, variable=self.explist[i], style="checkbuttonstyle.TCheckbutton")
			cb.grid(row=2*i, column=0, rowspan=2, sticky="NSEW")
			self.listofbuttons.append(cb)
			i+=1
		for button in self.listofbuttons:
			button.state(["!focus",'!selected'])

	def yoga(self):
		"""Deletes experiments and refreshes page"""
		datatodelete = []
		for button in self.listofbuttons:
			if button.instate(['selected']):
				datatodelete.append(button['text'])
		datatodelete = ", ".join(datatodelete)
		result = tkMessageBox.askquestion("Discard", "Are you sure you want \nto discard these data:\n\n" + datatodelete + "\n")
		if result == "yes":
			for experiment in datatodelete:
					shutil.rmtree("/home/pi/Desktop/ExperimentFolder/" + experiment + "/")
					app.show_frameFoxtrot(DataDelPg)

	def onFrameConfigure(self, event):
		self.canvas.configure(scrollregion=self.canvas.bbox("all")) # Resize scroll region

class AnalysisTypeForNone(tk.Frame, Experiment):
	"""Choose what to analyze control as"""
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.grid_columnconfigure(0, minsize=appwidth/2.5*.9) #back button
		self.grid_columnconfigure(1, minsize=appwidth/2.5*.1) #back button
		self.grid_columnconfigure(5, minsize=appwidth/2.5) #next button
		self.grid_columnconfigure(2, weight=1) # Central column (buttons start in column 1 technically)
		self.grid_rowconfigure(1, weight=1)	# Spacer
		self.grid_rowconfigure(7, weight=1) # Spacer
		self.grid_rowconfigure(8, minsize=appheight/3) #Next/back button rows

		self.userexpchoice = int()

		label = tk.Label(self, text="This experiment had no stimulus.\nChoose analysis type to be done.", font=MEDIUM_FONT) 
		label.grid(row=0, column=0, columnspan=6, sticky="ew") 

		button1 = ttk.Button(self, text="Back to\nChoose an Experiment\nto Analyze", style="TINYFONT.TButton", command=lambda: controller.show_frameFoxtrot2(DataAnalysisPg)) # Go back to choosing an experiment to analyze
		button1.grid(row=8, column= 0, columnspan=2, sticky="nsew", padx=xspacer, pady=yspacer)

		button2 = ttk.Button(self, text="Next", style="TINYFONT.TButton", command=lambda: self.checkchosenexp(parent, controller)) # Continue to data analysis
		button2.grid(row=8, column= 5, sticky="nsew", padx=xspacer, pady=yspacer)

		self.thermobutton = ttk.Radiobutton(self, text="Thermotaxis", style="radio.TRadiobutton", variable = "ExpOption", value = 1, command = lambda: self.qfb(1)) 
		self.chemobutton = ttk.Radiobutton(self, text="Chemotaxis", style="radio.TRadiobutton", variable = "ExpOption", value = 2, command = lambda: self.qfb(2)) 
		self.photobutton = ttk.Radiobutton(self, text="Phototaxis", style="radio.TRadiobutton", variable = "ExpOption", value = 3, command = lambda: self.qfb(3)) 
		self.scrunchbutton = ttk.Radiobutton(self, text="Scrunching", style="radio.TRadiobutton", variable = "ExpOption", value = 4, command = lambda: self.qfb(4)) 
		
		for button in [self.thermobutton, self.chemobutton, self.photobutton, self.scrunchbutton]:
			button.state(["!focus",'!selected'])

		self.thermobutton.grid(row=3, column= 1, columnspan=5, sticky="w")
		self.chemobutton.grid(row=4, column= 1, columnspan=5, sticky="w")
		self.photobutton.grid(row=5, column= 1, columnspan=5, sticky="w")
		self.scrunchbutton.grid(row=6, column= 1, columnspan=5, sticky="w")
		
	def qfb(self, ExpOptionChosen): 
		self.userexpchoice = str(ExpOptionChosen) # Store the seelction

	def checkchosenexp(self, parent, controller):
		"""Make sure a type was chosen and then proceed to analysis"""
		if self.userexpchoice == int():
			tkMessageBox.showwarning("Error", "Must select an experiment type")
		else:
			Momo.set_type(self.userexpchoice) # Store pseudo exptype in control's object
			controller.show_frameBean(DataAnalysisImagePg) # Go to actual data analysis


class CameraPreviewPg(tk.Frame):
	"""Preview page to adjust focus"""
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.grid_columnconfigure(0, weight=1)	

		label = tk.Label(self, text="Preview Camera", font=MEDIUM_FONT) 
		label.grid(row=0, column=0)

		button2 = ttk.Button(self, text="Back to Main Menu", style="TINYFONT.TButton", command=lambda: controller.show_frameZebra(StartPage)) # Stop preview and show start page
		button2.grid(row=2, column=0)


def saveobject(obj):
	"""Save experiment object"""
	filename = obj.savefile + "ExpParamObj"
	with open(filename, "wb") as output:
		pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

def getobject(expname):
	"""Return experiment object from experiment name"""
	filepath = "/home/pi/Desktop/ExperimentFolder/" + expname + "/ExpParamObj"
	with open(filepath, "rb") as input:
		variablename = pickle.load(input)
	return  variablename


def getpreviouslyanalyzed(expobj):
	"""Return text for experiment type"""
	if expobj.exptype =="0":
			return("No Stimulus")
	if expobj.exptype =="1":
			return("Thermotaxis")
	if expobj.exptype == "2":
			return("Chemotaxis")
	if expobj.exptype == "3":
			return("Phototaxis")
	if expobj.exptype == "4":
			return("Scrunching")	    	


app = BehaviorBox()
app.attributes('-fullscreen', True)
app.bind("<Escape>", lambda e: app.destroy())
app.mainloop()



