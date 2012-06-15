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

tests = json.loads(j)['tests']
tmod = eval('importCode(f,"'+ mod +'.py",1)')

for test in tests:
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
	args = args[:-1]+")"
	if "+-**/>=<==".find(test['function']) != -1:
		result = eval('ob '+test['function']+' argvs[0]')
	else:
		result = eval("ob."+test['function']+args)
	if result == eval('tmod.'+test['result']['testType']+'FromJson(test["result"])'):
		print "pass"
	else:
		print "fail, got: " + str(result) + " expected: " + str(eval('tmod.'+test['result']['testType']+'FromJson(test["result"])'))
	
