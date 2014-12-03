#include <string.h>
#include <stdlib.h>

typedef struct stack
{
	int size;
	int top;
	int *stackT;
}Stack;

void push(Stack &val,int pushed)
{
	if (val.size == val.top)
	{
		int nsize = val.size * 1.5;
		realloc(val.stackT,nsize);
		val.size = nsize;
	}
	val.stackT[val.top] = pushed;
	val.top += 1;
}

int peek(Stack &val)
{
	if (val.top >= 0)
		return val.stackT[val.top];
	else
		return NULL;
}

int pop(Stack &val)
{
	if (val.top >=0)
		return val.stackT[val.top--];
	else
		return NULL;
}
