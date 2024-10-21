#pragma once
#include "Evaluator.h"
#include "Individual.h"
#include <memory>
#include <functional>

class GeneticAlgorithm
{
public:
    GeneticAlgorithm(int populationSize, double crossProbability, double mutationProbability, CLFLnetEvaluator* evaluator);

    void runIteration();
    void runIterations(unsigned long n, const std::function<void(double)>& callback);

    Individual& getBestIndividual();

private:
    void initPopulation(int populationSize);
    Individual* getParentCandidate();
    Individual* getParentCandidateRoulette(const std::vector<double>& fitnesses);

    std::vector<double> cumulativeFitness();

    void evaluatePopulation();

    Individual bestIndividual;
    std::vector<std::unique_ptr<Individual>> population;
    double crossProbability;
    double mutationProbability;
    CLFLnetEvaluator* evaluator;
};
