#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

typedef struct vec2
{
	float x;
	float y;
}Vec2;

typedef struct vec3
{
	float x;
	float y;
	float z;
}Vec3;

typedef struct vec4
{
	float x;
	float y;
	float z;
	float w;
}Vec4;

class Vec2:
	def __init__(self,x,y):
		self.x = x * 1.0
		self.y = y * 1.0

Vec2* add(Vec2* self, Vec2* val)
{
	Vec2* temp;
	temp = (Vec2*)malloc(sizeof(Vec2));
	temp->x = self->x + val->x;
	temp->y = self->y + val->y;
	return temp;
}
Vec2* subtract(Vec2* self, Vec2* val)
{
	Vec2* temp;
	temp = (Vec2*)malloc(sizeof(Vec2));
	temp->x = self->x - val->x;
	temp->y = self->y - val->y;
	return temp;
}
int equal(Vec2* self, Vec2* val)
{
	if (self->x != val->x) return 0;
	if (self->y != val->y) return 0;
	return 1;
}
int notEqual(Vec2* self, Vec2* val)
{
	if (self->x == val->x && self->y == val->y) return 0;
	return 1;
}
int lessThan(Vec2* self, Vec2* val)
{
	if (self->x >= val->x) return 0;
	if (self->y >= val->y) return 0;
	return 1;
}
int lessOrEqual(Vec2* self, Vec2* val)
{
	if (self->x > val->x) return 0;
	if (self->y > val->y) return 0;
	return 1;
}
int greaterThan(Vec2* self, Vec2* val)
{
	if (self->x <= val->x) return 0;
	if (self->y <= val->y) return 0;
	return 1;
}
int greaterOrEqual(Vec2* self, Vec2* val)
{
	if (self->x < val->x) return 0;
	if (self->y < val->y) return 0;
	return 1;
}
char* __str__(Vec2* self)
{
	char* temp;
	temp = (char*)malloc(sizeof(char)*100);
	sprintf(temp,"X: %f Y: %f",self->x,self->y);
	realloc(temp,(size_t)strlen(temp)+1);
	return temp;
}
Vec2* Scale(Vec2* self, float val)
{
	Vec2* temp;
	temp = (Vec2*)malloc(sizeof(Vec2));
	temp->x = self->x * val;
	temp->y = self->y * val;
	return temp;	
}
float inline Dot(Vec2* self, Vec2* val)
{
	return (self->x * val->x + self->y * val->y);
}
float inline Magnitude(Vec2* self)
{
	return sqrt((self->x*self->x + self->y*self->y));
}
void Normalize(Vec2* self)
{
	float temp = Magnitude(self);
	self->x /= temp;
	self->y /= temp;
}
