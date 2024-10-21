#ifndef EXPRESSION_TREE_INTERFACE_H
#define EXPRESSION_TREE_INTERFACE_H

#include "PrefixExpressionTree.h"
#include "PrefixExpressionParser.h"
#include "Constants.h" // Include Constants.h for messages
#include <string>

template <typename T>
class ExpressionTreeInterface
{
public:
    static void run();

private:
    static void executeCommand(PrefixExpressionTree<T>& currentTree, PrefixExpressionParser<T>& parser, const std::string& command, std::string* variables, int argumentCount);

    static void handleEnterCommand(PrefixExpressionTree<T>& tree, PrefixExpressionParser<T>& parser, std::string* args, int size);
    static void handleVarsCommand(const PrefixExpressionTree<T>& tree);
    static void handleCompCommand(PrefixExpressionTree<T>& tree, std::string* args, int size);
    static void handleJoinCommand(PrefixExpressionTree<T>& tree, PrefixExpressionParser<T>& parser, std::string* args, int size);
    static void handlePrintCommand(const PrefixExpressionTree<T>& tree);
    static void handleWrongCommand(const std::string& command);

    static std::string* splitStringIntoArray(const std::string& inputString, int* arraySize);
    static std::string joinArrayIntoString(const std::string* stringArray, int arraySize);
};

template <typename T>
void ExpressionTreeInterface<T>::run()
{
    int numOfArgs = 0;

    PrefixExpressionTree<T> currentTree;
    PrefixExpressionParser<T> currentParser;

    while (true)
    {
        std::string userStringInput;
        std::getline(std::cin, userStringInput);

        std::string* variables = splitStringIntoArray(userStringInput, &numOfArgs);

        if (numOfArgs > 0)
        {
            std::string command = variables[0];

            if (command == "exit")
            {
                return;
            }
            else
            {
                executeCommand(currentTree, currentParser, command, variables, numOfArgs);
            }
        }
        else
        {
            std::cout << MESSAGE_NO_COMMAND << std::endl;
        }
    }
}

template <typename T>
void ExpressionTreeInterface<T>::executeCommand(PrefixExpressionTree<T>& currentTree, PrefixExpressionParser<T>& parser, const std::string& command, std::string* variables, int argumentCount) {
    if (command == "enter")
    {
        handleEnterCommand(currentTree, parser, variables, argumentCount);
    }
    else if (command == "vars")
    {
        handleVarsCommand(currentTree);
    }
    else if (command == "comp")
    {
        handleCompCommand(currentTree, variables, argumentCount);
    }
    else if (command == "join")
    {
        handleJoinCommand(currentTree, parser, variables, argumentCount);
    }
    else if (command == "print")
    {
        handlePrintCommand(currentTree);
    }
    else
    {
        handleWrongCommand(command);
    }
}

template <typename T>
void ExpressionTreeInterface<T>::handleEnterCommand(PrefixExpressionTree<T>& tree, PrefixExpressionParser<T>& parser, std::string* args, int size)
{
    if (size < 2)
    {
        std::cout << MESSAGE_WRONG_ENTER_COMMAND << std::endl;
        return;
    }
    else
    {
        std::string formula = joinArrayIntoString(args + 1, size - 1);
        parser.parseFormula(tree, formula);
    }
}

template <typename T>
void ExpressionTreeInterface<T>::handleVarsCommand(const PrefixExpressionTree<T>& tree)
{
    std::cout << MESSAGE_RESULT_VARS << tree.getVariables() << std::endl;
}

template <typename T>
void ExpressionTreeInterface<T>::handleCompCommand(PrefixExpressionTree<T>& tree, std::string* args, int size)
{
    std::string formula = joinArrayIntoString(args + 1, size - 1);

    T result = tree.evaluateWithVariables(formula); // TODO: change to T

    std::cout << MESSAGE_RESULT << result << std::endl;
}

template <typename T>
void ExpressionTreeInterface<T>::handleJoinCommand(PrefixExpressionTree<T>& tree, PrefixExpressionParser<T>& parser, std::string* args, int size)
{
    if (size >= 2)
    {
        PrefixExpressionTree<T> newTree;

        std::string formula = joinArrayIntoString(args + 1, size - 1);
        parser.parseFormula(newTree, formula);

        tree = tree + newTree;
    }
    else
    {
        std::cout << MESSAGE_WRONG_JOIN_COMMAND << std::endl;
        return;
    }
}

template <typename T>
void ExpressionTreeInterface<T>::handlePrintCommand(const PrefixExpressionTree<T>& tree)
{
    std::cout << MESSAGE_RESULT_PRINT << tree.toString() << std::endl;
}

template <typename T>
void ExpressionTreeInterface<T>::handleWrongCommand(const std::string& command) {
    std::cout << MESSAGE_WRONG_COMMAND << command << std::endl;
}

// Splits a string into an array of words. Returns the array and updates the size
template <typename T>
std::string* ExpressionTreeInterface<T>::splitStringIntoArray(const std::string& inputString, int* arraySize)
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

// Joins an array of strings into a single string with spaces.
template <typename T>
std::string ExpressionTreeInterface<T>::joinArrayIntoString(const std::string* stringArray, int arraySize)
{
    std::string resultString;

    for (int i = 0; i < arraySize; ++i)
    {
        resultString += stringArray[i];

        if (i < arraySize - 1)
        {
            resultString += " ";
        }
    }

    return resultString;
}

#endif // EXPRESSION_TREE_INTERFACE_H

//Jak mam drzewo doubli to każde mnożenie zwraca zero