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

try:
	from Tkinter import *
	import ttk
except:
	from tkinter import ttk
	from tkinter import *
	from tkinter.ttk import *

import tkMessageBox
import os

import matplotlib
matplotlib.use("TkAgg")

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
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
		label = tk.Label(self, text = "Figure Page!", font=LARGE_FONT)
		label.pack(pady=10, padx=10)

		#add subplot with all images in folder 'PictureFolder'
		f = Figure(figsize = (8,8), dpi=100)#define figure		
		i=1
		for picture in  os.listdir("/home/pi/Desktop/PictureFolder/"):
			a = f.add_subplot(6,1,i) #add subplot RCP. Pth pos on grid with R rows and C columns
			img = mpimg.imread("/home/pi/Desktop/PictureFolder/" + picture) #read in image
			a.imshow(img) #Renders image
			i+=1
			
		#add canvas which is what we intend to render graph to and fill it with figure
		canvas = FigureCanvasTkAgg(f, self) 
		#frame2 = tk.Frame(canvas)
		canvas.draw() #raise canvas
		canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.X, expand=True) #Fill options: BOTH, X, Y Expand options:  
		
		#Add figure toolbar
		toolbar = NavigationToolbar2Tk(canvas, self) #add traditionalmatplotlib toolbar
		toolbar.update()
		canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
		

		#Add scrollbar
		scrollbar = Scrollbar(canvas)
		scrollbar.config(command=canvas.yview)
		
		scrollbar.pack(side=RIGHT, fill = Y)
		canvas.pack(side=LEFT, expand = YES, fill=BOTH)
		
		canvas.config(yscrollcommand=scrollbar.set)



		
		
app = Project()
app.geometry("640x480")
app.mainloop()

mainloop()
