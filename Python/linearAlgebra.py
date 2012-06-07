#linearAlgebra -
#	Purpose - this contains the vectors and matrices and associated maths.
#	data types - vec2,vec3,vec4,matrix2x2,matrix3x3,matrix4x4.
#	functions - vecx(+,-,*,dot,cross(only for vec3), matrixx(+,-,*)

class Vec2:
	def __init__(self,x,y):
		self.x = x
		self.y = y

	def __add__(self,val):
		return Vec2(self.x+val.x,self.y+val.y)

	def __sub__(self,val):
		return Vec2(self.x-val.x,self.y-val.y)

	def Dot(self,val):
		return self.x*val.x + self.y*val.y

class Vec3:
	def __init__(self,x,y,z):
		self.x = x
		self.y = y
		self.z = z

	def __add__(self,val):
		return Vec3(self.x+val.x,self.y+val.y,self.z+val.z)

	def __sub__(self,val):
		return Vec3(self.x-val.x,self.y-val.y,self.z-val.z)

	def Dot(self,val):
		return self.x*val.x + self.y*val.y + self.z*val.z

	def Cross(self,val):
		x = self.y * val.z - self.z * val.y
		y = -(self.x * val.z - self.z * val.x)
		z = self.x * val.y - self.y * val.x
		return Vec3(x,y,z)

