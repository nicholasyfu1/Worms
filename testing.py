import Tkinter as tk
import os
from Tkinter import Tk, Canvas
from PIL import ImageTk, Image
root = Tk()
savefile = "/home/pi/Desktop/ExperimentFolder/Exp547/"
i=0
numpics = len(os.listdir(savefile + "ExpDataPictures"))
imglist = []

canvas=tk.Canvas(root, width=600, height=400)
canvas.grid(row=1, column=0, rowspan=2)
for k in range(11):
	canvas.create_text(20, k*100, text=(str(k*100)))
for picture in  os.listdir(savefile + "ExpDataPictures"):
	img = Image.open(savefile+ "ExpDataPictures/image" + str(i) + ".jpg", mode="r") #read in image
	tempimage = ImageTk.PhotoImage(img)
	imglist.append(tempimage)
	canvas.create_image(80,0+480*i,image=imglist[i],anchor="nw")
	width, height = img.size
	i+=1
	print(str(width))
	print(str(height))
	

scrollbar = tk.Scrollbar(root)
scrollbar.config(command=canvas.yview)
canvas.config(scrollregion=(canvas.bbox("all")))
print(canvas.bbox("all"))
scrollbar.grid(row=1, column=2, rowspan = 2, columnspan=1, sticky="NS")
canvas.config(yscrollcommand=scrollbar.set)
root.mainloop()


"""
from Tkinter import *
import Image, ImageTk

root = Tk()

frame = Frame(root, bd=2, relief=SUNKEN)

frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)

xscrollbar = Scrollbar(frame, orient=HORIZONTAL)
xscrollbar.grid(row=1, column=0, sticky=E+W)

yscrollbar = Scrollbar(frame)
yscrollbar.grid(row=0, column=1, sticky=N+S)

canvas = Canvas(frame, bd=0, xscrollcommand=xscrollbar.set, yscrollcommand=yscrollbar.set)
canvas.grid(row=0, column=0, sticky=N+S+E+W)

File = "/home/pi/Desktop/ExperimentFolder/Exp01/ExpDataPictures/image0.jpg"
img = ImageTk.PhotoImage(Image.open(File))
canvas.create_image(0,0,image=img, anchor="nw")

xscrollbar.config(command=canvas.xview)
yscrollbar.config(command=canvas.yview)
canvas.config(scrollregion=canvas.bbox(ALL))
frame.pack()
root.mainloop()
"""
