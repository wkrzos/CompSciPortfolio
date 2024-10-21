#pragma once
#ifndef EXPRESSIONTREE_H
#define EXPRESSIONTREE_H

#include "Node/Node.h"
#include "Node/OperatorNode.h"
#include "Node/ConstantNode.h"
#include "Node/VariableNode.h"
#include <iostream>

class ExpressionTree {
private:
    Node* root;

public:
    ExpressionTree();

    ExpressionTree(const ExpressionTree& other);

    // Operator Overloading for +
    ExpressionTree operator+(ExpressionTree& other);

    // Operator Overloading for =
    ExpressionTree& operator=(ExpressionTree& other);

    Node* getRoot();

    void setRoot(Node* Root);

    void print() const;

    ~ExpressionTree();
};

#endif // EXPRESSIONTREE_H
