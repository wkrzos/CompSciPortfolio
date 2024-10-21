#include "Evaluator.h"
#include "Optimizer.h"
#include "Timer.h"
#include "GeneticAlgorithm.h"

#include <exception>
#include <iostream>
#include <random>

using namespace TimeCounters;

using namespace std;


#define POP_SIZE 1
#define CROSS_PROB 0.95
#define MUT_PROB 0.00025
#define ITERATIONS 1


void printFitness(double fitness) {
	std::cout << "fitness: " << fitness << "\n";
}

void vRunExperiment(CLFLnetEvaluator &cConfiguredEvaluator)
{
	try
	{
		GeneticAlgorithm algorithm(POP_SIZE, CROSS_PROB, MUT_PROB, &cConfiguredEvaluator);

		algorithm.runIterations(ITERATIONS, printFitness);


		std::cout << "final fitness: \n";
		printFitness(algorithm.getBestIndividual().getFitness());

	}//try
	catch (exception &c_exception)
	{
		cout << c_exception.what() << endl;
	}//catch (exception &c_exception)
}//void vRunExperiment(const CEvaluator &cConfiguredEvaluator)



void  vRunLFLExperiment(CString  sNetName)
{
	CLFLnetEvaluator c_lfl_eval;
	c_lfl_eval.bConfigure(sNetName);
	
	vRunExperiment(c_lfl_eval);

	
}//void vRunRastriginExperiment(int iNumberOfBits, int iBitsPerFloat, int iMaskSeed)



void main(int iArgCount, char **ppcArgValues)
{
	random_device c_mask_seed_generator;
	int i_mask_seed = (int)c_mask_seed_generator();


	srand(time(NULL));

	CString  s_test;
	vRunLFLExperiment("104b00");

	/*vRunIsingSpinGlassExperiment(81, 0, i_mask_seed);
	vRunIsingSpinGlassExperiment(81, 0, iSEED_NO_MASK);

	vRunLeadingOnesExperiment(50, i_mask_seed);
	vRunLeadingOnesExperiment(50, iSEED_NO_MASK);

	vRunMaxSatExperiment(25, 0, 4.27f, i_mask_seed);
	vRunMaxSatExperiment(25, 0, 4.27f, iSEED_NO_MASK);

	vRunNearestNeighborNKExperiment(100, 0, 4, i_mask_seed);
	vRunNearestNeighborNKExperiment(100, 0, 4, iSEED_NO_MASK);

	vRunOneMaxExperiment(100, i_mask_seed);
	vRunOneMaxExperiment(100, iSEED_NO_MASK);

	vRunRastriginExperiment(200, 10, i_mask_seed);
	vRunRastriginExperiment(200, 10, iSEED_NO_MASK);*/
}//void main(int iArgCount, char **ppcArgValues)