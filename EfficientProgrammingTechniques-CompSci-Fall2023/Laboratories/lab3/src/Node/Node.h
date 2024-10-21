#pragma once
#include <set>
#include <string>
#include <map>
#include <iostream>

class Node {
public:
    virtual ~Node() = default;
    virtual double evaluate() const = 0;
    virtual void print() const = 0;
    virtual void printTree(int indent = 0) const = 0;
    virtual void printPrefix() const = 0;
    virtual void printVariables(std::set<std::string>& variableSet) const = 0;
    virtual size_t countVariables() const = 0;
    virtual double evaluateWithValues(const std::map<std::string, double>& values) const = 0;
    Node** traverseLeft(Node** root);
    bool isLeaf(Node* node);
};