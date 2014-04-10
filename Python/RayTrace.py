###################################################################################################
# This is a simple ray trace program. The point of it is to gain a better understanding of how    #
# ray-tracing works. I'm programming it first in python, and then I'll move later to c with simd  #
# to speed things up. I'm using this as an exercise in 3D physical systems. I want to gain an     #
# understanding of systems like colision dtection, bounding boxes, octrees, etc, in a system that #
# is much less complex first before I move on to implementing them as part of a physics           #
# simulation that will need to be running in openCL on the GPU.                                   #
# I plan on doing this in 3 phases. phase 1 is simple and straight forward. ray casts out till it #
# hits geometry, calculate from there to the lights to get the appropriate coloring. Phase 2 I    #
# will fix it up for reflecting n times, where n is a value specified when the job is dispatched. #
# Phase 3 i flip the system on its head. each light sends out hundreds of rays and paint the      #
# world, then rays our sent from where ever the collide to the camera and the pixels are added    #
# till a picture is created. 									  #
###################################################################################################

import math
import random
import time
from xml.dom import minidom
from PIL import Image, ImageDraw
from linearAlgebra import *
from Geometry import *
from Collision import *
from BoundingVolume import *

xRes = 640
yRes = 480

PI180 = 0.0174532925

gcams = []
gmesh = []
gmats = []

class Outs:
	def __init__(self,name,sizeX,sizeY,ext,counting):
		self.img = Image.new("RGB",(sizeX,sizeY))
		self.draw = ImageDraw.Draw(self.img)
		self.name = name
		self.ext = ext
		if counting:
			self.count = 0
		else:
			self.count = -1

	def drawPixelRGB(self,x,y,r,g,b):
		color = "#"
		mapping = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
		color += mapping[r/16]
		color += mapping[r%16]
		color += mapping[g/16]
		color += mapping[g%16]
		color += mapping[b/16]
		color += mapping[b%16]
		self.draw.point((x,y),color)

	def drawPixelColor(self,x,y,color):
		self.drawPixelRGB(x,y,color.x,color.y,color.z)

	def drawPixelHash(self,x,y,val):
		self.draw.point((x,y),val)

	def save(self):
		if self.count != -1:
			self.img.save(self.name + str(self.count) + "." + self.ext,self.ext)
			self.count += 1
		else:
			self.img.save(self.name + "." + self.ext,self.ext)

class Camera:
	def __init__(self,loc,direction,clipNear,clipFar,FOV,sizeX,sizeY,name):
		self.loc = loc
		self.d = direction
		self.cn = clipNear
		self.cf = clipFar
		self.fov = FOV
		self.x = sizeX
		self.y = sizeY
		self.aspect = sizeY/(sizeX*1.0)
		self.name = name
		self.outs = Outs(name,sizeX,sizeY,"BMP",True)
		self.xspan = math.tan((FOV/2*PI180))*clipNear*2
		self.yspan = self.xspan*self.aspect
		self.xpitch = self.xspan/sizeX
		self.ypitch = self.yspan/sizeY

	def draw(self,world):
		tstart = time.time()
		xguide = Point(0,1,0).Cross(self.d)
		yguide = self.d.Cross(xguide)
		xguide.Normalize()
		yguide.Normalize()
		#print "xguide:", str(xguide)
		#print "yguide:", str(yguide)
		rayplane = self.loc + self.d.Scale(self.cn)
		start = rayplane - xguide.Scale(self.xspan/2)
		start = start - yguide.Scale(self.yspan/2)
		pstart = time.time()
		for x in range(self.x):
			tempx = (self.xpitch * x) + self.xpitch/2
			print (x*100.0)/self.x,"percent complete, row took:",time.time()-pstart
			pstart = time.time()
			for y in range(self.y):
				tempy = (self.ypitch * y) + self.ypitch/2
				castpoint = start + xguide.Scale(tempx) + yguide.Scale(tempy)
#				print "cast point is:", str(castpoint)
#				print castpoint.x,',',castpoint.y
				castdir = castpoint - self.loc
				castdir.Normalize()
				castRay = Ray(self.loc,castdir)
				intersects = []
				for tri in world:
					col = IntersectSegTriangle(castRay,tri)
					if col:
						intersects.append(col)
				if len(intersects) == 0:
					self.outs.drawPixelRGB(x,y,0,0,0)
				else:
					self.outs.drawPixelRGB(x,y,255,255,255)
		self.outs.save()
		print "job took:", time.time()-tstart

class Color:
	def __init__(self,r,g,b,a):
		self.r = r
		self.g = g
		self.b = b
		self.a = a

class Mesh:
	def __init__(self):
		self.verts = []
		self.faces = []

	def addVert(self,vert):
		self.verts.append(vert)

	def addFace(self,a,b,c):
		self.faces.append(Triangle(self.verts[a],self.verts[b],self.verts[c]))

def scalarTriple(a,b,c):
	return a.cross(b).dot(c)
		
def loadObj(path,filename):
	f = open(path+filename,'r')
	points = []
	faces = []
	for line in f.readlines():
		if line[0] == 'v':
			l = line.split()
			points.append(Point(float(l[1]),float(l[2])*(-1),float(l[3])))
		elif line[0] == 'f':
			l = line.split()
			faces.append(Triangle(points[int(l[1])-1],points[int(l[2])-1],points[int(l[3])-1]))
			if len(l) == 5:
				faces.append(Triangle(
					points[int(l[1])-1],points[int(l[4])-1],points[int(l[3])-1]))
	return faces
A = Point( 00, 00,-1000.0)
B = Point( 00, 00, 1000.0)
R = LineSegment(A,B)
P1= Point( 0,  1,  0)
P2= Point( 1, -1, -1)
P3= Point(-1, -1,  1)
P = Triangle(P1,P2,P3)

#i = IntersectLineTriangle(R,P)
#print "i:", i

c = Camera(Point(0,0,2),Point(0,0,-1),.1,10000,90,xRes,yRes,"dotanuki out")
#c.draw(loadObj('','level.obj'))
c.draw([P])




#s = R in P
#if s:
#	print "collided at:", s.x,s.y,s.z
#else:
#	print "No collision"
	
#o = Outs("test",x,y,"BMP",True)
#drawWorld(o,drawRandom)
#o.save()
#print "done"

#.S.D.G.#
