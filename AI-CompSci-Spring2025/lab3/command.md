# run interpreter
docker run --rm -v $(pwd):/benchmarks aibasel/downward --alias lama-first /benchmarks/domain.pddl /benchmarks/problem.pddl