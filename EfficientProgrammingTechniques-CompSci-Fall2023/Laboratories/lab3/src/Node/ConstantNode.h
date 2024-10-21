#pragma once
#ifndef CONSTANTNODE_H
#define CONSTANTNODE_H

#include "Node.h"
#include <iostream>

class ConstantNode : public Node {
private:
    double value;

public:
    ConstantNode(double val);

    //def copy const

    double evaluate() const override;

    void print() const override;

    void printTree(int indent) const override;

    void printPrefix() const override;

    void printVariables(std::set<std::string>& variableSet) const override;

    size_t countVariables() const override;

    double evaluateWithValues(const std::map<std::string, double>& values) const override;
};

#endif // CONSTANTNODE_H
