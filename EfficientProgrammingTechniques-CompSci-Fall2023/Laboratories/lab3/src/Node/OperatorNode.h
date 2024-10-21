#pragma once
#ifndef OPERATORNODE_H
#define OPERATORNODE_H

#include "Node.h"
#include <cmath>
#include <iostream>

class OperatorNode : public Node {
private:
    char op;
    Node* left;
    Node* right;

public:
    OperatorNode(char operation, Node* l, Node* r);

    OperatorNode(const OperatorNode& other);

    ~OperatorNode() override;

    double evaluate() const override;

    size_t countVariables() const override;

    double evaluateWithValues(const std::map<std::string, double>& values) const override;

    OperatorNode* traverseLeftToOperatorNode(OperatorNode* root);

    void print() const override;

    void printTree(int indent) const override;

    void printPrefix() const override;

    void printVariables(std::set<std::string>& variableSet) const override;

    void setLeft(Node* Left);

    void setRight(Node* Right);

    Node* getLeft();
    Node** getLeftRef();

    Node* getRight();
};

#endif // OPERATORNODE_H

#pragma once
#ifndef SINNODE_H
#define SINNODE_H

#include "Node.h"
#include <cmath>
#include <iostream>

class SinNode : public Node {
private:
    Node* operand1;
    Node* operand2;
    Node* operand3;

public:
    SinNode(Node* op1, Node* op2, Node* op3);

    SinNode(const SinNode& other);

    ~SinNode() override;

    double evaluate() const override;

    void print() const override;

    void printTree(int indent) const override;

    void printPrefix() const override;

    void printVariables(std::set<std::string>& variableSet) const override;

    size_t countVariables() const override;

    double evaluateWithValues(const std::map<std::string, double>& values) const override; 

    Node* getOperand();
    Node** getOperandRef();
};

#endif // SINNODE_H


#pragma once
#ifndef COSNODE_H
#define COSNODE_H

#include "Node.h"
#include <cmath>
#include <iostream>

class CosNode : public Node {
private:
    Node* operand;

public:
    CosNode(Node* op);

    CosNode(const CosNode& other);

    ~CosNode() override;

    double evaluate() const override;

    void print() const override;

    void printTree(int indent) const override;

    void printPrefix() const override;

    void printVariables(std::set<std::string>& variableSet) const override;

    size_t countVariables() const override;

    double evaluateWithValues(const std::map<std::string, double>& values) const override;

    Node* getOperand();
    Node** getOperandRef();
};

#endif // COSNODE_H
