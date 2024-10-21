//Constants for the CTable Class
#define CTABLE_DEFAULT_SIZE 2
#define CTABLE_DEFAULT_NAME "Default Array"

#ifndef CTABLE_H //include guard https://en.wikipedia.org/wiki/Include_guard
#define CTABLE_H

#include <iostream>
using namespace std;

class CTable {
private:
    //Lower case notation with trailing underscore for vars that are members of the class
    string s_name;
    int i_table_len;
    int* pi_table;

public:
    // Non-parameterized constructor
    CTable();
    // Parameterized constructor
    CTable(string sName, int TableLen);
    // Copying constructor
    CTable(const CTable& pcOther);
    // Destructor
    ~CTable();

    void vSetName(string sName);
    bool bSetNewSize(int iTableLen);

    void vDoubleCopy(CTable*& pcClone0, CTable*& pcClone1); //mamy nasze ctable, mamy pcClone, zwracamy 2 kopie od razu przez argumenty, zwrocic samego siebie skopiowanego dwukrotnie

    CTable* pcClone();
    string GetName() const;
};

#endif // CTABLE_H

void runCTableTests();

void vModTab(CTable* pcTab, int iNewSize);

void vModTab(CTable cTab, int iNewSize);

void testModTabs();
