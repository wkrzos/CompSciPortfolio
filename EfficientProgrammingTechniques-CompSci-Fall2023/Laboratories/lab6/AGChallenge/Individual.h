#pragma once
#include <vector>
#include "Evaluator.h"

class Individual
{
public:
    Individual(std::vector<int> genotype, CLFLnetEvaluator* evaluator);
    Individual();
    Individual(const Individual& other);
    Individual(Individual&& other) noexcept;

    double getFitness() const;
    void mutate(double probability);
    std::vector<Individual*> cross(const Individual* with) const;

    Individual& operator=(const Individual& other);
    Individual& operator=(Individual&& other) noexcept;

private:
    std::vector<int> genotype;
    CLFLnetEvaluator* evaluator;
    double fitness;
};
