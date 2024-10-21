/* EXPRESSION TREE
#include "ExpressionTreeInterface.h"
#include "Constants.h"
#include "modification/MySmartPointer.h"
#include <iostream>
#include <string>


int main() {
    std::cout << WELCOME_MESSAGE << std::endl;

    std::cout << SELECT_DATA_TYPE_MESSAGE;
    int choice;
    std::cin >> choice;

    switch (choice) {
    case 1:
        ExpressionTreeInterface<int>::run();
        break;
    case 2:
        ExpressionTreeInterface<double>::run();
        break;
    case 3:
        ExpressionTreeInterface<std::string>::run();
        break;
    default:
        std::cerr << ERROR_CHOICE_MESSAGE << std::endl;
        return 1;
    }

    return 0;
}*/

#include <iostream>
#include "modification/MySmartPointer.h"

class Test {
public:
    Test() { std::cout << "Test Created c:\n"; }
    ~Test() { std::cout << "Test Destroyed :c\n"; }
    void greet() { std::cout << "Hello, I'm a Test object\n"; }
};

int main() {
    // Creating a new Test object with a smart pointer
    MySmartPointer<Test> ptr1(new Test());
    std::cout << "Counter ptr1 after ptr1 creation: " << ptr1.getCounter() << std::endl;

    // Using the -> operator to call a method
    ptr1->greet();

    // Creating another smart pointer pointing to the same object
    MySmartPointer<Test> ptr2 = ptr1;
    std::cout << "Counter ptr1 after ptr2 creation: " << ptr1.getCounter() << std::endl;
    std::cout << "Counter ptr2 after ptr2 creation: " << ptr2.getCounter() << std::endl;

    // Creating a third smart pointer using the duplicate method
    MySmartPointer<Test> ptr3 = ptr1.duplicate();
    std::cout << "Counter ptr1 after ptr3 creation: " << ptr1.getCounter() << std::endl;
    std::cout << "Counter ptr3 after ptr3 creation: " << ptr3.getCounter() << std::endl;

    // The Test object will be destroyed when the last smart pointer goes out of scope
    return 0;
}
