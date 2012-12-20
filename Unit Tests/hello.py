def simpleAddition__add__():
	arg0 = 2
	arg1 = 2
	exp = 4
	try:
		ret = arg0.__add__(arg1)
	except Exception as e:
		ret = e

	if not isinstance(ret,type(exp)): return False

	try:
		if ret != exp: return False
	except:
		try:
			if not re.equals(exp): return False
		except:
			return False

	return True

print simpleAddition__add__()
