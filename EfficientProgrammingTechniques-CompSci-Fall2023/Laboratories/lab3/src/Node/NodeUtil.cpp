#include "ConstantNode.h"
#include "OperatorNode.h"
#include "VariableNode.h"
#include "NodeUtil.h"

Node* copyNode(Node* from) {
    if (typeid(*from) == typeid(ConstantNode)) {
        return new ConstantNode(*dynamic_cast<ConstantNode*>(from));
    }
    else if (typeid(*from)==typeid(VariableNode)) {
        return new VariableNode(*dynamic_cast<VariableNode*>(from));
    }
    else if (typeid(*from)==typeid(OperatorNode)){
        return new OperatorNode(*dynamic_cast<OperatorNode*>(from));
    }
    else if (typeid(*from) == typeid(SinNode)) {
        return new SinNode(*dynamic_cast<SinNode*>(from));
    }
    else if (typeid(*from) == typeid (CosNode)) {
        return new CosNode(*dynamic_cast<CosNode*>(from));
    }
    else {
        return nullptr;
    }
}