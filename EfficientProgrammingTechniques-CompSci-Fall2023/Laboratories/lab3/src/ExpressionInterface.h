#ifndef EXPRESSIONINTERFACE_H
#define EXPRESSIONINTERFACE_H

#include "Node/Node.h"
#include "PrefixExpressionParser.h" // Assuming the PrefixExpressionParser is defined in another file
#include <iostream>
#include <sstream>
#include <vector>
#include <set>
#include <map>

class ExpressionInterface {
private:
    ExpressionTree* expressionTree;

public:
    ExpressionInterface();

    ~ExpressionInterface();

    void executeCommand(const std::string& command);

private:
    void handleEnterCommand(const std::string& formula);

    void handleVarsCommand() const;

    void handlePrintCommand() const;

    void handleCompCommand(const std::vector<double>& values) const;

    void handleJoinCommand(const std::string& formula);
};

#endif // EXPRESSIONINTERFACE_H
