#include <iostream>
#include "TableMakers.h"

void print1DimArray(int* piArray, int iSize) {
	for (int i = 0; i < iSize; i++) {
		std::cout << piArray[i];
	}
}

void vAllocTableFill34(int iSize) {

	if (iSize <= 0) {
		std::cout << "[DEBUG] Wrong size of table";
		return;
	}

	int* piNumber34Array;
	piNumber34Array = new int[iSize];

	for (int i = 0; i < iSize; i++) {
		piNumber34Array[i] = VALUE_TO_FILL_THE_EX1_TABLE_WITH;
	}

	print1DimArray(piNumber34Array, iSize);

	delete[] piNumber34Array;
}

/*
I used int ***piTable as the function parameter because you need to pass a pointer to a pointer to an integer to represent a two-dimensional array.

int * represents a pointer to an integer. It points to a single integer.

int ** represents a pointer to a pointer to an integer. It's used to represent a one-dimensional array of integers, 
where each element of the array is a pointer to an integer.

int *** represents a pointer to a pointer to a pointer to an integer. This is used to represent a two-dimensional array of integers, 
where each element of the array is a pointer to a one-dimensional array of integers. 
The extra level of indirection is required to create an array of arrays (rows).

When you pass int ***piTable to the function, you're essentially passing a pointer to a pointer to a pointer to an integer, 
which allows the function to allocate memory for a two-dimensional array and set piTable to point to it.

In the function implementation, *piTable is used to access and modify the two-dimensional array. 
The extra level of indirection is necessary because C does not support true multi-dimensional arrays, 
and you need to use pointers to simulate them.

TL;DR: We need the pointer to point to the newly allocated memory.
*/

bool bAllocTable2Dim(int ***piTable, int iSizeX, int iSizeY) {

	if (iSizeX <= 0) {
		std::cout << "[DEBUG] Wrong length: " << iSizeX << " of table" << std::endl;
		return false;
	}
	else if (iSizeY <= 0) {
		std::cout << "[DEBUG] Wrong length: " << iSizeY << " of table" << std::endl;
		return false;
	}

	int** piTwoDimensionalTable;
	piTwoDimensionalTable = new int* [iSizeX];

	for (int i = 0; i < iSizeX; i++) {
		piTwoDimensionalTable[i] = new int[iSizeY];
	}

	*piTable = piTwoDimensionalTable;

	return true;
}

//TL;DR: We are not allocating new memory, we don't need the extra level of indirection. We work on a pointer pointing directly to the data structure.
bool bDeallocTable2Dim(int **piTable, int iSizeX, int iSizeY) {
	if (iSizeX <= 0) {
		std::cout << "[DEBUG] Wrong length: " << iSizeX << " of table" << std::endl;
		return false;
	}
	else if (iSizeY <= 0) {
		std::cout << "[DEBUG] Wrong length: " << iSizeY << " of table" << std::endl;
		return false;
	}

	for (int i = 0; i < iSizeX; i++) {
		delete piTable[i];
	}

	delete piTable;

	return true;
}


//Debug function, non-excersice-related
void printTable2Dim(int **piTable, int iSizeX, int iSizeY) {
	for (int i = 0; i < iSizeX; i++) {
		for (int j = 0; j < iSizeY; j++) {
			std::cout << piTable[i][j] << " ";
		}
		std::cout << std::endl;
	}
}


/*int main() {
	//Excercise 1
	std::cout << std::endl << "========== EX 1 ==========" << std::endl;
	vAllocTableFill34(SIZE_OF_THE_EX1_ARRAY);

	//Excercise 2
	//So, ??? must be the & symbol, since we need the extra level of indirection.
	std::cout << std::endl << "========== EX 2 ==========" << std::endl;
	int** piTable;
	bAllocTable2Dim(&piTable, I_SIZE_X, I_SIZE_Y);
	printTable2Dim(piTable, I_SIZE_X, I_SIZE_Y);

	//Excercise 3
	std::cout << std::endl << "========== EX 3 ==========" << std::endl;
	bool isSuccess = bDeallocTable2Dim(piTable, I_SIZE_X, I_SIZE_Y);
	std::cout << std::endl << "Table deallocation ended. Outcome: " << isSuccess << std::endl;
}*/
