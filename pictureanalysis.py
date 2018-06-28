"""

Hallloweeen

"""
import pickle

#Function to save exp object
def saveobject(obj):
	filename = obj.savefile + "ExpParamObj"
	with open(filename, "wb") as output:
		pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)


#Function to get experiment object from user chosen exp
def getobject(expname):
	filepath = "/home/pi/Desktop/ExperimentFolder/" + expname + "/ExpParamObj"
	with open(filepath, "rb") as input:
		variablename = pickle.load(input)
	return  variablename
"""	
#function to 
def 
	#Pull up image
	#Draw circle based on exp type
	#Enter number of worms
	
	

		for picture in  os.listdir("/home/pi/Desktop/ExperimentFolder/PictureFolder"):
			a = f.add_subplot(5,1,i) #add subplot RCP. Pth pos on grid with R rows and C columns
			img = mpimg.imread("/home/pi/Desktop/ExperimentFolder/PictureFolder/" + picture) #read in image
			a.xaxis.set_visible(False)
			a.yaxis.set_visible(False)
			a.set_position([0,0+wubdub*(i-1),.5,wubdub])
			a.imshow(img) #Renders image
			i+=1	
"""	
	
	
	
	
	
	
	
	
	
class Experiment():
	
	def __init__(self):
		self.expnumber = str()
		self.exptype = str()
		self.exptime = int()
		self.savefile = "/home/pi/Desktop/ExperimentFolder/Exp" + "21" + "/"
		self.capturerate=5
	def set_number(self, number):
		self.expnumber = str(number)
	def set_type(self, exptype):
		self.exptype = str(exptype)
	def set_exptime(self, totaltime):
		self.exptime = int(totaltime)
	def set_savefile(self, savetofile):
		self.savefile = str(savetofile)
	
	


