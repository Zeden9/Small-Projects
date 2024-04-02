#include <iostream>

class Element_of_stack
{
	public:
		Element_of_stack* ptr;
		int value;

		Element_of_stack(int val)
		{
			value = val;
			ptr = nullptr;
		}

};

class Stack
{
	public:
		Element_of_stack* top;
		Stack(int val)
		{
			top = new Element_of_stack(val);
		}

		//void push(int val)
		//{
		//	Element_of_stack* elem = new Element_of_stack(val);
		//	elem->ptr = top;
		//	top = elem;
		//}

		//int pop()
		//{
		//	Element_of_stack* elem = top;
		//	int result = top->value;
		//	top = top->ptr;
		//	delete elem;
		//	return result;
		//}

		void operator++(int)
		{
			int val;
			std::cin >> val;
			Element_of_stack* elem = new Element_of_stack(val);
			elem->ptr = top;
			top = elem;
			
		}
		void operator--(int)
		{
			if (top == nullptr)
			{
				std::cout << "Stack is empty";
			}
			else
			{
				Element_of_stack* elem = top;
				top = top->ptr;
				delete elem;
			}
		}
};


std::ostream& operator<<(std::ostream& os, const Stack& stack)
		{
			Element_of_stack* elem = stack.top;
			while (elem != nullptr)
			{
				{
					os << elem->value;
					if (elem->ptr != nullptr) os << " ";
				}
				elem = elem->ptr;
			}
			os << std::endl;
			return os;
		}

int main()
{
	int a;
	Stack s1(5);
	s1++;
	s1++;
	s1--;
	std::cout << s1;
	s1--;
	std::cout << s1;
	s1--;
	s1--;

	return 0;

}