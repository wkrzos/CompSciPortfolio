#include "GeneticAlgorithm.h"
#include "MyMath.h"
#include <algorithm>

GeneticAlgorithm::GeneticAlgorithm(int populationSize, double crossProbability, double mutationProbability, CLFLnetEvaluator* evaluator)
	: crossProbability(crossProbability),
	mutationProbability(mutationProbability),
	evaluator(evaluator),
	bestIndividual()
{
	initPopulation(populationSize);
}

Individual* GeneticAlgorithm::getParentCandidate()
{
	Individual *individual1 = population[lRand(population.size())].get();
	Individual *individual2 = population[lRand(population.size())].get();
	if (individual1->getFitness() > individual2->getFitness()) {
		return individual1;
	}
	else {
		return individual2;
	}

}

Individual * GeneticAlgorithm::getParentCandidateRoulette(const std::vector<double>& fitnesses)
{
	double selection = dRand() * fitnesses[population.size() - 1];

	int l = 0;
	int r = population.size() - 1;

	while (l <= r) {
		int m = (l + r) / 2;
		if (fitnesses[m] == selection) {
			l = m;
			r = m;
		}
		else if (fitnesses[m] < selection) {
			l = m + 1;
		}
		else {
			r = m - 1;	
		}

	}

#define DEBUG

#ifdef DEBUG
	std::cout << "poszukiwanie rodzica\n";
	std::cout << "tablica: ";
	for (int i = 0; i < population.size(); i++) {
		std::cout << fitnesses[i] << " ";
	}
	std::cout << "\n" << "poszukiwana wartosc: " << selection << "\n";
	std::cout << "znaleeziony indeks:" << l << "\n";
#endif

	return population[l].get();
}

std::vector<double> GeneticAlgorithm::cumulativeFitness()
{
	std::vector<double> fitnesses(population.size());

	if (!population.empty()) {
		fitnesses[0] = population[0]->getFitness();
		for (size_t i = 1; i < population.size(); ++i) {
			fitnesses[i] = fitnesses[i - 1] + population[i]->getFitness();
		}
	}

	return fitnesses;
}

void GeneticAlgorithm::evaluatePopulation()
{
	Individual *currBest = &bestIndividual;
	for (int i = 1; i < population.size(); i++) {
		if (currBest->getFitness() < population[i]->getFitness()) {
			currBest = population[i].get();
		}

	}
	bestIndividual = *currBest;
}

void GeneticAlgorithm::runIteration()
{
	std::vector<std::unique_ptr<Individual>> newPopulation;

	while (newPopulation.size() < population.size()) {
		auto fitnesses = cumulativeFitness();
		Individual* parent1 = getParentCandidateRoulette(fitnesses);
		Individual* parent2 = getParentCandidateRoulette(fitnesses);

		// crossing and mutation logic...

	}

	// Swap the old population with the new one
	population.swap(newPopulation);
	evaluatePopulation();
}

void GeneticAlgorithm::runIterations(unsigned long n, const std::function<void(double)>& callback)
{
	for (unsigned long i = 0; i < n; ++i) {
		runIteration();
		callback(bestIndividual.getFitness());
	}
}

Individual & GeneticAlgorithm::getBestIndividual()
{
	return bestIndividual;
}

void GeneticAlgorithm::initPopulation(int populationSize)
{
	int genotypeSize = evaluator->iGetNumberOfBits();
	for (int i = 0; i < populationSize; i++) {
		std::vector<int> genotype;

		for (int j = 0; j < genotypeSize; j++) {
			genotype.push_back(lRand(evaluator->iGetNumberOfValues(j)));
		}
		std::unique_ptr<Individual> individual = std::make_unique<Individual>(genotype, evaluator);

		population.push_back(std::move(individual)); // Transfer ownership to the population vector
	}
	evaluatePopulation();
}
