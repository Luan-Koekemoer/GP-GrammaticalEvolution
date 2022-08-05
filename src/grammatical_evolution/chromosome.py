from random import Random
from copy import deepcopy
from .gp_tree.tree import Tree, ArithmaticNode


class Chromosome:
    def __init__(self, interpreter, n_codons=100, rng=None):
        self.rng = rng if rng is not None else Random()
        self.codons = []
        self.codons_cache = []
        self.interpreter = interpreter
        self.tree = None
        self.fitness = 0

        self.__gen_random_codons__(n_codons)

    def to_tree(self):
        # The codons_cache is a deepcopy of the codons, thus in the event
        # that the codons do change do to some genetic operation, we know
        # that we should then rebuild the tree otherwise we just keep the
        # tree as is, no need to rebuild if no changes have taken place
        if self.codons != self.codons_cache:
            self.tree = self.interpreter.create_tree(self)
            self.codons_cache = deepcopy(self.codons)

        elif self.tree is None:
            # A potential problem is, big trees will always get created
            # so we check the None case secondly
            self.tree = self.interpreter.create_tree(self)
            self.codons_cache = deepcopy(self.codons)

        # else: Do nothings, self.tree == self.tree

    def compute(self, x):
        # self.to_tree()  # TODO: Find a better safer way of creating new trees
        if self.tree is None:
            return None

        return self.tree.compute_tree(x)

    def calc_fitness(self, fitness_func):
        if self.tree is None:
            self.fitness = 0

        self.fitness = fitness_func(self)

    def __gen_random_codons__(self, n_codons):
        for _ in range(n_codons):
            val = self.rng.choice(range(0, 256))
            self.codons.append(val)
        self.to_tree()

    @staticmethod
    def generate_chromosomes(population_size, n_codons, bnf, rng=None):
        interpreter = ChromosomeInterpreter(bnf)

        chromosomes = []
        rng = rng if rng is not None else Random()
        for _ in range(population_size):
            c = Chromosome(interpreter, n_codons, rng)

            chromosomes.append(c)
        return chromosomes


class ChromosomeInterpreter:
    # TODO: ADD var for node creator function to make create_tree more generic
    def __init__(self, bnf):
        self.bnf = bnf

    def create_tree(self, chromosome):
        instr = self.__create_instruction(chromosome)

        if instr is None:
            return None

        trees = []
        for i in instr:
            mapping = self.bnf.function_map[i]
            trees.append(Tree(ArithmaticNode(mapping[0], mapping[1])))

        root = self.__create_tree_recursively(trees, trees.pop(0))
        root.instructions = instr
        return root

    # construct tree post order traversal i.e. start from the root
    def __create_tree_recursively(self, trees, root):
        while len(trees) > 0:
            if root.base_node.arity == 0:
                return root
            elif len(root.sub_trees) == root.base_node.arity:
                return root
            else:
                root.add_sub_tree(self.__create_tree_recursively(trees, trees.pop(0)))

        return root

    def __create_instruction(self, chromsome):
        codons = chromsome.codons
        instruction = [self.bnf.bnf_dict["<s>"][0]]
        codon_index = 0
        expr_count = 1
        sub_expr_count = len(self.bnf.bnf_dict["<sub-expr>"])
        c_count = len(codons)
        # [UNRAVEL ALL <EXPRs>]
        while expr_count > 0:

            # [EVALUATE THE NEXT <EXPR> STRING]
            expr_index = instruction.index("<expr>")

            if len(instruction) > len(codons):
                return

            # determines if it's going to become a sub-expr or a full expr
            next_str = codons[codon_index] % 2
            codon_index = codon_index + 1 if codon_index + 1 < c_count else 0

            if next_str == 0:
                # write a instruction in a way to allow for easy pre order
                # traversal when creating the tree

                instruction[expr_index] = "<expr>"
                instruction.insert(expr_index - 1, "<op>")
                instruction.insert(expr_index + 1, "<expr>")
                expr_count += 1
            else:
                instruction[expr_index] = self.bnf.bnf_dict["<sub-expr>"][
                    codons[codon_index] % sub_expr_count
                ]
                codon_index = codon_index + 1 if codon_index + 1 < c_count else 0

                expr_count -= 1

        for i in range(len(instruction)):
            sub_instr_lst = self.bnf.bnf_dict[instruction[i]]
            sub_instr = sub_instr_lst[codons[codon_index] % len(sub_instr_lst)]
            codon_index = codon_index + 1 if codon_index + 1 < c_count else 0
            while sub_instr[0] == "<":
                sub_instr_lst = self.bnf.bnf_dict[sub_instr]
                sub_instr = sub_instr_lst[codons[codon_index] % len(sub_instr_lst)]
                codon_index = codon_index + 1 if codon_index + 1 < c_count else 0

            instruction[i] = sub_instr

        return instruction

    # def create_trees(self, chromosomes):
    #     trees = []
    #     for c in chromosomes:
    #         trees.append(self.__create_tree(c))
    #
    #     return trees

    # def compute_trees(self):
    #     pass
