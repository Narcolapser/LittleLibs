###################################################################################################
##	Program:	LittleLibs Unit Test Genorator
##	Version:	0.1
##	Date:		12/10/30
##	Programmer:	Toben "Littlefoot" Archer
##	Purpose:	This program parses in the json unit test descriptor and out puts an
##		appropriate unit test for the desired language based off of the user's request.
###################################################################################################

import json
import sys

class Test:
	def __init__(self,unitTest):
		self.phases = []
		for phase in unitTest['phases']:
			self.phases.append(Phase(phase))

	def c(self):
		pass

	def python(self):
		pass

	def cpp(self):
		pass

class Phase:
	def __init__(self,phase):
		self.units = []
		for unit in phase['tests']:
			self.units.append(Unit(phase['phaseName'],unit))

	def c(self):
		pass

	def python(self):
		output = "phasePassed = True\n"
		for unit in self.units:
			output += "args = [] \n"
			for a in unit.args:
				output += "args.append("
				output += a.['testType']
				output += "("
				for arg in range(a['argc']):
					
	def pythonLoadJsonArgString(self,val):
		if val['testType'] == "float" or val['testType'] == "string" or val['testType'] == "array" or val['testType'] == "bool" or val['testType'] == "int":
			return val['arg0']
		retString = val['testType']+"("
		for arg in range(val['argc']):
			if val['testType'] == "float" or val['testType'] == "string" or val['testType'] == "array" or val['testType'] == "bool" or val['testType'] == "int":
			retString += 
phasePassed = True
args = []
args.append(Vec2(1,1))
args.append(Vec2(2,2))
phasePassed &= Vec2_common_cases_Dot_product(args)

			

	def cpp(self):
		pass

class Unit:
	def __init__(self,phase,unit):
		self.testName = (phase + '_' + unit['testName']).replace(" ","_")
		self.func = unit['function']
		self.argc = int(unit['argc'])
		self.args = unit['args']
		self.result = unit['result']

	def c(self):
		pass

	def python(self):
		function = "\tdef " + self.testName + "(args)\n"
		function += "\t\ttry:\n\t\t\tresult = args[0]." + self.func + "( "
		for i in range(self.argc-1):
			function += "args[" + str(i+1) + "],"
		function = function[:-1]+")\n"
		function += "\t\texcept Exception as e:\n\t\t\tresult = e\n"
		function += "\t\tif not isinstance(result,type(self.result)): return False\n"
		function += "\t\ttry:\n\t\t\tif not (result == self.result): return False\n"
		function += "\t\texcept:\n\t\t\tpass\n"
		function += "\t\ttry:\n\t\t\tif not (result.equals(self.result)): return False\n"
		function += "\t\texcept:\n\t\t\treturn False\n"
		function += "\t\treturn True\n"
		return function

	def Dot_product(args):
		try:
			result = args[0].Dot(args[1])
		except Exception as e:
			result = e
		if not isinstance(result,float): return False
		try:
			if (result != self.result): return False
		except:
			pass
		try:
			if not (self.result.equals(result)): return False
		except:
			return False
		return True

	def cpp(self):
		pass

if len(sys.argv) < 3:
	print "Insufficient arguments. Usage:"
	print "python unitTest.py [name of module] [language] [optional output directory]"
	print "language is declared by naming the extension. Available extensions:"
	print "\t-py,-c"
	exit()

mod = sys.argv[1]
if len(sys.argv) > 3:
	outputDir = sys.argv[3]
else:
	outputDir = ""

textTests = open(mod,'r')
jsonTests = json.loads(textTests)

test = Test(jsonTests)

if sys.argv[2] == "-py":
	output = test.python()
	out = open(outputDir+mod+".py","w")
	out.write(output)
	out.close()
else if sys.argv[2] == "-c":
	output = test.c()
	out = open(outputDir+mod+".c","w")
	out.write(output)
	out.close()
else:
	print "un-recognized language."
	exit()

