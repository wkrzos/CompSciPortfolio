#include "PrefixExpressionParser.h"

Node* PrefixExpressionParser::parseExpression() {
    if (currentTokenIndex >= tokens.size()) {
        // end of tokens so fill it up with ones
        return new ConstantNode(1.0);
    }

    std::string token = tokens[currentTokenIndex++];

    if (isdigit(token[0]) || (token.length() >= 2 && token[0] == '-' && isdigit(token[1]))) {
        // negative numbers should not be handled so remove the sign
        return new ConstantNode(std::abs(std::stod(token)));
    }

    else if (isalpha(token[0])) {
        if (token == "sin" || token == "cos") {
            Node* operand1 = parseExpression();
            Node* operand2 = parseExpression();
            Node* operand3 = parseExpression();

            if (operand1 != nullptr && operand2 != nullptr && operand3 != nullptr) {
                if (token == "sin") {
                    return new SinNode(operand1, operand2, operand3);
                }
                else if (token == "cos") {
                    return new CosNode(operand1);
                }
            }
        }
        else {
            return new VariableNode(token);
        }
    }
    else if (token.size() == 1 && strchr("+-*/", token[0])) {
        Node* left = parseExpression();
        Node* right = parseExpression();
        return new OperatorNode(token[0], left, right);
    }
    else {
        std::cerr << "Error: Invalid token " << token << std::endl;
        return nullptr;
    }
}

PrefixExpressionParser::PrefixExpressionParser(const std::string& expression) {
    std::istringstream iss(expression);
    std::string token;
    while (iss >> token) {
        tokens.push_back(token);
    }
    currentTokenIndex = 0;
}

PrefixExpressionParser::~PrefixExpressionParser() = default;

Node* PrefixExpressionParser::parse() {
    return parseExpression();
}

void PrefixExpressionParser::printTree() {
    Node* expressionTree = parseExpression();
    if (expressionTree != nullptr) {
        std::cout << "Expression Tree: ";
        expressionTree->print();
        std::cout << std::endl;
        std::cout << "Tree Structure:" << std::endl;
        expressionTree->printTree();
        std::cout << "Prefix Form: ";
        expressionTree->printPrefix();
        std::cout << std::endl;
        std::cout << "Variables: ";
        std::set<std::string> variableSet;
        expressionTree->printVariables(variableSet);
        std::cout << std::endl;
    }
    delete expressionTree;
}
