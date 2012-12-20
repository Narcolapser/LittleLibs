###################################################################################################
##	Program:	LittleLibs Unit Test Genorator
##	Version:	0.2
##	Date:		12/11/22
##	Programmer:	Toben "Littlefoot" Archer
##	Purpose:	This program parses in the json unit test descriptor and out puts an
##		appropriate unit test for the desired language based off of the user's request.
###################################################################################################

import json
import sys

class Battery:
	def __init__(self,json):
		self.name = json['args']['arg0']['value']
		self.units = []
		for unit in units:
			self.units.append(loadTests(unit['args']['arg1']['value']))

	def c(self):
		pass

	def python(self):
		battery = ""

		for unit in self.units:
			battery += unit.python()
		
		battery += self.name + 'Passed = True\n\n'
		for unit in self.unit:
			battery += self.name + 'Passed &= ' + unit.name + 'Passed\n'

		battery += 'if ' + self.name + 'Passed: print "Battery completely passed. This module is white box tested and correct."\n'
		battery += 'else: print "Battery failed. So this module isn\' perfect, but it probably does well."\n\n'

		return battery

	def cpp(self):
		pass

class Unit:
	def __init__(self,json):
		self.name = json['args']['arg0']['value']
		self.phases = []
		for phase in json['args']['arg1']['value']:
			self.phases.append(loadTests(phase))

	def c(self):
		pass

	def python(self):
		print "building unit test:" + self.name
		unit = ""

		for phase in self.phases:
			unit += phase.python()
		
		unit += self.name + 'Passed = True\n'
		for phase in self.phases:
			unit += self.name + 'Passed &= ' + phase.name + 'Passed\n'

		unit += '\nif ' + self.name + 'Passed: print "Unit passed. This module is black box correct."\n'
		unit += 'else: print "Unit failed. This module needs work."\n\n'

		return unit

	def cpp(self):
		pass

class Phase:
	def __init__(self,json):
		self.name = json['args']['arg0']['value']
		self.tests = []
		for test in json['args']['arg1']['value']:
			self.tests.append(loadTests(test))

	def c(self):
		pass

	def python(self):
		print "building phase:" + self.name
		phase = ""

		for test in self.tests:
			phase += test.python()
		
		phase += 'print "running phase ' + self.name + ':"\n'
		phase += self.name + 'Passed = True\n\n'
		

		for test in self.tests:
			phase += 'print "test ' + test.name + test.function + ': " + str('
			phase += test.name + test.function + '())\n'
			phase += self.name + 'Passed &= ' + test.name + test.function + '()\n'

		phase += '\nif ' + self.name + 'Passed:\n\tprint "All tests passed, this phase cleared."\n'
		phase += 'else: print "One or more tests failed, this phase was not cleared."\n#####     End of Phase: ' + self.name + '     #########################\n\n\n'

		return phase

	def cpp(self):
		pass

class Test:
	def __init__(self,name,function,argc,args,ret):
		self.name = name
		self.function = function
		self.argc = argc
		self.args = []
		for i in args:
			self.args.append(tLoader(i))
		self.ret = tLoader(ret)
		try:
			self.retEquality = ret['ret']
		except:
			self.retEquality = True

	def c(self):
		pass

	def python(self):
		print "building test:" + self.name
		test = ""
		test += "def " + self.name + self.function + "():\n"
		for i,arg in enumerate(self.args):
			test += "\targ" + str(i) + " = " 
			test += self.args[i].python() + "\n"
		test += "\texp = " + self.ret.python() + "\n"
		
		test += "\ttry:\n\t\tret = arg0." + self.function + "("
		for i,arg in enumerate(self.args[1:]):
			test += "arg" + str(i+1) + ", "
		test = test[:-2] + ")\n"
		test += "\t\tif ret == NotImplemented: raise Exception()\n"
		test += "\texcept Exception as e:\n\t\tret = Exception()\n\n"

		test += "\tif not isinstance(ret,type(exp)): return False\n\n"

		test += "\tif isinstance(ret,Exception): return True\n"
		test += "\tif isinstance(ret,type(None)): return True\n\n"

		if self.retEquality:
			test += "\ttry:\n\t\tif ret != exp: return False\n\texcept:\n"

			test += "\t\ttry:\n\t\t\tif not re.equals(exp): return False\n\t\texcept:\n\t\t\treturn False\n\n"

			test += "\treturn True\n\n"

			return test
		

		test += "\ttry:\n\t\tif ret == exp: return False\n\texcept:\n"

		test += "\t\ttry:\n\t\t\tif re.equals(exp): return False\n\t\texcept:\n\t\t\treturn False\n\n"

		test += "\treturn True\n\n"

		return test

	def cpp(self):
		pass

def loadTests(val):
	if val['value'] == "battery":
		return Battery(val)
	if val['value'] == "unit":
		return Unit(val)
	if val['value'] == "phase":
		return Phase(val)
	if val['value'] == "test":
		return Test(val['args']['arg0']['value'],
			val['args']['arg1']['value'],
			val['args']['arg2']['value'],
			val['args']['arg3']['value'],
			val['args']['arg4'])
	return None

def tLoader(val):
	if val['type'] == 'object':
		return Tobject(val)
	elif val['type'] == 'list':
		return Tlist(val['value'])
	elif val['type'] == 'string':
		return Tstring(val['value'])
	elif val['type'] == 'float':
		return Tfloat(val['value'])
	elif val['type'] == 'number':
		return Tnumber(val['value'])
	elif val['type'] == 'char':
		return Tchar(val['value'])
	elif val['type'] == 'bool':
		return Tbool(val['value'])
	elif val['type'] == 'exception':
		return Texception()
	else:
		return TNULL()

class Tobject:
	def __init__(self,val):
		self.obType = val['value']
		self.argc = val['argc']
		self.args = []
		for i in val['args']:
			self.args.append(tLoader(i))

class Tlist:
	def __init__(self,val):
		self.items = []
		for i in val:
			self.items.append(tLoader(i))

class Tstring:
	def __init__(self,val):
		self.val = val

	def python(self):
		return '"' + self.val + '"'

class Tfloat:
	def __init__(self,val):
		self.val = val

class Tnumber:
	def __init__(self,val):
		self.val = val

	def python(self):
		return str(self.val)

class Tchar:
	def __init__(self,val):
		self.val = val

class Tbool:
	def __init__(self,val):
		self.val = val

class Texception:
	def __init__(self):
		pass

	def python(self):
		return "Exception()"

class TNULL:
	def __init__(self):
		pass

	def python(self):
		return "None"

def jsonIn(json):
	if json['type'] == "object":
		return jsonInObject(json)
	elif json['type'] == "list":
		return jsonInObject(json)
	elif json['type'] == "string":
		return jsonInObject(json)
	elif json['type'] == "number":
		return jsonInObject(json)
	elif json['type'] == "float":
		return jsonInObject(json)
	elif json['type'] == "bool":
		return jsonInObject(json)
	elif json['type'] == "exception":
		return jsonInObject(json)
	elif json['type'] == "char":
		return jsonInObject(json)
	elif json['type'] == "null":
		return jsonInObject(json)
	else:
		return None

#def jsonInObject(json):
#	try:
#		args = []
#		for arg in json['args']:
#			args.append(jsonIn(json))
#		exes = json['value'] + "("
#		for arg in range(len(args)):
#			exes+= "args[" + str(arg) + "],"
#		exes = exes[:-1] + ")"
#		return exec(exes)			

#	except:
#		return None

#def jsonInList(json):
#	ret = []
#	for item in json['value']:
#		ret.append(jsonIn(itme))
#	return ret

#def jsonInString(json):
#	return json['value']

#def jsonInNumber(json):
#	return json['value']

#def jsonInFloat(json):
#	return float.fromhex(json['value'])

#def jsonInBool(json):
#	return json['value']

#def jsonInChar(json):
#	return json['value']

#def jsonInException(json):
#	return Exception()

#def jsonInNull(json):
#	return None

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

fileTests = open(mod+".json",'r')
textTests = fileTests.read()
jsonTests = json.loads(textTests)

test = loadTests(jsonTests)

if sys.argv[2] == "-py":
	output = test.python()
	out = open(outputDir+mod+".py","w")
	out.write(output)
	out.close()
elif sys.argv[2] == "-c":
	output = test.c()
	out = open(outputDir+mod+".c","w")
	out.write(output)
	out.close()
else:
	print "un-recognized language."
	exit()


