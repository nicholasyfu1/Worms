"""

Andrew Huynh
Summer 2018
Behavior Box project


This code is for if the user selects themotaxis or chemotaxis

"""


try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk


import ttk



import tkMessageBox
import os

import matplotlib
matplotlib.use("TkAgg")

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

LARGE_FONT = ("Verdana", 12)



class Project(tk.Tk):

    #Base line code to initialize everything 

    def __init__(self, *args, **kwargs):        
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Project")
        
        container = tk.Frame(self) #Define frame/edge of window
        container.pack(side="top", fill="both", expand=True) #fill will fill space you have allotted pack. Expand will take up all white space.
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1) #0 sets minimum size weight sets priority

        self.frames = {}
        
        for F in [StartPage]:
            frame = F(container, self)
            self.frames[F] = frame 
            frame.grid(row=0, column=0, sticky="nsew") 

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise() #raise to front


class StartPage(tk.Frame):
      			
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		label = tk.Label(self, text = "Keep This Experiment's Data?", font=LARGE_FONT)
		label.grid(row = 0, column=1, columnspan = 2, sticky="NSEW")
		
		button1 = ttk.Button(self,text="Back", command=lambda: controller.show_frame(ExpFinishPg))
		button1.grid(row=1, column = 0, sticky="NS")
		

		button3 = ttk.Button(self,text="Discard", command=lambda: tkMessageBox.showwarning("Confirm Delete", "Are you sure you want \nto discard these data?")) #WAMBA
		button3.grid(row=2, column = 4, sticky="NS")

	    	i=1
		numpics = len(os.listdir("/home/pi/Desktop/ExperimentFolder/Exp22/ExpDataPictures"))
		wubdub= float(1.0/numpics)
	    	self.f = Figure(figsize = (10,40), facecolor = "R")#define figure	
	    	for picture in  os.listdir("/home/pi/Desktop/ExperimentFolder/Exp22/ExpDataPictures"):
			a = self.f.add_subplot(numpics,1,i) #add subplot RCP. Pth pos on grid with R rows and C columns
			img = mpimg.imread("/home/pi/Desktop/ExperimentFolder/Exp22/ExpDataPictures/image" + str(numpics-i) + ".jpg") #read in image
			a.xaxis.set_visible(False)
			a.yaxis.set_visible(False)
			a.set_position([0,0+wubdub*(i-1),1,wubdub])
			a.imshow(img) #Renders image
			i+=1
		#add canvas which is what we intend to render graph to and fill it with figure
		canvas = FigureCanvasTkAgg(self.f, self) 
		canvas.draw() #raise canvas
		canvas.get_tk_widget().grid(row=1, column=1, rowspan = 10, sticky="NS") #Fill options: BOTH, X, Y Expand options:  


		#Add scrollbar
		scrollbar = tk.Scrollbar(self)
		scrollbar.config(command=canvas.get_tk_widget().yview)
	#	canvas.get_tk_widget().config(scrollregion=(canvas.get_tk_widget().bbox("all")))
		canvas.get_tk_widget().config(width=630, height=numpics*450)
		canvas.get_tk_widget().config(scrollregion=(0,0,630,numpics*900))
		scrollbar.grid(row=1, column=3, sticky="NS", rowspan = 2)
		canvas.get_tk_widget().config(yscrollcommand=scrollbar.set)
		

		
		
app = Project()
app.geometry("800x480")
app.mainloop()


