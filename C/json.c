#include "json.h"

struct value
{
	Datum datum;
	value_t type;
};

struct object
{
	Pair* head;
};

struct pair
{
	String name;
	Value value;
	Pair* next;
};

struct array
{
	void* values;
	unsigned int size;	//the amount of the array list in use
	unsigned int length;	//the amount of the array list can hold
};

struct number
{
	int sign;
	int numerator;
	int denominator;
};

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


int main(int argc, char* argv[]){return 0;}

/*.S.D.G.*/
