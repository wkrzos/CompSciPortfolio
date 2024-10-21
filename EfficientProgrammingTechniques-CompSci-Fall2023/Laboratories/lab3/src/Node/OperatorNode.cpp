#include "OperatorNode.h"
#include "NodeUtil.h"
#include "ConstantNode.h"
#include "VariableNode.h"

OperatorNode::OperatorNode(char operation, Node* l, Node* r) : op(operation), left(l), right(r) {}

OperatorNode::OperatorNode(const OperatorNode& other) : op(other.op), left(nullptr), right(nullptr) {
    if (other.left != nullptr) {
        left = copyNode(other.left);
    }
    if (other.right != nullptr) {
        right = copyNode(other.right);
    }
}

OperatorNode::~OperatorNode() {
    delete left;
    delete right;
}

double OperatorNode::evaluate() const {
    switch (op) {
    case '+':
        return left->evaluate() + right->evaluate();
    case '-':
        return left->evaluate() - right->evaluate();
    case '*':
        return left->evaluate() * right->evaluate();
    case '/':
        return left->evaluate() / right->evaluate();
    case 's':
        return std::sin(right->evaluate());
    case 'c':
        return std::cos(right->evaluate());
    default:
        std::cerr << "Error: Unknown operator " << op << std::endl;
        return 0.0;
    }
}

size_t OperatorNode::countVariables() const {
    return left->countVariables() + right->countVariables();
}

double OperatorNode::evaluateWithValues(const std::map<std::string, double>& values) const {
    double leftValue = left->evaluateWithValues(values);
    double rightValue = right->evaluateWithValues(values);

    switch (op) {
    case '+':
        return leftValue + rightValue;
    case '-':
        return leftValue - rightValue;
    case '*':
        return leftValue * rightValue;
    case '/':
        return leftValue / rightValue;
    case 's':
        return std::sin(rightValue);
    case 'c':
        return std::cos(rightValue);
    default:
        std::cerr << "Error: Unknown operator " << op << std::endl;
        return 0.0;
    }
}

OperatorNode* OperatorNode::traverseLeftToOperatorNode(OperatorNode* root) {
    if (typeid(root->left) == typeid(OperatorNode)) {
        return dynamic_cast<OperatorNode*>(root->left);
    }
    else if (typeid(root->left) == typeid(ConstantNode) || typeid(root->left) == typeid(VariableNode)) {
        std::cerr << "Error: Leaf node of type ConstantNode or VariableNode encountered while traversing left." << std::endl;
        return nullptr;
    }
    else if (typeid(root->left) == typeid(OperatorNode)) {
        return traverseLeftToOperatorNode(dynamic_cast<OperatorNode*>(root->left));
    }
    else {
        std::cerr << "Error: Unexpected node type encountered on the left side." << std::endl;
        return nullptr;
    }
}

void OperatorNode::print() const {
    if (op == 's' || op == 'c') {
        std::cout << op;
        right->print();
    }
    else {
        std::cout << "(";
        left->print();
        std::cout << " " << op << " ";
        right->print();
        std::cout << ")";
    }
}

void OperatorNode::printTree(int indent) const {
    std::cout << std::string(indent, ' ') << "OperatorNode: " << op << std::endl;
    if (op == 's' || op == 'c') {
        right->printTree(indent + 2);
    }
    else {
        left->printTree(indent + 2);
        right->printTree(indent + 2);
    }
}

void OperatorNode::printPrefix() const {
    std::cout << op << " ";
    left->printPrefix();
    std::cout << " ";
    right->printPrefix();
}

void OperatorNode::printVariables(std::set<std::string>& variableSet) const {
    left->printVariables(variableSet);
    right->printVariables(variableSet);
}

void OperatorNode::setLeft(Node* Left) {
    left = Left;
}

void OperatorNode::setRight(Node* Right) {
    right = Right;
}

Node* OperatorNode::getLeft() {
    return left;
}

Node** OperatorNode::getLeftRef()
{
    return &left;
}

Node* OperatorNode::getRight() {
    return right;
}

SinNode::SinNode(Node* op1, Node* op2, Node* op3) : operand1(op1), operand2(op2), operand3(op3) {}

SinNode::SinNode(const SinNode& other) : operand1(nullptr), operand2(nullptr), operand3(nullptr) {
    if (other.operand1 != nullptr && other.operand2 != nullptr && other.operand3 != nullptr) {
        operand1 = copyNode(other.operand1);
        operand2 = copyNode(other.operand2);
        operand3 = copyNode(other.operand3);
    }
}

SinNode::~SinNode() {
    delete operand1;
    delete operand2;
    delete operand3;
}

double SinNode::evaluate() const {
    return std::sin(operand1->evaluate() + operand2->evaluate() + operand3->evaluate());
}

void SinNode::print() const {
    std::cout << "sin(";
    operand1->print();
    std::cout << "+";
    operand2->print();
    std::cout << "+";
    operand3->print();
    std::cout << ")";
}

void SinNode::printTree(int indent) const {
    std::cout << std::string(indent, ' ') << "SinNode" << std::endl;
    operand1->printTree(indent + 2);
}

void SinNode::printPrefix() const {
    std::cout << "sin ";
    operand1->printPrefix();
    std::cout << "+";
    operand2->printPrefix();
    std::cout << "+";
    operand3->printPrefix();
}

void SinNode::printVariables(std::set<std::string>& variableSet) const {
    operand1->printVariables(variableSet);
    operand2->printVariables(variableSet);
    operand3->printVariables(variableSet);
}

size_t SinNode::countVariables() const {
    size_t temp = operand1->countVariables() + operand2->countVariables() + operand3->countVariables();
    return temp;
}

double SinNode::evaluateWithValues(const std::map<std::string, double>& values) const {
    return std::sin(operand1->evaluateWithValues(values) + operand2->evaluateWithValues(values) + operand3->evaluateWithValues(values));
}

Node* SinNode::getOperand() {
    return operand1;
}

Node** SinNode::getOperandRef()
{
    return &operand1;
}


CosNode::CosNode(Node* op) : operand(op) {}

CosNode::CosNode(const CosNode& other) : operand(nullptr) {
    if (other.operand != nullptr) {
        operand = copyNode(other.operand);
    }
}

CosNode::~CosNode() {
    delete operand;
}

double CosNode::evaluate() const {
    return std::cos(operand->evaluate());
}

void CosNode::print() const {
    std::cout << "cos(";
    operand->print();
    std::cout << ")";
}

void CosNode::printTree(int indent) const {
    std::cout << std::string(indent, ' ') << "CosNode" << std::endl;
    operand->printTree(indent + 2);
}

void CosNode::printPrefix() const {
    std::cout << "cos ";
    operand->printPrefix();
}

void CosNode::printVariables(std::set<std::string>& variableSet) const {
    operand->printVariables(variableSet);
}

size_t CosNode::countVariables() const {
    return operand->countVariables();
}

double CosNode::evaluateWithValues(const std::map<std::string, double>& values) const {
    return std::cos(operand->evaluateWithValues(values));
}

Node* CosNode::getOperand() {
    return operand;
}
Node** CosNode::getOperandRef()
{
    return &operand;
}