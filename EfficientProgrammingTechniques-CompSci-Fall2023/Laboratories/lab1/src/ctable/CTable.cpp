#include <iostream>
#include <cassert>
#include "CTable.h"

using namespace std;

//Non-parameterized construtor
CTable::CTable() {
	s_name = CTABLE_DEFAULT_NAME;

	std::cout << "[DEBUG] bezp: " << s_name << std::endl;
	
	i_table_len = CTABLE_DEFAULT_SIZE;
	pi_table = new int[CTABLE_DEFAULT_SIZE];
}

//Parameterized constructor
//Used case notation as to discern s_name from sName
CTable::CTable(string sName, int iTableLen) {
	s_name = sName;

	std::cout << "[DEBUG] parametr:" << s_name << std::endl;

	i_table_len = iTableLen;
	pi_table = new int[i_table_len];
}

//Copying constructor
CTable::CTable(const CTable& pcOther) {
    s_name = pcOther.s_name + "_copy";
    i_table_len = pcOther.i_table_len;
    pi_table = new int[i_table_len];
    
	//Originally, pcCopy was used. However, it lead to an infinite 
	//infinite loop and stack overflow.
    for (int i = 0; i < i_table_len; ++i) {
        pi_table[i] = pcOther.pi_table[i];
    }
    
    std::cout << "[DEBUG] kopiuj:" << s_name << std::endl;
}

//Destructor
CTable::~CTable() {
	delete[] pi_table;
}

bool CTable::bSetNewSize(int iTableLen) {
	if (iTableLen <= 0) {
		cout << "[DEBUG] Blad: Nowy rozmiar musi byc wiekszy od zera." << endl;
		return false;
	}

	int* piNewTable = new int[iTableLen];
	int iMinLength = (i_table_len < iTableLen) ? i_table_len : iTableLen; // ? used an an else if; <iMinLength> if condition true : <iMinLength> if condition false 

	for (int i = 0; i < iMinLength; ++i) {
		piNewTable[i] = pi_table[i];
	}

	delete[] pi_table;  // Delete the old array before assigning the new one
	pi_table = piNewTable;
	i_table_len = iTableLen;
	return true;
}

void CTable::vDoubleCopy(CTable*& pcClone0, CTable*& pcClone1) {
    pcClone0 = pcClone();
    pcClone1 = pcClone();
}

CTable* CTable::pcClone() {
	return new CTable(*this);
}

string CTable::GetName() const {
	return s_name;
}

void CTable::vSetName(string sName) {
	s_name = sName;
}


void runCTableTests() {
	CTable* testTableDefault1 = new CTable();
	std::cout << "[DEBUG] Default Table Created. Name: " << testTableDefault1->GetName() << std::endl;
	CTable* testTableParametrized1 = new CTable("Parametrized table", 20);
	std::cout << "[DEBUG] Parametrized Table Created. Name: " << testTableParametrized1->GetName() << std::endl;

	testModTabs();

	delete testTableDefault1;
	delete testTableParametrized1;
}

// This modifies the actuall object, as it takes the pointer to the object.
// Any changes inside the function will affect the original object.
void vModTab(CTable* pcTab, int iNewSize) {
	pcTab->bSetNewSize(iNewSize);
}

// Doesn't modify the actual object. Creates a shallow copy, and the original
// object remains uneffected. Inside the function, we modify the copy.
void vModTab(CTable cTab, int iNewSize) {
	cTab.bSetNewSize(iNewSize); // Użyj odpowiedniej metody do zmiany rozmiaru tablicy w klasie CTable
}

void testModTabs() {
	//Procedures
	cout << std::endl << "PROCEDURES" << std::endl;
	CTable testTab1("Table1", 3);
	CTable testTab2("Table2", 3);

	// Test the v_mod_tab function that takes a pointer to CTable
	vModTab(&testTab1, 4);
	cout << "[DEBUG] c_my_tab1 size after modification: " << testTab1.bSetNewSize(1) << endl;

	// Test the v_mod_tab function that takes a CTable by value
	vModTab(testTab2, 2);
	cout << "[DEBUG] c_my_tab2 size after modification: " << testTab2.bSetNewSize(1) << endl;

	//Dynamically and statically allocated CTables
	cout << std::endl << "DYNAMIC AND STATIC ALLOCATION" << std::endl;

	//Static call order :
	//1.1 Parametrised
	//2.1 Non-parametrised
	//2.2 Destructor
	
	CTable testStaticTab1("StaticTab1", 5);

	testStaticTab1.~CTable();

	//Dynamic call order :
	//1. Non parametrised
	//2. SetName
	//3. Destructor

	CTable* testDynamicTab1 = new CTable;

	testDynamicTab1->vSetName("DynamicTab1");

	testDynamicTab1->~CTable();
}


int main() {
	//Excercise 4
	cout << std::endl << "========== EX 4 ==========" << std::endl;
	runCTableTests();

	CTable cOriginal;
	cOriginal.vSetName("Test Name For Modifcation");
	cout << cOriginal.GetName();

	CTable* pCCTable0 = &cOriginal;
	CTable* pCCTable1 = &cOriginal;
	cOriginal.vDoubleCopy(pCCTable0, pCCTable1);

	cOriginal.vSetName("aaaa");

	cout << std::endl << "Name of pc_c0" << cOriginal.GetName() << std::endl;
	cout << std::endl << "Name of pc_c1" << pCCTable1->GetName() << std::endl;

	delete pCCTable0;
	delete pCCTable1;
}
