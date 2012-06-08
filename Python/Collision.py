#	Purpose this contains the functions associated for detecting collisions between Geometry and BoundingVolumes.
#	functions - tests for different types.

from Geometry import *
from linearAlgebra import *
from BoundingVolume import *

#####     Closets-point Computations     ##########################################################

def CPonPlaneToPoint(plane,point):
	t = plane.n.Dot(point) - plane.d
	return point - plane.n.Scale(t)

def CPonLineSegmentToPoint(LineSeg,point):
	ab = LineSeg.b - LineSeg.a
	t = (point - LineSeg.a).Dot(ab)
	if(t <= 0):
		return LineSeg.a
	denom = ab.Dot(ab)
	if(t >= denom):
		return LineSeg.b
	t /= denom
	return a + ab.Scale(t)

def CPonAABBToPoint(val,point):
	v1,v2,v3 = 0,0,0
	v1 = point.x
	if v1 < val.min.x: v1 = val.min.x
	if v1 > val.max.x: v1 = val.max.x

	v2 = point.y
	if v2 < val.min.y: v2 = val.min.y
	if v2 > val.max.y: v2 = val.max.y

	v3 = point.z
	if v2 < val.min.z: v2 = val.min.z
	if v2 > val.max.z: v2 = val.max.z

	return Point(v1,v2,v3)

def CPonOBBToPoint(val,point):
	d = point - val.loc

	q = b.loc
	v1 = d.Dot(b.u[0])
	if dist > b.e.x: dist = b.e.x
	elif dist < b.e.x: dist = -b.e.x
	q += b.u[0].scale(v1)

	v2 = d.Dot(b.u[1])
	if dist > b.e.y: dist = b.e.y
	elif dist < b.e.y: dist = -b.e.y
	q += b.u[1].scale(v2)

	v3 = d.Dot(b.u[2])
	if dist > b.e.z: dist = b.e.z
	elif dist < b.e.z: dist = -b.e.y
	q += b.u[2].scale(v3)
	return Point(v1,v2,v3)

def CPonTriangleToPoint(tri,point):
	pass

def CP2Lines(foo,bar):
	pass

def CPLineAndTriangle(line,tri):
	pass

def CP2Tris(foo,bar):
	pass

#####     Geometry Primative tests     ############################################################
def IntersectSpherePlane(sphere,plane):
	pass

def IntersectBoxPlane(box,plane):
	pass

def IntersectSphereAABB(sphere,aabb):
	pass

def IntersectSphereOBB(sphere,obb):
	pass

def IntersectSphereTriangle(sphere,tri):
	pass

def IntersectAABBTriangle(aabb,tri):
	pass

def IntersectTriTri(foo,bar):
	pass

#####     line/ray intersect tests     ############################################################
def IntersectSegPlane(seg,plane):
	pass

def IntersectSegSphere(ray,sphere):
	pass

def IntersectSegBox(ray,box):
	pass

def IntersectLineTriangle(line,tri):
	pass

def IntersectSegTriangle(seg,tri):
	if isinstance(seg,LineSegment):
		x,y = seg.a,seg.b
	else:
		x,y = seg.loc,seg.loc + seg.d.Scale(1000)
	a,b,c = tri.a,tri.b,tri.c

	xy = y - x
	pl = ComputePlane(a,b,c)

	if pl.n.Dot(xy):
		t = (pl.d - pl.n.Dot(x))/ pl.n.Dot(xy)
	else:
		t = (pl.d - pl.n.Dot(x))

	if not(t >= 0 and t <= 1): return None

	p = x + (xy.Scale(t))
	a -= p
	b -= p
	c -= p

	ab = a.Dot(b)
	ac = a.Dot(c)
	bc = b.Dot(c)
	cc = c.Dot(c)
	if (bc * ac - cc * ab < 0): return None
	bb = b.Dot(b)
	if (ab * bc - ac * bb < 0): return None
	return p

