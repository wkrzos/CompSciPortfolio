#pragma once
#ifndef VARIABLENODE_H
#define VARIABLENODE_H

#include "Node.h"
#include <iostream>
#include <set>
#include <map>

class VariableNode : public Node {
private:
    std::string name;
    double value;

public:
    VariableNode(const std::string& varName);

    //def copy const

    void assignValue(double val);

    double evaluate() const override;

    void print() const override;

    void printTree(int indent) const override;

    void printPrefix() const override;

    void printVariables(std::set<std::string>& variableSet) const override;

    size_t countVariables() const override;

    double evaluateWithValues(const std::map<std::string, double>& values) const override;
};

#endif // VARIABLENODE_H
