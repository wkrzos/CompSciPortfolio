#include "Node.h"
#include "OperatorNode.h"
#include "ConstantNode.h"
#include "VariableNode.h"

Node** Node::traverseLeft(Node** root) {
    if (root == nullptr) {
        std::cerr << "Error: Root is null." << std::endl;
        return nullptr;
    }

    if (typeid(**root) == typeid(OperatorNode)) {

        OperatorNode* node = dynamic_cast<OperatorNode*>(*root);

        if (isLeaf(node->getLeft())) {
            return node->getLeftRef();
        }
        else {
            return traverseLeft(root);
        }    
    }
    else if (typeid(**root) == typeid(SinNode)) {
        SinNode* node = dynamic_cast<SinNode*>(*root);

        if (isLeaf(node->getOperand())) {
            return node->getOperandRef();
        }
        else {
            return traverseLeft(root);
        }
    }
    else if (typeid(**root) == typeid(CosNode)) {
        SinNode* node = dynamic_cast<SinNode*>(*root);

        if (isLeaf(node->getOperand())) {
            return node->getOperandRef();
        }
        else {
            return traverseLeft(root);
        }
    }
    else {
        return root;
    }
}

bool Node::isLeaf(Node* node) {
    if (typeid(*node) == typeid(ConstantNode) || typeid(*node) == typeid(VariableNode)) {
        return true;
    }
    else {
        return false;
    }
}