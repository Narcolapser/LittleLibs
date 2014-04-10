#	Purpose this contains the functions associated for detecting collisions between Geometry and BoundingVolumes.
#	functions - tests for different types.

from Geometry import *
from linearAlgebra import *
from BoundingVolume import *
import math

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
	ab = tri.b - tri.a
	ac = tri.c - tri.a
	ap = point - tri.a

	d1 = ab.Dot(ap)
	d2 = ac.Dot(ap)
	if d1 <=0 and d2 <= 0: return tri.a

	bp = p - b
	d3 = ab.Dot(bp)
	d4 = ac.Dot(bp)
	if d3 >= 0 and d4 <= d3: return tri.b

	vc = d1*d4 - d3*d2
	if vc <= 0 and d1 >=0 and d3 <= 0:
		v = d1 / (d1-d3)
		return tri.a + ab.Scale(v)

	cp = point - tri.c
	d5 = ab.Dot(cp)
	d6 = ac.Dot(cp)
	if d6 >= 0 and d5 <= d6: return tri.c

	vb = d5*d2 - d1*d6
	if vb <= 0 and d2 >= 0 and d6 <= 0:
		w = d2 / (d2-d6)
		return tri.a + ac.Scale(w)

	va = d3*d6 - d5*d4
	if va <= 0 and (d4-d3) >=0 and (d5 - d6) >= 0:
		w = (d4 -d3) / ((d4 -d3) + (d5 -d6))
		return tri.b + (c-b).Scale(w)

	denom = 1.0 / (va+vb+vc)
	v = vb * denom
	w = vc * denom
	return a + ab.Scale(v) + ac.Scale(w)

#def CP2Lines(foo,bar):
#	pass

#def CPLineAndTriangle(line,tri):
#	pass

#def CP2Tris(foo,bar):
#	pass

#####     Geometry Primative tests     ############################################################
def IntersectSpherePlane(sphere,plane):
	dist = sphere.loc.Dot(plane.n) - plane.d
	return abs(dist) <= sphere.r

def SphereBehindPlane(sphere, plane):
	dist = sphere.c.Dot(plane.n) - plane.d
	return dist < -sphere.r

def IntersectBoxPlane(box,plane):
	r = box.e.x*abs(plane.n.Dot(b.u[0])) + box.e.y*abs(plane.n.Dot(b.u[1])) + box.e.z*abs(plane.n.Dot(b.u[2]))

	s = plane.n.Dot(box.loc) - plane.d

	return abs(s) <= r

def IntersectSphereAABB(sphere,aabb):
	p = CPonAABBToPoint(aabb,sphere.loc)
	v = p - sphere.loc
	return v.Magnitude() <= sphere.r**2

def IntersectSphereOBB(sphere,obb):
	p = CPonOBBToPoint(obb,sphere.loc)
	v = p - sphere.loc
	return v.Magnitude() <= sphere.r**2

def IntersectSphereTriangle(sphere,tri):
	p = CPonTriangleToPoint(tri,sphere.loc)
	v = p - sphere.loc
	return v.Magnitude() <= sphere.r**2

#def IntersectAABBTriangle(aabb,tri):
#	pass

#def IntersectTriTri(foo,bar):
#	pass

#####     line/ray intersect tests     ############################################################
def IntersectSegPlane(seg,plane):
	ab = seg.b - seg.a
	t = (plane.d - plane.n.Dot(seg.a))/ plane.n.Dot(ab)

	if( t >= 0 and t <= 1):
		q = seg.a + ab.Scale(t)
		return q

	return None

def IntersectSegSphere(ray,sphere):
	m = ray.loc - sphere.loc

	b = m.Dot(ray.d)
	c = m.Magnitude() - sphere.r**2

	if c> 0 and b > 0: return None
	discr = b**2 - c

	if discr < 0: return None

	t = -b - math.sqrt(discr)

	if (t < 0): t = 0
	q = ray.loc + ray.d.Scale(t)
	return q

def IntersectSegBox(ray,box):
	tmin = 0
	tmax = float("inf")

	if(abs(ray.d.x) < EPSILON):
		if ray.loc.x < box.min.x or ray.loc.x > box.max.x: return None
	else:
		ood = 1/ray.d.x
		t1 = (box.min.x-ray.loc.x) - ood
		t2 = (box.max.x-ray.loc.x) - ood

		if(t1 > t2):
			temp = t1
			t1 = t2
			t2 = temp

		tmin = max(tmin,t1)
		tmax = min(tmax,t2)

		if(tmin>tmax): return 0
	
	if(abs(ray.d.y) < EPSILON):
		if ray.loc.y < box.min.y or ray.loc.y > box.max.y: return None
	else:
		ood = 1/ray.d.y
		t1 = (box.min.y-ray.loc.y) - ood
		t2 = (box.max.y-ray.loc.y) - ood

		if(t1 > t2):
			temp = t1
			t1 = t2
			t2 = temp

		tmin = max(tmin,t1)
		tmax = min(tmax,t2)

		if(tmin>tmax): return 0

	if(abs(ray.d.z) < EPSILON):
		if ray.loc.z < box.min.z or ray.loc.z > box.max.z: return None
	else:
		ood = 1/ray.d.z
		t1 = (box.min.z-ray.loc.z) - ood
		t2 = (box.max.z-ray.loc.z) - ood

		if(t1 > t2):
			temp = t1
			t1 = t2
			t2 = temp

		tmin = max(tmin,t1)
		tmax = min(tmax,t2)

		if(tmin>tmax): return 0

	q = ray.loc + ray.d.Scale(tmin)
	return 1	

#def IntersectLineTriangle(line,tri):
#	pass

def IntersectSegTriangle(seg,tri):
	if isinstance(seg,LineSegment):
		x,y = seg.a,seg.b
	else:
		x,y = seg.loc,seg.loc + seg.d.Scale(seg.clip)
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

