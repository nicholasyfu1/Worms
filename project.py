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
		#label = tk.Label(self, text = "Figure Page!", font=LARGE_FONT)
		#label.pack(pady=10, padx=10)

		#add subplot with all images in folder 'PictureFolder'
		#f = Figure(figsize = (20,8))#define figure
		f = plt.figure(figsize = (20,8))#define figure
		i=1
		for picture in  os.listdir("/home/pi/Desktop/PictureFolder/"):
			a = f.add_subplot(6,1,i) #add subplot RCP. Pth pos on grid with R rows and C columns
			img = mpimg.imread("/home/pi/Desktop/PictureFolder/" + picture) #read in image
			a.xaxis.set_visible(False)
			a.yaxis.set_visible(False)
			"""
			#a.axis("Off")
			x0,x1=a.get_xlim()
			y0,y1=a.get_ylim()
			#a.set_aspect(abs(x1-x0)/abs(y1-y0))
			a.set_aspect(2)
			"""
			a.imshow(img) #Renders image
			i+=1
		
		#add canvas which is what we intend to render graph to and fill it with figure
		canvas = FigureCanvasTkAgg(f, self) 
		canvas.get_tk_widget().config(width=630, height=480)
		#canvas.get_tk_widget().grid_rowconfigure(1, minsize=200) 
		#canvas.get_tk_widget().grid_columnconfigure(1, minsize=200) 
		#frame2 = tk.Frame(canvas)
		canvas.draw() #raise canvas
		canvas.get_tk_widget().grid(row=0, column=0, sticky="NS") #Fill options: BOTH, X, Y Expand options:  


		#Add scrollbar
		scrollbar = tk.Scrollbar(self)
		scrollbar.config(command=canvas.get_tk_widget().yview)
#		canvas.get_tk_widget().config(scrollregion=(canvas.get_tk_widget().bbox("all")))
		canvas.get_tk_widget().config(scrollregion=(0,0,630,960))
		scrollbar.grid(row=0, column=1, sticky="NS")
		canvas.get_tk_widget().config(yscrollcommand=scrollbar.set)
		



		
		
app = Project()
app.geometry("640x480")
app.mainloop()


