#ifndef PREFIXEXPRESSIONPARSER_H
#define PREFIXEXPRESSIONPARSER_H

#include "Node/Node.h"
#include "Node/ConstantNode.h"
#include "Node/VariableNode.h"
#include "Node/OperatorNode.h"
#include "ExpressionTree.h"
#include <iostream>
#include <string>
#include <vector>
#include <sstream>
#include <set>

class PrefixExpressionParser {
private:
    std::vector<std::string> tokens;
    size_t currentTokenIndex;

    Node* parseExpression();

public:
    PrefixExpressionParser(const std::string& expression);

    ~PrefixExpressionParser();

    Node* parse();

    void printTree();
};

#endif // PREFIXEXPRESSIONPARSER_H
