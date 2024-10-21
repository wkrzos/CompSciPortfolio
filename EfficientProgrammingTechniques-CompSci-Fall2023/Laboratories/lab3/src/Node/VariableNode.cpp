#include "VariableNode.h"

VariableNode::VariableNode(const std::string& varName) : name(varName), value(0.0) {}

void VariableNode::assignValue(double val) {
    value = val;
}

double VariableNode::evaluate() const {
    return value;
}

void VariableNode::print() const {
    std::cout << name;
}

void VariableNode::printTree(int indent) const {
    std::cout << std::string(indent, ' ') << "VariableNode: " << name << std::endl;
}

void VariableNode::printPrefix() const {
    std::cout << name;
}

void VariableNode::printVariables(std::set<std::string>& variableSet) const {
    // Check if the variable has been encountered before
    if (variableSet.find(name) == variableSet.end()) {
        variableSet.insert(name); // Add the variable to the set to mark it as encountered
    }
}

size_t VariableNode::countVariables() const {
    return 1;
}

double VariableNode::evaluateWithValues(const std::map<std::string, double>& values) const {
    // Return the value assigned to the variable
    return values.at(name);
}
