#include <iostream>
#include "CNumber.h"

using namespace std;

int main() {

    //EXCERCISE 1
    cout << std::endl << "EXCERCISE 1" << std::endl;

    // Creating two objects of the CNumber class
    CNumber number1;
    CNumber number2;

    // Initializing objects with int values
    int value1 = 12345;
    int value2 = -6789;

    // Assigning values to CNumber objects
    number1 = value1;
    number2 = value2;

    // Displaying the values of CNumber objects
    std::cout << "Number 1: ";
    number1.vPrint();

    std::cout << "Number 2: ";
    number2.vPrint();

    //EXCERCISE 2
    cout << std::endl << "EXCERCISE 2" << std::endl;

    CNumber num_1, num_2;
    
    num_1 = 368;
    num_1.vPrint();

    num_2 = 1567;
    num_2.vPrint();

    num_1 = num_2;
    num_1.vPrint();

    //EXCERCISE 3
    /*
    After deleting the constructior, some functionality has been lost. It was used in both operator= functions to delete the arrays.
    */

    //EXCERCISE 5
    cout << std::endl << "EXCERCISE 5" << std::endl;

    string str_1;

    str_1 = num_1.sToStr();

    cout << str_1;

    //EXCERCISE 6
    cout << std::endl << "EXCERCISE 6" << std::endl;

    CNumber num33, num22, num11;
    string str33;

    num22 = 222;
    num11 = 2;
    str33 = num22.sToStr();
    cout << str33;

    cout << std::endl << "addition" << std::endl;

    num33 = num22 + num11;  
    str33 = num33.sToStr();
    cout << str33;

    cout << std::endl << "subtraction" << std::endl;

    num33 = num22 - num11;
    str33 = num33.sToStr();
    cout << str33;

    cout << std::endl << "multiplication" << std::endl;
    
    num33 = num11 * num22;
    str33 = num33.sToStr();
    cout << str33;

    /*
    cout << std::endl << "division" << std::endl;

    num33 = num11 / num22;
    str33 = num33.sToStr();
    cout << str33;
    */
    

}