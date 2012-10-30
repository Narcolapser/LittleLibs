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
		pass

	def c(self):
		pass

	def python(self):
		pass

	def cpp(self):
		pass

class Phase:
	def __init__(self,phase):
		self.units = None

	def c(self):
		pass

	def python(self):
		pass

	def cpp(self):
		pass

class Unit:
	def __init__(self,unit):
		self.testName = unit['testName'].replace(" ","_")
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


