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

def getpreviouslyanalyzed(Momo):
	
	if Momo.exptype =="1":
	    	return("Thermotaxis")
	if Momo.exptype == "2":
	    	return("Chemotaxis")
	if Momo.exptype == "3":
	    	return("Phototaxis")


	
	
	
	
	
	
	
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
	
	


