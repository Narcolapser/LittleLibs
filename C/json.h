#ifndef JSON_H
#define JSON_H
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

enum value_t {STRING,NUMBER,OBJECT,ARRAY,TRUE,FALSE,NONE,COUNT};

typedef struct object Object;
typedef struct pair Pair;
typedef struct array Array;
typedef struct number Number;
typedef struct value Value;
typedef char* String;
typedef union datum
{
	String string;
	Number* number;
	Object* object;
	Array* array;
	int boolean;
	void* null;
}Datum;

//methods concerned with the object
Value valueOf(Object* self, String member);

//methods concerned with pair
Value get(Pair* self);
void insert(Pair* self, Pair* val);


//methods conderned with array
int append(Array* self);
void* valueAt(Array* self, int loc);


//methods concerned with number
float asFloat(Pair* self);
double asDouble(Pair* self);


//methods concerned with string

/*.S.D.G.*/
#endif//JSON_H
