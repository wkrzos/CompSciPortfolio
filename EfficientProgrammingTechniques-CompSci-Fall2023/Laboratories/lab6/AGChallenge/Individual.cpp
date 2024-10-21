#include "Individual.h"

Individual::Individual(std::vector<int> genotype, CLFLnetEvaluator* evaluator)
    : genotype(std::move(genotype)), evaluator(evaluator), fitness(evaluator->dEvaluate(&this->genotype))
{
}

Individual::Individual()
    : evaluator(nullptr), fitness(0.0)
{
}

Individual::Individual(const Individual& other)
    : genotype(other.genotype), evaluator(other.evaluator), fitness(other.fitness)
{
}

Individual::Individual(Individual&& other) noexcept
    : genotype(std::move(other.genotype)), evaluator(other.evaluator), fitness(other.fitness)
{
    other.evaluator = nullptr;
    other.fitness = 0.0;
}

double Individual::getFitness() const
{
    return fitness;
}

void Individual::mutate(double probability)
{
    for (int& gene : genotype) {
        if (dRand() < probability) {
            gene = lRand(evaluator->iGetNumberOfValues(&gene - &genotype[0]));
        }
    }
    fitness = evaluator->dEvaluate(&genotype);
}

std::vector<Individual*> Individual::cross(const Individual* with) const
{
    int slicePoint = lRand(genotype.size() - 1) + 1;
    std::vector<int> genotype1(genotype.begin(), genotype.begin() + slicePoint);
    genotype1.insert(genotype1.end(), with->genotype.begin() + slicePoint, with->genotype.end());

    std::vector<int> genotype2(with->genotype.begin(), with->genotype.begin() + slicePoint);
    genotype2.insert(genotype2.end(), genotype.begin() + slicePoint, genotype.end());

    return { new Individual(genotype1, evaluator), new Individual(genotype2, evaluator) };
}

Individual& Individual::operator=(const Individual& other)
{
    if (this != &other) {
        genotype = other.genotype;
        evaluator = other.evaluator;
        fitness = other.fitness;
    }
    return *this;
}

Individual& Individual::operator=(Individual&& other) noexcept
{
    if (this != &other) {
        genotype = std::move(other.genotype);
        evaluator = other.evaluator;
        fitness = other.fitness;

        other.evaluator = nullptr;
        other.fitness = 0.0;
    }
    return *this;
}
