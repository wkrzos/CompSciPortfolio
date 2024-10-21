#include "ExpressionTreeInterface.h"
#include "Constants.h"
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
}