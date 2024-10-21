#ifndef PREFIXEXPRESSIONTREE_H
#define PREFIXEXPRESSIONTREE_H

#include "Node.h"
#include <map>
#include <cmath>
#include <string>
#include <vector>
#include <iostream>
#include <sstream>
#include <numeric>
#include "Constants.h" // Include Constants.h for error messages and type descriptions

template <typename T>
class PrefixExpressionTree
{
public:
    
    PrefixExpressionTree();
    PrefixExpressionTree(const PrefixExpressionTree& otherTree);
    ~PrefixExpressionTree();

    PrefixExpressionTree<T>& operator=(const PrefixExpressionTree<T>& otherTree);
    PrefixExpressionTree<T> operator+(const PrefixExpressionTree<T>& otherTree) const;

    std::string toString() const;
    void printNodes() const;

    T evaluateWithVariables(std::string variables);

    // Getter Methods
    std::string getVariables() const;

    // Argument Handling
    void clearVariables();
    static T getDefaultNodeKey();
    void setVariable(std::string variable, T key);

    void setRoot(Node* newRoot); // New method to set the root
    Node* getRoot(); // New method to access the root

private:
    Node* root;

    std::map<std::string, T> variables;
    std::vector<std::string> v_variables;

    // Helper Methods
    bool isCorrectConstant(std::string string);
    static T stringToConstant(std::string string);
    T evaluateWithVariables(Node* currentNode);
    void deleteVariable(std::string variable);
    void setVariableWithIndex(int index, T Key);
    static int stringToNumber(std::string string);
    std::string* splitStringIntoArray(const std::string& inputString, int* arraySize);
};

template <typename T>
PrefixExpressionTree<T>::PrefixExpressionTree() : root(NULL), variables(), v_variables()
{
}

template <typename T>
PrefixExpressionTree<T>::~PrefixExpressionTree()
{
    delete root;
}

template <typename T>
PrefixExpressionTree<T>::PrefixExpressionTree(const PrefixExpressionTree& other) : root(NULL)
{
    if (other.root != NULL)
    {
        root = new Node(*other.root);
    }

    variables = other.variables;
    v_variables = other.v_variables;
}

template <typename T>
T PrefixExpressionTree<T>::stringToConstant(std::string str)
{
    T value = T(); // Initialize to default value of T

    // Convert string to value of type T
    std::istringstream(str) >> value;
    return value;
}

template <>
std::string PrefixExpressionTree<std::string>::stringToConstant(std::string str)
{
    // Remove the first and last characters (assuming they are quotes)
    if (str.length() > 2)
    {
        return str.substr(1, str.length() - 2);
    }
    return ""; // Return an empty string if input is too short
}

template <>
int PrefixExpressionTree<int>::getDefaultNodeKey()
{
    return -401;
}

template <>
double PrefixExpressionTree<double>::getDefaultNodeKey()
{
    return -401;
}

template <>
std::string PrefixExpressionTree<std::string>::getDefaultNodeKey()
{
    return "-401";
}

template <typename T>
PrefixExpressionTree<T> PrefixExpressionTree<T>::operator+(const PrefixExpressionTree<T>& newValue) const
{
    PrefixExpressionTree result = *this;

    if (result.root == NULL)
    {
        result.root = new Node(*newValue.root);
    }

    Node* currentNode = result.root;
    Node* parent = NULL;

    while (currentNode->getNodesCounter() > 0)
    {
        parent = currentNode;
        currentNode = currentNode->getNode(currentNode->getNodesCounter() - 1);
    }

    Node* newNode = new Node(*newValue.root);

    if (currentNode->getNodeType() == CONSTANT)
    {
        result.deleteVariable(currentNode->getKey());
    }

    if (parent != NULL)
    {
        parent->setNode(parent->getNodesCounter() - 1, *newNode);
    }
    else
    {
        result.root = newNode;
    }

    for (int i = 0; i < newValue.v_variables.size(); i++)
    {
        result.setVariable(newValue.v_variables[i], getDefaultNodeKey());
    }

    // Merge variables and v_variables
    for (const auto& arg : newValue.variables)
    {
        // How to handle conflicts here?
        result.variables[arg.first] = arg.second;
    }

    // Update v_variables
    for (const auto& arg : newValue.v_variables)
    {
        if (std::find(result.v_variables.begin(), result.v_variables.end(), arg) == result.v_variables.end())
        {
            result.v_variables.push_back(arg);
        }
    }

    return result;
}

template <typename T>
PrefixExpressionTree<T>& PrefixExpressionTree<T>::operator=(const PrefixExpressionTree<T>& newValue)
{
    if (this == &newValue)
    {
        return *this;
    }

    if (root != NULL)
    {
        delete root;
    }

    if (newValue.root != NULL)
    {
        root = new Node(*newValue.root);
    }

    for (int i = 0; i < newValue.v_variables.size(); i++)
    {
        setVariable(newValue.v_variables[i], getDefaultNodeKey());
    }

    return *this;
}

template <typename T>
T PrefixExpressionTree<T>::evaluateWithVariables(std::string args)
{
    int size = 0;

    std::string* argsArray = splitStringIntoArray(args, &size);

    if (size != variables.size())
    {
        std::cout << ERROR_WRONG_NUM_ARGS << std::endl;

        delete[] argsArray;

        return getDefaultNodeKey();
    }

    for (int i = 0; i < size; i++)
    {
        if (isCorrectConstant(argsArray[i]))
        {
            setVariableWithIndex(i, stringToConstant(argsArray[i]));
        }
        else
        {
            std::cout << ERROR_INVALID_ARG << std::endl;

            delete[] argsArray;

            return getDefaultNodeKey();
        }
    }

    if (root == NULL)
    {
        std::cout << ERROR_NO_FORMULA << std::endl;

        delete[] argsArray;

        return getDefaultNodeKey();
    }

    T result = evaluateWithVariables(root);

    delete[] argsArray;

    return result;
}

template <typename T>
std::string PrefixExpressionTree<T>::getVariables() const
{
    if (v_variables.empty())
    {
        return "";
    }

    std::string result;
    result.reserve(std::accumulate(v_variables.begin(), v_variables.end(), 0,
        [](size_t sum, const std::string& str) { return sum + str.length() + 1; }));

    for (const auto& arg : v_variables)
    {
        result += arg + " ";
    }

    result.pop_back(); // Remove the last space
    return result;
}

template <typename T>
void PrefixExpressionTree<T>::printNodes() const
{
    if (root != NULL)
    {
        for (int i = 0; i < root->getNodesCounter(); i++)
        {
            std::cout << root->getNode(i)->toString() << std::endl;
        }
    }
}

template <typename T>
T PrefixExpressionTree<T>::evaluateWithVariables(Node* currentNode)
{
    if (currentNode->getNodeType() == CONSTANT)
    {
        return stringToConstant(currentNode->getKey());
    }
    else if (currentNode->getNodeType() == OPERATION)
    {
        if (currentNode->getKey() == "+")
        {
            return evaluateWithVariables(currentNode->getNode(0)) + evaluateWithVariables(currentNode->getNode(1));
        }
        else if (currentNode->getKey() == "-")
        {
            return evaluateWithVariables(currentNode->getNode(0)) - evaluateWithVariables(currentNode->getNode(1));
        }
        else if (currentNode->getKey() == "*")
        {
            return evaluateWithVariables(currentNode->getNode(0)) * evaluateWithVariables(currentNode->getNode(1));
        }
        else if (currentNode->getKey() == "/")
        {
            T secondNodeValue = evaluateWithVariables(currentNode->getNode(1));

            if (secondNodeValue == 0)
            {
                throw std::invalid_argument(ERROR_DIVISION_BY_ZERO);
            }

            return evaluateWithVariables(currentNode->getNode(0)) / secondNodeValue;
        }
        else if (currentNode->getKey() == "sin")
        {
            return sin(evaluateWithVariables(currentNode->getNode(0)));
        }
        else if (currentNode->getKey() == "cos")
        {
            return cos(evaluateWithVariables(currentNode->getNode(0)));
        }
    }
    else if (currentNode->getNodeType() == VARIABLE)
    {
        typename std::map<std::string, T>::const_iterator argsIterator = variables.find(currentNode->getKey());

        if (argsIterator == variables.end())
        {
            std::cout << ERROR_UNKNOWN_ARG << std::endl;
            return getDefaultNodeKey();
        }

        return argsIterator->second;
    }

    return getDefaultNodeKey();
}

template <>
double PrefixExpressionTree<double>::evaluateWithVariables(Node* currentNode)
{
    if (currentNode->getNodeType() == CONSTANT)
    {
        return stringToConstant(currentNode->getKey());
    }
    else if (currentNode->getNodeType() == OPERATION)
    {
        if (currentNode->getKey() == "+")
        {
            return evaluateWithVariables(currentNode->getNode(0)) + evaluateWithVariables(currentNode->getNode(1));
        }
        else if (currentNode->getKey() == "-")
        {
            return evaluateWithVariables(currentNode->getNode(0)) - evaluateWithVariables(currentNode->getNode(1));
        }
        else if (currentNode->getKey() == "*")
        {
            return 0;
        }
        else if (currentNode->getKey() == "/")
        {
            double secondNodeValue = evaluateWithVariables(currentNode->getNode(1));

            if (secondNodeValue == 0)
            {
                throw std::invalid_argument(ERROR_DIVISION_BY_ZERO);
            }

            return evaluateWithVariables(currentNode->getNode(0)) / secondNodeValue;
        }
        else if (currentNode->getKey() == "sin")
        {
            return sin(evaluateWithVariables(currentNode->getNode(0)));
        }
        else if (currentNode->getKey() == "cos")
        {
            return cos(evaluateWithVariables(currentNode->getNode(0)));
        }
    }
    else if (currentNode->getNodeType() == VARIABLE)
    {
        typename std::map<std::string, double>::const_iterator argsIterator = variables.find(currentNode->getKey());

        if (argsIterator == variables.end())
        {
            std::cout << ERROR_UNKNOWN_ARG << std::endl;
            return getDefaultNodeKey();
        }

        return argsIterator->second;
    }

    return getDefaultNodeKey();
}

template <>
std::string PrefixExpressionTree<std::string>::evaluateWithVariables(Node* currentNode)
{
    if (currentNode->getNodeType() == CONSTANT)
    {
        return stringToConstant(currentNode->getKey());
    }
    else if (currentNode->getNodeType() == OPERATION)
    {
        if (currentNode->getKey() == "+")
        {
            return evaluateWithVariables(currentNode->getNode(0)) + evaluateWithVariables(currentNode->getNode(1));
        }
        else if (currentNode->getKey() == "-")
        {
            std::string firstNodeValue = evaluateWithVariables(currentNode->getNode(0));
            int pos = firstNodeValue.rfind(evaluateWithVariables(currentNode->getNode(1)));
            if (pos != std::string::npos)
            {
                firstNodeValue.erase(pos, evaluateWithVariables(currentNode->getNode(0)).length());
            }
            return firstNodeValue;
        }
        else if (currentNode->getKey() == "*")
        {
            std::string secondValue = evaluateWithVariables(currentNode->getNode(1));
            std::string firstValue = evaluateWithVariables(currentNode->getNode(0));

            if (secondValue.length() < 1)
            {
                return firstValue;
            }

            std::string newString = "";
            std::string stringToCopy = secondValue.substr(1);

            for (int i = 0; i < firstValue.length(); i++)
            {
                newString += firstValue[i];
                if (firstValue[i] == secondValue[0])
                {
                    newString += stringToCopy;
                }
            }

            return newString;
        }
        else if (currentNode->getKey() == "/")
        {
            std::string secondValue = evaluateWithVariables(currentNode->getNode(1));
            std::string firstValue = evaluateWithVariables(currentNode->getNode(0));

            if (secondValue.length() < 1)
            {
                return firstValue;
            }

            std::string newString = "";

            for (int i = 0; i < firstValue.length(); i++)
            {
                newString += firstValue[i];

                if (firstValue.substr(i, secondValue.length()) == secondValue)
                {
                    i += secondValue.length() - 1;
                }
            }

            return newString;
        }
    }
    else if (currentNode->getNodeType() == VARIABLE)
    {
        std::map<std::string, std::string>::const_iterator argsIterator = variables.find(currentNode->getKey());

        if (argsIterator == variables.end())
        {
            std::cout << ERROR_UNKNOWN_ARG << std::endl;
            return getDefaultNodeKey();
        }

        return argsIterator->second;
    }

    return getDefaultNodeKey();
}

template <typename T>
void PrefixExpressionTree<T>::clearVariables()
{
    variables.clear();
    v_variables.clear();
}

template <typename T>
void PrefixExpressionTree<T>::deleteVariable(std::string arg)
{
    typename std::map<std::string, T>::const_iterator argsIterator = variables.find(arg);

    if (argsIterator != variables.end())
    {
        variables.erase(arg);
    }

    for (int i = 0; i < v_variables.size(); i++)
    {
        if (v_variables[i] == arg)
        {
            v_variables.erase(v_variables.begin() + i);
            break;
        }
    }
}

template <typename T>
void PrefixExpressionTree<T>::setVariable(std::string arg, T value)
{
    typename std::map<std::string, T>::const_iterator argsIterator = variables.find(arg);

    if (argsIterator == variables.end())
    {
        v_variables.push_back(arg);
    }

    variables[arg] = value;
}

template <typename T>
std::string PrefixExpressionTree<T>::toString() const
{
    return root->toString();
}

template <typename T>
int PrefixExpressionTree<T>::stringToNumber(std::string str)
{
    int i = 0;

    std::istringstream(str) >> i;

    return i;
}

template <typename T>
void PrefixExpressionTree<T>::setRoot(Node* newRoot)
{
    root = newRoot;
}

template <typename T>
Node* PrefixExpressionTree<T>::getRoot()
{
    return root;
}

template <typename T>
bool PrefixExpressionTree<T>::isCorrectConstant(std::string value)
{
    return true;
}

template <>
bool PrefixExpressionTree<int>::isCorrectConstant(std::string value)
{
    return value.find_first_not_of("0123456789") == std::string::npos;
}

template <>
bool PrefixExpressionTree<double>::isCorrectConstant(std::string value)
{
    double tempDouble;
    std::istringstream stream(value);
    // Check if the string can be fully converted to a double
    return (stream >> tempDouble >> std::ws).eof();
}

template <>
bool PrefixExpressionTree<std::string>::isCorrectConstant(std::string value)
{
    // Ensure the string is at least 3 characters long, "*", must be
    if (value.length() < 3) {return false;}

    // Check if the string starts and ends with double quotes
    return (value.front() == '"' && value.back() == '"');
}

template <typename T>
void PrefixExpressionTree<T>::setVariableWithIndex(int index, T value)
{
    if (index >= v_variables.size())
    {
        return;
    }

    variables[v_variables[index]] = value;
}

// Splits a string into an array of words. Returns the array and updates the size.
template <typename T>
std::string* PrefixExpressionTree<T>::splitStringIntoArray(const std::string& inputString, int* arraySize)
{
    std::string* wordArray = new std::string[inputString.length()]; // Allocate maximum possible size
    int wordCount = 0;
    std::string currentWord;

    for (char ch : inputString)
    {
        if (ch == ' ')
        {
            if (!currentWord.empty())
            {
                wordArray[wordCount++] = currentWord;
                currentWord.clear();
            }
        }
        else
        {
            currentWord += ch;
        }
    }

    if (!currentWord.empty())
    {
        wordArray[wordCount++] = currentWord;
    }

    *arraySize = wordCount;
    return wordArray;
}

#endif