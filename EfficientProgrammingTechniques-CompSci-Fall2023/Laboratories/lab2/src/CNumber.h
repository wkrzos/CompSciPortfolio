#include <string>
#define NUMBER_DEFAULT_LENGTH 10

class CNumber {

public:

	CNumber() { i_length = NUMBER_DEFAULT_LENGTH; pi_number = new int[i_length]; };
	//~CNumber() { delete pi_number; }

	void operator=(const int iValue);
	void operator=(const CNumber& pcOther);

	CNumber operator+(const CNumber& pcNewVal);
	CNumber operator*(const CNumber& pcNewVal);
	CNumber operator-(const CNumber& pcNewVal);
	CNumber operator/(const CNumber& pcNewVal);

	CNumber operator+(int iNewVal);
	CNumber operator*(int iNewVal);
	CNumber operator-(int iNewVal);
	CNumber operator/(int iNewVal);

	std::string sToStr();
	void vPrint();

private: 

	int* pi_number;
	int i_length;
	bool isNegative;
};