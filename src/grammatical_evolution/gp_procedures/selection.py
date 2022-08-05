from random import Random
from copy import deepcopy


class Selection:
    def __init__(self, rng=None):
        self.rng = rng if rng is not None else Random()

    def tournament_selection(self, population, tournament_size):
        candidates = self.rng.choices(population, k=tournament_size)
        best = candidates[0]

        for c in candidates:
            if best.fitness > c.fitness:
                best = c

        return deepcopy(best)
