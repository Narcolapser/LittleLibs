#	data types - AABB, OBB, BoundSphere, static Octree, dynamic Octree.
#	functions - Create{AABB,OBB,BoundSphere}(Mesh,triangle,sphere,Point[]).

import Geometry

class AABB:
	def __init__(self,ma,mi):
		self.max = ma
		self.min = mi

	def translate(self,vec):
		self.max.translate(vec)
		self.min.translate(vec)

class OBB:
	def __init__(self,loc,u,e):
		self.loc = loc
		self.u = u #these are the local axi.
		self.e = e ##positive half width extents of OBB along each axis.

class BoundingSphere(Sphere):
	pass

class StaticOctree(AABB):
	pass

class DynamicOctree(AABB):
	pass
