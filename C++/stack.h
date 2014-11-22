#include <stdlib.h>
#include <stdio.h>

using namespace std;

template <class T>
class Stack
{
	public:
		Stack ();
		virtual ~Stack ();

	private:
		struct node
		{
			struct node* next;
			T val;
		};
		struct node Head;
};
