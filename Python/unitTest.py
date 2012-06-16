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

mod = sys.argv[1]
f = open(mod+'.py','r')

jin = open('../Unit Tests/' + mod+'.json','r')
j = jin.read()
tmod = eval('importCode(f,"'+ mod +'.py",1)')

phases = json.loads(j)['phases']
testsPassed = True
print "\nTesting library: " + mod + ".py\n"
for phase in phases:
	print "begining phase: " + phase['phaseName']
	phasePass = True
	for test in phase['tests']:
		obJson = test['args'][0]
		ob = eval('tmod.'+obJson['testType']+'FromJson(obJson)')
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
		try:
			if "+-**/>=<==".find(test['function']) != -1:
				result = eval('ob '+test['function']+' argvs[0]')
			else:
				result = eval("ob."+test['function']+args)
		except Exception as e:
			result = e

		if "float int string bool Exception".find(test['result']['testType']) == -1:
			expect = eval('tmod.'+test['result']['testType']+'FromJson(test["result"])')
		elif test['result']['testType'] == 'Exception':
			expect = Exception()
		else:
			expect = test['result']['val']
		if result == expect or (isinstance(result,Exception) and isinstance(expect,Exception)):
			print "passed: " + test['testName']
		else:
			print "fail: "+test['testName'] + ", got: " + str(result) + " expected: " + str(expect)
			phasePass = False
	if phasePass:
		print "Phase sucessefully completed.\n"
	else:
		print "Phase was not sucessful.\n"
		testsPassed = False
if testsPassed:
	print "All tests completed sucessfully, library is correct."
else:
	print "Not all tests were completed sucessfully, review code."
