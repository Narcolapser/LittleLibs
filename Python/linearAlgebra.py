#linearAlgebra -
#	Purpose - this contains the vectors and matrices and associated maths.
#	data types - vec2,vec3,vec4,matrix2x2,matrix3x3,matrix4x4.
#	functions - vecx(+,-,*,dot,cross(only for vec3), matrixx(+,-,*,det,inverse)

import math

EPSILON = 4.94065645841e-324

class Vec2:
	def __init__(self,x,y):
		self.x = x * 1.0
		self.y = y * 1.0

	def __add__(self,val):
		return Vec2(self.x+val.x,self.y+val.y)

	def __sub__(self,val):
		return Vec2(self.x-val.x,self.y-val.y)

	def __eq__(self,val):
		return self.x == val.x and self.y == val.y

	def __ne__(self,val):
		return not self == val

	def __lt__(self,val):
		return self.x < val.x and self.y < val.y

	def __le__(self,val):
		return self < val or self == val

	def __gt__(self,val):
		return self.x > val.x and self.y > val.y

	def __ge__(self,val):
		return self > val or self == val

	def __str__(self):
		return "X: " + str(self.x) + " Y: " + str(self.y)

	def Scale(self,val):
		return Vec2(self.x*val,self.y*val)

	def Dot(self,val):
		return self.x*val.x + self.y*val.y

	def Magnitude(self):
		return math.sqrt(self.Dot(self))

	def Normalize(self):
		w = math.sqrt(self.x * self.x + self.y * self.y)
		if w == 0 and self.x == 0: return self
		self.x /= w
		self.y /= w
		return self

def Vec2FromJson(json):
	return Vec2(json['x'],json['y'])

class Vec3:
	def __init__(self,x,y,z):
		self.x = x * 1.0
		self.y = y * 1.0
		self.z = z * 1.0

	def __add__(self,val):
		return Vec3(self.x+val.x,self.y+val.y,self.z+val.z)

	def __sub__(self,val):
		return Vec3(self.x-val.x,self.y-val.y,self.z-val.z)

	def __eq__(self,val):
		return self.x == val.x and self.y == val.y and self.z == val.z 

	def __ne__(self,val):
		return not self == val

	def __lt__(self,val):
		return self.x < val.x and self.y < val.y and self.z < val.y

	def __le__(self,val):
		return self < val or self == val

	def __gt__(self,val):
		return self.x > val.x and self.y > val.y and self.z > val.z

	def __ge__(self,val):
		return self > val or self == val

	def __str__(self):
		return "X: " + str(self.x) + " Y: " + str(self.y) + " Z: " + str(self.z)

	def Scale(self,val):
		return Vec3(self.x*val,self.y*val,self.z*val)

	def Dot(self,val):
		return self.x*val.x + self.y*val.y + self.z*val.z

	def Cross(self,val):
		x = self.y * val.z - self.z * val.y
		y = -(self.x * val.z - self.z * val.x)
		z = self.x * val.y - self.y * val.x
		return Vec3(x,y,z)

	def Magnitude(self):
		return math.sqrt(self.Dot(self))

	def Normalize(self):
		if(self.y == 0 and self.x == 0 and self.z == 0): return self
		w = self.Magnitude()
		self.x /= w
		self.y /= w
		self.z /= w
		return self

def Vec3FromJson(json):
	return Vec3(json['x'],json['y'],json['z'])

class Vec4:
	def __init__(self,x,y,z,w):
		self.x = x
		self.y = y
		self.z = z
		self.w = w

	def __add__(self,val):
		return Vec4(self.x+val.x,self.y+val.y,self.z+val.z,self.w+val.w)

	def __sub__(self,val):
		return Vec4(self.x-val.x,self.y-val.y,self.z-val.z,self.w-val.w)

	def __eq__(self,val):
		return self.x == val.x and self.y == val.y and self.z == val.z and self.w == val.w

	def __ne__(self,val):
		return not self == val

	def __lt__(self,val):
		return self.x < val.x and self.y < val.y and self.z < val.y and self.w == val.w

	def __le__(self,val):
		return self < val or self == val

	def __gt__(self,val):
		return self.x > val.x and self.y > val.y and self.z > val.z and self.w == val.w

	def __ge__(self,val):
		return self > val or self == val

	def __str__(self):
		return "X: " + str(self.x) + " Y: " + str(self.y) + " Z: " + str(self.z) + " W: " + str(self.w)

	def Scale(self,val):
		return Vec4(self.x*val,self.y*val,self.z*val,self.w*val)

	def Dot(self,val):
		return self.x*val.x + self.y*val.y + self.z*val.z + self.w*val.w

	def Magnitude(self):
		return self.Dot(self)

	def Normalize(self):
		w = self.Magnitude()
		self.x /= w
		self.y /= w
		self.z /= w
		self.w /= w
		return self

def Vec4FromJson(json):
	return Vec4(json['x'],json['y'],json['z'],json['w'])

class Matrix2x2:
	def __init__(self,a,b):
		self.a = a
		self.b = b

	def __add__(self,val):
		return Matrix2x2(self.a+val.a,self.b+val.b)

	def __sub__(self,val):
		return Matrix2x2(self.a-val.a,self.b-val.b)

	def __mul__(self,val):
		a = Vec2(self.a.x*val.a.x + self.b.x*val.a.y,
				self.a.x*val.b.x + self.b.x*val.b.y)
		b = Vec2(self.a.x*val.a.x + self.b.x*val.a.y,
				self.a.x*val.b.x + self.b.x*val.b.y)
		return Matrix2x2(a,b)

class Matrix3x3:
	def __init__(self,a,b,c):
		self.a = a
		self.b = b
		self.c = c

	def __add__(self,val):
		return Matrix3x3(self.a+val.a,self.b+val.b,self.c+val.c)

	def __sub__(self,val):
		return Matrix3x3(self.a-val.a,self.b-val.b,self.c+val.c)

class Matrix4x4:
	def __init__(self,a,b,c):
		self.a = a
		self.b = b
		self.c = c
		self.d = d

	def __add__(self,val):
		return Matrix4x4(self.a+val.a,self.b+val.b,self.c+val.c,self.d+val.d)

	def __sub__(self,val):
		return Matrix4x4(self.a-val.a,self.b-val.b,self.c+val.c,self.d+val.d)
