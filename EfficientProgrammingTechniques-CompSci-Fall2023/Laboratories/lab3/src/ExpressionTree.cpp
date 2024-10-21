#include "ExpressionTree.h"
#include "Node/NodeUtil.h"
#include "Node/Node.h"

ExpressionTree::ExpressionTree() : root(nullptr) {}

ExpressionTree::ExpressionTree(const ExpressionTree& other) {
    this->root = copyNode(other.root);
}

ExpressionTree::~ExpressionTree() {
    delete root;
}

ExpressionTree ExpressionTree::operator+(ExpressionTree& other) {

    ExpressionTree newTree = ExpressionTree(*this);

    Node** leaf = newTree.getRoot()->traverseLeft(&newTree.root);

    delete (*leaf);

    *leaf = copyNode(other.getRoot());

    return newTree;
}

ExpressionTree& ExpressionTree::operator=(ExpressionTree& other) {
    if (this != &other) {
        delete root;
        root = copyNode(other.getRoot());
    }
    return *this;
}

Node* ExpressionTree::getRoot() {
    return root;
}

void ExpressionTree::setRoot(Node* Root) {
    root = Root;
}

void ExpressionTree::print() const {
    root->print();
}
