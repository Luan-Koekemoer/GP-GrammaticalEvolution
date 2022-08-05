class Tree:
    def __init__(self, node) -> None:
        self.base_node = node
        self.sub_trees = []
        self.instructions = []

    def add_sub_tree(self, tree):
        self.sub_trees.append(tree)

    def compute_tree(self, x):
        ops = []
        for t in self.sub_trees:
            ops.append(t.compute_tree(x))

        return self.base_node.eval_node(ops, x)


class ArithmaticNode:
    def __init__(self, node_attribute, arity):
        self.node_attribute = node_attribute
        self.arity = arity

    def eval_node(self, inputs, x):
        if self.arity == 0:
            return x if self.node_attribute == "x" else self.node_attribute
        else:
            return self.node_attribute(inputs)

    def __repr__(self):
        if self.arity > 0:
            return str(self.node_attribute.__name__)
        else:
            return str(self.node_attribute)
