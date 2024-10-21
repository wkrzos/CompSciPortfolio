#ifndef PARSER_H
#define PARSER_H

#include "PrefixExpressionTree.h"
#include "PrefixExpressionParser.h"
#include "Constants.h" // Include Constants.h for error messages

template<typename T>
class PrefixExpressionParser
{
public:
    void parseFormula(PrefixExpressionTree<T>& peTree, std::string formula);

private:
    int parseNodes(Node* currentNode, std::string formula, int start, bool* wasError, PrefixExpressionTree<T>& tree);
    static const std::map<std::string, int> funMap;
    static std::map<std::string, int> createFunctionMap();

    bool isCorrectConstant(std::string value);
    bool isValidVariable(std::string value);
};

template<typename T>
void PrefixExpressionParser<T>::parseFormula(PrefixExpressionTree<T>& outputTree, std::string formula)
{
    // Clear the existing tree if necessary
    if (outputTree.getRoot() != nullptr) {
        delete outputTree.getRoot();
        outputTree.setRoot(nullptr);
    }

    // Create a new root node
    Node* root = new Node();
    outputTree.setRoot(root);

    // Reset the state for a new parsing session
    bool wasError = false;
    outputTree.clearVariables(); // Resets variables and v_variables

    // Parse the nodes starting from the root
    int start = parseNodes(root, formula, 0, &wasError, outputTree);

    // Check for leftover unprocessed formula
    if (formula.length() > start)
    {
        std::cout << ERROR_WRONG_NUM_ARGS << std::endl;
        wasError = true;
    }

    // Provide feedback if there was an error during parsing
    if (wasError)
    {
        std::cout << FORMULA_CORRECTED << std::endl;
    }
}

template<typename T>
int PrefixExpressionParser<T>::parseNodes(Node* currentNode, std::string formula, int start, bool* wasError, PrefixExpressionTree<T>& tree)
{
    start = formula.find_first_not_of(' ', start);
    if (start == std::string::npos) {
        return formula.length();
    }

    // Find the end of the current token
    int end = formula.find(' ', start);
    std::string value = formula.substr(start, end - start);

    // Update the current node with the value
    currentNode->setKey(value);

    auto numberOfArgsIterator = funMap.find(value);
    if (numberOfArgsIterator != funMap.end())
    {
        // Handle operation node
        currentNode->setNodesCounter(numberOfArgsIterator->second);
        currentNode->setNodeType(OPERATION);

        for (int i = 0; i < currentNode->getNodesCounter(); i++)
        {
            if (end == std::string::npos)
            {
                std::cout << ERROR_NOT_ENOUGH_ARGS << std::endl;
                currentNode->getNode(i)->setNodesCounter(0);
                currentNode->getNode(i)->setNodeType(CONSTANT);
                currentNode->getNode(i)->setKey("1");
                *wasError = true;
                break;
            }
            else
            {
                start = parseNodes(currentNode->getNode(i), formula, end, wasError, tree);
                end = formula.find(' ', start);
            }
        }
    }
    else if (isCorrectConstant(value))
    {
        currentNode->setNodeType(CONSTANT);
        currentNode->setNodesCounter(0);

    }
    else if (isValidVariable(value))
    {       
        currentNode->setNodeType(VARIABLE);
        currentNode->setNodesCounter(0);
    }
    else
    {
        std::cout << ERROR_UNKNOWN_OPERATION << std::endl;
        *wasError = true;
    }

    return end == std::string::npos ? formula.length() : end;
}

template <typename T>
bool PrefixExpressionParser<T>::isValidVariable(std::string value)
{
  
    bool isValid = false;

    if (value.empty()) { return isValid; }

    // Check each character in the string
    for (char ch : value)
    {
        if (isalpha(ch))
        {
            isValid = true;
        }
        else if (!isdigit(ch))
        {
            std::cout << ERROR_INVALID_CHARACTER << std::endl;
            return false; // Exit early if an invalid character is found
        }
    }

    // Return true only if at least one letter is present
    return isValid;
}

template <typename T>
std::map<std::string, int> PrefixExpressionParser<T>::createFunctionMap()
{
    return {{"+", 2}, {"-", 2}, {"*", 2}, {"/", 2}, {"Sin", 1}, {"Cos", 1}};
}

template<typename T>
const std::map<std::string, int> PrefixExpressionParser<T>::funMap = createFunctionMap();

template <>
bool PrefixExpressionParser<int>::isCorrectConstant(std::string value)
{
    return value.find_first_not_of("1234567890") == std::string::npos;
}

template <>
bool PrefixExpressionParser<double>::isCorrectConstant(std::string value)
{
    double tempDouble;
    std::istringstream stream(value);
    // Check if the string can be fully converted to a double
    return (stream >> tempDouble >> std::ws).eof();
}

template <>
bool PrefixExpressionParser<std::string>::isCorrectConstant(std::string value)
{
    // The only option is "x", so must be at least 3 char long
    if (value.length() < 3) { return false; }

    // Check if the string starts and ends with double quotes
    return (value.front() == '"' && value.back() == '"');

    return true;
}

#endif