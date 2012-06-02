#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>
#include <float.h>

#define EPSILON 0.19209E-07

typedef float v4sf __attribute__ ((vector_size (16)));
typedef v4sf Point;
typedef v4sf matrix4x4[4];


float Dot4(Point lhs, Point rhs)
{
	Point temp = lhs * rhs;
	return temp[0] + temp[1] + temp[2] + temp[3];
}

float Dot(Point lhs, Point rhs)
{
	Point temp = lhs * rhs;
	return temp[0] + temp[1] + temp[2];
}

Point Cross(Point u, Point v)
{
	Point temp = {u[1]*v[2] - u[2]*v[1],u[2]*v[0] - u[0]*v[2],u[0]*v[1] - u[1]*v[0],0.0};
	return temp;
}

float STP(Point u, Point v, Point w)
{
	return Dot(Cross(u,v),w);
}

float Det3x3(matrix4x4 val)
{
	return STP(val[0],val[1],val[2]);
}

Point Mul(Point foo, float bar)
{
	Point temp = {foo[0]*bar,foo[1]*bar,foo[2]*bar,foo[3]*bar};
	return temp;
}

int GreaterThan(Point lhs, Point rhs)
{
	return lhs[0] > rhs[0] & lhs[1] > rhs[1] & lhs[2] > rhs[2];
}

int GreaterThan4(Point lhs, Point rhs)
{
	return lhs[0] > rhs[0] & lhs[1] > rhs[1] & lhs[2] > rhs[2] & lhs[3] > rhs[3];
}

int LessThan(Point lhs, Point rhs)
{
	return lhs[0] < rhs[0] & lhs[1] < rhs[1] & lhs[2] < rhs[2];
}

int LessThan4(Point lhs, Point rhs)
{
	return lhs[0] < rhs[0] & lhs[1] < rhs[1] & lhs[2] < rhs[2] & lhs[3] < rhs[3];
}

float Magnitudep2(Point val)
{
	return val[0]*val[0] + val[1]*val[1] + val[2]*val[2];
}

float Magnitude(Point val)
{
	return sqrtf(Magnitudep2(val));
}

Point Normalize(Point val)
{
	float mag = Magnitude(val);
	Point p = {val[0]/mag,val[1]/mag,val[2]/mag,1};
}	

void Barycentric(Point a, Point b, Point c, Point p, float *u, float *v, float *w)
{
	Point p0 = b - a, p1 = c - a, p2 = p - a;
	float d00 = Dot(p0,p0);
	float d01 = Dot(p0,p1);
	float d11 = Dot(p1,p1);
	float d20 = Dot(p2,p0);
	float d21 = Dot(p2,p1);
	float denom = d00 * d11 - d01 * d01;
	float t1 = (d11 * d20 - d01 * d21) / denom;
	float t2 = (d00 * d21 - d01 * d20) / denom;
	(*v) = t1;
	(*w) = t2;
	(*u) = 1.0f - t1 - t2;
}

typedef struct plane
{
	Point n;// plane Normal. Points x on the plane satisfy Dot(nx) = d
	float d;// d = dot(n,p) for a given point in p on the plane.
} Plane;

Plane ComputePlane(Point a, Point b, Point c)
{
	Plane p;
	p.n = Normalize(Cross(b-a,c-a));
	p.d = Dot(p.n,a);
	return p;
}

typedef struct aabb
{
	Point min;
	Point max;
} AABB;

void ExtremePointsAlongDirection(Point dir, Point pt[], int n, int *imin, int *imax)
{
	float minproj = FLT_MAX, maxproj = -FLT_MAX;
	int i = 0;
	for(i = 0; i < n; i++)
	{
		float proj = Dot(pt[i], dir);
		// keep track of least distant point along direction vector
		if (proj < minproj) 
		{
			minproj = proj;
			(*imin) = i;
		}
		if (proj > maxproj)
		{
			maxproj = proj;
			(*imax) = i;
		}
	}
}

typedef struct sphere
{
	Point c;
	float r;
} Sphere;

/* JUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUMP!
WOOOO
WOOOOO
wooooo
woowowowowooo
wooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
*/

int TestAABBAABB(AABB a, AABB b)
{
	//exit with no intersection if separated along an axis
	if(a.max[0] < b.min[0] || a.min[0] > b.max[0]) return 0;
	if(a.max[1] < b.min[1] || a.min[1] > b.max[1]) return 0;
	if(a.max[2] < b.min[2] || a.min[2] > b.max[2]) return 0;
	//overlapping on all axes means AABBs are intersecting
	return 1;
}

int IntersectSegmentPlane(Point a, Point b, Plane p, float *t, Point *q)
{
	Point ab = b -a;
	float val = (p.d - Dot(p.n,a))/Dot(p.n,ab);
	if (val >= 0.0f && val <= 1.0f)
	{
		(*q) = a + Mul(ab,val);
		(*t) = val;
		return 1;
	}
	return 0;
}

int PointInTriangle(Point p, Point a, Point b, Point c)
{
	a -= p; b -= p; c -= p;
	float ab = Dot(a,b);
	float ac = Dot(a,c);
	float bc = Dot(b,c);
	float cc = Dot(c,c);
	
	if(bc*ac - cc*ab < 0.0f) return 0;
	float bb = Dot(b,b);
	if(ab*bc - ac*bb < 0.0f) return 0;
	return 1;
}

int IntersectRayAABB(Point p, Point d, AABB a, float *tmin, Point *q)
{
	(*tmin) = 0.0f;
	float tmax = FLT_MAX;

	//for all three slabs
	int i;
	for (i = 0; i < 3; ++i)
	{
		if (Abs(d[i]) < EPSILON)
			if (p[i] < a.min[i] || p[i] > a.max[i]) return 0;
		else
		{
			float ood = 1.0f / d[i];
			float t1 = (a.min[i] - p[i]) * ood;
			float t2 = (a.max[i] - p[i]) * ood;
			if(t1 > t2) Swap(t1,t2);
			(*tmin) = Max(tmin, t1);
			tmax = Max(tmax, t2);

			if((*tmin) > tmax) return 0;
		}
	}

	(*q) = p + Mul(d,(*tmin));
	return 1;
}

int PointInAABB(Point p, AABB a)
{
	return GreaterThan(p,a.min) & LessThan(p,a.max);
}

int TriangleInAABB(Point a, Point b, Point c, AABB val)
{
	return PointInAABB(a,val) & PointInAABB(b,val) & PointInAABB(c,val);
}


