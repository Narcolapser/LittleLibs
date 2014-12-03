#include <stdio.h>
#include <stdlib.h>

struct node
{
	struct node *next;
	void* val;
};

typedef struct stack
{
	struct node *head;
}Stack;



void push(Stack *val,void* pushed)
{
	struct node *temp = malloc(sizeof(struct node));
	temp->val = pushed;
	temp->next = val->head;
	val->head = temp;
}

void* peek(Stack *val)
{
	if (val->head != NULL)
		return val->head->val;
	else
		return NULL;
}

void* pop(Stack *val)
{
	if (val->head != NULL)
	{
		struct node *temp = val->head;
		void *ret = temp->val;
		val->head = val->head->next;
		free(temp);
		return ret;
	}
	else
		return NULL;
}

int main()
{
	Stack *t = (Stack*)malloc(sizeof(Stack));
	int ex[5] = {1,2,3,4,5};
	push(t,(void*)&(ex[0]));
	push(t,(void*)&(ex[1]));
	push(t,(void*)&(ex[2]));
	push(t,(void*)&(ex[3]));
	push(t,(void*)&(ex[4]));
	
	printf("pop 1: %i\n",*(int*)(pop(t)));
	printf("pop 2: %i\n",*(int*)(pop(t)));
	printf("pop 3: %i\n",*(int*)(pop(t)));
	printf("pop 4: %i\n",*(int*)(pop(t)));
	printf("pop 5: %i\n",*(int*)(pop(t)));
	
}
