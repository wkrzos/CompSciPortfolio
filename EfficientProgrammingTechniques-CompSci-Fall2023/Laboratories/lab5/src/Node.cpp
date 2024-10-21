#include "Node.h"
#include <string>

std::string Node::toString() const
{
    std::string result = key;

    for (int i = 0; i < nodesCounter; i++)
    {
        result += " " + nodes[i].toString();
    }

    return result;
}

std::string Node::getKey() const
{
    return key;
}

Node* Node::getNode(int index) const
{
    return &nodes[index];
}

Node* Node::getNodes() const
{
    return nodes;
}

int Node::getNodesCounter() const
{
    return nodesCounter;
}

TYPE Node::getNodeType() const
{
    return type;
}

void Node::setNodesCounter(int numberOfNodes)
{
    this->nodesCounter = numberOfNodes;
    this->nodes = new Node[numberOfNodes];
}

void Node::setNodeType(TYPE type)
{
    this->type = type;
}

void Node::setKey(std::string value)
{
    this->key = value;
}

void Node::setNode(int index, Node& node)
{
    if (index >= nodesCounter)
    {
        return;
    }

    this->nodes[index] = node;
}