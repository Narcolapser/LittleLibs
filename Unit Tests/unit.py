def simpleAddition__add__():
	arg0 = 2
	arg1 = 2
	exp = 4
	try:
		ret = arg0.__add__(arg1)
		if ret == NotImplemented: raise Exception()
	except Exception as e:
		ret = Exception()

	if not isinstance(ret,type(exp)): return False

	if isinstance(ret,Exception): return True
	if isinstance(ret,type(None)): return True

	try:
		if ret != exp: return False
	except:
		try:
			if not re.equals(exp): return False
		except:
			return False

	return True

def simpleSubtraction__sub__():
	arg0 = 2
	arg1 = 2
	exp = 0
	try:
		ret = arg0.__sub__(arg1)
		if ret == NotImplemented: raise Exception()
	except Exception as e:
		ret = Exception()

	if not isinstance(ret,type(exp)): return False

	if isinstance(ret,Exception): return True
	if isinstance(ret,type(None)): return True

	try:
		if ret != exp: return False
	except:
		try:
			if not re.equals(exp): return False
		except:
			return False

	return True

print "running phase simpleArithmaticCommonCase:"
simpleArithmaticCommonCasePassed = True

print "test simpleAddition__add__: " + str(simpleAddition__add__())
simpleArithmaticCommonCasePassed &= simpleAddition__add__()
print "test simpleSubtraction__sub__: " + str(simpleSubtraction__sub__())
simpleArithmaticCommonCasePassed &= simpleSubtraction__sub__()

if simpleArithmaticCommonCasePassed:
	print "All tests passed, this phase cleared."
else: print "One or more tests failed, this phase was not cleared."
#####     End of Phase: simpleArithmaticCommonCase     #########################


def simpleAddition__add__():
	arg0 = 2
	arg1 = 5
	exp = 4
	try:
		ret = arg0.__add__(arg1)
		if ret == NotImplemented: raise Exception()
	except Exception as e:
		ret = Exception()

	if not isinstance(ret,type(exp)): return False

	if isinstance(ret,Exception): return True
	if isinstance(ret,type(None)): return True

	try:
		if ret == exp: return False
	except:
		try:
			if re.equals(exp): return False
		except:
			return False

	return True

def simpleSubtraction__sub__():
	arg0 = 2
	arg1 = 2
	exp = 4
	try:
		ret = arg0.__sub__(arg1)
		if ret == NotImplemented: raise Exception()
	except Exception as e:
		ret = Exception()

	if not isinstance(ret,type(exp)): return False

	if isinstance(ret,Exception): return True
	if isinstance(ret,type(None)): return True

	try:
		if ret == exp: return False
	except:
		try:
			if re.equals(exp): return False
		except:
			return False

	return True

print "running phase simpleArithmaticCommonFailCases:"
simpleArithmaticCommonFailCasesPassed = True

print "test simpleAddition__add__: " + str(simpleAddition__add__())
simpleArithmaticCommonFailCasesPassed &= simpleAddition__add__()
print "test simpleSubtraction__sub__: " + str(simpleSubtraction__sub__())
simpleArithmaticCommonFailCasesPassed &= simpleSubtraction__sub__()

if simpleArithmaticCommonFailCasesPassed:
	print "All tests passed, this phase cleared."
else: print "One or more tests failed, this phase was not cleared."
#####     End of Phase: simpleArithmaticCommonFailCases     #########################


def simpleAddition__add__():
	arg0 = 2
	arg1 = "two"
	exp = Exception()
	try:
		ret = arg0.__add__(arg1)
		if ret == NotImplemented: raise Exception()
	except Exception as e:
		ret = Exception()

	if not isinstance(ret,type(exp)): return False

	if isinstance(ret,Exception): return True
	if isinstance(ret,type(None)): return True

	try:
		if ret != exp: return False
	except:
		try:
			if not re.equals(exp): return False
		except:
			return False

	return True

def simpleSubtraction__sub__():
	arg0 = 2
	arg1 = None
	exp = Exception()
	try:
		ret = arg0.__sub__(arg1)
		if ret == NotImplemented: raise Exception()
	except Exception as e:
		ret = Exception()

	if not isinstance(ret,type(exp)): return False

	if isinstance(ret,Exception): return True
	if isinstance(ret,type(None)): return True

	try:
		if ret != exp: return False
	except:
		try:
			if not re.equals(exp): return False
		except:
			return False

	return True

print "running phase simpleArithmaticBroken:"
simpleArithmaticBrokenPassed = True

print "test simpleAddition__add__: " + str(simpleAddition__add__())
simpleArithmaticBrokenPassed &= simpleAddition__add__()
print "test simpleSubtraction__sub__: " + str(simpleSubtraction__sub__())
simpleArithmaticBrokenPassed &= simpleSubtraction__sub__()

if simpleArithmaticBrokenPassed:
	print "All tests passed, this phase cleared."
else: print "One or more tests failed, this phase was not cleared."
#####     End of Phase: simpleArithmaticBroken     #########################


intsPassed = True
intsPassed &= simpleArithmaticCommonCasePassed
intsPassed &= simpleArithmaticCommonFailCasesPassed
intsPassed &= simpleArithmaticBrokenPassed

if intsPassed: print "Unit passed. This module is black box correct."
else: print "Unit failed. This module needs work."

