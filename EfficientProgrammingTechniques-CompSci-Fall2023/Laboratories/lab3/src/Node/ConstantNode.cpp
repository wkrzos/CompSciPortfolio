#include "ConstantNode.h"

ConstantNode::ConstantNode(double val) : value(val) {}

double ConstantNode::evaluate() const {
    return value;
}

void ConstantNode::print() const {
    std::cout << value;
}

void ConstantNode::printTree(int indent) const {
    std::cout << std::string(indent, ' ') << "ConstantNode: " << value << std::endl;
}

void ConstantNode::printPrefix() const {
    std::cout << value;
}

void ConstantNode::printVariables(std::set<std::string>& variableSet) const {
    // Constants don't have variables
}

size_t ConstantNode::countVariables() const {
    return 0;
}

double ConstantNode::evaluateWithValues(const std::map<std::string, double>& values) const {
    // Constants don't depend on variables
    return value;
}
