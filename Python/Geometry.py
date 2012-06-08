#Geometry -
#	Purpose - this contains the data types and associated maths for the representation of 2D and 3D geometry. 
#	data types - Point, Vector, BarycentricCoordinate(BC), Ray, LineSegment, AABB, Sphere, Plane, Triangle, Mesh, VoronoiRegion, tMatrix, Quaternion.
#	functions - GeometryType + Vector = GeometryType(translated). BC * (Point, Point, Point) = Point, Vector by axis = Quaternion.
import linearAlgebra

class Point(Vec3):
	def translate(self,vec):
		self += vec

class Vector(Vec3):
	pass

class BC(Vec3):
	def __init__(self,a,b,c,t):
		self.x = t.x
		self.y = t.y
		self.z = t.z
		self.a = a
		self.b = b
		self.c = c

	def locatePoint(self):
		a = self.a.scale(self.x)
		b = self.b.scale(self.y)
		c = self.c.scale(self.z)
		return a+b+c

class Ray:
	def __init__(self,loc,d):
		self.loc = loc
		self.d = d

	def translate(self,vec):
		self.loc.translate(vec)

class LineSegment:
	def __init__(self,p1,p2):
		self.p1 = p1
		self.p2 = p2

	def translate(self,vec):
		self.p1.translate(vec)
		self.p2.translate(vec)

class Sphere:
	def __init__(self,loc,rad):
		self.loc = loc
		self.r = rad

	def translate(self,vec):
		self.loc.translate(vec)

class Plane:
	def __init__(self,n,d):
		self.n = n
		self.d = d

	def translate(self,vec):
		self.n.translate(vec)

def ComputePlane(a,b,c):
	n = (b-a).Cross(c-a).normalize()
	d = n.Dot(a)
	return(Plane(n,d))

class Triangle:
	def __init__(self,a,b,c):
		self.a = a
		self.b = b
		self.c = c

	def translate(self,vec):
		self.a.translate(vec)
		self.b.translate(vec)
		self.c.translate(vec)
class Mesh:
	def __init__(self,tris):
		self.tris = tris

	def translate(self,vec):
		for tri in self.tris:
			tri.translate(vec)

class VoroniRegion:
	pass

class tMatrix:
	pass

class Quaternion(Vec4):
	pass
