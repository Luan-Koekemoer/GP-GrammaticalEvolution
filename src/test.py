from pandas import DataFrame
from grammatical_evolution import bnf
from grammatical_evolution import chromosome
from grammatical_evolution.gp_procedures import *


def add(vals):
    return sum(vals)


def sub(vals):
    val = vals[0]
    for i in range(1, len(vals), 1):
        val -= vals[i]
    return val


def mul(vals):
    val = vals[0]
    for i in range(1, len(vals), 1):
        val *= vals[i]
    return val


fn_map = {
    "+": [add, 2],
    "-": [sub, 2],
    "*": [mul, 2],
    "x": ["x", 0],
    "0": [0, 0],
    "1": [1, 0],
    "2": [2, 0],
    "3": [3, 0],
}


def gen_test_data():
    # y = 2x + 1
    y = []
    x = []
    for i in range(20):
        x.append(i)
        y.append(2 * i + 1)

    data = {"x": x, "y": y}

    return DataFrame(data)


df = gen_test_data()
# for _, row in df.iterrows():
#     print(row["x"], row["y"])


mybnf = bnf.Bnf("../grammar/linear_reg.pybnf", fn_map)

pop = 100
cods = 1000
generations = 100

# Genetic operators
mutation_rate = 0.4
crossover_rate = 0.2

population = chromosome.Chromosome.generate_chromosomes(pop, cods, mybnf)
fit = fitness.FitnessXY(df)
ffunc = fit.mse

# population[0].calc_fitness(ffunc)
# print(population[0].fitness)


# crr = op.crossover(chromos[0], chromos[0], 0.4)
# muta = op.mutate_hard(chromos[0], 0.2)

select = selection.Selection()
op = operators.Operators()

fits = []
for gen in range(generations):
    print(gen)
    for chr in population:
        chr.calc_fitness(fit.mse)

    pop_new = []
    for _ in range(len(population)):
        p1 = select.tournament_selection(population, 2)
        p2 = select.tournament_selection(population, 2)
        offspring = op.crossover(p1, p2, crossover_rate)
        offspring = op.mutate(offspring, mutation_rate)
        offspring.to_tree()
        pop_new.append(offspring)

    population = pop_new

fits = [x.fitness for x in population]
print(max(fits))
    
