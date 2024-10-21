#ifndef NODE_H
#define NODE_H

#include <string>

enum TYPE
{
    CONSTANT,
    VARIABLE,
    OPERATION,
    NO_TYPE
};

class Node
{
private:
    int nodesCounter;
    TYPE type;
    std::string key;
    Node* nodes;

public:
    // Constructors
    Node() : type(NO_TYPE) {}
    Node(TYPE t, std::string k) : type(t), key(std::move(k)) {}

    // Copy Constructor
    Node(const Node& otherNode) = default;

    // Move Constructor
    Node(Node&& otherNode) noexcept
        : type(otherNode.type), key(std::move(otherNode.key)), nodes(std::move(otherNode.nodes)) {}

    // Destructor (no manual memory management needed)
    ~Node() = default;

    // Copy Assignment Operator
    Node& operator=(const Node& newValue) = default;

    // Move Assignment Operator
    Node& operator=(Node&& newValue) noexcept
    {
        if (this != &newValue)
        {
            type = newValue.type;
            key = std::move(newValue.key);
            nodes = std::move(newValue.nodes);
        }
        return *this;
    }

    // Util
    std::string toString() const;

    // Accessor Methods
    int getNodesCounter() const;
    std::string getKey() const;
    TYPE getNodeType() const;

    Node* getNode(int index) const;
    Node* getNodes() const;

    // Mutator Methods
    void setNode(int index, Node& node);

    void setNodesCounter(int numberOfNodes);
    void setKey(std::string value);
    void setNodeType(TYPE type);
};

#endif