from random import Random
from copy import deepcopy


class Operators:
    def __init__(self, rng=None):
        self.rng = rng if rng is not None else Random()

    def mutate_hard(self, chromosome1, rate):
        c = deepcopy(chromosome1)
        for i in range(len(chromosome1.codons)):
            if rate >= self.rng.random():
                c.codons[i] = self.rng.choice(range(0, 256))
        return c

    def mutate(self, chromosome1, rate):
        c = deepcopy(chromosome1)
        for i in range(len(chromosome1.codons)):
            if rate >= self.rng.random():
                c.codons[i] = self.rng.choice(range(0, 256))
                return c
        return c

    def crossover(self, chromosome1, chromosome2, rate):
        c1 = deepcopy(chromosome1)
        c2 = deepcopy(chromosome2)

        i1 = i2 = -1

        for i in range(len(c1.codons)):
            if rate > self.rng.random():
                i1 = i
                break

        for i in range(len(c2.codons)):
            if rate > self.rng.random():
                i2 = i
                break

        if i1 > -1 and i2 > -1:
            c1.codons[i1] = c2.codons[i2]

        return c1
