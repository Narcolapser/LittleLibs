import json
import sys
import imp

def importCode(code,name,add_to_sys_modules=0):
	"""
	Import dynamically generated code as a module. code is the
	object containing the code (a string, a file handle or an
	actual compiled code object, same types as accepted by an
	exec statement). The name is the name to give to the module,
	and the final argument says wheter to add it to sys.modules
	or not. If it is added, a subsequent import statement using
	name will return this module. If it is not added to sys.modules
	import will try to load it in the normal fashion.

	import foo
	
	is equivalent to
	
	foofile = open("/path/to/foo.py")
	foo = importCode(foofile,"foo",1)

	Returns a newly generated module.
	"""
	module = imp.new_module(name)

	exec code in module.__dict__
	if add_to_sys_modules:
		sys.modules[name] = module

	return module

def getPhases(mod):
	jin = open('../Unit Tests/' + mod+'.json','r')
	j = jin.read()
	jin.close()
	return json.loads(j)['phases']

def getTestedModuleResult(test,argvs,args):
	try:
		if "+-**/>=<==".find(test['function']) != -1:
			return eval('ob '+test['function']+' argvs[0]')
		else:
			return eval('ob.'+test['function']+args)
	except Exception as e:
		return e

def getTestArguments(tmod, test):
	args = "("
	argvs = []
	for i,arg in enumerate(test['args'][1:]):
		if "float int string bool".find(arg['testType']) == -1:
			argvs.append(eval('tmod.'+arg['testType']+'FromJson(arg)'))
		else:
			argvs.append(arg['val'])
		args += "argvs["+str(i)+"],"
	if (len(args)==1):
		args+= ")"
	else:
		args = args[:-1]+")"
	return (args,argvs)

def getExpectedResult(tmod,test):
	if "float int string bool Exception".find(test['result']['testType']) == -1:
		return eval('tmod.'+test['result']['testType']+'FromJson(test["result"])')
	elif test['result']['testType'] == 'Exception':
		return Exception()
	else:
		return test['result']['val']

def compareResults(test, result,expect):
	#This checks the most common cases, the ones where simply they are the same. a second
	#condition was added as well to cover the case where an exception is what was expected.
	if  (isinstance(result,Exception) and isinstance(expect,Exception)):
		print "passed: " + test['testName']
		return True
	try:
		if  result == expect:
			print "passed: " + test['testName']
			return True

	except Exception as e:
		pass

	try:
		if str(result) == str(expect):
			print "passed: " + test['testName']
			return True
		else:
			print "fail: "+test['testName'] + ", got: " + str(result) + " expected: " + str(expect)
			return False
	except Exception as e:
		pass

	print "fail: "+test['testName'] + ", got: " + str(result) + " expected: " + str(expect)
	return False



mod = sys.argv[1]
f = open(mod+'.py','r')
tmod = eval('importCode(f,"'+ mod +'.py",1)')

phases = getPhases(mod)
testsPassed = True
print "\nTesting library: " + mod + ".py\n"

for phase in phases:
	print "begining phase: " + phase['phaseName']
	phasePass = True
	for test in phase['tests']:
		obJson = test['args'][0]
		ob = eval('tmod.'+obJson['testType']+'FromJson(obJson)')
		args = ""
		argvs = []

		args,argvs = getTestArguments(tmod,test)
		result = getTestedModuleResult(test,argvs,args)
		expect = getExpectedResult(tmod,test)

		testPassed = compareResults(test,result,expect)

		phasePass = testPassed and phasePass

	if phasePass:
		print "Phase sucessefully completed.\n"
	else:
		print "Phase was not sucessful.\n"
		testsPassed = False
if testsPassed:
	print "All tests completed sucessfully, library is correct."
else:
	print "Not all tests were completed sucessfully, review code."
