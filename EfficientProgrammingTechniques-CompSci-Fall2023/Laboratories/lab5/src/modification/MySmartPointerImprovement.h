/* oh lord this code is boomin
#ifndef MYSMARTPOINTER_H
#define MYSMARTPOINTER_H

#include <utility> // for std::swap
#include "RefCounter.h"

template <typename T>
class MySmartPointerImprovement {
public:
    explicit MySmartPointerImprovement(T* pcPointer = nullptr);
    MySmartPointerImprovement(const MySmartPointerImprovement& pcOther);
    MySmartPointerImprovement(MySmartPointerImprovement&& pcOther) noexcept;
    ~MySmartPointerImprovement();

    MySmartPointerImprovement& operator=(MySmartPointerImprovement pcOther);
    T& operator*() const;
    T* operator->() const;

    void reset(T* pcPointer = nullptr);
    void swap(MySmartPointerImprovement& pcOther) noexcept;
    int use_count() const;

private:
    RefCounter* pc_counter;
    T* pc_pointer;

    void release();
};

template <typename T>
MySmartPointerImprovement<T>::MySmartPointerImprovement(T* pcPointer)
    : pc_counter(pcPointer ? new RefCounter() : nullptr), pc_pointer(pcPointer) {
    if (pc_pointer) {
        pc_counter->add();
    }
}

template <typename T>
MySmartPointerImprovement<T>::MySmartPointerImprovement(const MySmartPointerImprovement& pcOther)
    : pc_counter(pcOther.pc_counter), pc_pointer(pcOther.pc_pointer) {
    if (pc_counter) {
        pc_counter->add();
    }
}

template <typename T>
MySmartPointerImprovement<T>::MySmartPointerImprovement(MySmartPointerImprovement&& pcOther) noexcept
    : pc_counter(nullptr), pc_pointer(nullptr) {
    pcOther.swap(*this);
}

template <typename T>
MySmartPointerImprovement<T>::~MySmartPointerImprovement() {
    release();
}

template <typename T>
MySmartPointerImprovement<T>& MySmartPointerImprovement<T>::operator=(MySmartPointerImprovement pcOther) {
    pcOther.swap(*this);
    return *this;
}

template <typename T>
T& MySmartPointerImprovement<T>::operator*() const {
    return *pc_pointer;
}

template <typename T>
T* MySmartPointerImprovement<T>::operator->() const {
    return pc_pointer;
}

template <typename T>
void MySmartPointerImprovement<T>::reset(T* pcPointer) {
    MySmartPointerImprovement(pcPointer).swap(*this);
}

template <typename T>
void MySmartPointerImprovement<T>::swap(MySmartPointerImprovement& pcOther) noexcept {
    using std::swap;
    swap(pc_counter, pcOther.pc_counter);
    swap(pc_pointer, pcOther.pc_pointer);
}

template <typename T>
int MySmartPointerImprovement<T>::use_count() const {
    return pc_counter ? pc_counter->get() : 0;
}

template <typename T>
void MySmartPointerImprovement<T>::release() {
    if (pc_counter && pc_counter->dec() == 0) {
        delete pc_pointer;
        delete pc_counter;
    }
    pc_pointer = nullptr;
    pc_counter = nullptr;
}

#endif // MYSMARTPOINTER_H
*/