#ifndef MYSMARTPOINTER_H
#define MYSMARTPOINTER_H

#include "RefCounter.h"

template <typename T>
class MySmartPointer
{
public:
    MySmartPointer(T* pcPointer);
    MySmartPointer();
    MySmartPointer(const MySmartPointer& pcOther);
    ~MySmartPointer();

    MySmartPointer& operator=(const MySmartPointer& pcOther);

    T& operator*();
    T* operator->();

    MySmartPointer<T> duplicate() const; // Modification
    int getCounter() const;

private:
    RefCounter* pc_counter;
    T* pc_pointer;
};

template <typename T>
MySmartPointer<T>::MySmartPointer(T* pcPointer) : pc_counter(new RefCounter()), pc_pointer(pcPointer)
{
    pc_counter->add();
}

template <typename T>
MySmartPointer<T>::MySmartPointer() : pc_counter(new RefCounter()), pc_pointer(nullptr)
{
}

template <typename T>
MySmartPointer<T>::MySmartPointer(const MySmartPointer& pcOther) : pc_counter(pcOther.pc_counter), pc_pointer(pcOther.pc_pointer)
{
    pc_counter->add();
}

template <typename T>
MySmartPointer<T>::~MySmartPointer()
{
    if (pc_counter->dec() == 0)
    {
        delete pc_pointer;
        delete pc_counter;
    }
}

template <typename T>
MySmartPointer<T>& MySmartPointer<T>::operator=(const MySmartPointer& pcOther)
{
    if (this == &pcOther) // Check for self-assignment
        return *this;

    if (pc_counter->dec() == 0)
    {
        delete pc_pointer;
        delete pc_counter;
    }

    pc_counter = pcOther.pc_counter;
    pc_pointer = pcOther.pc_pointer;
    pc_counter->add();

    return *this;
}

template <typename T>
T& MySmartPointer<T>::operator*()
{
    return *pc_pointer;
}

template <typename T>
T* MySmartPointer<T>::operator->()
{
    return pc_pointer;
}

template <typename T>
MySmartPointer<T> MySmartPointer<T>::duplicate() const
{
    return MySmartPointer(*this);
}

template <typename T>
int MySmartPointer<T>::getCounter() const
{
    return pc_counter->get();
}

#endif
