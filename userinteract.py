"""

Andrew Huynh
Summer 2018
Behavior Box project


This code is for if the user selects themotaxis or chemotaxis

"""
# The code for changing pages was derived from: http://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter
# License: http://creativecommons.org/licenses/by-sa/3.0/	

import Tkinter as tk
import ttk


LARGE_FONT= ("Verdana", 12)


class SeaofBTCapp(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)

    
        tk.Tk.wm_title(self, "Sea of BTC Client")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageOne, PageTwo):

            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()


        
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        
 	
	self.phone = int(3)
	home = ttk.Radiobutton(parent, text='Home', variable=self.phone, value= 1, command = lambda: self.selected(home.value))
	office = ttk.Radiobutton(parent, text='Office', variable=self.phone, value= 2, command = lambda: self.selected(office.value))
	home.grid(row=10)
	office.grid(row=1)
	
    def selected(self, value):
        self.phone.set(value)
        if self.phone == 3:
        	print ("It initalized")
	elif self.phone == "":
		print("Still empty")
	elif self.phone == 1:
		print("You made it")
	elif self.phone == 2:
		print("Heyyy it worked")
class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Page One!!!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = ttk.Button(self, text="Page Two",
                            command=lambda: controller.show_frame(PageTwo))
        button2.pack()


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Page Two!!!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = ttk.Button(self, text="Page One",
                            command=lambda: controller.show_frame(PageOne))
        button2.pack()
        


app = SeaofBTCapp()
app.mainloop()
