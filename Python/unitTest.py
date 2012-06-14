import json
import sys

f = open(sys.argv[1],'r')
j = f.read()

tests = json.loads(j)['tests']

print len(tests)
